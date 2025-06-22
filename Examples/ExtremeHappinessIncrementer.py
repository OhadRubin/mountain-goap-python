# // <copyright file="ExtremeHappinessIncrementer.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import Dict, Any, Optional

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.ExtremeGoal import ExtremeGoal
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoapLogging.DefaultLogger import DefaultLogger

class ExtremeHappinessIncrementer:
    """
    Simple goal to maximize happiness using extreme goals.
    """

    @staticmethod
    def run() -> None:
        _ = DefaultLogger() # Initialize logger to subscribe to events
        
        agent = Agent(
            name="Happiness Agent",
            state={
                "happiness": 0,
                "health": False,
            },
            goals=[
                ExtremeGoal(
                    name="Maximize Happiness",
                    desired_state={
                        "happiness": True # True to maximize, False to minimize
                    })
            ],
            actions=[
                Action(
                    name="Seek Happiness",
                    executor=ExtremeHappinessIncrementer._seek_happiness_action,
                    preconditions={
                        "health": True # Requires health to seek happiness
                    },
                    arithmetic_postconditions={
                        "happiness": 1
                    }
                ),
                Action(
                    name="Seek Greater Happiness",
                    executor=ExtremeHappinessIncrementer._seek_greater_happiness_action,
                    preconditions={
                        "health": True # Requires health to seek greater happiness
                    },
                    arithmetic_postconditions={
                        "happiness": 2
                    }
                ),
                Action(
                    name="Seek Health",
                    executor=ExtremeHappinessIncrementer._seek_health,
                    postconditions={
                        "health": True # Sets health to true
                    }
                ),
            ]
        )

        # C# while loop condition: `while (agent.State["happiness"] is int happiness && happiness != 10)`
        while agent.State.get("happiness") != 10:
            agent.step()
            print(f"NEW HAPPINESS IS {agent.State.get('happiness')}")
            # import time
            # time.sleep(0.1)

    @staticmethod
    def _seek_happiness_action(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        print("Seeking happiness.")
        return ExecutionStatus.Succeeded

    @staticmethod
    def _seek_greater_happiness_action(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        print("Seeking even greater happiness.")
        return ExecutionStatus.Succeeded

    @staticmethod
    def _seek_health(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        print("Seeking health.")
        return ExecutionStatus.Succeeded

