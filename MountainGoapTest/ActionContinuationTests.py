# // <copyright file="ActionContinuationTests.py" company="Chris Muller">
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
from MountainGoap.StepMode import StepMode
from typing import Dict, Any

class ActionContinuationTests:
    @pytest.fixture(autouse=True) # Ensure events are cleared for each test
    def _fixture_setup(self, setup_teardown_events):
        pass

    def test_it_can_continue_actions(self):
        times_executed = 0

        def custom_executor(agent_instance: Agent, action_instance: Action) -> ExecutionStatus:
            nonlocal times_executed
            times_executed += 1
            if isinstance(agent_instance.State.get("progress"), int) and agent_instance.State["progress"] < 3:
                agent_instance.State["progress"] = agent_instance.State["progress"] + 1
                return ExecutionStatus.Executing
            else:
                return ExecutionStatus.Succeeded

        agent = Agent(
            state={
                "key": False,
                "progress": 0
            },
            goals=[
                Goal(
                    desired_state={
                        "key": True
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": False
                    },
                    postconditions={
                        "key": True # This is applied only when the action SUCCEEDS, not when it's Executing
                    },
                    executor=custom_executor
                )
            ]
        )

        agent.step(StepMode.OneAction)
        assert agent.State["key"] is False
        assert times_executed == 1
        assert agent.CurrentActionSequences[0][0].ExecutionStatus == ExecutionStatus.Executing

        agent.step(StepMode.OneAction)
        assert agent.State["key"] is False
        assert times_executed == 2
        assert agent.CurrentActionSequences[0][0].ExecutionStatus == ExecutionStatus.Executing

        agent.step(StepMode.OneAction)
        assert agent.State["key"] is False
        assert times_executed == 3
        assert agent.CurrentActionSequences[0][0].ExecutionStatus == ExecutionStatus.Executing

        agent.step(StepMode.OneAction)
        assert agent.State["key"] is True # Now it should be True as the action successfully completed
        assert times_executed == 4
        assert not agent.CurrentActionSequences # Plan should be empty now
        assert not agent.IsBusy # Agent should no longer be busy

