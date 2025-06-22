# // <copyright file="RpgCharacterFactory.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

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

# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

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
                "hp": 10,
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

