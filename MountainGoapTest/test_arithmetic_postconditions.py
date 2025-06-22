# // <copyright file="ArithmeticPostconditionsTests.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import pytest
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.ComparativeGoal import ComparativeGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.StepMode import StepMode

class TestArithmeticPostconditions:
    @pytest.fixture(autouse=True) # Ensure events are cleared for each test
    def _fixture_setup(self, setup_teardown_events):
        pass

    def test_minimal_example_test(self):
        goals = [
            ComparativeGoal(
                name="Goal1",
                desired_state={
                    "i": ComparisonValuePair(
                        value=100,
                        operator=ComparisonOperator.GreaterThan
                    )
                },
                weight=1.0
            ),
        ]

        actions = [
            Action(
                name="Action1",
                executor=lambda agent_inst, action_inst: ExecutionStatus.Succeeded,
                arithmetic_postconditions={
                    "i": 10
                },
                cost=0.5
            ),
        ]

        agent = Agent(
            goals=goals,
            actions=actions,
            state={
                "i": 0
            }
        )

        agent.step(StepMode.OneAction)
        assert agent.State["i"] == 10
        assert not agent.IsBusy # Should not be busy after one step as goal not met and it keeps planning

        # Agent should re-plan and execute again
        agent.step(StepMode.OneAction)
        assert agent.State["i"] == 20
        assert not agent.IsBusy

        # Keep stepping until goal is met
        for _ in range(8): # From 20 to 100 requires 8 more steps of +10
            agent.step(StepMode.OneAction)

        assert agent.State["i"] == 100
        # The goal is "greater than 100", so 100 is not enough. It will need one more.
        assert not agent.CurrentActionSequences # Should be empty as it planned to 100 but not > 100

        # Plan and execute one more step to reach > 100
        agent.step(StepMode.OneAction)
        assert agent.State["i"] == 110
        assert not agent.IsBusy
        assert not agent.CurrentActionSequences

