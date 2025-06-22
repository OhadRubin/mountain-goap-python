# // <copyright file="ActionNodeTests.py" company="Chris Muller">
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
from typing import Dict, Any, Optional

class TestAgent:
    @pytest.fixture(autouse=True) # Ensure events are cleared for each test
    def _fixture_setup(self, setup_teardown_events):
        pass

    def test_it_handles_initial_null_state_values_correctly(self):
        agent = Agent(
            state={
                "key": None
            },
            goals=[
                Goal(
                    desired_state={
                        "key": "non-null value"
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": None
                    },
                    postconditions={
                        "key": "non-null value"
                    },
                    executor=lambda agent_inst, action_inst: ExecutionStatus.Succeeded
                )
            ]
        )
        agent.step(StepMode.OneAction)
        assert agent.State["key"] is not None
        assert agent.State["key"] == "non-null value"

    def test_it_handles_null_goals_correctly(self):
        agent = Agent(
            state={
                "key": "non-null value"
            },
            goals=[
                Goal(
                    desired_state={
                        "key": None
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": "non-null value"
                    },
                    postconditions={
                        "key": None
                    },
                    executor=lambda agent_inst, action_inst: ExecutionStatus.Succeeded
                )
            ]
        )
        agent.step(StepMode.OneAction)
        assert agent.State["key"] is None

    def test_it_handles_non_null_state_values_correctly(self):
        agent = Agent(
            state={
                "key": "value"
            },
            goals=[
                Goal(
                    desired_state={
                        "key": "new value"
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": "value"
                    },
                    postconditions={
                        "key": "new value"
                    },
                    executor=lambda agent_inst, action_inst: ExecutionStatus.Succeeded
                )
            ]
        )
        agent.step(StepMode.OneAction)
        value = agent.State["key"]
        assert value is not None
        assert value == "new value"

    def test_it_executes_one_action_in_one_action_step_mode(self):
        action_count = 0

        def custom_executor(agent_inst: Agent, action_inst: Action) -> ExecutionStatus:
            nonlocal action_count
            action_count += 1
            return ExecutionStatus.Succeeded

        agent = Agent(
            state={
                "key": "value"
            },
            goals=[
                Goal(
                    desired_state={
                        "key": "new value"
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": "value"
                    },
                    postconditions={
                        "key": "new value"
                    },
                    executor=custom_executor
                )
            ]
        )
        agent.step(StepMode.OneAction)
        assert action_count == 1
        assert agent.State["key"] == "new value"
        assert not agent.IsBusy
        assert not agent.CurrentActionSequences # Plan should be completed

    def test_it_executes_all_actions_in_all_actions_step_mode(self):
        action_count = 0

        def first_executor(agent_inst: Agent, action_inst: Action) -> ExecutionStatus:
            nonlocal action_count
            action_count += 1
            return ExecutionStatus.Succeeded

        def second_executor(agent_inst: Agent, action_inst: Action) -> ExecutionStatus:
            nonlocal action_count
            action_count += 1
            return ExecutionStatus.Succeeded

        agent = Agent(
            state={
                "key": "value"
            },
            goals=[
                Goal(
                    desired_state={
                        "key": "new value"
                    }
                )
            ],
            actions=[
                Action(
                    preconditions={
                        "key": "value"
                    },
                    postconditions={
                        "key": "intermediate value"
                    },
                    executor=first_executor
                ),
                Action(
                    preconditions={
                        "key": "intermediate value"
                    },
                    postconditions={
                        "key": "new value"
                    },
                    executor=second_executor
                )
            ]
        )
        agent.step(StepMode.AllActions)
        assert action_count == 2
        assert agent.State["key"] == "new value"
        assert not agent.IsBusy
        assert not agent.CurrentActionSequences # Plan should be completed

