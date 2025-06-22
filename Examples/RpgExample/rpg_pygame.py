
import random
import sys
import time
import math
import os
import pygame
from typing import List, Dict, Any, Optional, TYPE_CHECKING

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.Goal import Goal
from MountainGoap.ExtremeGoal import ExtremeGoal
from MountainGoap.Sensor import Sensor
from MountainGoap.StepMode import StepMode
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair
from MountainGoapLogging.DefaultLogger import DefaultLogger
from MountainGoap.ComparativeGoal import ComparativeGoal
from MountainGoap.Internals.ActionNode import ActionNode # For type hints in cost callbacks



# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]





# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]


MaxX: int = 20

MaxY: int = 20

# C# `System.Numerics.Vector2` equivalent for this example
class Vector2:
    def __init__(self, x: float, y: float):
        self.X = x
        self.Y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.X == other.X and self.Y == other.Y

    def __hash__(self) -> int:
        return hash((self.X, self.Y))
    
    def __repr__(self) -> str:
        return f"Vector2({self.X}, {self.Y})"

class RpgUtils:
    """
    Utility classes for the RPG example.
    """

    @staticmethod
    def in_distance(pos1: Vector2, pos2: Vector2, max_distance: float) -> bool:
        """
        Checks if two positions are within a certain distance of one another.
        """
        distance = RpgUtils._distance(pos1, pos2)
        return distance <= max_distance

    @staticmethod
    def get_enemy_in_range(source: Agent, agents: List[Agent], distance: float) -> Optional[Agent]:
        """
        Gets an enemy within a given range of a source agent.
        """
        for agent in agents:
            if agent == source:
                continue
            
            # Type checking and access values
            source_pos = source.State.get("position")
            agent_pos = agent.State.get("position")
            source_faction = source.State.get("faction")
            agent_faction = agent.State.get("faction")

            if isinstance(source_pos, Vector2) and \
               isinstance(agent_pos, Vector2) and \
               isinstance(source_faction, str) and \
               isinstance(agent_faction, str) and \
               RpgUtils.in_distance(source_pos, agent_pos, distance) and \
               source_faction != agent_faction:
                return agent
        return None

    @staticmethod
    def move_towards_other_position(pos1: Vector2, pos2: Vector2) -> Vector2:
        """
        Moves a position towards another position one space and returns the result.
        This is a simple Manhattan-like move.
        """
        new_pos = Vector2(pos1.X, pos1.Y) # Create a copy to modify
        
        x_diff = pos2.X - new_pos.X
        y_diff = pos2.Y - new_pos.Y

        x_sign = 0
        if x_diff > 0: x_sign = 1
        elif x_diff < 0: x_sign = -1

        y_sign = 0
        if y_diff > 0: y_sign = 1
        elif y_diff < 0: y_sign = -1
        
        # C# Math.Sign behavior
        # `if (xSign != 0) pos1.X += xSign; else pos1.Y += ySign;`
        # This means it prioritizes X movement, and only moves Y if X is aligned.
        if x_sign != 0:
            new_pos.X += x_sign
        elif y_sign != 0: # Only if x_sign is 0, move in Y direction
            new_pos.Y += y_sign
        
        return new_pos

    @staticmethod
    def enemy_permutations(state: StateDictionary) -> List[Any]:
        """
        Permutation selector to grab all enemies.
        """
        enemies: List[Any] = []
        
        agents_list = state.get("agents")
        agent_faction = state.get("faction")

        if not isinstance(agents_list, list) or \
           not all(isinstance(a, Agent) for a in agents_list) or \
           not isinstance(agent_faction, str):
            return enemies
        
        # Filter agents that are not in the same faction as the current agent
        for agent in agents_list:
            if isinstance(agent.State.get("faction"), str) and agent.State["faction"] != agent_faction:
                enemies.append(agent)
        return enemies

    @staticmethod
    def food_permutations(state: StateDictionary) -> List[Any]:
        """
        Permutation selector to grab all food positions.
        """
        food_positions: List[Any] = []
        
        source_positions = state.get("foodPositions")
        
        if not isinstance(source_positions, list) or \
           not all(isinstance(p, Vector2) for p in source_positions):
            return food_positions
        
        # Copy elements from sourcePositions to foodPositions (list copy)
        food_positions.extend(source_positions)
        return food_positions

    @staticmethod
    def starting_position_permutations(state: StateDictionary) -> List[Any]:
        """
        Gets a list of all possible starting positions for a move action.
        """
        starting_positions: List[Any] = []
        position = state.get("position")
        
        if not isinstance(position, Vector2):
            return starting_positions
        
        starting_positions.append(position)
        return starting_positions

    @staticmethod
    def go_to_enemy_cost(action: Action, state: StateDictionary) -> float:
        """
        Gets the cost of moving to an enemy.
        """
        starting_position = action.get_parameter("startingPosition")
        target_agent = action.get_parameter("target")

        if not isinstance(starting_position, Vector2) or \
           not isinstance(target_agent, Agent):
            return float('inf') # float.MaxValue in C#
        
        target_position = target_agent.State.get("position")

        if not isinstance(target_position, Vector2):
            return float('inf')
        
        return RpgUtils._distance(starting_position, target_position)

    @staticmethod
    def go_to_food_cost(action: Action, state: StateDictionary) -> float:
        """
        Gets the cost of moving to food.
        """
        starting_position = action.get_parameter("startingPosition")
        target_position = action.get_parameter("target")

        if not isinstance(starting_position, Vector2) or \
           not isinstance(target_position, Vector2):
            return float('inf') # float.MaxValue in C#
        
        return RpgUtils._distance(starting_position, target_position)

    @staticmethod
    def _distance(pos1: Vector2, pos2: Vector2) -> float:
        """
        Calculates the Euclidean distance between two Vector2 positions.
        """
        return math.sqrt(math.pow(abs(pos2.X - pos1.X), 2) + math.pow(abs(pos2.Y - pos1.Y), 2))



import os


USE_EXTREME_GOAL = os.getenv("USE_EXTREME_GOAL", "false").lower() == "true"
class PlayerFactory:
    @staticmethod
    def create(agents: List[Agent], food_positions: List[Vector2], name: str = "Player") -> Agent:
        """
        Returns a player agent with healing and combat capabilities.
        """
        if False:
            food_goal = ExtremeGoal(
                name="Maximize Food Eaten",
                weight=1.0,  # Higher weight than combat
                desired_state={
                    "food_eaten": True  # Maximize food_eaten
                }
            )
        else:
            food_goal = ComparativeGoal(
                    name="Get at least 5 food",
                    weight=1.0,
                    desired_state={
                        "food_eaten": ComparisonValuePair(
                            operator=ComparisonOperator.GreaterThanOrEquals,
                            value=3
                        )
                    })
                

        # Lower weight combat goal
        remove_enemies_goal = Goal(
            name="Remove Enemies",
            weight=10.0,
            desired_state={
                "canSeeEnemies": False
            }
        )

        # Sensors
        see_enemies_sensor = Sensor(PlayerFactory._see_enemies_sensor_handler, "Enemy Sight Sensor")
        enemy_proximity_sensor = Sensor(PlayerFactory._enemy_proximity_sensor_handler, "Enemy Proximity Sensor")
        see_food_sensor = Sensor(PlayerFactory._see_food_sensor_handler, "Food Sight Sensor")
        food_proximity_sensor = Sensor(PlayerFactory._food_proximity_sensor_handler, "Food Proximity Sensor")

        # Combat actions
        go_to_enemy_action = Action(
            name="Go To Enemy",
            executor=PlayerFactory._go_to_enemy_executor,
            preconditions={
                "canSeeEnemies": True,
                "nearEnemy": False
            },
            postconditions={
                "nearEnemy": True
            },
            permutation_selectors={
                "target": RpgUtils.enemy_permutations,
                "startingPosition": RpgUtils.starting_position_permutations
            },
            cost_callback=RpgUtils.go_to_enemy_cost
        )

        kill_nearby_enemy_action = Action(
            name="Kill Nearby Enemy",
            executor=PlayerFactory._kill_nearby_enemy_executor,
            preconditions={
                "nearEnemy": True
            },
            postconditions={
               "canSeeEnemies": False,
               "nearEnemy": False
            }
        )

        # Healing actions
        look_for_food_action = Action(
            name="Look For Food",
            executor=PlayerFactory._look_for_food_executor,
            preconditions={
                "canSeeFood": False
            },
            postconditions={
                "canSeeFood": True
            }
        )

        go_to_food_action = Action(
            name="Go To Food",
            executor=PlayerFactory._go_to_food_executor,
            preconditions={
                "canSeeFood": True,
                "nearFood": False
            },
            postconditions={
                "nearFood": True
            },
            permutation_selectors={
                "target": RpgUtils.food_permutations,
                "startingPosition": RpgUtils.starting_position_permutations
            },
            cost_callback=RpgUtils.go_to_food_cost
        )

        eat_food_action = Action(
            name="Eat Food",
            executor=PlayerFactory._eat_food_executor,
            preconditions={
                "nearFood": True
            },
            arithmetic_postconditions={
                "food_eaten": 1  # Increment food eaten count
            }
        )
        
        rest_action = Action(
            name="Rest",
            executor= lambda agent_instance, action_instance: ExecutionStatus.Succeeded,
            preconditions={
                # "nearFood": False,
                "canSeeEnemies": False,
                # "nearEnemy": False,
                "canSeeFood": False,
            },

            arithmetic_postconditions={
                "rest_count": 1
            }
        )
        

        agent = Agent(
            name=name,
            state={
                "canSeeEnemies": False,
                "nearEnemy": False,
                "canSeeFood": False,
                "nearFood": False,
                "hp": 80,
                "food_eaten": 0,
                "position": Vector2(10, 10),
                "faction": "player",
                "agents": agents,
                "foodPositions": food_positions,
                "rest_count": 0
            },
            goals=[
                food_goal,
                remove_enemies_goal,
                ExtremeGoal(
                name="Idle",
                weight=0.1,  # Higher weight than combat
                desired_state={
                    "rest_count": True  # Maximize food_eaten
                }
            )
            ],
            sensors=[
                see_enemies_sensor,
                enemy_proximity_sensor,
                see_food_sensor,
                food_proximity_sensor
            ],
            actions=[
                go_to_enemy_action,
                kill_nearby_enemy_action,
                look_for_food_action,
                go_to_food_action,
                eat_food_action,
                rest_action
            ]
        )
        return agent

    @staticmethod
    def _see_enemies_sensor_handler(agent_instance: Agent) -> None:
        agents_in_state = agent_instance.State.get("agents")
        if isinstance(agents_in_state, list):
            enemy_in_range = RpgUtils.get_enemy_in_range(agent_instance, agents_in_state, 10.0)
            agent_instance.State["canSeeEnemies"] = (enemy_in_range is not None)

    @staticmethod
    def _enemy_proximity_sensor_handler(agent_instance: Agent) -> None:
        agents_in_state = agent_instance.State.get("agents")
        if isinstance(agents_in_state, list):
            enemy_in_range = RpgUtils.get_enemy_in_range(agent_instance, agents_in_state, 1.0)
            agent_instance.State["nearEnemy"] = (enemy_in_range is not None)

    @staticmethod
    def _see_food_sensor_handler(agent_instance: Agent) -> None:
        agent_position = agent_instance.State.get("position")
        food_positions_in_state = agent_instance.State.get("foodPositions")

        if isinstance(agent_position, Vector2) and isinstance(food_positions_in_state, list):
            food_in_range = PlayerFactory._get_food_in_range(agent_position, food_positions_in_state, 20.0)
            agent_instance.State["canSeeFood"] = (food_in_range is not None)

    @staticmethod
    def _food_proximity_sensor_handler(agent_instance: Agent) -> None:
        agent_position = agent_instance.State.get("position")
        food_positions_in_state = agent_instance.State.get("foodPositions")

        if isinstance(agent_position, Vector2) and isinstance(food_positions_in_state, list):
            food_in_range = PlayerFactory._get_food_in_range(agent_position, food_positions_in_state, 1.0)
            agent_instance.State["nearFood"] = (food_in_range is not None)

    @staticmethod
    def _get_food_in_range(source: Vector2, food_positions: List[Vector2], range_val: float) -> Optional[Vector2]:
        """
        Gets the first food position within a given range of a source position.
        """
        for position in food_positions:
            if RpgUtils.in_distance(source, position, range_val):
                return position
        return None

    @staticmethod
    def _kill_nearby_enemy_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        agents_in_state = agent_instance.State.get("agents")
        if isinstance(agents_in_state, list):
            target_enemy = RpgUtils.get_enemy_in_range(agent_instance, agents_in_state, 1.0)
            if target_enemy is not None:
                current_hp = target_enemy.State.get("hp")
                if isinstance(current_hp, int):
                    current_hp -= 1
                    target_enemy.State["hp"] = current_hp
                    print(f"{agent_instance.Name} attacked {target_enemy.Name}. {target_enemy.Name} HP: {current_hp}")
                    if current_hp <= 0:
                        print(f"{target_enemy.Name} defeated!")
                        return ExecutionStatus.Succeeded
        return ExecutionStatus.Failed

    @staticmethod
    def _go_to_enemy_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        target_agent = action_instance.get_parameter("target")
        agent_position = agent_instance.State.get("position")

        if not isinstance(target_agent, Agent) or \
           not isinstance(agent_position, Vector2):
            return ExecutionStatus.Failed
        
        target_position = target_agent.State.get("position")
        if not isinstance(target_position, Vector2):
            return ExecutionStatus.Failed
        
        new_position = RpgUtils.move_towards_other_position(agent_position, target_position)
        agent_instance.State["position"] = new_position
        
        if RpgUtils.in_distance(new_position, target_position, 1.0):
            return ExecutionStatus.Succeeded
        else:
            return ExecutionStatus.Executing

    @staticmethod
    def _look_for_food_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        agent_position = agent_instance.State.get("position")
        if isinstance(agent_position, Vector2):
            import random
            new_x = agent_position.X + random.randint(-1, 1)
            new_y = agent_position.Y + random.randint(-1, 1)

            # Clamp position within world bounds
            
            new_x = max(0, min(new_x, MaxX - 1))
            new_y = max(0, min(new_y, MaxY - 1))

            agent_instance.State["position"] = Vector2(new_x, new_y)

        can_see_food = agent_instance.State.get("canSeeFood")
        if isinstance(can_see_food, bool) and can_see_food:
            return ExecutionStatus.Succeeded
        return ExecutionStatus.Failed

    @staticmethod
    def _go_to_food_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        food_position = action_instance.get_parameter("target")
        agent_position = agent_instance.State.get("position")

        if not isinstance(food_position, Vector2) or \
           not isinstance(agent_position, Vector2):
            return ExecutionStatus.Failed
        
        new_position = RpgUtils.move_towards_other_position(agent_position, food_position)
        agent_instance.State["position"] = new_position

        if RpgUtils.in_distance(new_position, food_position, 1.0):
            return ExecutionStatus.Succeeded
        else:
            return ExecutionStatus.Executing

    @staticmethod
    def _eat_food_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        food_positions_in_state = agent_instance.State.get("foodPositions")
        agent_position = agent_instance.State.get("position")

        if isinstance(food_positions_in_state, list) and isinstance(agent_position, Vector2):
            food_to_eat = PlayerFactory._get_food_in_range(agent_position, food_positions_in_state, 1.0)
            if food_to_eat is not None:
                food_eaten = agent_instance.State.get("food_eaten", 0)
                print(f"{agent_instance.Name} ate food at {food_to_eat}. Food eaten: {food_eaten} -> {food_eaten + 1}")
                food_positions_in_state.remove(food_to_eat)
                return ExecutionStatus.Succeeded
        return ExecutionStatus.Failed
    


class RpgCharacterFactory:
    """
    Class for generating an RPG character.
    """

    @staticmethod
    def create(agents: List[Agent], name: str = "Player") -> Agent:
        """
        Returns an RPG character agent.
        """
        remove_enemies_goal = Goal(
            name="Remove Enemies",
            weight=1.0,
            desired_state={
                "canSeeEnemies": False
            }
        )

        see_enemies_sensor = Sensor(RpgCharacterFactory._see_enemies_sensor_handler, "Enemy Sight Sensor")
        enemy_proximity_sensor = Sensor(RpgCharacterFactory._enemy_proximity_sensor_handler, "Enemy Proximity Sensor")

        go_to_enemy_action = Action(
            name="Go To Enemy",
            executor=RpgCharacterFactory._go_to_enemy_executor,
            preconditions={
                "canSeeEnemies": True,
                "nearEnemy": False
            },
            postconditions={
                "nearEnemy": True
            },
            permutation_selectors={
                "target": RpgUtils.enemy_permutations,
                "startingPosition": RpgUtils.starting_position_permutations
            },
            cost_callback=RpgUtils.go_to_enemy_cost
        )

        kill_nearby_enemy_action = Action(
            name="Kill Nearby Enemy",
            executor=RpgCharacterFactory._kill_nearby_enemy_executor,
            preconditions={
                "nearEnemy": True
            },
            postconditions={
               "canSeeEnemies": False, # After killing, you might not see enemies immediately
               "nearEnemy": False      # And certainly not near this one
            }
        )

        agent = Agent(
            name=name,
            state={
                "canSeeEnemies": False,
                "nearEnemy": False,
                "hp": 80,
                "position": Vector2(10, 10), # Initial position
                "faction": "enemy" if "Monster" in name else "player", # Set default faction, will be overridden for player
                "agents": agents # Reference to the list of all agents in the world
            },
            goals=[
                remove_enemies_goal
            ],
            sensors=[
                see_enemies_sensor,
                enemy_proximity_sensor
            ],
            actions=[
                go_to_enemy_action,
                kill_nearby_enemy_action
            ]
        )
        return agent

    @staticmethod
    def _see_enemies_sensor_handler(agent_instance: Agent) -> None:
        agents_in_state = agent_instance.State.get("agents")
        if isinstance(agents_in_state, list):
            enemy_in_range = RpgUtils.get_enemy_in_range(agent_instance, agents_in_state, 5.0)
            agent_instance.State["canSeeEnemies"] = (enemy_in_range is not None)

    @staticmethod
    def _enemy_proximity_sensor_handler(agent_instance: Agent) -> None:
        agents_in_state = agent_instance.State.get("agents")
        if isinstance(agents_in_state, list):
            enemy_in_range = RpgUtils.get_enemy_in_range(agent_instance, agents_in_state, 1.0)
            agent_instance.State["nearEnemy"] = (enemy_in_range is not None)

    @staticmethod
    def _kill_nearby_enemy_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        agents_in_state = agent_instance.State.get("agents")
        if isinstance(agents_in_state, list):
            target_enemy = RpgUtils.get_enemy_in_range(agent_instance, agents_in_state, 1.0)
            if target_enemy is not None:
                current_hp = target_enemy.State.get("hp")
                if isinstance(current_hp, int):
                    current_hp -= 1
                    target_enemy.State["hp"] = current_hp
                    print(f"{agent_instance.Name} attacked {target_enemy.Name}. {target_enemy.Name} HP: {current_hp}")
                    if current_hp <= 0:
                        print(f"{target_enemy.Name} defeated!")
                        return ExecutionStatus.Succeeded # Action succeeds if enemy is defeated
        return ExecutionStatus.Failed # Action fails if no enemy or enemy not defeated

    @staticmethod
    def _go_to_enemy_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        target_agent = action_instance.get_parameter("target")
        agent_position = agent_instance.State.get("position")

        if not isinstance(target_agent, Agent) or \
           not isinstance(agent_position, Vector2):
            return ExecutionStatus.Failed
        
        target_position = target_agent.State.get("position")
        if not isinstance(target_position, Vector2):
            return ExecutionStatus.Failed
        
        # Move one step towards the target
        new_position = RpgUtils.move_towards_other_position(agent_position, target_position)
        agent_instance.State["position"] = new_position
        
        # Check if now within attacking distance (1 unit)
        if RpgUtils.in_distance(new_position, target_position, 1.0):
            return ExecutionStatus.Succeeded # Reached the proximity to engage
        else:
            return ExecutionStatus.Executing # Still moving, action continues next step




class RpgMonsterFactory:
    """
    Class for generating an RPG monster.
    """

    _rng = random.Random() # Static Random instance
    _counter = 1 # Static counter for naming monsters

    @staticmethod
    def create(agents: List[Agent], food_positions: List[Vector2]) -> Agent:
        """
        Returns an RPG monster agent.
        """
        monster_name = f"Monster {RpgMonsterFactory._counter}"
        RpgMonsterFactory._counter += 1
        
        # Monster is an RPG character, so create using RpgCharacterFactory and then customize
        agent = RpgCharacterFactory.create(agents, monster_name)
        agent.State["faction"] = "enemy" # Ensure monster has enemy faction

        eat_food_goal = Goal(
            name="Eat Food",
            weight=0.1, # Lower weight than 'Remove Enemies' (which is 1.0)
            desired_state={
                "eatingFood": True
            }
        )

        see_food_sensor = Sensor(RpgMonsterFactory._see_food_sensor_handler, "Food Sight Sensor")
        food_proximity_sensor = Sensor(RpgMonsterFactory._food_proximity_sensor_handler, "Food Proximity Sensor")

        look_for_food_action = Action(
            name="Look For Food",
            executor=RpgMonsterFactory._look_for_food_executor,
            preconditions={
                "canSeeFood": False,
                "canSeeEnemies": False # Don't look for food if enemies are visible
            },
            postconditions={
                "canSeeFood": True # This action attempts to see food by moving around
            }
        )

        go_to_food_action = Action(
            name="Go To Food",
            executor=RpgMonsterFactory._go_to_food_executor,
            preconditions={
                "canSeeFood": True,
                "canSeeEnemies": False # Don't go to food if enemies are visible
            },
            postconditions={
                "nearFood": True
            },
            permutation_selectors={
                "target": RpgUtils.food_permutations,
                "startingPosition": RpgUtils.starting_position_permutations
            },
            cost_callback=RpgUtils.go_to_food_cost
        )

        eat_action = Action(
            name="Eat",
            executor=RpgMonsterFactory._eat_executor,
            preconditions={
                "nearFood": True,
                "canSeeEnemies": False # Don't eat if enemies are visible
            },
            postconditions={
                "eatingFood": True # This state means the food is consumed
            }
        )
        
        # Set initial monster-specific state
        agent.State["canSeeFood"] = False
        agent.State["nearFood"] = False
        agent.State["eatingFood"] = False
        agent.State["foodPositions"] = food_positions # Reference to global food positions
        agent.State["hp"] = 2 # Monsters have less HP than player

        # Add monster-specific goals, sensors, actions
        agent.Goals.append(eat_food_goal)
        agent.Sensors.append(see_food_sensor)
        agent.Sensors.append(food_proximity_sensor)
        agent.Actions.append(go_to_food_action)
        agent.Actions.append(look_for_food_action)
        agent.Actions.append(eat_action)
        
        return agent

    @staticmethod
    def _get_food_in_range(source: Vector2, food_positions: List[Vector2], range_val: float) -> Optional[Vector2]:
        """
        Gets the first food position within a given range of a source position.
        """
        # C# FirstOrDefault with a default value.
        # In Python, we can loop or use next with a generator expression.
        for position in food_positions:
            if RpgUtils.in_distance(source, position, range_val):
                return position
        return None # No food found in range

    @staticmethod
    def _see_food_sensor_handler(agent_instance: Agent) -> None:
        agent_position = agent_instance.State.get("position")
        food_positions_in_state = agent_instance.State.get("foodPositions")

        if isinstance(agent_position, Vector2) and isinstance(food_positions_in_state, list):
            food_in_range = RpgMonsterFactory._get_food_in_range(agent_position, food_positions_in_state, 5.0)
            if food_in_range is not None:
                agent_instance.State["canSeeFood"] = True
            else:
                agent_instance.State["canSeeFood"] = False
                agent_instance.State["eatingFood"] = False # Cannot be eating if no food is seen

    @staticmethod
    def _food_proximity_sensor_handler(agent_instance: Agent) -> None:
        agent_position = agent_instance.State.get("position")
        food_positions_in_state = agent_instance.State.get("foodPositions")

        if isinstance(agent_position, Vector2) and isinstance(food_positions_in_state, list):
            food_in_range = RpgMonsterFactory._get_food_in_range(agent_position, food_positions_in_state, 1.0)
            if food_in_range is not None:
                agent_instance.State["nearFood"] = True
            else:
                agent_instance.State["nearFood"] = False
                agent_instance.State["eatingFood"] = False # Cannot be eating if not near food

    @staticmethod
    def _look_for_food_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        agent_position = agent_instance.State.get("position")
        if isinstance(agent_position, Vector2):
            new_x = agent_position.X + RpgMonsterFactory._rng.randint(-1, 1) # randint includes both ends
            new_y = agent_position.Y + RpgMonsterFactory._rng.randint(-1, 1)

            # Clamp position within world bounds
            new_x = max(0, min(new_x, MaxX - 1))
            new_y = max(0, min(new_y, MaxY - 1))

            agent_instance.State["position"] = Vector2(new_x, new_y) # Update position

        # Check if food is now seen *after* moving
        # The sensor would run *after* this executor in the agent.step cycle,
        # but this check needs to be against the *current* state of `canSeeFood` before executor.
        # This executor is designed to succeed if food becomes true *after* its application.
        # However, the current code checks it *before* sensor updates the state.
        # The C# original also checks `agent.State["canSeeFood"]` after modifying `position` but before agent.Step finishes.
        # The crucial part is that `agent.State["canSeeFood"]` would be updated by the sensor *after* this action executes.
        # So, this action's success is determined by whether it *enabled* the sensor to see food.
        # If agent.State["canSeeFood"] is true from a prior run of the sensor, it means it's seen.
        # The `is bool canSeeFood && canSeeFood` checks `canSeeFood` as it *currently* is.
        # This implies it returns Succeeded if food was seen *before* the action or if the action doesn't change it.
        # A more direct interpretation of "look for food" succeeding when food is *now visible* might require
        # checking the condition immediately after its own effects are applied but before sensors run again.
        # For strict verbatim, use the existing state value:
        can_see_food = agent_instance.State.get("canSeeFood")
        if isinstance(can_see_food, bool) and can_see_food:
            return ExecutionStatus.Succeeded
        return ExecutionStatus.Failed # Continue searching

    @staticmethod
    def _go_to_food_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        food_position = action_instance.get_parameter("target")
        agent_position = agent_instance.State.get("position")

        if not isinstance(food_position, Vector2) or \
           not isinstance(agent_position, Vector2):
            return ExecutionStatus.Failed
        
        new_position = RpgUtils.move_towards_other_position(agent_position, food_position)
        agent_instance.State["position"] = new_position

        if RpgUtils.in_distance(new_position, food_position, 1.0):
            return ExecutionStatus.Succeeded # Reached the food
        else:
            return ExecutionStatus.Executing # Still moving towards food

    @staticmethod
    def _eat_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        food_positions_in_state = agent_instance.State.get("foodPositions")
        agent_position = agent_instance.State.get("position")

        if isinstance(food_positions_in_state, list) and isinstance(agent_position, Vector2):
            food_to_eat = RpgMonsterFactory._get_food_in_range(agent_position, food_positions_in_state, 1.0)
            if food_to_eat is not None:
                print(f"{agent_instance.Name} ate food at {food_to_eat}")
                # Remove the food from the global list
                food_positions_in_state.remove(food_to_eat)
                return ExecutionStatus.Succeeded
        return ExecutionStatus.Failed




# Pygame constants
CELL_SIZE = 30
WIDTH = 20 * CELL_SIZE
HEIGHT = 20 * CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)


class RpgExampleComparativePygame:
    """
    RPG example demo.
    """


    @staticmethod
    def run() -> None:
        _ = DefaultLogger(log_to_console=True, logging_file="rpg-example.log", filter_string="Monster")
        
        # Initialize pygame
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("RPG GOAP Example")
        clock = pygame.time.Clock()
        
        _random = random.Random() # Instance of Random
        agents: List[Agent] = []
        food_positions: List[Vector2] = []

        player = PlayerFactory.create(agents, food_positions)
        agents.append(player)

        # Create food positions
        for _ in range(20):
            food_positions.append(Vector2(_random.randint(0, MaxX - 1), _random.randint(0, MaxY - 1)))
        
        # Create monsters
        for _ in range(10):
            monster = RpgMonsterFactory.create(agents, food_positions)
            monster.State["position"] = Vector2(_random.randint(0, MaxX - 1), _random.randint(0, MaxY - 1))
            agents.append(monster)
        
        # Game loop
        running = True
        turn = 0
        last_update = pygame.time.get_ticks()
        
        while running and turn < 600:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Update game state every 200ms
            current_time = pygame.time.get_ticks()
            if current_time - last_update >= 200:
                turn += 1
                print(f"--- Turn {turn} ---")
                
                for agent in agents:
                    agent.step(mode=StepMode.OneAction) # Each agent executes one action
                
                RpgExampleComparativePygame._process_deaths(agents)
                last_update = current_time

                # Check if player is still alive
                if player not in agents:
                    print("Player defeated! Game Over.")
                    break
                # Check if all monsters are defeated (goal met for player)
                monsters_alive = [a for a in agents if a.State.get("faction") == "enemy"]
            
            # Render
            RpgExampleComparativePygame._render_grid(screen, agents, food_positions)
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
            
        print("Game finished.")
        pygame.quit()

    @staticmethod
    def _render_grid(screen: pygame.Surface, agents: List[Agent], food_positions: List[Vector2]) -> None:
        # Clear screen
        screen.fill(BLACK)
        
        # Draw grid lines
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

        # Draw food
        for pos in food_positions:
            if 0 <= pos.X < MaxX and 0 <= pos.Y < MaxY:
                rect = pygame.Rect(int(pos.X) * CELL_SIZE + 2, int(pos.Y) * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
                pygame.draw.ellipse(screen, YELLOW, rect)

        # Draw agents
        for agent in agents:
            agent_pos = agent.State.get("position")
            agent_faction = agent.State.get("faction")
            
            if isinstance(agent_pos, Vector2) and isinstance(agent_faction, str):
                if 0 <= agent_pos.X < MaxX and 0 <= agent_pos.Y < MaxY:
                    rect = pygame.Rect(int(agent_pos.X) * CELL_SIZE + 2, int(agent_pos.Y) * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
                    
                    if agent_faction == "player":
                        # Red if health below 30, otherwise blue
                        agent_hp = agent.State.get("hp")
                        color = RED if isinstance(agent_hp, int) and agent_hp < 30 else BLUE
                        pygame.draw.rect(screen, color, rect)
                    else: # Monster
                        pygame.draw.rect(screen, GREEN, rect)

    @staticmethod
    def _process_deaths(agents: List[Agent]) -> None:
        cull_list: List[Agent] = []
        for agent in agents:
            hp = agent.State.get("hp")
            if isinstance(hp, int) and hp <= 0:
                cull_list.append(agent)
        
        for agent_to_remove in cull_list:
            agents.remove(agent_to_remove)
            print(f"Agent {agent_to_remove.Name} has died.")


if __name__ == "__main__":
    RpgExampleComparativePygame.run()

