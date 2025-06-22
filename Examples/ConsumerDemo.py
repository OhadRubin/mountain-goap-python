# // <copyright file="ConsumerDemo.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import sys
import os
from typing import Dict, Any, Optional, List

# Assuming MountainGoap and MountainGoapLogging are available in PYTHONPATH
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.ComparativeGoal import ComparativeGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.PermutationSelectorGenerators import PermutationSelectorGenerators
from MountainGoapLogging.DefaultLogger import DefaultLogger

class ConsumerDemo:
    """
    Goal to create enough food to eat by working and grocery shopping.
    """

    @staticmethod
    def run() -> None:
        _ = DefaultLogger() # Initialize logger to subscribe to events
        
        locations = ["home", "work", "store"]
        
        agent = Agent(
            name="Consumer Agent",
            state={
                "food": 0,
                "energy": 100,
                "money": 0,
                "inCar": False,
                "location": "home",
                "justTraveled": False
            },
            goals=[
                ComparativeGoal(
                    name="Get at least 5 food",
                    desired_state={
                        "food": ComparisonValuePair(
                            operator=ComparisonOperator.GreaterThanOrEquals,
                            value=5
                        )
                    })
            ],
            actions=[
                Action(
                    name="Walk",
                    cost=6.0,
                    executor=ConsumerDemo._generic_executor,
                    preconditions={
                        "inCar": False
                    },
                    permutation_selectors={
                        "location": PermutationSelectorGenerators.select_from_collection(locations)
                    },
                    comparative_preconditions={
                        "energy": ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0)
                    },
                    arithmetic_postconditions={
                        "energy": -1
                    },
                    parameter_postconditions={
                        "location": "location" # Parameter 'location' (from permutation selector) copied to state 'location'
                    }
                ),
                Action(
                    name="Drive",
                    cost=1.0,
                    preconditions={
                        "inCar": True,
                        "justTraveled": False
                    },
                    comparative_preconditions={
                        "energy": ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0)
                    },
                    executor=ConsumerDemo._generic_executor,
                    permutation_selectors={
                        "location": PermutationSelectorGenerators.select_from_collection(locations)
                    },
                    arithmetic_postconditions={
                        "energy": -1
                    },
                    parameter_postconditions={
                        "location": "location"
                    },
                    postconditions={
                        "justTraveled": True # Prevent repeated driving in one logical "turn" if the action implies a single move
                    }
                ),
                Action(
                    name="Get in car",
                    cost=1.0,
                    preconditions={
                        "inCar": False,
                        "justTraveled": False # Cannot get in car if just traveled implies it's part of same "turn"
                    },
                    comparative_preconditions={
                        "energy": ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0)
                    },
                    postconditions={
                        "inCar": True
                    },
                    arithmetic_postconditions={
                        "energy": -1
                    },
                    executor=ConsumerDemo._generic_executor
                ),
                Action(
                    name="Get out of car",
                    cost=1.0,
                    preconditions={
                        "inCar": True
                    },
                    comparative_preconditions={
                        "energy": ComparisonOperator.GreaterThan, value=0 # C# code is missing ComparisonValuePair() here.
                                                                           # Assuming it should be `ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0)`
                    },
                    postconditions={
                        "inCar": False
                    },
                    arithmetic_postconditions={
                        "energy": -1
                    },
                    executor=ConsumerDemo._generic_executor
                ),
                Action(
                    name="Work",
                    cost=1.0,
                    preconditions={
                        "location": "work",
                        "inCar": False
                    },
                    comparative_preconditions={
                        "energy": ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0)
                    },
                    arithmetic_postconditions={
                        "energy": -1,
                        "money": 1
                    },
                    postconditions={
                        "justTraveled": False # Reset justTraveled after arriving and working
                    },
                    executor=ConsumerDemo._generic_executor
                ),
                Action(
                    name="Shop",
                    cost=1.0,
                    preconditions={
                        "location": "store",
                        "inCar": False
                    },
                    comparative_preconditions={
                        "energy": ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0),
                        "money": ComparisonValuePair(operator=ComparisonOperator.GreaterThan, value=0)
                    },
                    arithmetic_postconditions={
                        "energy": -1,
                        "money": -1, # Spend money to buy food
                        "food": 1
                    },
                    postconditions={
                        "justTraveled": False # Reset justTraveled after arriving and shopping
                    },
                    executor=ConsumerDemo._generic_executor
                )
            ]
        )

        # C# while loop condition: `while (agent.State["food"] is int food && food < 5)`
        step_count = 0
        max_steps = 100 # Safety break to prevent infinite loops in demos
        while agent.State.get("food") is not None and agent.State["food"] < 5 and step_count < max_steps:
            agent.step()
            step_count += 1
            print(f"--- Step {step_count} ---")
            print(f"Food: {agent.State.get('food')}, Energy: {agent.State.get('energy')}, Money: {agent.State.get('money')}, Location: {agent.State.get('location')}, In Car: {agent.State.get('inCar')}, Just Traveled: {agent.State.get('justTraveled')}")
            # import time
            # time.sleep(0.1)

        if step_count >= max_steps:
            print(f"ConsumerDemo stopped after {max_steps} steps without reaching goal.")
        else:
            print(f"ConsumerDemo finished in {step_count} steps. Food: {agent.State.get('food')}")


    @staticmethod
    def _generic_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
        # print(f"Executing {action_instance.Name}. Params: {action_instance._parameters}")
        return ExecutionStatus.Succeeded


if __name__ == "__main__":
    ConsumerDemo.run()

