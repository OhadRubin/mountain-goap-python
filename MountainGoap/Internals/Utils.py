# // <copyright file="Utils.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Any, Optional, TYPE_CHECKING
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from ..BaseGoal import BaseGoal
    from ..Goal import Goal
    from ..ExtremeGoal import ExtremeGoal
    from ..ComparativeGoal import ComparativeGoal
    from ..ComparisonOperator import ComparisonOperator
    from .ActionNode import ActionNode

class Utils:
    """
    Utilities for the MountainGoap library.
    """

    @staticmethod
    def is_lower_than(a: Any, b: Any) -> bool:
        """
        Indicates whether a is lower than b.
        """
        if a is None or b is None:
            return False
        # Python's comparison operators work for various numeric types and datetime objects directly
        # and handle mixed types if they are compatible (e.g., int vs float).
        # For explicit type checking like C#, we can use isinstance.
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a < b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a < b
        # Add other type comparisons if needed, following the C# logic.
        # Python's native comparison is generally more flexible.
        try:
            return a < b
        except TypeError:
            return False


    @staticmethod
    def is_higher_than(a: Any, b: Any) -> bool:
        """
        Indicates whether a is higher than b.
        """
        if a is None or b is None:
            return False
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a > b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a > b
        try:
            return a > b
        except TypeError:
            return False

    @staticmethod
    def is_lower_than_or_equals(a: Any, b: Any) -> bool:
        """
        Indicates whether a is lower than or equal to b.
        """
        if a is None or b is None:
            return False
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a <= b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a <= b
        try:
            return a <= b
        except TypeError:
            return False

    @staticmethod
    def is_higher_than_or_equals(a: Any, b: Any) -> bool:
        """
        Indicates whether a is higher than or equal to b.
        """
        if a is None or b is None:
            return False
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a >= b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a >= b
        try:
            return a >= b
        except TypeError:
            return False

    @staticmethod
    def meets_goal(goal: 'BaseGoal', action_node: 'ActionNode', current: 'ActionNode') -> bool:
        """
        Indicates whether or not a goal is met by an action node.
        """
        from ..Goal import Goal # Import locally to avoid circular dependency issues
        from ..ExtremeGoal import ExtremeGoal
        from ..ComparativeGoal import ComparativeGoal
        from ..ComparisonOperator import ComparisonOperator

        if isinstance(goal, Goal):
            for key, desired_value in goal.DesiredState.items():
                if key not in action_node.State:
                    return False
                current_value = action_node.State[key]
                if current_value is None and desired_value is not None:
                    return False
                elif current_value is not None and current_value != desired_value:
                    return False
            return True
        elif isinstance(goal, ExtremeGoal):
            if action_node.Action is None:
                return False
            for key, maximize in goal.DesiredState.items():
                if key not in action_node.State or key not in current.State:
                    return False

                current_value = action_node.State[key]
                previous_value = current.State[key]

                if maximize:
                    if not Utils.is_higher_than_or_equals(current_value, previous_value):
                        return False
                else: # minimize
                    if not Utils.is_lower_than_or_equals(current_value, previous_value):
                        return False
            return True
        elif isinstance(goal, ComparativeGoal):
            if action_node.Action is None:
                return False
            for key, comparison_value_pair in goal.DesiredState.items():
                if key not in action_node.State or key not in current.State: # C# checks against current.State, not necessarily needed for meeting goal, but for consistency.
                    return False

                current_value = action_node.State[key]
                desired_value = comparison_value_pair.Value
                operator = comparison_value_pair.Operator

                if operator == ComparisonOperator.Undefined:
                    return False
                elif operator == ComparisonOperator.Equals:
                    if current_value != desired_value:
                        return False
                elif operator == ComparisonOperator.LessThan:
                    if not Utils.is_lower_than(current_value, desired_value):
                        return False
                elif operator == ComparisonOperator.GreaterThan:
                    if not Utils.is_higher_than(current_value, desired_value):
                        return False
                elif operator == ComparisonOperator.LessThanOrEquals:
                    if not Utils.is_lower_than_or_equals(current_value, desired_value):
                        return False
                elif operator == ComparisonOperator.GreaterThanOrEquals:
                    if not Utils.is_higher_than_or_equals(current_value, desired_value):
                        return False
            return True
        return False

