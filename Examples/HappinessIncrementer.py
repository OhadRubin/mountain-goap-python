# // <copyright file="HappinessIncrementer.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import Dict, Any, Optional

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.Goal import Goal
from MountainGoap.Sensor import Sensor
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoapLogging.DefaultLogger import DefaultLogger

class HappinessIncrementer:
    """
    Simple goal to increment happiness using normal goals and a sensor.
    """

    @staticmethod
    def run() -> None:
        _ = DefaultLogger() # Initialize logger to subscribe to events
        
        agent = Agent(
            name="Happiness Agent",
            state={
                "happiness": 0,
                "happinessRecentlyIncreased": False
            },
            goals=[
                Goal(
                    name="Maximize Happiness",
                    desired_state={
                        "happinessRecentlyIncreased": True
                    })
            ],
            sensors=[
                Sensor(HappinessIncrementer._ennui_sensor_handler, "Ennui Sensor")
            ],
            actions=[
                Action(
                    name="Seek Happiness",
                    executor=HappinessIncrementer._seek_happiness_action,
                    preconditions={
                        "happinessRecentlyIncreased": False
                    },
                    postconditions={
                        "happinessRecentlyIncreased": True
                    }
                )
            ]
        )

        # C# while loop condition: `while (agent.State["happiness"] is int happiness && happiness != 10)`
        while agent.State.get("happiness") != 10:
            agent.step()
            # The Console.WriteLine for happiness is in SeekHappinessAction executor itself
            # import time
            # time.sleep(0.1)

    @staticmethod
    def _seek_happiness_action(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        happiness: Optional[int] = agent_instance.State.get("happiness")
        if happiness is not None and isinstance(happiness, int):
            happiness += 1
            agent_instance.State["happiness"] = happiness
            print("Seeking happiness.")
            print(f"NEW HAPPINESS IS {happiness}")
        return ExecutionStatus.Succeeded

    @staticmethod
    def _ennui_sensor_handler(agent_instance: Agent) -> None:
        agent_instance.State["happinessRecentlyIncreased"] = False


if __name__ == "__main__":
    HappinessIncrementer.run()
