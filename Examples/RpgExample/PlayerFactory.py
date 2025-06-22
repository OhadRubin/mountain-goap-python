# // <copyright file="PlayerFactory.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import List, Dict, Any, Optional

# Assuming MountainGoap and RpgUtils are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.Goal import Goal
from MountainGoap.ExtremeGoal import ExtremeGoal
from MountainGoap.Sensor import Sensor
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.BaseGoal import BaseGoal

from Examples.RpgExample.RpgUtils import RpgUtils, Vector2

# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

class PlayerFactory:
    """
    Class for generating a player character with healing abilities.
    """

    @staticmethod
    def create(agents: List[Agent], food_positions: List[Vector2], name: str = "Player") -> Agent:
        """
        Returns a player agent with healing and combat capabilities.
        """
        # High priority goal to maximize food eaten
        food_goal = ExtremeGoal(
            name="Maximize Food Eaten",
            weight=10.0,  # Higher priority than combat
            desired_state={
                "food_eaten": True  # Maximize food_eaten
            }
        )

        # Lower priority combat goal
        remove_enemies_goal = Goal(
            name="Remove Enemies",
            weight=1.0,
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
                "foodPositions": food_positions
            },
            goals=[
                food_goal,
                remove_enemies_goal
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
                eat_food_action
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
    def _see_food_sensor_handler(agent_instance: Agent) -> None:
        agent_position = agent_instance.State.get("position")
        food_positions_in_state = agent_instance.State.get("foodPositions")

        if isinstance(agent_position, Vector2) and isinstance(food_positions_in_state, list):
            food_in_range = PlayerFactory._get_food_in_range(agent_position, food_positions_in_state, 5.0)
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
            from Examples.RpgExample.RpgExampleComparative import RpgExampleComparative
            new_x = max(0, min(new_x, RpgExampleComparative.MaxX - 1))
            new_y = max(0, min(new_y, RpgExampleComparative.MaxY - 1))

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