# // <copyright file="CarDemo.py" company="Chris Muller">
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
from MountainGoap.PermutationSelectorGenerators import PermutationSelectorGenerators
from MountainGoapLogging.DefaultLogger import DefaultLogger

class CarDemo:
    """
    Simple goal to travel via walking or driving.
    """

    @staticmethod
    def run() -> None:
        _ = DefaultLogger() # Initialize logger to subscribe to events
        
        agent = Agent(
            name="Driving Agent",
            state={
                "distanceTraveled": 0,
                "inCar": False
            },
            goals=[
                ComparativeGoal(
                    name="Travel 50 miles",
                    desired_state={
                        "distanceTraveled": ComparisonValuePair(
                            operator=ComparisonOperator.GreaterThanOrEquals,
                            value=50
                        )
                    })
            ],
            actions=[
                Action(
                    name="Walk",
                    cost=50.0,
                    postconditions={
                        "distanceTraveled": 50
                    },
                    executor=CarDemo._travel_executor
                ),
                Action(
                    name="Drive",
                    cost=5.0,
                    preconditions={
                        "inCar": True
                    },
                    postconditions={
                        "distanceTraveled": 50
                    },
                    executor=CarDemo._travel_executor
                ),
                Action(
                    name="Get in Car",
                    cost=1.0,
                    preconditions={
                        "inCar": False
                    },
                    postconditions={
                        "inCar": True
                    },
                    executor=CarDemo._get_in_car_executor
                )
            ]
        )

        # C# while loop condition: `while (agent.State["distanceTraveled"] is int distance && distance < 50)`
        while agent.State.get("distanceTraveled") is not None and agent.State["distanceTraveled"] < 50:
            agent.step()
            # Optional: Add print statement to see progress
            # print(f"Distance traveled: {agent.State.get('distanceTraveled')}, In car: {agent.State.get('inCar')}")
            # import time
            # time.sleep(0.1)

    @staticmethod
    def _travel_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        # print(f"Executing {action_instance.Name}")
        return ExecutionStatus.Succeeded

    @staticmethod
    def _get_in_car_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        # print(f"Executing {action_instance.Name}")
        return ExecutionStatus.Succeeded

