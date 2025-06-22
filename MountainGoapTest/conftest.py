# conftest.py can be used for global fixtures or imports in pytest.
# This replaces the C# `Usings.cs` which adds global `using` directives.

import pytest
import sys
import os

# Add the project root to sys.path to allow relative imports
# Assuming 'MountainGoap' and 'MountainGoapTest' are siblings
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Global imports for tests, similar to C# Usings.cs
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.Goal import Goal
from MountainGoap.ComparativeGoal import ComparativeGoal
from MountainGoap.ComparisonOperator import ComparisonOperator
from MountainGoap.ComparisonValuePair import ComparisonValuePair
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.StepMode import StepMode
from MountainGoap.PermutationSelectorGenerators import PermutationSelectorGenerators
from MountainGoap.Sensor import Sensor

# You might want to define fixtures here for common test setup
@pytest.fixture(autouse=True)
def setup_teardown_events():
    """
    Fixture to clear event handlers before and after each test
    to prevent cross-test interference.
    """
    # Before test: Clear all handlers
    Agent._on_agent_step_handlers.clear()
    Agent._on_agent_action_sequence_completed_handlers.clear()
    Agent._on_planning_started_handlers.clear()
    Agent._on_planning_started_for_single_goal_handlers.clear()
    Agent._on_planning_finished_for_single_goal_handlers.clear()
    Agent._on_planning_finished_handlers.clear()
    Agent._on_plan_updated_handlers.clear()
    Agent._on_evaluated_action_node_handlers.clear()
    Action._on_begin_execute_action_handlers.clear()
    Action._on_finish_execute_action_handlers.clear()
    Sensor._on_sensor_run_handlers.clear()

    yield # This runs the test

    # After test: Clear again, just in case (though pytest runs fixtures per test usually)
    Agent._on_agent_step_handlers.clear()
    Agent._on_agent_action_sequence_completed_handlers.clear()
    Agent._on_planning_started_handlers.clear()
    Agent._on_planning_started_for_single_goal_handlers.clear()
    Agent._on_planning_finished_for_single_goal_handlers.clear()
    Agent._on_planning_finished_handlers.clear()
    Agent._on_plan_updated_handlers.clear()
    Agent._on_evaluated_action_node_handlers.clear()
    Action._on_begin_execute_action_handlers.clear()
    Action._on_finish_execute_action_handlers.clear()
    Sensor._on_sensor_run_handlers.clear()

