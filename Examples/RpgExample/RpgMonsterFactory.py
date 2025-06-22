# // <copyright file="RpgMonsterFactory.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import random
import sys
import os
from typing import List, Dict, Any, Optional

# Assuming MountainGoap and RpgUtils are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.Goal import Goal
from MountainGoap.Sensor import Sensor
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair

from .RpgUtils import RpgUtils, Vector2
from .RpgCharacterFactory import RpgCharacterFactory
from .RpgExample import RpgExample # To access MaxX, MaxY


# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

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
            from .RpgExample import RpgExample # Local import to get MaxX, MaxY
            new_x = max(0, min(new_x, RpgExample.MaxX - 1))
            new_y = max(0, min(new_y, RpgExample.MaxY - 1))

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

