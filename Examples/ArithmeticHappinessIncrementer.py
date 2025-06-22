# // <copyright file="ArithmeticHappinessIncrementer.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import Dict, Any, Optional

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
# or current directory structure allows direct relative imports
# For this example, assuming sys.path has been configured (e.g., via conftest.py or manual setup)
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.Goal import Goal
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoapLogging.DefaultLogger import DefaultLogger

class ArithmeticHappinessIncrementer:
    """
    Simple goal to maximize happiness using arithmetic postconditions.
    """

    @staticmethod
    def run() -> None:
        _ = DefaultLogger() # Initialize logger to subscribe to events
        
        agent = Agent(
            name="Happiness Agent",
            state={
                "happiness": 0,
            },
            goals=[
                Goal(
                    name="Maximize Happiness",
                    desired_state={
                        "happiness": 10
                    })
            ],
            actions=[
                Action(
                    name="Seek Happiness",
                    executor=ArithmeticHappinessIncrementer._seek_happiness_action,
                    arithmetic_postconditions={
                        "happiness": 1
                    }
                ),
                Action(
                    name="Seek Greater Happiness",
                    executor=ArithmeticHappinessIncrementer._seek_greater_happiness_action,
                    arithmetic_postconditions={
                        "happiness": 2
                    }
                )
            ]
        )

        # The loop condition in C#: `while (agent.State["happiness"] is int happiness && happiness != 10)`
        # `is int happiness` performs a type check and casts. In Python, we just check the value.
        while agent.State.get("happiness") != 10:
            agent.step()
            print(f"NEW HAPPINESS IS {agent.State.get('happiness')}")
            # Add a small delay to make output readable if running fast
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

