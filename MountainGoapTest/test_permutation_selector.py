# // <copyright file="PermutationSelectorTests.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# global using Xunit;
# global using MountainGoap;
# These are handled by conftest.py
import pytest
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.Goal import Goal
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.PermutationSelectorGenerators import PermutationSelectorGenerators
from MountainGoap.Sensor import Sensor
from MountainGoap.StepMode import StepMode
from typing import Dict, Any, List, Optional

class TestPermutationSelector:
    @pytest.fixture(autouse=True) # Ensure events are cleared for each test
    def _fixture_setup(self, setup_teardown_events):
        pass

    def test_it_selects_from_a_dynamically_generated_collection_in_state(self):
        collection = [1, 2, 3]
        selector = PermutationSelectorGenerators.select_from_collection_in_state("collection")

        def sample_executor(agent_inst: Agent, action_inst: Action) -> ExecutionStatus:
            return ExecutionStatus.Succeeded

        def sample_sensor_run(agent_inst: Agent) -> None:
            if isinstance(agent_inst.State.get("collection"), list):
                # Ensure it's a list of ints explicitly if needed, though Python is dynamic
                agent_inst.State["collection"].append(len(agent_inst.State["collection"]) + 1)

        agent = Agent(
            name="sample agent",
            state={
                "collection": collection,
                "goalAchieved": False
            },
            goals=[
                Goal(
                    name="sample goal",
                    desired_state={
                        "goalAchieved": True
                    }
                )
            ],
            actions=[
                Action(
                    name="sample action",
                    cost=1.0,
                    preconditions={
                        "goalAchieved": False
                    },
                    postconditions={
                        "goalAchieved": True
                    },
                    executor=sample_executor
                )
            ],
            sensors=[
                Sensor(
                    run_callback=sample_sensor_run,
                    name="sample sensor"
                )
            ]
        )

        # Before any steps, the selector should see the initial collection size
        permutations = selector(agent.State)
        assert len(permutations) == 3
        assert agent.State["collection"] == [1, 2, 3]

        # Step 1: Agent plans and executes 'sample action'. Sensor runs BEFORE planning.
        # So, the collection should be updated by the sensor before the planner uses it.
        agent.step(StepMode.OneAction) # Sensor runs, then plan, then 1 action executed
        
        # After step 1, the sensor should have added an item.
        # The plan for step 1 was based on the state *before* the sensor run in this step.
        # But for the *next* planning cycle (after this step is done), the new state is visible.
        # Let's re-evaluate permutations (which reads current agent.State)
        permutations = selector(agent.State)
        assert len(permutations) == 4
        assert agent.State["collection"] == [1, 2, 3, 4]
        assert agent.State["goalAchieved"] is True # The action should have completed the goal

        # Step 2: Agent tries to plan again, but goal is met, so no new plan.
        # Sensor will still run.
        agent.step(StepMode.OneAction)
        
        permutations = selector(agent.State)
        assert len(permutations) == 5
        assert agent.State["collection"] == [1, 2, 3, 4, 5]
        # goalAchieved remains true, no new action from planning.

