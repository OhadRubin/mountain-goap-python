import heapq
import itertools
import decimal
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, TypeVar
from .goals import BaseGoal, Goal, ComparativeGoal, ExtremeGoal, ComparisonOperator

from .types import StateDictionary, PermutationSelectorCallback


class PriorityQueueNode:
    Priority: float
    QueueIndex: int

    def __init__(self):
        self.Priority = 0.0
        self.QueueIndex = 0


T = TypeVar("T", bound=PriorityQueueNode)


class PriorityQueue:
    """A priority queue implementation using Python's `heapq` module."""

    def __init__(self, initial_capacity: int = 0):
        self._heap: list[list] = []
        self._entry_finder: dict[T, list] = {}
        self._counter = itertools.count()
        self._REMOVED = "<removed>"  # sentinel value

    def enqueue(self, item: T, priority: float) -> None:
        if item in self._entry_finder:
            self._entry_finder[item][-1] = self._REMOVED
        entry = [priority, next(self._counter), item]
        self._entry_finder[item] = entry
        heapq.heappush(self._heap, entry)

    def dequeue(self) -> T:
        while self._heap:
            _, _, item = heapq.heappop(self._heap)
            if item is not self._REMOVED:
                del self._entry_finder[item]
                return item
        raise KeyError("Cannot dequeue from an empty priority queue.")

    def update_priority(self, item: T, new_priority: float) -> None:
        self.enqueue(item, new_priority)

    def contains(self, item: T) -> bool:
        return item in self._entry_finder

    @property
    def count(self) -> int:
        return len(self._entry_finder)


class DictionaryExtensionMethods:
    @staticmethod
    def copy_dict(dictionary: StateDictionary) -> StateDictionary:
        return dictionary.copy()

    @staticmethod
    def copy_concurrent_dict(dictionary: StateDictionary) -> StateDictionary:
        return dictionary.copy()

    @staticmethod
    def copy_comparison_value_pair_dict(
        dictionary: Dict[str, "ComparisonValuePair"],
    ) -> Dict[str, "ComparisonValuePair"]:
        return dictionary.copy()

    @staticmethod
    def copy_string_dict(dictionary: Dict[str, str]) -> Dict[str, str]:
        return dictionary.copy()

    @staticmethod
    def copy_non_nullable_dict(dictionary: Dict[str, Any]) -> Dict[str, Any]:
        return dictionary.copy()


class Utils:
    @staticmethod
    def is_lower_than(a: Any, b: Any) -> bool:
        if a is None or b is None:
            return False
        if isinstance(a, (int, float, decimal.Decimal)) and isinstance(
            b, (int, float, decimal.Decimal)
        ):
            return a < b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a < b
        return False

    @staticmethod
    def is_higher_than(a: Any, b: Any) -> bool:
        if a is None or b is None:
            return False
        if isinstance(a, (int, float, decimal.Decimal)) and isinstance(
            b, (int, float, decimal.Decimal)
        ):
            return a > b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a > b
        return False

    @staticmethod
    def is_lower_than_or_equals(a: Any, b: Any) -> bool:
        if a is None or b is None:
            return False
        if isinstance(a, (int, float, decimal.Decimal)) and isinstance(
            b, (int, float, decimal.Decimal)
        ):
            return a <= b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a <= b
        return False

    @staticmethod
    def is_higher_than_or_equals(a: Any, b: Any) -> bool:
        if a is None or b is None:
            return False
        if isinstance(a, (int, float, decimal.Decimal)) and isinstance(
            b, (int, float, decimal.Decimal)
        ):
            return a >= b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a >= b
        return False

    @staticmethod
    def meets_goal(goal: "BaseGoal", action_node: "ActionNode", current: "ActionNode") -> bool:
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
                if current_value is not None and previous_value is not None:
                    if maximize:
                        if not Utils.is_higher_than_or_equals(current_value, previous_value):
                            return False
                    else:
                        if not Utils.is_lower_than_or_equals(current_value, previous_value):
                            return False
            return True
        elif isinstance(goal, ComparativeGoal):
            for key, comparison_value_pair in goal.DesiredState.items():
                if key not in action_node.State:
                    return False
                if key not in current.State:
                    return False
                current_value = action_node.State[key]
                desired_value = comparison_value_pair.Value
                operator = comparison_value_pair.Operator
                if operator == ComparisonOperator.Undefined:
                    return False
                if operator == ComparisonOperator.Equals:
                    if current_value != desired_value:
                        return False
                elif operator == ComparisonOperator.LessThan:
                    if current_value is None or desired_value is None:
                        return False
                    if not Utils.is_lower_than(current_value, desired_value):
                        return False
                elif operator == ComparisonOperator.GreaterThan:
                    if current_value is None or desired_value is None:
                        return False
                    if not Utils.is_higher_than(current_value, desired_value):
                        return False
                elif operator == ComparisonOperator.LessThanOrEquals:
                    if current_value is None or desired_value is None:
                        return False
                    if not Utils.is_lower_than_or_equals(current_value, desired_value):
                        return False
                elif operator == ComparisonOperator.GreaterThanOrEquals:
                    if current_value is None or desired_value is None:
                        return False
                    if not Utils.is_higher_than_or_equals(current_value, desired_value):
                        return False
            return True
        return False


class PermutationSelectorGenerators:
    @staticmethod
    def select_from_collection(values: Iterable[TypeVar("T")]) -> PermutationSelectorCallback:
        def selector(state: StateDictionary) -> List[Any]:
            output: List[Any] = []
            for item in values:
                if item is not None:
                    output.append(item)
            return output

        return selector

    @staticmethod
    def select_from_collection_in_state(key: str) -> PermutationSelectorCallback:
        def selector(state: StateDictionary) -> List[Any]:
            output: List[Any] = []
            if key in state and isinstance(state[key], Iterable):
                values = state[key]
                for item in values:
                    if item is not None:
                        output.append(item)
            return output

        return selector

    @staticmethod
    def select_from_integer_range(lower_bound: int, upper_bound: int) -> PermutationSelectorCallback:
        def selector(state: StateDictionary) -> List[Any]:
            output: List[Any] = []
            for i in range(lower_bound, upper_bound):
                output.append(i)
            return output

        return selector
