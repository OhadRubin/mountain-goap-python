# // <copyright file="ComparativeHappinessIncrementer.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import Dict, Any, Optional

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.ComparativeGoal import ComparativeGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoapLogging.DefaultLogger import DefaultLogger

class ComparativeHappinessIncrementer:
    """
    Simple goal to maximize happiness using comparative goals.
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
                ComparativeGoal(
                    name="Maximize Happiness",
                    desired_state={
                        "happiness": ComparisonValuePair(
                            operator=ComparisonOperator.GreaterThanOrEquals,
                            value=10
                        )
                    })
            ],
            actions=[
                Action(
                    name="Seek Happiness",
                    executor=ComparativeHappinessIncrementer._seek_happiness_action,
                    arithmetic_postconditions={
                        "happiness": 1
                    }
                ),
                Action(
                    name="Seek Greater Happiness",
                    executor=ComparativeHappinessIncrementer._seek_greater_happiness_action,
                    arithmetic_postconditions={
                        "happiness": 2
                    }
                )
            ]
        )

        # C# while loop condition: `while (agent.State["happiness"] is int happiness && happiness < 10)`
        while agent.State.get("happiness") is not None and agent.State["happiness"] < 10:
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


if __name__ == "__main__":
    ComparativeHappinessIncrementer.run()

