I attempted to port this C# code to python. But it's not correct.
Right now this is what is being printed when i run it (you should be seeing prints of player eating the food/ killing monsters):
```
Hello from the pygame community. https://www.pygame.org/contribute.html
--- Turn 1 ---
--- Turn 2 ---
--- Turn 3 ---
--- Turn 4 ---
--- Turn 5 ---
--- Turn 6 ---
--- Turn 7 ---
--- Turn 8 ---
--- Turn 9 ---
--- Turn 10 ---
--- Turn 11 ---
--- Turn 12 ---
--- Turn 13 ---
--- Turn 14 ---
--- Turn 15 ---
--- Turn 16 ---
--- Turn 17 ---
--- Turn 18 ---
--- Turn 19 ---
--- Turn 20 ---
--- Turn 21 ---
--- Turn 22 ---
--- Turn 23 ---
--- Turn 24 ---
--- Turn 25 ---
--- Turn 26 ---
--- Turn 27 ---
--- Turn 28 ---
--- Turn 29 ---
--- Turn 30 ---
--- Turn 31 ---
--- Turn 32 ---
--- Turn 33 ---
--- Turn 34 ---
--- Turn 35 ---
--- Turn 36 ---
--- Turn 37 ---
--- Turn 38 ---
--- Turn 39 ---
--- Turn 40 ---
--- Turn 41 ---
--- Turn 42 ---
--- Turn 43 ---
--- Turn 44 ---
--- Turn 45 ---
--- Turn 46 ---
--- Turn 47 ---
--- Turn 48 ---
--- Turn 49 ---
--- Turn 50 ---
--- Turn 51 ---
--- Turn 52 ---
--- Turn 53 ---
--- Turn 54 ---
Game finished.
```
Do the following:

Part 1: (in your thoughts only, don't output this back to me) Read both code and give me a list of 100 differences between the two?
In your answer, only mention something if it changes the correctness of the port.
The assumption is that if the C# code has it. than it is better.
Formulate your statement as a todo list where one needs to change the python code to be like in C# code.
Go over the code line by line and check for differences.
In your answer here, consider that we do not care about type safety, logging or thread safety at this point, so do not include any fixes related to them right now.

Part 2:
(still in your thought)
Out of the 100 differences you came up with, give me a list of 10 differences that are the most important to fix.
Order them by urgency.
Be highly detailed in your todo here, for each:
1 explain what the C# code is doing
1. what the python code is doing
2. why the python code is wrong.
3. how to convert the python code to be like the C# code.
In your answer here, consider that we do not care about type safety, logging or thread safety at this point, so do not include any fixes related to them right now.

for each in 1-4, include a language explanation AND a code snippet. The language explanation must be very detailed.

Part 3:
(out loud, not only in your thoughts)
Consider Part 2, did you chose any differences that resulted in "No change is needed" since "The python code is more robust"?
If so, then remove that difference from the list and pick a different one. Since the python code is broken you saying "oh but we need to address this change" is wasting my time. So pick a different one, if you can't find one, then go over the entire code again line by line and fine a difference that **does** need to be addressed.
Output the 10 **significant** differences you chose (1-4 for each).
You should focus on differences that would cause the python code to not work the same as the C#.


<python>
import pygame
import random
import math
import uuid
import threading
import os  # For USE_EXTREME_GOAL environment variable
import decimal
from typing import (
    Callable,
    Dict,
    Any,
    List,
    Optional,
    TypeVar,
    Iterable,
    Union,
    Tuple,
    cast,
)
from enum import Enum
from datetime import datetime, timedelta

# A type alias for the state dictionary (defined once globally)
StateDictionary = Dict[str, Optional[Any]]


# --- DefaultLogger Placeholder ---
# This class is a placeholder for the DefaultLogger, which was referenced but not provided.
# It ensures the application can run without a missing dependency.
class DefaultLogger:
    def __init__(
        self,
        log_to_console: bool = True,
        logging_file: str = "default.log",
        filter_string: str = "",
    ):
        self.log_to_console = log_to_console
        self.logging_file = logging_file
        self.filter_string = filter_string

    def log_info(self, message: str):
        if self.filter_string and self.filter_string not in message:
            return
        if self.log_to_console:
            print(f"[INFO] {message}")

    def log_debug(self, message: str):
        if self.filter_string and self.filter_string not in message:
            return
        if self.log_to_console:
            print(f"[DEBUG] {message}")

    def log_error(self, message: str, exception: Exception = None):
        if self.filter_string and self.filter_string not in message:
            return
        if self.log_to_console:
            print(f"[ERROR] {message}")
            if exception:
                import traceback

                traceback.print_exc()


# --- Callback Delegates (Consolidated) ---
# Original content from various CallbackDelegate files
CostCallback = Callable[["Action", StateDictionary], float]
ExecutorCallback = Callable[["Agent", "Action"], "ExecutionStatus"]
PermutationSelectorCallback = Callable[[StateDictionary], List[Any]]
SensorRunCallback = Callable[["Agent"], None]
StateCheckerCallback = Callable[["Action", StateDictionary], bool]
StateCostDeltaMultiplierCallback = Callable[[Optional["Action"], str], float]
StateMutatorCallback = Callable[["Action", StateDictionary], None]

# --- Event Delegates (Consolidated) ---
# Original content from various Event files
AgentActionSequenceCompletedEvent = Callable[["Agent"], None]
AgentStepEvent = Callable[["Agent"], None]
BeginExecuteActionEvent = Callable[["Agent", "Action", Dict[str, Any]], None]
EvaluatedActionNodeEvent = Callable[
    ["ActionNode", Dict["ActionNode", "ActionNode"]], None
]
FinishExecuteActionEvent = Callable[
    ["Agent", "Action", "ExecutionStatus", Dict[str, Any]], None
]
PlanUpdatedEvent = Callable[["Agent", List["Action"]], None]
PlanningFinishedEvent = Callable[["Agent", Optional["BaseGoal"], float], None]
PlanningFinishedForSingleGoalEvent = Callable[["Agent", "BaseGoal", float], None]
PlanningStartedEvent = Callable[["Agent"], None]
PlanningStartedForSingleGoalEvent = Callable[["Agent", "BaseGoal"], None]
SensorRunEvent = Callable[["Agent", "Sensor"], None]


# --- Priority Queue Implementation (Only FastPriorityQueue and its Node are kept) ---
# Original content from FastPriorityQueueNode.py
class FastPriorityQueueNode:
    Priority: float
    QueueIndex: int

    def __init__(self):
        self.Priority = 0.0
        self.QueueIndex = 0


# Original content from FastPriorityQueue.py
T = TypeVar("T", bound=FastPriorityQueueNode)


class FastPriorityQueue:
    _num_nodes: int
    _nodes: List[T]

    def __init__(self, max_nodes: int):
        if max_nodes <= 0:
            raise ValueError("New queue size cannot be smaller than 1")
        self._num_nodes = 0
        self._nodes = [cast(T, None)] * (max_nodes + 1)

    @property
    def count(self) -> int:
        return self._num_nodes

    @property
    def max_size(self) -> int:
        return len(self._nodes) - 1

    def clear(self) -> None:
        # Mimic C#'s Array.Clear by setting elements to None in place.
        # Also, reset node's internal state to indicate it's no longer in a queue.
        # Starting from index 1 as the 0th element is unused in this heap implementation.
        for i in range(1, self._num_nodes + 1):
            node_to_clear = self._nodes[i]
            if node_to_clear is not None:
                # Reset the node's internal queue state, as if it was removed/reset
                node_to_clear.QueueIndex = 0
            self._nodes[i] = cast(T, None)  # Set the array slot to None
        self._num_nodes = 0

    def contains(self, node: T) -> bool:
        if node is None:
            raise ValueError("node cannot be None")
        # C# only checks: return (_nodes[node.QueueIndex] == node);
        # Python should rely only on node.QueueIndex being valid and pointing to itself in _nodes
        is_at_correct_index = (
            0 < node.QueueIndex <= self._num_nodes  # Ensure index is within bounds of active nodes
            and self._nodes[node.QueueIndex] == node
        )
        return is_at_correct_index  # Direct check, no dict lookup

    def enqueue(self, node: T, priority: float) -> None:
        if node is None:
            raise ValueError("node cannot be None")
        if self._num_nodes >= self.max_size:
            raise RuntimeError("Queue is full - node cannot be added")
        node.Priority = priority
        self._num_nodes += 1
        node.QueueIndex = self._num_nodes
        self._nodes[self._num_nodes] = node
        self._cascade_up(node)

    def _cascade_up(self, node: T) -> None:
        current_index = node.QueueIndex
        while current_index > 1:
            parent_index = current_index // 2
            parent_node = self._nodes[parent_index]
            if self._has_higher_or_equal_priority(parent_node, node):
                break
            self._nodes[current_index] = parent_node
            if parent_node is not None:
                parent_node.QueueIndex = current_index
            self._nodes[parent_index] = node
            node.QueueIndex = parent_index
            current_index = parent_index

    def _cascade_down(self, node: T) -> None:
        current_index = node.QueueIndex
        while True:
            child_left_index = 2 * current_index
            child_right_index = 2 * current_index + 1
            swap_index = 0
            if child_left_index <= self._num_nodes:
                child_left = self._nodes[child_left_index]
                if self._has_higher_priority(child_left, node):
                    swap_index = child_left_index
            if child_right_index <= self._num_nodes:
                child_right = self._nodes[child_right_index]
                if swap_index == 0:
                    if self._has_higher_priority(child_right, node):
                        swap_index = child_right_index
                else:
                    child_to_compare = self._nodes[swap_index]
                    if self._has_higher_priority(child_right, child_to_compare):
                        swap_index = child_right_index
            if swap_index == 0:
                break
            swap_node = self._nodes[swap_index]
            self._nodes[current_index] = swap_node
            if swap_node is not None:
                swap_node.QueueIndex = current_index
            self._nodes[swap_index] = node
            node.QueueIndex = swap_index
            current_index = swap_index

    def _has_higher_priority(self, higher: T, lower: T) -> bool:
        return higher.Priority < lower.Priority

    def _has_higher_or_equal_priority(self, higher: T, lower: T) -> bool:
        return higher.Priority <= lower.Priority

    def dequeue(self) -> T:
        if self._num_nodes <= 0:
            raise RuntimeError("Cannot call dequeue() on an empty queue")
        return_me = self._nodes[1]
        if return_me is None:
            raise RuntimeError("Heap root is unexpectedly None")
        if self._num_nodes == 1:
            self._nodes[1] = None
            self._num_nodes = 0
            return_me.QueueIndex = 0
            return return_me
        former_last_node = self._nodes[self._num_nodes]
        if former_last_node is None:
            raise RuntimeError("Last node is unexpectedly None")
        self._nodes[1] = former_last_node
        former_last_node.QueueIndex = 1
        self._nodes[self._num_nodes] = None
        self._num_nodes -= 1
        return_me.QueueIndex = 0
        self._cascade_down(former_last_node)
        return return_me

    def resize(self, max_nodes: int) -> None:
        if max_nodes <= 0:
            raise ValueError("Queue size cannot be smaller than 1")
        if max_nodes < self._num_nodes:
            raise ValueError(
                f"Called Resize({max_nodes}), but current queue contains {self._num_nodes} nodes"
            )
        new_nodes = [None] * (max_nodes + 1)
        for i in range(1, self._num_nodes + 1):
            new_nodes[i] = self._nodes[i]
        self._nodes = new_nodes

    @property
    def first(self) -> T:
        if self._num_nodes <= 0:
            raise RuntimeError("Cannot call .first on an empty queue")
        if self._nodes[1] is None:
            raise RuntimeError("First element in heap is unexpectedly None")
        return self._nodes[1]

    def update_priority(self, node: T, priority: float) -> None:
        if node is None:
            raise ValueError("node cannot be None")
        old_priority = node.Priority
        node.Priority = priority
        self._on_node_updated(node)

    def _on_node_updated(self, node: T) -> None:
        parent_index = node.QueueIndex // 2
        if parent_index > 0 and self._has_higher_priority(node, self._nodes[parent_index]):
            self._cascade_up(node)
        else:
            self._cascade_down(node)

    def remove(self, node: T) -> None:
        if node is None:
            raise ValueError("node cannot be None")
        if node.QueueIndex == self._num_nodes:
            self._nodes[self._num_nodes] = None
            self._num_nodes -= 1
            node.QueueIndex = 0
            return
        former_last_node = self._nodes[self._num_nodes]
        if former_last_node is None:
            raise RuntimeError(
                "Last node in heap is unexpectedly None during remove operation"
            )
        old_priority_of_former_last_node = former_last_node.Priority
        self._nodes[node.QueueIndex] = former_last_node
        former_last_node.QueueIndex = node.QueueIndex
        self._nodes[self._num_nodes] = None
        self._num_nodes -= 1
        node.QueueIndex = 0
        self._on_node_updated(former_last_node)

    def reset_node(self, node: T) -> None:
        if node is None:
            raise ValueError("node cannot be None")
        node.QueueIndex = 0

    def __iter__(self) -> Iterable[T]:
        active_nodes = []
        for i in range(1, self._num_nodes + 1):
            node = self._nodes[i]
            if node is not None:
                active_nodes.append(node)
        return iter(active_nodes)

    def is_valid_queue(self) -> bool:
        for i in range(1, self._num_nodes + 1):
            current_node = self._nodes[i]
            if current_node is None:
                return False
            if current_node.QueueIndex != i:
                return False
            child_left_index = 2 * i
            if child_left_index <= self._num_nodes:
                child_left = self._nodes[child_left_index]
                if child_left is None or self._has_higher_priority(
                    child_left, current_node
                ):
                    return False
            child_right_index = 2 * i + 1
            if child_right_index <= self._num_nodes:
                child_right = self._nodes[child_right_index]
                if child_right is None or self._has_higher_priority(
                    child_right, current_node
                ):
                    return False
        return True


# --- Internal GOAP Components ---
# Original content from DictionaryExtensionMethods.py
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


# Original content from ActionNode.py
class ActionNode(FastPriorityQueueNode):
    State: StateDictionary
    Parameters: Dict[str, Optional[Any]]
    Action: Optional["Action"]

    def __init__(
        self,
        action: Optional["Action"],
        state: StateDictionary,
        parameters: Dict[str, Optional[Any]],
    ):
        super().__init__()
        self.Action = action.copy() if action is not None else None
        self.State = DictionaryExtensionMethods.copy_concurrent_dict(state)
        self.Parameters = DictionaryExtensionMethods.copy_dict(parameters)
        if self.Action is not None:
            self.Action.set_parameters(self.Parameters)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ActionNode):
            return NotImplemented
        if self is other:
            return True
        if self.Action is None:
            if other.Action is not None:
                return False
        elif other.Action is None:
            return False
        elif not self.Action.__eq__(other.Action):
            return False
        return self._state_matches(other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    def __hash__(self) -> int:
        action_hash = hash(self.Action) if self.Action is not None else hash(None)
        
        def make_hashable(obj):
            """Recursively convert objects to hashable form, or return None if not possible."""
            if obj is None:
                return None
            
            # Try basic types first
            try:
                hash(obj)
                return obj
            except TypeError:
                pass
            
            # Handle lists/tuples recursively
            if isinstance(obj, (list, tuple)):
                try:
                    hashable_items = []
                    for item in obj:
                        hashable_item = make_hashable(item)
                        if hashable_item is None:
                            return None  # Skip entire list if any item is unhashable
                        hashable_items.append(hashable_item)
                    return tuple(hashable_items)
                except:
                    return None
            
            # Handle dicts recursively
            if isinstance(obj, dict):
                try:
                    hashable_items = []
                    for k, v in obj.items():
                        hashable_k = make_hashable(k)
                        hashable_v = make_hashable(v)
                        if hashable_k is None or hashable_v is None:
                            return None  # Skip entire dict if any item is unhashable
                        hashable_items.append((hashable_k, hashable_v))
                    return tuple(sorted(hashable_items))
                except:
                    return None
            
            # For other objects, return None (skip from hash)
            return None
        
        hashable_items = []
        for key, value in self.State.items():
            hashable_value = make_hashable(value)
            if hashable_value is not None:
                hashable_items.append((key, hashable_value))
        
        state_hash = hash(frozenset(hashable_items))
        return hash((action_hash, state_hash))

    def cost(self, current_state: StateDictionary) -> float:
        if self.Action is None:
            return float("inf")
        return self.Action.get_cost(current_state)

    def _state_matches(self, other_node: "ActionNode") -> bool:
        # Replicate C#'s flawed two-way dictionary comparison
        for key, value in self.State.items():
            if key not in other_node.State:
                return False
            if other_node.State[key] != value:
                return False
        for key, value in other_node.State.items():
            if key not in self.State:
                return False
            # Fixed: Compare other_node's value against self's value for the same key
            if self.State.get(key) != value:
                return False
        return True


# Original content from ActionGraph.py
class ActionGraph:
    ActionNodes: List[ActionNode]

    def __init__(self, actions: List["Action"], state: StateDictionary):
        self.ActionNodes = []
        for action in actions:
            permutations = action.get_permutations(state)
            for permutation in permutations:
                self.ActionNodes.append(ActionNode(action, state, permutation))

    def neighbors(self, node: ActionNode) -> Iterable[ActionNode]:
        for other_node_template in self.ActionNodes:
            if (
                other_node_template.Action is not None
                and other_node_template.Action.is_possible(node.State)
            ):
                new_action = other_node_template.Action.copy()
                new_state = DictionaryExtensionMethods.copy_concurrent_dict(node.State)
                new_parameters = DictionaryExtensionMethods.copy_dict(
                    other_node_template.Parameters
                )
                new_node = ActionNode(new_action, new_state, new_parameters)
                if new_node.Action is not None:
                    new_node.Action.apply_effects(new_node.State)
                yield new_node


# Original content from Utils.py
class Utils:
    @staticmethod
    def is_lower_than(a: Any, b: Any) -> bool:
        if a is None or b is None:
            return False
        # Add decimal.Decimal to the numeric type check
        if isinstance(a, (int, float, decimal.Decimal)) and isinstance(b, (int, float, decimal.Decimal)):
            return a < b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a < b
        return False

    @staticmethod
    def is_higher_than(a: Any, b: Any) -> bool:
        if a is None or b is None:
            return False
        # Add decimal.Decimal to the numeric type check
        if isinstance(a, (int, float, decimal.Decimal)) and isinstance(b, (int, float, decimal.Decimal)):
            return a > b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a > b
        return False

    @staticmethod
    def is_lower_than_or_equals(a: Any, b: Any) -> bool:
        if a is None or b is None:
            return False
        # Add decimal.Decimal to the numeric type check
        if isinstance(a, (int, float, decimal.Decimal)) and isinstance(b, (int, float, decimal.Decimal)):
            return a <= b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a <= b
        return False

    @staticmethod
    def is_higher_than_or_equals(a: Any, b: Any) -> bool:
        if a is None or b is None:
            return False
        # Add decimal.Decimal to the numeric type check
        if isinstance(a, (int, float, decimal.Decimal)) and isinstance(b, (int, float, decimal.Decimal)):
            return a >= b
        if isinstance(a, datetime) and isinstance(b, datetime):
            return a >= b
        return False

    @staticmethod
    def meets_goal(
        goal: "BaseGoal", action_node: "ActionNode", current: "ActionNode"
    ) -> bool:
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
                    return False  # Key must exist in both nodes for ExtremeGoal
                
                current_value = action_node.State[key]
                previous_value = current.State[key]

                # C# only performs comparison if both values are not null.
                # If either is None, C# effectively skips this KVP, so Python should too.
                if current_value is not None and previous_value is not None:
                    if maximize:
                        # Also incorporates fix from Todo 3 for comparison operator
                        if not Utils.is_higher_than_or_equals(current_value, previous_value): 
                            return False
                    else:  # minimize
                        # Also incorporates fix from Todo 3 for comparison operator
                        if not Utils.is_lower_than_or_equals(current_value, previous_value):
                            return False
                # If current_value or previous_value is None, and we reach here, C# would continue.
                # So Python should too. No explicit `return False` for the `None` case.
            return True
        elif isinstance(goal, ComparativeGoal):
            if action_node.Action is None:
                return False
            for key, comparison_value_pair in goal.DesiredState.items():
                # C# doesn't check current.State.ContainsKey(key) for ComparativeGoal here explicitly
                # It does actionNode.State.ContainsKey(kvp.Key) then relies on 'is object' checks.
                if key not in action_node.State:
                    return False  # Key must exist in action_node's state
                
                current_value = action_node.State[key]
                desired_value = comparison_value_pair.Value
                operator = comparison_value_pair.Operator

                if operator == ComparisonOperator.Undefined:
                    return False

                if operator == ComparisonOperator.Equals:
                    if current_value != desired_value:  # Handles None vs None (True) and None vs Value (False) correctly
                        return False
                elif operator == ComparisonOperator.LessThan:
                    if current_value is None or desired_value is None:  # If either is None, C# fails the goal
                        return False
                    if not Utils.is_lower_than(current_value, desired_value):
                        return False
                elif operator == ComparisonOperator.GreaterThan:
                    if current_value is None or desired_value is None:  # If either is None, C# fails the goal
                        return False
                    if not Utils.is_higher_than(current_value, desired_value):
                        return False
                elif operator == ComparisonOperator.LessThanOrEquals:
                    if current_value is None or desired_value is None:  # If either is None, C# fails the goal
                        return False
                    if not Utils.is_lower_than_or_equals(current_value, desired_value):
                        return False
                elif operator == ComparisonOperator.GreaterThanOrEquals:
                    if current_value is None or desired_value is None:  # If either is None, C# fails the goal
                        return False
                    if not Utils.is_higher_than_or_equals(current_value, desired_value):
                        return False
            return True
        return False


# Original content from ActionAStar.py
class ActionAStar:
    _goal: "BaseGoal"

    def __init__(
        self,
        graph: ActionGraph,
        start: ActionNode,
        goal: "BaseGoal",
        cost_maximum: float,
        step_maximum: int,
    ):
        self._goal = goal
        self.FinalPoint: Optional[ActionNode] = None
        self.CostSoFar: Dict[ActionNode, float] = {}
        self.StepsSoFar: Dict[ActionNode, int] = {}
        self.CameFrom: Dict[ActionNode, ActionNode] = {}
        
        frontier = FastPriorityQueue(100000)
        frontier.enqueue(start, 0.0)
        self.CameFrom[start] = start
        self.CostSoFar[start] = 0.0
        self.StepsSoFar[start] = 0
        while frontier.count > 0:
            current = frontier.dequeue()
            if self._meets_goal(current, start):
                self.FinalPoint = current
                break
            for next_node in graph.neighbors(current):
                action_cost = next_node.cost(current.State)
                new_cost = self.CostSoFar[current] + action_cost
                new_step_count = self.StepsSoFar[current] + 1
                if new_cost > cost_maximum or new_step_count > step_maximum:
                    continue
                if (
                    next_node not in self.CostSoFar
                    or new_cost < self.CostSoFar[next_node]
                ):
                    self.CostSoFar[next_node] = new_cost
                    self.StepsSoFar[next_node] = new_step_count
                    priority = new_cost + self._heuristic(next_node, goal, current)
                    if frontier.contains(next_node):
                        frontier.update_priority(next_node, priority)
                    else:
                        frontier.enqueue(next_node, priority)
                    self.CameFrom[next_node] = current
                    Agent.OnEvaluatedActionNode(next_node, self.CameFrom)

    def _heuristic(
        self,
        action_node: ActionNode,
        goal: "BaseGoal",
        previous_node_in_path: ActionNode,
    ) -> float:
        cost = 0.0
        if isinstance(goal, Goal):
            for key, desired_value in goal.DesiredState.items():
                if (
                    key not in action_node.State
                    or action_node.State[key] != desired_value
                ):
                    cost += 1.0
        elif isinstance(goal, ExtremeGoal):
            for key, maximize in goal.DesiredState.items():
                value_diff_multiplier = (
                    action_node.Action.StateCostDeltaMultiplier
                    if action_node.Action
                    else Action.default_state_cost_delta_multiplier
                )(action_node.Action, key)
                if (
                    key not in action_node.State
                    or key not in previous_node_in_path.State
                ):
                    cost += float("inf")
                    continue
                current_val = action_node.State[key]
                prev_val = previous_node_in_path.State[key]
                if current_val is None or prev_val is None:
                    cost += float("inf")
                    continue
                try:
                    current_val_f = float(current_val)
                    prev_val_f = float(prev_val)
                except (ValueError, TypeError):
                    cost += float("inf")
                    continue
                value_diff = current_val_f - prev_val_f
                if maximize:
                    # C# penalizes if current_val_f <= prev_val_f (no progress or regression)
                    # value_diff = current_val_f - prev_val_f will be negative or zero.
                    # C#: cost -= valueDiff * valueDiffMultiplier => cost + (-(current-prev)) * multiplier => cost + |current-prev| * multiplier
                    if Utils.is_lower_than_or_equals(current_val_f, prev_val_f):
                        cost += abs(value_diff) * value_diff_multiplier
                else: # minimize
                    # C# penalizes if current_val_f >= prev_val_f (no progress or regression)
                    # value_diff = current_val_f - prev_val_f will be positive or zero.
                    # C#: cost += valueDiff * valueDiffMultiplier => cost + (current-prev) * multiplier => cost + |current-prev| * multiplier
                    if Utils.is_higher_than_or_equals(current_val_f, prev_val_f):
                        cost += abs(value_diff) * value_diff_multiplier
        elif isinstance(goal, ComparativeGoal):
            for key, comp_value_pair in goal.DesiredState.items():
                value_diff_multiplier = (
                    action_node.Action.StateCostDeltaMultiplier
                    if action_node.Action
                    else Action.default_state_cost_delta_multiplier
                )(action_node.Action, key)
                if (
                    key not in action_node.State
                    or key not in previous_node_in_path.State
                ):
                    cost += float("inf")
                    continue
                current_val = action_node.State[key]
                desired_val = comp_value_pair.Value
                operator = comp_value_pair.Operator
                if current_val is None or desired_val is None:
                    if operator != ComparisonOperator.Undefined:
                        cost += float("inf")
                        continue
                try:
                    current_val_f = float(current_val)
                    desired_val_f = (
                        float(desired_val) if desired_val is not None else float("nan")
                    )
                    prev_val_f = float(previous_node_in_path.State[key])
                except (ValueError, TypeError):
                    current_val_f = float("nan")
                    prev_val_f = float("nan")
                value_diff_from_previous_step = abs(current_val_f - prev_val_f)
                if operator == ComparisonOperator.Undefined:
                    cost += float("inf")
                elif operator == ComparisonOperator.Equals:
                    if current_val != desired_val:
                        cost += value_diff_from_previous_step * value_diff_multiplier
                elif operator == ComparisonOperator.LessThan:
                    if not Utils.is_lower_than(current_val, desired_val):
                        cost += value_diff_from_previous_step * value_diff_multiplier
                elif operator == ComparisonOperator.GreaterThan:
                    if not Utils.is_higher_than(current_val, desired_val):
                        cost += value_diff_from_previous_step * value_diff_multiplier
                elif operator == ComparisonOperator.LessThanOrEquals:
                    if not Utils.is_lower_than_or_equals(current_val, desired_val):
                        cost += value_diff_from_previous_step * value_diff_multiplier
                elif operator == ComparisonOperator.GreaterThanOrEquals:
                    if not Utils.is_higher_than_or_equals(current_val, desired_val):
                        cost += value_diff_from_previous_step * value_diff_multiplier
        return cost

    def _meets_goal(
        self, action_node: ActionNode, previous_node_in_path: ActionNode
    ) -> bool:
        return Utils.meets_goal(self._goal, action_node, previous_node_in_path)


# Original content from Planner.py
class Planner:
    """
    Planner for an agent.
    """

    @staticmethod
    def plan(agent: "Agent", cost_maximum: float, step_maximum: int) -> None:
        Agent.OnPlanningStarted(agent)
        best_plan_utility = 0.0
        best_astar: Optional[ActionAStar] = None
        best_goal: Optional["BaseGoal"] = None
        for goal in agent.Goals:
            Agent.OnPlanningStartedForSingleGoal(agent, goal)
            graph = ActionGraph(agent.Actions, agent.State)
            start_node = ActionNode(None, agent.State, {})
            astar_result = ActionAStar(
                graph, start_node, goal, cost_maximum, step_maximum
            )
            cursor = astar_result.FinalPoint
            current_goal_utility = 0.0
            if cursor is not None:
                plan_cost = astar_result.CostSoFar.get(cursor, 0.0)

                # C# logs 0 utility for 0 cost, but for actual comparison, it uses Weight / Cost (Infinity).
                # Mimic C#'s behavior for the logging event:
                reported_utility = 0.0
                if plan_cost == 0:
                    reported_utility = 0.0  # C# logs 0.0 if cost is 0
                else:
                    reported_utility = goal.Weight / plan_cost
                Agent.OnPlanningFinishedForSingleGoal(agent, goal, reported_utility)

                # For the actual best_plan_utility comparison, C# uses the result of the division,
                # which can be float.PositiveInfinity if plan_cost is 0 and goal.Weight > 0.
                comparison_utility = reported_utility  # Start with reported_utility
                if plan_cost == 0 and goal.Weight > 0:
                    comparison_utility = float('inf')
                elif plan_cost == 0 and goal.Weight <= 0:  # Handle Weight 0 or negative with 0 cost, resulting in NaN or -inf in C#
                    comparison_utility = float('nan') if goal.Weight == 0 else float('-inf')

                if cursor.Action is not None and comparison_utility > best_plan_utility:
                    best_plan_utility = comparison_utility
                    best_astar = astar_result
                    best_goal = goal
            else:
                Agent.OnPlanningFinishedForSingleGoal(agent, goal, 0.0)
        if (
            best_plan_utility > 0
            and best_astar is not None
            and best_goal is not None
            and best_astar.FinalPoint is not None
        ):
            Planner._update_agent_action_list(best_astar.FinalPoint, best_astar, agent)
            agent.IsBusy = True
            Agent.OnPlanningFinished(agent, best_goal, best_plan_utility)
        else:
            Agent.OnPlanningFinished(agent, None, 0.0)
        agent.IsPlanning = False

    @staticmethod
    def _update_agent_action_list(
        start_node: ActionNode, astar: ActionAStar, agent: "Agent"
    ) -> None:
        cursor: Optional[ActionNode] = start_node
        action_list: List["Action"] = []
        while cursor is not None and cursor.Action is not None and cursor in astar.CameFrom:
            action_list.append(cursor.Action)
            prev_cursor = astar.CameFrom.get(cursor)
            # C# relies on `cursor.Action != null` (where start node has null action) to terminate.
            # Remove the extra check for `cursor == prev_cursor` to match C#'s more implicit termination.
            cursor = prev_cursor
        action_list.reverse()
        agent.CurrentActionSequences.append(action_list)
        Agent.OnPlanUpdated(agent, action_list)


# --- GOAP Core Components ---
# Original content from BaseGoal.py
class BaseGoal:
    Name: str
    Weight: float

    def __init__(self, name: str = None, weight: float = 1.0):
        self.Name = name if name is not None else f"Goal {uuid.uuid4()}"
        self.Weight = weight


# Original content from ComparisonOperator.py
class ComparisonOperator(Enum):
    Undefined = 0
    Equals = 1
    LessThan = 2
    LessThanOrEquals = 3
    GreaterThan = 4
    GreaterThanOrEquals = 5


# Original content from ComparisonValuePair.py
class ComparisonValuePair:
    Value: Optional[Any] = None
    Operator: ComparisonOperator = ComparisonOperator.Undefined

    def __init__(
        self,
        value: Optional[Any] = None,
        operator: ComparisonOperator = ComparisonOperator.Undefined,
    ):
        self.Value = value
        self.Operator = operator


# Original content from ComparativeGoal.py
class ComparativeGoal(BaseGoal):
    DesiredState: Dict[str, ComparisonValuePair]

    def __init__(
        self,
        name: Optional[str] = None,
        weight: float = 1.0,
        desired_state: Optional[Dict[str, ComparisonValuePair]] = None,
    ):
        super().__init__(name, weight)
        self.DesiredState = desired_state if desired_state is not None else {}


# Original content from ExecutionStatus.py
class ExecutionStatus(Enum):
    NotYetExecuted = 1
    Executing = 2
    Succeeded = 3
    Failed = 4
    NotPossible = 5


# Original content from ExtremeGoal.py
class ExtremeGoal(BaseGoal):
    DesiredState: Dict[str, bool]

    def __init__(
        self,
        name: Optional[str] = None,
        weight: float = 1.0,
        desired_state: Optional[Dict[str, bool]] = None,
    ):
        super().__init__(name, weight)
        self.DesiredState = desired_state if desired_state is not None else {}


# Original content from Goal.py
class Goal(BaseGoal):
    DesiredState: StateDictionary

    def __init__(
        self,
        name: Optional[str] = None,
        weight: float = 1.0,
        desired_state: Optional[StateDictionary] = None,
    ):
        super().__init__(name, weight)
        self.DesiredState = desired_state if desired_state is not None else {}


# Original content from PermutationSelectorGenerators.py
class PermutationSelectorGenerators:
    @staticmethod
    def select_from_collection(values: Iterable[T]) -> PermutationSelectorCallback:
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
    def select_from_integer_range(
        lower_bound: int, upper_bound: int
    ) -> PermutationSelectorCallback:
        def selector(state: StateDictionary) -> List[Any]:
            output: List[Any] = []
            for i in range(lower_bound, upper_bound):
                output.append(i)
            return output

        return selector


# Original content from Sensor.py
class Sensor:
    Name: str
    _run_callback: SensorRunCallback
    _on_sensor_run_handlers: List[SensorRunEvent] = []

    @classmethod
    def OnSensorRun(cls, agent: "Agent", sensor: "Sensor"):
        for handler in cls._on_sensor_run_handlers:
            handler(agent, sensor)

    @classmethod
    def register_on_sensor_run(cls, handler: SensorRunEvent):
        cls._on_sensor_run_handlers.append(handler)

    def __init__(self, run_callback: SensorRunCallback, name: Optional[str] = None):
        callback_name = (
            run_callback.__name__
            if hasattr(run_callback, "__name__")
            else str(run_callback)
        )
        self.Name = (
            name if name is not None else f"Sensor {uuid.uuid4()} ({callback_name})"
        )
        self._run_callback = run_callback

    def run(self, agent: "Agent") -> None:
        Sensor.OnSensorRun(agent, self)
        self._run_callback(agent)


# Original content from StepMode.py
class StepMode(Enum):
    Default = 1
    OneAction = 2
    AllActions = 3


# Original content from Action.py
class Action:
    Name: str
    _cost_base: float
    _permutation_selectors: Dict[str, PermutationSelectorCallback]
    _executor: ExecutorCallback
    _cost_callback: CostCallback
    _preconditions: Dict[str, Optional[Any]]
    _comparative_preconditions: Dict[str, ComparisonValuePair]
    _postconditions: Dict[str, Optional[Any]]
    _arithmetic_postconditions: Dict[str, Any]
    _parameter_postconditions: Dict[str, str]
    _state_mutator: Optional[StateMutatorCallback]
    _state_checker: Optional[StateCheckerCallback]
    _parameters: Dict[str, Optional[Any]]
    StateCostDeltaMultiplier: Optional[StateCostDeltaMultiplierCallback]
    ExecutionStatus: ExecutionStatus = ExecutionStatus.NotYetExecuted

    def __init__(
        self,
        name: Optional[str] = None,
        permutation_selectors: Optional[Dict[str, PermutationSelectorCallback]] = None,
        executor: Optional[ExecutorCallback] = None,
        cost: float = 1.0,
        cost_callback: Optional[CostCallback] = None,
        preconditions: Optional[Dict[str, Optional[Any]]] = None,
        comparative_preconditions: Optional[Dict[str, ComparisonValuePair]] = None,
        postconditions: Optional[Dict[str, Optional[Any]]] = None,
        arithmetic_postconditions: Optional[Dict[str, Any]] = None,
        parameter_postconditions: Optional[Dict[str, str]] = None,
        state_mutator: Optional[StateMutatorCallback] = None,
        state_checker: Optional[StateCheckerCallback] = None,
        state_cost_delta_multiplier: Optional[StateCostDeltaMultiplierCallback] = None,
    ):
        self._permutation_selectors = (
            permutation_selectors if permutation_selectors is not None else {}
        )
        self._executor = (
            executor if executor is not None else Action._default_executor_callback
        )
        executor_name = (
            self._executor.__name__
            if hasattr(self._executor, "__name__")
            else str(self._executor)
        )
        self.Name = (
            name if name is not None else f"Action {uuid.uuid4()} ({executor_name})"
        )
        self._cost_base = cost
        self._cost_callback = (
            cost_callback
            if cost_callback is not None
            else Action._default_cost_callback
        )
        self._preconditions = preconditions if preconditions is not None else {}
        self._comparative_preconditions = (
            comparative_preconditions if comparative_preconditions is not None else {}
        )
        self._postconditions = postconditions if postconditions is not None else {}
        self._arithmetic_postconditions = (
            arithmetic_postconditions if arithmetic_postconditions is not None else {}
        )
        self._parameter_postconditions = (
            parameter_postconditions if parameter_postconditions is not None else {}
        )
        self._state_mutator = state_mutator
        self._state_checker = state_checker
        self.StateCostDeltaMultiplier = (
            state_cost_delta_multiplier
            if state_cost_delta_multiplier is not None
            else Action.default_state_cost_delta_multiplier
        )
        self._parameters = {}

    _on_begin_execute_action_handlers: List[BeginExecuteActionEvent] = []
    _on_finish_execute_action_handlers: List[FinishExecuteActionEvent] = []

    @classmethod
    def OnBeginExecuteAction(
        cls, agent: "Agent", action: "Action", parameters: Dict[str, Optional[Any]]
    ) -> None:
        for handler in cls._on_begin_execute_action_handlers:
            handler(agent, action, parameters)

    @classmethod
    def OnFinishExecuteAction(
        cls,
        agent: "Agent",
        action: "Action",
        status: ExecutionStatus,
        parameters: Dict[str, Optional[Any]],
    ) -> None:
        for handler in cls._on_finish_execute_action_handlers:
            handler(agent, action, status, parameters)

    @classmethod
    def register_on_begin_execute_action(cls, handler: BeginExecuteActionEvent):
        cls._on_begin_execute_action_handlers.append(handler)

    @classmethod
    def register_on_finish_execute_action(cls, handler: FinishExecuteActionEvent):
        cls._on_finish_execute_action_handlers.append(handler)

    @staticmethod
    def default_state_cost_delta_multiplier(
        action: Optional["Action"], state_key: str
    ) -> float:
        return 1.0

    @staticmethod
    def _default_executor_callback(agent: "Agent", action: "Action") -> ExecutionStatus:
        return ExecutionStatus.Failed

    @staticmethod
    def _default_cost_callback(
        action: "Action", current_state: StateDictionary
    ) -> float:
        return action._cost_base

    def copy(self) -> "Action":
        new_action = Action(
            name=self.Name,
            permutation_selectors=self._permutation_selectors,
            executor=self._executor,
            cost=self._cost_base,
            cost_callback=self._cost_callback,
            preconditions=DictionaryExtensionMethods.copy_dict(self._preconditions),
            comparative_preconditions=DictionaryExtensionMethods.copy_comparison_value_pair_dict(
                self._comparative_preconditions
            ),
            postconditions=DictionaryExtensionMethods.copy_dict(self._postconditions),
            arithmetic_postconditions=DictionaryExtensionMethods.copy_non_nullable_dict(
                self._arithmetic_postconditions
            ),
            parameter_postconditions=DictionaryExtensionMethods.copy_string_dict(
                self._parameter_postconditions
            ),
            state_mutator=self._state_mutator,
            state_checker=self._state_checker,
            state_cost_delta_multiplier=self.StateCostDeltaMultiplier,
        )
        new_action._parameters = DictionaryExtensionMethods.copy_dict(self._parameters)
        return new_action

    def set_parameter(self, key: str, value: Any) -> None:
        self._parameters[key] = value

    def get_parameter(self, key: str) -> Optional[Any]:
        return self._parameters.get(key)

    def get_cost(self, current_state: StateDictionary) -> float:
        try:
            return self._cost_callback(self, current_state)
        except Exception:
            return float("inf")

    def execute(self, agent: "Agent") -> ExecutionStatus:
        Action.OnBeginExecuteAction(agent, self, self._parameters)
        if self.is_possible(agent.State):
            new_status = self._executor(agent, self)
            if new_status == ExecutionStatus.Succeeded:
                self.apply_effects(agent.State)
            self.ExecutionStatus = new_status
            Action.OnFinishExecuteAction(
                agent, self, self.ExecutionStatus, self._parameters
            )
            return new_status
        else:
            self.ExecutionStatus = ExecutionStatus.NotPossible
            Action.OnFinishExecuteAction(
                agent, self, self.ExecutionStatus, self._parameters
            )
            return ExecutionStatus.NotPossible

    def is_possible(self, state: StateDictionary) -> bool:
        for key, value in self._preconditions.items():
            if key not in state:
                return False
            
            current_value = state.get(key)
            
            # This structure now mirrors the C# logic exactly.
            if current_value is None:
                if value is not None:
                    return False  # state is null, precondition is not.
                # else, both are None, so we continue to the next precondition.
            else: # current_value is not None
                if current_value != value: # In Python, `!=` calls `__ne__`, which is the correct equivalent to C#'s `!Equals()`
                    return False
        for key, comp_value_pair in self._comparative_preconditions.items():
            if key not in state:  # Key must exist
                return False
            
            current_val = state[key]
            desired_val = comp_value_pair.Value
            operator = comp_value_pair.Operator

            if operator == ComparisonOperator.Undefined:
                return False

            if operator == ComparisonOperator.Equals:
                if current_val != desired_val:
                    return False
            elif current_val is None or desired_val is None:
                # C# explicitly fails if current_val or desired_val is null for relational ops
                return False
            else:
                # Both current_val and desired_val are guaranteed to be non-None here
                if operator == ComparisonOperator.LessThan:
                    if not Utils.is_lower_than(current_val, desired_val):
                        return False
                elif operator == ComparisonOperator.GreaterThan:
                    if not Utils.is_higher_than(current_val, desired_val):
                        return False
                elif operator == ComparisonOperator.LessThanOrEquals:
                    if not Utils.is_lower_than_or_equals(current_val, desired_val):
                        return False
                elif operator == ComparisonOperator.GreaterThanOrEquals:
                    if not Utils.is_higher_than_or_equals(current_val, desired_val):
                        return False
        if self._state_checker is not None and not self._state_checker(self, state):
            return False
        return True

    def get_permutations(
        self, state: StateDictionary
    ) -> List[Dict[str, Optional[Any]]]:
        if not self._permutation_selectors:
            return []  # Match C# behavior: no permutations if no selectors

        combined_outputs: List[Dict[str, Optional[Any]]] = []
        outputs: Dict[str, List[Any]] = {}
        for key, selector_callback in self._permutation_selectors.items():
            outputs[key] = selector_callback(state)
            # ADD this check to match C#
            if not outputs[key]:
                return []
        permutation_parameters = list(outputs.keys())
        indices = [0] * len(permutation_parameters)
        counts = [len(outputs[param]) for param in permutation_parameters]
        while True:
            single_output: Dict[str, Optional[Any]] = {}
            for i in range(len(indices)):
                if indices[i] >= counts[i]:
                    continue
                param_key = permutation_parameters[i]
                single_output[param_key] = outputs[param_key][indices[i]]
            combined_outputs.append(single_output)
            if Action._indices_at_maximum(indices, counts):
                return combined_outputs
            Action._increment_indices(indices, counts)

    def apply_effects(self, state: StateDictionary) -> None:
        for key, value in self._postconditions.items():
            state[key] = value
        for key, value_to_add in self._arithmetic_postconditions.items():
            if key not in state:
                continue
            current_value = state[key]
            if isinstance(current_value, (int, float)) and isinstance(
                value_to_add, (int, float)
            ):
                state[key] = current_value + value_to_add
            elif isinstance(current_value, datetime) and isinstance(
                value_to_add, timedelta
            ):
                state[key] = current_value + value_to_add
            else:
                try:
                    state[key] = cast(Any, current_value) + cast(Any, value_to_add)
                except TypeError:
                    pass
        for param_key, state_key in self._parameter_postconditions.items():
            if param_key not in self._parameters:
                continue
            state[state_key] = self._parameters[param_key]
        if self._state_mutator is not None:
            self._state_mutator(self, state)

    def set_parameters(self, parameters: Dict[str, Optional[Any]]) -> None:
        self._parameters = parameters

    @staticmethod
    def _indices_at_maximum(indices: List[int], counts: List[int]) -> bool:
        for i in range(len(indices)):
            if indices[i] < counts[i] - 1:
                return False
        return True

    @staticmethod
    def _increment_indices(indices: List[int], counts: List[int]) -> None:
        if Action._indices_at_maximum(indices, counts):
            return
        for i in range(len(indices)):
            if indices[i] == counts[i] - 1:
                indices[i] = 0
            else:
                indices[i] += 1
                return

    def __hash__(self) -> int:
        return hash(self.Name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Action):
            return NotImplemented
        return self.Name == other.Name


# Original content from Agent.py
class Agent:
    Name: str
    CurrentActionSequences: List[List[Action]]
    State: StateDictionary
    Memory: Dict[str, Optional[Any]]
    Goals: List[BaseGoal]
    Actions: List[Action]
    Sensors: List[Sensor]
    CostMaximum: float
    StepMaximum: int
    _on_agent_step_handlers: List[AgentStepEvent] = []
    _on_agent_action_sequence_completed_handlers: List[
        AgentActionSequenceCompletedEvent
    ] = []
    _on_planning_started_handlers: List[PlanningStartedEvent] = []
    _on_planning_started_for_single_goal_handlers: List[
        PlanningStartedForSingleGoalEvent
    ] = []
    _on_planning_finished_for_single_goal_handlers: List[
        PlanningFinishedForSingleGoalEvent
    ] = []
    _on_planning_finished_handlers: List[PlanningFinishedEvent] = []
    _on_plan_updated_handlers: List[PlanUpdatedEvent] = []
    _on_evaluated_action_node_handlers: List[EvaluatedActionNodeEvent] = []

    @classmethod
    def OnAgentStep(cls, agent: "Agent"):
        for handler in cls._on_agent_step_handlers:
            handler(agent)

    @classmethod
    def OnAgentActionSequenceCompleted(cls, agent: "Agent"):
        for handler in cls._on_agent_action_sequence_completed_handlers:
            handler(agent)

    @classmethod
    def OnPlanningStarted(cls, agent: "Agent"):
        for handler in cls._on_planning_started_handlers:
            handler(agent)

    @classmethod
    def OnPlanningStartedForSingleGoal(cls, agent: "Agent", goal: BaseGoal):
        for handler in cls._on_planning_started_for_single_goal_handlers:
            handler(agent, goal)

    @classmethod
    def OnPlanningFinishedForSingleGoal(
        cls, agent: "Agent", goal: BaseGoal, utility: float
    ):
        for handler in cls._on_planning_finished_for_single_goal_handlers:
            handler(agent, goal, utility)

    @classmethod
    def OnPlanningFinished(
        cls, agent: "Agent", goal: Optional[BaseGoal], utility: float
    ):
        for handler in cls._on_planning_finished_handlers:
            handler(agent, goal, utility)

    @classmethod
    def OnPlanUpdated(cls, agent: "Agent", action_list: List[Action]):
        for handler in cls._on_plan_updated_handlers:
            handler(agent, action_list)

    @classmethod
    def OnEvaluatedActionNode(
        cls, node: ActionNode, nodes: Dict[ActionNode, ActionNode]
    ):
        for handler in cls._on_evaluated_action_node_handlers:
            handler(node, nodes)

    @classmethod
    def register_on_agent_step(cls, handler: AgentStepEvent):
        cls._on_agent_step_handlers.append(handler)

    @classmethod
    def register_on_agent_action_sequence_completed(
        cls, handler: AgentActionSequenceCompletedEvent
    ):
        cls._on_agent_action_sequence_completed_handlers.append(handler)

    @classmethod
    def register_on_planning_started(cls, handler: PlanningStartedEvent):
        cls._on_planning_started_handlers.append(handler)

    @classmethod
    def register_on_planning_started_for_single_goal(
        cls, handler: PlanningStartedForSingleGoalEvent
    ):
        cls._on_planning_started_for_single_goal_handlers.append(handler)

    @classmethod
    def register_on_planning_finished_for_single_goal(
        cls, handler: PlanningFinishedForSingleGoalEvent
    ):
        cls._on_planning_finished_for_single_goal_handlers.append(handler)

    @classmethod
    def register_on_planning_finished(cls, handler: PlanningFinishedEvent):
        cls._on_planning_finished_handlers.append(handler)

    @classmethod
    def register_on_plan_updated(cls, handler: PlanUpdatedEvent):
        cls._on_plan_updated_handlers.append(handler)

    @classmethod
    def register_on_evaluated_action_node(cls, handler: EvaluatedActionNodeEvent):
        cls._on_evaluated_action_node_handlers.append(handler)

    def __init__(
        self,
        name: Optional[str] = None,
        state: Optional[StateDictionary] = None,
        memory: Optional[Dict[str, Optional[Any]]] = None,
        goals: Optional[List[BaseGoal]] = None,
        actions: Optional[List[Action]] = None,
        sensors: Optional[List[Sensor]] = None,
        cost_maximum: float = float("inf"),
        step_maximum: int = float("inf"),
    ):
        self._lock = threading.Lock()
        self.Name = name if name is not None else f"Agent {uuid.uuid4()}"
        self.State = state if state is not None else {}
        self.Memory = memory if memory is not None else {}
        self.Goals = goals if goals is not None else []
        self.Actions = actions if actions is not None else []
        self.Sensors = sensors if sensors is not None else []
        self.CostMaximum = cost_maximum
        self.StepMaximum = step_maximum
        # Initialize instance-specific list
        self.CurrentActionSequences = []
        # Initialize instance-specific state flags
        self.IsBusy = False
        self.IsPlanning = False

    def step(self, mode: StepMode = StepMode.Default) -> None:
        Agent.OnAgentStep(self)
        for sensor in self.Sensors:
            sensor.run(self)
        if mode == StepMode.Default:
            self._step_async()
            return
        if not self.IsBusy:
            Planner.plan(self, self.CostMaximum, self.StepMaximum)
        if mode == StepMode.OneAction:
            self._execute()
        elif mode == StepMode.AllActions:
            while self.IsBusy:
                self._execute()

    def clear_plan(self) -> None:
        self.CurrentActionSequences.clear()

    def plan(self) -> None:
        if not self.IsBusy and not self.IsPlanning:
            self.IsPlanning = True
            Planner.plan(self, self.CostMaximum, self.StepMaximum)

    def plan_async(self) -> None:
        if not self.IsBusy and not self.IsPlanning:
            self.IsPlanning = True
            thread = threading.Thread(
                target=Planner.plan, args=(self, self.CostMaximum, self.StepMaximum)
            )
            thread.start()

    def execute_plan(self) -> None:
        if not self.IsPlanning:
            self._execute()

    def _step_async(self) -> None:
        if not self.IsBusy and not self.IsPlanning:
            self.IsPlanning = True
            thread = threading.Thread(
                target=Planner.plan, args=(self, self.CostMaximum, self.StepMaximum)
            )
            thread.start()
        elif not self.IsPlanning:
            self._execute()

    def _execute(self) -> None:
        if len(self.CurrentActionSequences) > 0:
            cullable_sequences = []
            for sequence in self.CurrentActionSequences:
                if len(sequence) > 0:
                    action_to_execute = sequence[0]
                    execution_status = action_to_execute.execute(self)
                    if execution_status != ExecutionStatus.Executing:
                        sequence.pop(0)
                    if len(sequence) == 0:
                        cullable_sequences.append(sequence)
                else:
                    cullable_sequences.append(sequence)
            for sequence in cullable_sequences:
                self.CurrentActionSequences.remove(sequence)
                Agent.OnAgentActionSequenceCompleted(self)
            # Check if agent has run out of plans and should no longer be busy
            if not self.CurrentActionSequences:
                self.IsBusy = False
        else:
            # IsBusy is only set to False if there were no sequences to start with.
            self.IsBusy = False


# --- RPG Specific Utilities and Factories ---
MaxX: int = 20
MaxY: int = 20


class Vector2:
    def __init__(self, x: float, y: float):
        self.X = x
        self.Y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.X == other.X and self.Y == other.Y

    def __hash__(self) -> int:
        return hash((self.X, self.Y))

    def __repr__(self) -> str:
        return f"Vector2({self.X}, {self.Y})"


class RpgUtils:
    @staticmethod
    def in_distance(pos1: Vector2, pos2: Vector2, max_distance: float) -> bool:
        distance = RpgUtils._distance(pos1, pos2)
        return distance <= max_distance

    @staticmethod
    def get_enemy_in_range(
        source: "Agent", agents: List["Agent"], distance: float
    ) -> Optional["Agent"]:
        for agent in agents:
            if agent == source:
                continue
            source_pos = source.State.get("position")
            agent_pos = agent.State.get("position")
            source_faction = source.State.get("faction")
            agent_faction = agent.State.get("faction")
            if (
                isinstance(source_pos, Vector2)
                and isinstance(agent_pos, Vector2)
                and isinstance(source_faction, str)
                and isinstance(agent_faction, str)
                and RpgUtils.in_distance(source_pos, agent_pos, distance)
                and source_faction != agent_faction
            ):
                return agent
        return None

    @staticmethod
    def move_towards_other_position(pos1: Vector2, pos2: Vector2) -> Vector2:
        new_pos = Vector2(pos1.X, pos1.Y)
        x_diff = pos2.X - new_pos.X
        y_diff = pos2.Y - new_pos.Y
        x_sign = 0
        if x_diff > 0:
            x_sign = 1
        elif x_diff < 0:
            x_sign = -1
        y_sign = 0
        if y_diff > 0:
            y_sign = 1
        elif y_diff < 0:
            y_sign = -1
        if x_sign != 0:
            new_pos.X += x_sign
        elif y_sign != 0:
            new_pos.Y += y_sign
        return new_pos

    @staticmethod
    def enemy_permutations(state: StateDictionary) -> List[Any]:
        enemies: List[Any] = []
        agents_list = state.get("agents")
        agent_faction = state.get("faction")
        if (
            not isinstance(agents_list, list)
            or not all(isinstance(a, Agent) for a in agents_list)
            or not isinstance(agent_faction, str)
        ):
            return enemies
        for agent in agents_list:
            if (
                isinstance(agent.State.get("faction"), str)
                and agent.State["faction"] != agent_faction
            ):
                enemies.append(agent)
        return enemies

    @staticmethod
    def food_permutations(state: StateDictionary) -> List[Any]:
        food_positions: List[Any] = []
        source_positions = state.get("foodPositions")
        if not isinstance(source_positions, list) or not all(
            isinstance(p, Vector2) for p in source_positions
        ):
            return food_positions
        food_positions.extend(source_positions)
        return food_positions

    @staticmethod
    def starting_position_permutations(state: StateDictionary) -> List[Any]:
        starting_positions: List[Any] = []
        position = state.get("position")
        if not isinstance(position, Vector2):
            return starting_positions
        starting_positions.append(position)
        return starting_positions

    @staticmethod
    def go_to_enemy_cost(action: Action, state: StateDictionary) -> float:
        starting_position = action.get_parameter("startingPosition")
        target_agent = action.get_parameter("target")
        if not isinstance(starting_position, Vector2) or not isinstance(
            target_agent, Agent
        ):
            return float("inf")
        target_position = target_agent.State.get("position")
        if not isinstance(target_position, Vector2):
            return float("inf")
        return RpgUtils._distance(starting_position, target_position)

    @staticmethod
    def go_to_food_cost(action: Action, state: StateDictionary) -> float:
        starting_position = action.get_parameter("startingPosition")
        target_position = action.get_parameter("target")
        if not isinstance(starting_position, Vector2) or not isinstance(
            target_position, Vector2
        ):
            return float("inf")
        return RpgUtils._distance(starting_position, target_position)

    @staticmethod
    def _distance(pos1: Vector2, pos2: Vector2) -> float:
        return math.sqrt(
            math.pow(abs(pos2.X - pos1.X), 2) + math.pow(abs(pos2.Y - pos1.Y), 2)
        )


# Consolidated Common RPG Agent Logic for sensors and executors
class CommonRpgAgentHandlers:
    _rng = random.Random()

    @staticmethod
    def _get_food_in_range(
        source: Vector2, food_positions: List[Vector2], range_val: float
    ) -> Optional[Vector2]:
        for position in food_positions:
            if RpgUtils.in_distance(source, position, range_val):
                return position
        return None

    @staticmethod
    def see_enemies_sensor_handler(agent_instance: "Agent") -> None:
        with agent_instance._lock:
            agents_in_state = agent_instance.State.get("agents")
            if isinstance(agents_in_state, list):
                sight_range = agent_instance.State.get(
                    "sight_range", 10.0
                )  # Use agent-specific sight range
                enemy_in_range = RpgUtils.get_enemy_in_range(
                    agent_instance, agents_in_state, sight_range
                )
                agent_instance.State["canSeeEnemies"] = enemy_in_range is not None

    @staticmethod
    def enemy_proximity_sensor_handler(agent_instance: "Agent") -> None:
        with agent_instance._lock:
            agents_in_state = agent_instance.State.get("agents")
            if isinstance(agents_in_state, list):
                enemy_in_range = RpgUtils.get_enemy_in_range(
                    agent_instance, agents_in_state, 1.0
                )
                agent_instance.State["nearEnemy"] = enemy_in_range is not None

    @staticmethod
    def kill_nearby_enemy_executor(
        agent_instance: "Agent", action_instance: "Action"
    ) -> ExecutionStatus:
        with agent_instance._lock:
            agents_in_state = agent_instance.State.get("agents")
            if isinstance(agents_in_state, list):
                target_enemy = RpgUtils.get_enemy_in_range(
                    agent_instance, agents_in_state, 1.0
                )
                if target_enemy is not None:
                    with target_enemy._lock:
                        current_hp = target_enemy.State.get("hp")
                        if isinstance(current_hp, int):
                            current_hp -= 1
                            target_enemy.State["hp"] = current_hp
                            print(
                                f"{agent_instance.Name} attacked {target_enemy.Name}. {target_enemy.Name} HP: {current_hp}"
                            )
                            if current_hp <= 0:
                                print(f"{target_enemy.Name} defeated!")
                                return ExecutionStatus.Succeeded
            return ExecutionStatus.Failed

    @staticmethod
    def go_to_enemy_executor(
        agent_instance: "Agent", action_instance: "Action"
    ) -> ExecutionStatus:
        with agent_instance._lock:
            target_agent = action_instance.get_parameter("target")
            agent_position = agent_instance.State.get("position")
            if not isinstance(target_agent, Agent) or not isinstance(
                agent_position, Vector2
            ):
                return ExecutionStatus.Failed
            with target_agent._lock:
                target_position = target_agent.State.get("position")
            if not isinstance(target_position, Vector2):
                return ExecutionStatus.Failed
            new_position = RpgUtils.move_towards_other_position(
                agent_position, target_position
            )
            agent_instance.State["position"] = new_position
            if RpgUtils.in_distance(new_position, target_position, 1.0):
                return ExecutionStatus.Succeeded
            else:
                return ExecutionStatus.Executing

    @staticmethod
    def see_food_sensor_handler(agent_instance: "Agent") -> None:
        with agent_instance._lock:
            agent_position = agent_instance.State.get("position")
            food_positions_in_state = agent_instance.State.get("foodPositions")
            if isinstance(agent_position, Vector2) and isinstance(
                food_positions_in_state, list
            ):
                food_sight_range = agent_instance.State.get(
                    "food_sight_range", 20.0
                )  # Use agent-specific food sight range
                food_in_range = CommonRpgAgentHandlers._get_food_in_range(
                    agent_position, food_positions_in_state, food_sight_range
                )
                agent_instance.State["canSeeFood"] = food_in_range is not None
                if not agent_instance.State["canSeeFood"] and agent_instance.State.get(
                    "eatingFood"
                ):
                    agent_instance.State["eatingFood"] = False

    @staticmethod
    def food_proximity_sensor_handler(agent_instance: "Agent") -> None:
        with agent_instance._lock:
            agent_position = agent_instance.State.get("position")
            food_positions_in_state = agent_instance.State.get("foodPositions")
            if isinstance(agent_position, Vector2) and isinstance(
                food_positions_in_state, list
            ):
                food_in_range = CommonRpgAgentHandlers._get_food_in_range(
                    agent_position, food_positions_in_state, 1.0
                )
                agent_instance.State["nearFood"] = food_in_range is not None
                if not agent_instance.State["nearFood"] and agent_instance.State.get(
                    "eatingFood"
                ):
                    agent_instance.State["eatingFood"] = False

    @staticmethod
    def look_for_food_executor(
        agent_instance: "Agent", action_instance: "Action"
    ) -> ExecutionStatus:
        agent_position = agent_instance.State.get("position")
        if isinstance(agent_position, Vector2):
            new_x = agent_position.X + CommonRpgAgentHandlers._rng.randint(-1, 1)
            new_y = agent_position.Y + CommonRpgAgentHandlers._rng.randint(-1, 1)
            new_x = max(0, min(new_x, MaxX - 1))
            new_y = max(0, min(new_y, MaxY - 1))
            agent_instance.State["position"] = Vector2(new_x, new_y)
        can_see_food = agent_instance.State.get("canSeeFood")
        if isinstance(can_see_food, bool) and can_see_food:
            return ExecutionStatus.Succeeded
        return ExecutionStatus.Failed

    @staticmethod
    def go_to_food_executor(
        agent_instance: "Agent", action_instance: "Action"
    ) -> ExecutionStatus:
        food_position = action_instance.get_parameter("target")
        agent_position = agent_instance.State.get("position")
        if not isinstance(food_position, Vector2) or not isinstance(
            agent_position, Vector2
        ):
            return ExecutionStatus.Failed
        new_position = RpgUtils.move_towards_other_position(
            agent_position, food_position
        )
        agent_instance.State["position"] = new_position
        if RpgUtils.in_distance(new_position, food_position, 1.0):
            return ExecutionStatus.Succeeded
        else:
            return ExecutionStatus.Executing

    @staticmethod
    def eat_food_executor(
        agent_instance: "Agent", action_instance: "Action"
    ) -> ExecutionStatus:
        food_positions_in_state = agent_instance.State.get("foodPositions")
        agent_position = agent_instance.State.get("position")
        if isinstance(food_positions_in_state, list) and isinstance(
            agent_position, Vector2
        ):
            food_to_eat = CommonRpgAgentHandlers._get_food_in_range(
                agent_position, food_positions_in_state, 1.0
            )
            if food_to_eat is not None:
                food_eaten = agent_instance.State.get(
                    "food_eaten", 0
                )  # This state is only for player, monster does not have it.
                print(
                    f"{agent_instance.Name} ate food at {food_to_eat}. Food eaten: {food_eaten} -> {food_eaten + 1}"
                    if "food_eaten" in agent_instance.State
                    else f"{agent_instance.Name} ate food at {food_to_eat}"
                )
                food_positions_in_state.remove(food_to_eat)
                return ExecutionStatus.Succeeded
        return ExecutionStatus.Failed


# --- RPG Character Factories ---
class RpgCharacterFactory:
    @staticmethod
    def create(agents: List["Agent"], name: str = "Player") -> "Agent":
        remove_enemies_goal = Goal(
            name="Remove Enemies", weight=1.0, desired_state={"canSeeEnemies": False}
        )
        see_enemies_sensor = Sensor(
            CommonRpgAgentHandlers.see_enemies_sensor_handler, "Enemy Sight Sensor"
        )
        enemy_proximity_sensor = Sensor(
            CommonRpgAgentHandlers.enemy_proximity_sensor_handler,
            "Enemy Proximity Sensor",
        )
        go_to_enemy_action = Action(
            name="Go To Enemy",
            executor=CommonRpgAgentHandlers.go_to_enemy_executor,
            preconditions={"canSeeEnemies": True, "nearEnemy": False},
            postconditions={"nearEnemy": True},
            permutation_selectors={
                "target": RpgUtils.enemy_permutations,
                "startingPosition": RpgUtils.starting_position_permutations,
            },
            cost_callback=RpgUtils.go_to_enemy_cost,
        )
        kill_nearby_enemy_action = Action(
            name="Kill Nearby Enemy",
            executor=CommonRpgAgentHandlers.kill_nearby_enemy_executor,
            preconditions={"nearEnemy": True},
            postconditions={"canSeeEnemies": False, "nearEnemy": False},
        )
        agent = Agent(
            name=name,
            state={
                "canSeeEnemies": False,
                "nearEnemy": False,
                "hp": 80,
                "position": Vector2(10, 10),
                "faction": "enemy" if "Monster" in name else "player",
                "agents": agents,
                "sight_range": (
                    5.0 if "Monster" in name else 10.0
                ),  # Set range based on type
            },
            goals=[remove_enemies_goal],
            sensors=[see_enemies_sensor, enemy_proximity_sensor],
            actions=[go_to_enemy_action, kill_nearby_enemy_action],
        )
        return agent


class PlayerFactory:
    @staticmethod
    def create(
        agents: List["Agent"], food_positions: List[Vector2], name: str = "Player"
    ) -> "Agent":
        USE_EXTREME_GOAL = os.getenv("USE_EXTREME_GOAL", "false").lower() == "true"
        if USE_EXTREME_GOAL:
            food_goal = ExtremeGoal(
                name="Maximize Food Eaten",
                weight=1.0,
                desired_state={"food_eaten": True},
            )
        else:
            food_goal = ComparativeGoal(
                name="Get at least 5 food",
                weight=1.0,
                desired_state={
                    "food_eaten": ComparisonValuePair(
                        operator=ComparisonOperator.GreaterThanOrEquals, value=3
                    )
                },
            )
        remove_enemies_goal = Goal(
            name="Remove Enemies", weight=10.0, desired_state={"canSeeEnemies": False}
        )
        see_enemies_sensor = Sensor(
            CommonRpgAgentHandlers.see_enemies_sensor_handler, "Enemy Sight Sensor"
        )
        enemy_proximity_sensor = Sensor(
            CommonRpgAgentHandlers.enemy_proximity_sensor_handler,
            "Enemy Proximity Sensor",
        )
        see_food_sensor = Sensor(
            CommonRpgAgentHandlers.see_food_sensor_handler, "Food Sight Sensor"
        )
        food_proximity_sensor = Sensor(
            CommonRpgAgentHandlers.food_proximity_sensor_handler,
            "Food Proximity Sensor",
        )
        go_to_enemy_action = Action(
            name="Go To Enemy",
            executor=CommonRpgAgentHandlers.go_to_enemy_executor,
            preconditions={"canSeeEnemies": True, "nearEnemy": False},
            postconditions={"nearEnemy": True},
            permutation_selectors={
                "target": RpgUtils.enemy_permutations,
                "startingPosition": RpgUtils.starting_position_permutations,
            },
            cost_callback=RpgUtils.go_to_enemy_cost,
        )
        kill_nearby_enemy_action = Action(
            name="Kill Nearby Enemy",
            executor=CommonRpgAgentHandlers.kill_nearby_enemy_executor,
            preconditions={"nearEnemy": True},
            postconditions={"canSeeEnemies": False, "nearEnemy": False},
        )
        look_for_food_action = Action(
            name="Look For Food",
            executor=CommonRpgAgentHandlers.look_for_food_executor,
            preconditions={"canSeeFood": False},
            postconditions={"canSeeFood": True},
        )
        go_to_food_action = Action(
            name="Go To Food",
            executor=CommonRpgAgentHandlers.go_to_food_executor,
            preconditions={"canSeeFood": True, "nearFood": False},
            postconditions={"nearFood": True},
            permutation_selectors={
                "target": RpgUtils.food_permutations,
                "startingPosition": RpgUtils.starting_position_permutations,
            },
            cost_callback=RpgUtils.go_to_food_cost,
        )
        eat_food_action = Action(
            name="Eat Food",
            executor=CommonRpgAgentHandlers.eat_food_executor,
            preconditions={"nearFood": True},
            arithmetic_postconditions={"food_eaten": 1},
        )
        rest_action = Action(
            name="Rest",
            executor=lambda agent_instance, action_instance: ExecutionStatus.Succeeded,
            preconditions={
                "canSeeEnemies": False,
                "canSeeFood": False,
            },
            arithmetic_postconditions={"rest_count": 1},
        )
        agent = Agent(
            name=name,
            state={
                "canSeeEnemies": False,
                "nearEnemy": False,
                "canSeeFood": False,
                "nearFood": False,
                "hp": 80,
                "food_eaten": 0,
                "position": Vector2(10, 10),
                "faction": "player",
                "agents": agents,
                "foodPositions": food_positions,
                "rest_count": 0,
                "sight_range": 10.0,
                "food_sight_range": 20.0,
            },
            goals=[
                food_goal,
                remove_enemies_goal,
                ExtremeGoal(
                    name="Idle", weight=0.1, desired_state={"rest_count": True}
                ),
            ],
            sensors=[
                see_enemies_sensor,
                enemy_proximity_sensor,
                see_food_sensor,
                food_proximity_sensor,
            ],
            actions=[
                go_to_enemy_action,
                kill_nearby_enemy_action,
                look_for_food_action,
                go_to_food_action,
                eat_food_action,
                rest_action,
            ],
        )
        return agent


class RpgMonsterFactory:
    _counter = 1

    @staticmethod
    def create(agents: List["Agent"], food_positions: List[Vector2]) -> "Agent":
        monster_name = f"Monster {RpgMonsterFactory._counter}"
        RpgMonsterFactory._counter += 1
        agent = RpgCharacterFactory.create(agents, monster_name)
        agent.State["faction"] = "enemy"
        eat_food_goal = Goal(
            name="Eat Food", weight=0.1, desired_state={"eatingFood": True}
        )
        see_food_sensor = Sensor(
            CommonRpgAgentHandlers.see_food_sensor_handler, "Food Sight Sensor"
        )
        food_proximity_sensor = Sensor(
            CommonRpgAgentHandlers.food_proximity_sensor_handler,
            "Food Proximity Sensor",
        )
        look_for_food_action = Action(
            name="Look For Food",
            executor=CommonRpgAgentHandlers.look_for_food_executor,
            preconditions={"canSeeFood": False, "canSeeEnemies": False},
            postconditions={"canSeeFood": True},
        )
        go_to_food_action = Action(
            name="Go To Food",
            executor=CommonRpgAgentHandlers.go_to_food_executor,
            preconditions={"canSeeFood": True, "canSeeEnemies": False},
            postconditions={"nearFood": True},
            permutation_selectors={
                "target": RpgUtils.food_permutations,
                "startingPosition": RpgUtils.starting_position_permutations,
            },
            cost_callback=RpgUtils.go_to_food_cost,
        )
        eat_action = Action(
            name="Eat",
            executor=CommonRpgAgentHandlers.eat_food_executor,
            preconditions={"nearFood": True, "canSeeEnemies": False},
            postconditions={"eatingFood": True},
        )
        agent.State["canSeeFood"] = False
        agent.State["nearFood"] = False
        agent.State["eatingFood"] = False
        agent.State["foodPositions"] = food_positions
        agent.State["hp"] = 2
        agent.State["sight_range"] = 5.0
        agent.State["food_sight_range"] = 5.0
        agent.Goals.append(eat_food_goal)
        agent.Sensors.append(see_food_sensor)
        agent.Sensors.append(food_proximity_sensor)
        agent.Actions.append(go_to_food_action)
        agent.Actions.append(look_for_food_action)
        agent.Actions.append(eat_action)
        return agent


# --- Pygame Integration ---
# Pygame constants
CELL_SIZE = 30
WIDTH = 20 * CELL_SIZE
HEIGHT = 20 * CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)


class RpgExampleComparativePygame:
    @staticmethod
    def run() -> None:
        _ = DefaultLogger(
            log_to_console=True, logging_file="rpg-example.log", filter_string="Monster"
        )

        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("RPG GOAP Example")
        clock = pygame.time.Clock()

        _random = random.Random()
        agents: List[Agent] = []
        food_positions: List[Vector2] = []

        player = PlayerFactory.create(agents, food_positions)
        agents.append(player)

        for _ in range(20):
            food_positions.append(
                Vector2(_random.randint(0, MaxX - 1), _random.randint(0, MaxY - 1))
            )

        for _ in range(10):
            monster = RpgMonsterFactory.create(agents, food_positions)
            monster.State["position"] = Vector2(
                _random.randint(0, MaxX - 1), _random.randint(0, MaxY - 1)
            )
            agents.append(monster)

        running = True
        turn = 0
        last_update = pygame.time.get_ticks()

        while running and turn < 600:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_time = pygame.time.get_ticks()
            if current_time - last_update >= 200:
                turn += 1
                print(f"--- Turn {turn} ---")

                # Iterate on a copy of the agents list to safely handle agents being removed (defeated)
                for agent in list(agents):
                    if agent in agents:  # Check if agent wasn't removed by a previous death this turn
                        agent.step(mode=StepMode.OneAction)
                        # Process deaths immediately after each action to prevent dead agents from acting
                        RpgExampleComparativePygame._process_deaths(agents)
                last_update = current_time

                if player not in agents:
                    print("Player defeated! Game Over.")
                    break

            RpgExampleComparativePygame._render_grid(screen, agents, food_positions)
            pygame.display.flip()
            clock.tick(60)

        print("Game finished.")
        pygame.quit()

    @staticmethod
    def _render_grid(
        screen: pygame.Surface, agents: List["Agent"], food_positions: List[Vector2]
    ) -> None:
        screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

        for pos in food_positions:
            if 0 <= pos.X < MaxX and 0 <= pos.Y < MaxY:
                rect = pygame.Rect(
                    int(pos.X) * CELL_SIZE + 2,
                    int(pos.Y) * CELL_SIZE + 2,
                    CELL_SIZE - 4,
                    CELL_SIZE - 4,
                )
                pygame.draw.ellipse(screen, YELLOW, rect)

        for agent in agents:
            agent_pos = agent.State.get("position")
            agent_faction = agent.State.get("faction")

            if isinstance(agent_pos, Vector2) and isinstance(agent_faction, str):
                if 0 <= agent_pos.X < MaxX and 0 <= agent_pos.Y < MaxY:
                    rect = pygame.Rect(
                        int(agent_pos.X) * CELL_SIZE + 2,
                        int(agent_pos.Y) * CELL_SIZE + 2,
                        CELL_SIZE - 4,
                        CELL_SIZE - 4,
                    )

                    if agent_faction == "player":
                        agent_hp = agent.State.get("hp")
                        color = (
                            RED if isinstance(agent_hp, int) and agent_hp < 30 else BLUE
                        )
                        pygame.draw.rect(screen, color, rect)
                    else:
                        pygame.draw.rect(screen, GREEN, rect)

    @staticmethod
    def _process_deaths(agents: List["Agent"]) -> None:
        cull_list: List["Agent"] = []
        for agent in agents:
            hp = agent.State.get("hp")
            if isinstance(hp, int) and hp <= 0:
                cull_list.append(agent)

        for agent_to_remove in cull_list:
            agents.remove(agent_to_remove)
            print(f"Agent {agent_to_remove.Name} has died.")


if __name__ == "__main__":
    RpgExampleComparativePygame.run()

</python>

<csharp>
├── MountainGoap.sln
├── MountainGoap
    ├── Action.cs
    ├── Agent.cs
    ├── BaseGoal.cs
    ├── CallbackDelegates
    │   ├── CostCallback.cs
    │   ├── ExecutorCallback.cs
    │   ├── PermutationSelectorCallback.cs
    │   ├── SensorRunCallback.cs
    │   ├── StateCheckerCallback.cs
    │   ├── StateCostDeltaMultiplierCallback.cs
    │   └── StateMutatorCallback.cs
    ├── ComparativeGoal.cs
    ├── ComparisonOperator.cs
    ├── ComparisonValuePair.cs
    ├── Events
    │   ├── AgentActionSequenceCompletedEvent.cs
    │   ├── AgentStepEvent.cs
    │   ├── BeginExecuteActionEvent.cs
    │   ├── EvaluatedActionNodeEvent.cs
    │   ├── FinishExecuteActionEvent.cs
    │   ├── PlanUpdatedEvent.cs
    │   ├── PlanningFinishedEvent.cs
    │   ├── PlanningFinishedForSingleGoalEvent.cs
    │   ├── PlanningStartedEvent.cs
    │   ├── PlanningStartedForSingleGoalEvent.cs
    │   └── SensorRunningEvent.cs
    ├── ExecutionStatus.cs
    ├── ExtremeGoal.cs
    ├── Goal.cs
    ├── Internals
    │   ├── ActionAStar.cs
    │   ├── ActionGraph.cs
    │   ├── ActionNode.cs
    │   ├── DictionaryExtensionMethods.cs
    │   ├── Planner.cs
    │   └── Utils.cs
    ├── MountainGoap.csproj
    ├── PermutationSelectorGenerators.cs
    ├── PriorityQueue
    │   ├── FastPriorityQueue.cs
    │   ├── FastPriorityQueueNode.cs
    │   ├── GenericPriorityQueue.cs
    │   ├── GenericPriorityQueueNode.cs
    │   ├── IFixedSizePriorityQueue.cs
    │   ├── IPriorityQueue.cs
    │   ├── Priority Queue.csproj
    │   ├── Priority Queue.nuspec
    │   ├── Priority Queue.snk
    │   ├── Properties
    │   │   └── AssemblyInfo.cs
    │   ├── SimplePriorityQueue.cs
    │   ├── StablePriorityQueue.cs
    │   ├── StablePriorityQueueNode.cs
    │   └── packages.config
    ├── Sensor.cs
    ├── StepMode.cs
    └── stylecop.json
├── MountainGoapLogging
    ├── DefaultLogger.cs
    └── MountainGoapLogging.csproj
└── MountainGoapTest
    ├── ActionContinuationTests.cs
    ├── ActionNodeTests.cs
    ├── ArithmeticPostconditionsTests.cs
    ├── MountainGoapTest.csproj
    ├── PermutationSelectorGeneratorTests.cs
    ├── PermutationSelectorTests.cs
    └── Usings.cs

/MountainGoap.sln
--------------------------------------------------------------------------------

 1 | ﻿
 2 | Microsoft Visual Studio Solution File, Format Version 12.00
 3 | # Visual Studio Version 17
 4 | VisualStudioVersion = 17.3.32825.248
 5 | MinimumVisualStudioVersion = 10.0.40219.1
 6 | Project("{9A19103F-16F7-4668-BE54-9A1E7A4F7556}") = "MountainGoap", "MountainGoap\MountainGoap.csproj", "{3EBEB82D-FD0F-4194-B8C0-0C276203536F}"
 7 | EndProject
 8 | Project("{9A19103F-16F7-4668-BE54-9A1E7A4F7556}") = "Examples", "Examples\Examples.csproj", "{22E10E1F-2DA6-4E69-9252-EE653D90A1C4}"
 9 | EndProject
10 | Project("{9A19103F-16F7-4668-BE54-9A1E7A4F7556}") = "MountainGoapLogging", "MountainGoapLogging\MountainGoapLogging.csproj", "{6102C0D5-E087-4F6E-A477-03B3CDAC0FAC}"
11 | EndProject
12 | Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "MountainGoapTest", "MountainGoapTest\MountainGoapTest.csproj", "{32147608-90CE-4D4C-8A58-0789C5B0CCED}"
13 | EndProject
14 | Global
15 |  GlobalSection(SolutionConfigurationPlatforms) = preSolution
16 |   Debug|Any CPU = Debug|Any CPU
17 |   Release|Any CPU = Release|Any CPU
18 |  EndGlobalSection
19 |  GlobalSection(ProjectConfigurationPlatforms) = postSolution
20 |   {3EBEB82D-FD0F-4194-B8C0-0C276203536F}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
21 |   {3EBEB82D-FD0F-4194-B8C0-0C276203536F}.Debug|Any CPU.Build.0 = Debug|Any CPU
22 |   {3EBEB82D-FD0F-4194-B8C0-0C276203536F}.Release|Any CPU.ActiveCfg = Release|Any CPU
23 |   {3EBEB82D-FD0F-4194-B8C0-0C276203536F}.Release|Any CPU.Build.0 = Release|Any CPU
24 |   {22E10E1F-2DA6-4E69-9252-EE653D90A1C4}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
25 |   {22E10E1F-2DA6-4E69-9252-EE653D90A1C4}.Debug|Any CPU.Build.0 = Debug|Any CPU
26 |   {22E10E1F-2DA6-4E69-9252-EE653D90A1C4}.Release|Any CPU.ActiveCfg = Release|Any CPU
27 |   {22E10E1F-2DA6-4E69-9252-EE653D90A1C4}.Release|Any CPU.Build.0 = Release|Any CPU
28 |   {6102C0D5-E087-4F6E-A477-03B3CDAC0FAC}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
29 |   {6102C0D5-E087-4F6E-A477-03B3CDAC0FAC}.Debug|Any CPU.Build.0 = Debug|Any CPU
30 |   {6102C0D5-E087-4F6E-A477-03B3CDAC0FAC}.Release|Any CPU.ActiveCfg = Release|Any CPU
31 |   {6102C0D5-E087-4F6E-A477-03B3CDAC0FAC}.Release|Any CPU.Build.0 = Release|Any CPU
32 |   {32147608-90CE-4D4C-8A58-0789C5B0CCED}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
33 |   {32147608-90CE-4D4C-8A58-0789C5B0CCED}.Debug|Any CPU.Build.0 = Debug|Any CPU
34 |   {32147608-90CE-4D4C-8A58-0789C5B0CCED}.Release|Any CPU.ActiveCfg = Release|Any CPU
35 |   {32147608-90CE-4D4C-8A58-0789C5B0CCED}.Release|Any CPU.Build.0 = Release|Any CPU
36 |  EndGlobalSection
37 |  GlobalSection(SolutionProperties) = preSolution
38 |   HideSolutionNode = FALSE
39 |  EndGlobalSection
40 |  GlobalSection(ExtensibilityGlobals) = postSolution
41 |   SolutionGuid = {3411896C-FE2B-4361-AEF1-8DE5302E7FA7}
42 |  EndGlobalSection
43 | EndGlobal
44 |

--------------------------------------------------------------------------------

/MountainGoap/Action.cs
--------------------------------------------------------------------------------

  1 | ﻿// <copyright file="Action.cs" company="Chris Muller">
  2 | // Copyright (c) Chris Muller. All rights reserved.
  3 | // </copyright>
  4 | namespace MountainGoap {
  5 |     using System;
  6 |     using System.Collections.Concurrent;
  7 |     using System.Collections.Generic;
  8 |     using System.Linq;
  9 |     using System.Reflection;
 10 |
 11 |     /// <summary>
 12 |     /// Represents an action in a GOAP system.
 13 |     /// </summary>
 14 |     public class Action {
 15 |         /// <summary>
 16 |         /// Name of the action.
 17 |         /// </summary>
 18 |         public readonly string Name;
 19 |
 20 |         /// <summary>
 21 |         /// Cost of the action.
 22 |         /// </summary>
 23 |         private readonly float cost;
 24 |
 25 |         /// <summary>
 26 |         /// The permutation selector callbacks for the action.
 27 |         /// </summary>
 28 |         private readonly Dictionary<string, PermutationSelectorCallback> permutationSelectors;
 29 |
 30 |         /// <summary>
 31 |         /// The executor callback for the action.
 32 |         /// </summary>
 33 |         private readonly ExecutorCallback executor;
 34 |
 35 |         /// <summary>
 36 |         /// The cost callback for the action.
 37 |         /// </summary>
 38 |         private readonly CostCallback costCallback;
 39 |
 40 |         /// <summary>
 41 |         /// Preconditions for the action. These things are required for the action to execute.
 42 |         /// </summary>
 43 |         private readonly Dictionary<string, object?> preconditions = new();
 44 |
 45 |         /// <summary>
 46 |         /// Comnparative preconditions for the action. Indicates that a value must be greater than or less than a certain value for the action to execute.
 47 |         /// </summary>
 48 |         private readonly Dictionary<string, ComparisonValuePair> comparativePreconditions = new();
 49 |
 50 |         /// <summary>
 51 |         /// Postconditions for the action. These will be set when the action has executed.
 52 |         /// </summary>
 53 |         private readonly Dictionary<string, object?> postconditions = new();
 54 |
 55 |         /// <summary>
 56 |         /// Arithmetic postconditions for the action. These will be added to the current value when the action has executed.
 57 |         /// </summary>
 58 |         private readonly Dictionary<string, object> arithmeticPostconditions = new();
 59 |
 60 |         /// <summary>
 61 |         /// Parameter postconditions for the action. When the action has executed, the value of the parameter given in the key will be copied to the state with the name given in the value.
 62 |         /// </summary>
 63 |         private readonly Dictionary<string, string> parameterPostconditions = new();
 64 |
 65 |         /// <summary>
 66 |         /// State mutator for modifying state programmatically after action execution or evaluation.
 67 |         /// </summary>
 68 |         private readonly StateMutatorCallback? stateMutator;
 69 |
 70 |         /// <summary>
 71 |         /// State checker for checking state programmatically before action execution or evaluation.
 72 |         /// </summary>
 73 |         private readonly StateCheckerCallback? stateChecker;
 74 |
 75 |         /// <summary>
 76 |         /// Parameters to be passed to the action.
 77 |         /// </summary>
 78 |         private Dictionary<string, object?> parameters = new();
 79 |
 80 |         /// <summary>
 81 |         /// Initializes a new instance of the <see cref="Action"/> class.
 82 |         /// </summary>
 83 |         /// <param name="name">Name for the action, for eventing and logging purposes.</param>
 84 |         /// <param name="permutationSelectors">The permutation selector callback for the action's parameters.</param>
 85 |         /// <param name="executor">The executor callback for the action.</param>
 86 |         /// <param name="cost">Cost of the action.</param>
 87 |         /// <param name="costCallback">Callback for determining the cost of the action.</param>
 88 |         /// <param name="preconditions">Preconditions required in the world state in order for the action to occur.</param>
 89 |         /// <param name="comparativePreconditions">Preconditions indicating relative value requirements needed for the action to occur.</param>
 90 |         /// <param name="postconditions">Postconditions applied after the action is successfully executed.</param>
 91 |         /// <param name="arithmeticPostconditions">Arithmetic postconditions added to state after the action is successfully executed.</param>
 92 |         /// <param name="parameterPostconditions">Parameter postconditions copied to state after the action is successfully executed.</param>
 93 |         /// <param name="stateMutator">Callback for modifying state after action execution or evaluation.</param>
 94 |         /// <param name="stateChecker">Callback for checking state before action execution or evaluation.</param>
 95 |         /// <param name="stateCostDeltaMultiplier">Callback for multiplier for delta value to provide delta cost.</param>
 96 |         public Action(string? name = null, Dictionary<string, PermutationSelectorCallback>? permutationSelectors = null, ExecutorCallback? executor = null, float cost = 1f, CostCallback? costCallback = null, Dictionary<string, object?>? preconditions = null, Dictionary<string, ComparisonValuePair>? comparativePreconditions = null, Dictionary<string, object?>? postconditions = null, Dictionary<string, object>? arithmeticPostconditions = null, Dictionary<string, string>? parameterPostconditions = null, StateMutatorCallback? stateMutator = null, StateCheckerCallback? stateChecker = null, StateCostDeltaMultiplierCallback? stateCostDeltaMultiplier = null) {
 97 |             if (permutationSelectors == null) this.permutationSelectors = new();
 98 |             else this.permutationSelectors = permutationSelectors;
 99 |             if (executor == null) this.executor = DefaultExecutorCallback;
100 |             else this.executor = executor;
101 |             Name = name ??
quot;Action {Guid.NewGuid()} ({this.executor.GetMethodInfo().Name})";
102 |             this.cost = cost;
103 |             this.costCallback = costCallback ?? DefaultCostCallback;
104 |             if (preconditions != null) this.preconditions = preconditions;
105 |             if (comparativePreconditions != null) this.comparativePreconditions = comparativePreconditions;
106 |             if (postconditions != null) this.postconditions = postconditions;
107 |             if (arithmeticPostconditions != null) this.arithmeticPostconditions = arithmeticPostconditions;
108 |             if (parameterPostconditions != null) this.parameterPostconditions = parameterPostconditions;
109 |             if (stateMutator != null) this.stateMutator = stateMutator;
110 |             if (stateChecker != null) this.stateChecker = stateChecker;
111 |             StateCostDeltaMultiplier = stateCostDeltaMultiplier ?? DefaultStateCostDeltaMultiplier;
112 |         }
113 |
114 |         /// <summary>
115 |         /// Gets or sets multiplier for delta value to provide delta cost.
116 |         /// </summary>
117 |         public StateCostDeltaMultiplierCallback? StateCostDeltaMultiplier { get; set; }
118 |
119 |         public static float DefaultStateCostDeltaMultiplier(Action? action, string stateKey) => 1f;
120 |
121 |         /// <summary>
122 |         /// Event that triggers when an action begins executing.
123 |         /// </summary>
124 |         public static event BeginExecuteActionEvent OnBeginExecuteAction = (agent, action, parameters) => { };
125 |
126 |         /// <summary>
127 |         /// Event that triggers when an action finishes executing.
128 |         /// </summary>
129 |         public static event FinishExecuteActionEvent OnFinishExecuteAction = (agent, action, status, parameters) => { };
130 |
131 |         /// <summary>
132 |         /// Gets or sets the execution status of the action.
133 |         /// </summary>
134 |         internal ExecutionStatus ExecutionStatus { get; set; } = ExecutionStatus.NotYetExecuted;
135 |
136 |         /// <summary>
137 |         /// Makes a copy of the action.
138 |         /// </summary>
139 |         /// <returns>A copy of the action.</returns>
140 |         public Action Copy() {
141 |             var newAction = new Action(Name, permutationSelectors, executor, cost, costCallback, preconditions.Copy(), comparativePreconditions.Copy(), postconditions.Copy(), arithmeticPostconditions.CopyNonNullable(), parameterPostconditions.Copy(), stateMutator, stateChecker, StateCostDeltaMultiplier) {
142 |                 parameters = parameters.Copy()
143 |             };
144 |             return newAction;
145 |         }
146 |
147 |         /// <summary>
148 |         /// Sets a parameter to the action.
149 |         /// </summary>
150 |         /// <param name="key">Key to be set.</param>
151 |         /// <param name="value">Value to be set.</param>
152 |         public void SetParameter(string key, object value) {
153 |             parameters[key] = value;
154 |         }
155 |
156 |         /// <summary>
157 |         /// Gets a parameter to the action.
158 |         /// </summary>
159 |         /// <param name="key">Key for the value to be retrieved.</param>
160 |         /// <returns>The value stored at the key specified.</returns>
161 |         public object? GetParameter(string key) {
162 |             if (parameters.ContainsKey(key)) return parameters[key];
163 |             return null;
164 |         }
165 |
166 |         /// <summary>
167 |         /// Gets the cost of the action.
168 |         /// </summary>
169 |         /// <param name="currentState">State as it will be when cost is relevant.</param>
170 |         /// <returns>The cost of the action.</returns>
171 |         public float GetCost(ConcurrentDictionary<string, object?> currentState) {
172 |             try {
173 |                 return costCallback(this, currentState);
174 |             }
175 |             catch {
176 |                 return float.MaxValue;
177 |             }
178 |         }
179 |
180 |         /// <summary>
181 |         /// Executes a step of work for the agent.
182 |         /// </summary>
183 |         /// <param name="agent">Agent executing the action.</param>
184 |         /// <returns>The execution status of the action.</returns>
185 |         internal ExecutionStatus Execute(Agent agent) {
186 |             OnBeginExecuteAction(agent, this, parameters);
187 |             if (IsPossible(agent.State)) {
188 |                 var newState = executor(agent, this);
189 |                 if (newState == ExecutionStatus.Succeeded) ApplyEffects(agent.State);
190 |                 ExecutionStatus = newState;
191 |                 OnFinishExecuteAction(agent, this, ExecutionStatus, parameters);
192 |                 return newState;
193 |             }
194 |             else {
195 |                 OnFinishExecuteAction(agent, this, ExecutionStatus.NotPossible, parameters);
196 |                 return ExecutionStatus.NotPossible;
197 |             }
198 |         }
199 |
200 |         /// <summary>
201 |         /// Determines whether or not an action is possible.
202 |         /// </summary>
203 |         /// <param name="state">The current world state.</param>
204 |         /// <returns>True if the action is possible, otherwise false.</returns>
205 |         internal bool IsPossible(ConcurrentDictionary<string, object?> state) {
206 |             foreach (var kvp in preconditions) {
207 |                 if (!state.ContainsKey(kvp.Key)) return false;
208 |                 if (state[kvp.Key] == null && state[kvp.Key] != kvp.Value) return false;
209 |                 else if (state[kvp.Key] == null && state[kvp.Key] == kvp.Value) continue;
210 |                 if (state[kvp.Key] is object obj && !obj.Equals(kvp.Value)) return false;
211 |             }
212 |             foreach (var kvp in comparativePreconditions) {
213 |                 if (!state.ContainsKey(kvp.Key)) return false;
214 |                 if (state[kvp.Key] == null) return false;
215 |                 if (state[kvp.Key] is object obj && kvp.Value.Value is object obj2) {
216 |                     if (kvp.Value.Operator == ComparisonOperator.LessThan && !Utils.IsLowerThan(obj, obj2)) return false;
217 |                     else if (kvp.Value.Operator == ComparisonOperator.GreaterThan && !Utils.IsHigherThan(obj, obj2)) return false;
218 |                     else if (kvp.Value.Operator == ComparisonOperator.LessThanOrEquals && !Utils.IsLowerThanOrEquals(obj, obj2)) return false;
219 |                     else if (kvp.Value.Operator == ComparisonOperator.GreaterThanOrEquals && !Utils.IsHigherThanOrEquals(obj, obj2)) return false;
220 |                 }
221 |                 else return false;
222 |             }
223 |             if (stateChecker?.Invoke(this, state) == false) return false;
224 |             return true;
225 |         }
226 |
227 |         /// <summary>
228 |         /// Gets all permutations of parameters possible for an action.
229 |         /// </summary>
230 |         /// <param name="state">World state when the action would be performed.</param>
231 |         /// <returns>A list of possible parameter dictionaries that could be used.</returns>
232 |         internal List<Dictionary<string, object?>> GetPermutations(ConcurrentDictionary<string, object?> state) {
233 |             List<Dictionary<string, object?>> combinedOutputs = new();
234 |             Dictionary<string, List<object>> outputs = new();
235 |             foreach (var kvp in permutationSelectors) outputs[kvp.Key] = kvp.Value(state);
236 |             var permutationParameters = outputs.Keys.ToList();
237 |             List<int> indices = new();
238 |             List<int> counts = new();
239 |             foreach (var parameter in permutationParameters) {
240 |                 indices.Add(0);
241 |                 if (outputs[parameter].Count == 0) return combinedOutputs;
242 |                 counts.Add(outputs[parameter].Count);
243 |             }
244 |             while (true) {
245 |                 var singleOutput = new Dictionary<string, object?>();
246 |                 for (int i = 0; i < indices.Count; i++) {
247 |                     if (indices[i] >= outputs[permutationParameters[i]].Count) continue;
248 |                     singleOutput[permutationParameters[i]] = outputs[permutationParameters[i]][indices[i]];
249 |                 }
250 |                 combinedOutputs.Add(singleOutput);
251 |                 if (IndicesAtMaximum(indices, counts)) return combinedOutputs;
252 |                 IncrementIndices(indices, counts);
253 |             }
254 |         }
255 |
256 |         /// <summary>
257 |         /// Applies the effects of the action.
258 |         /// </summary>
259 |         /// <param name="state">World state to which to apply effects.</param>
260 |         internal void ApplyEffects(ConcurrentDictionary<string, object?> state) {
261 |             foreach (var kvp in postconditions) state[kvp.Key] = kvp.Value;
262 |             foreach (var kvp in arithmeticPostconditions) {
263 |                 if (!state.ContainsKey(kvp.Key)) continue;
264 |                 if (state[kvp.Key] is int stateInt && kvp.Value is int conditionInt) state[kvp.Key] = stateInt + conditionInt;
265 |                 else if (state[kvp.Key] is float stateFloat && kvp.Value is float conditionFloat) state[kvp.Key] = stateFloat + conditionFloat;
266 |                 else if (state[kvp.Key] is double stateDouble && kvp.Value is double conditionDouble) state[kvp.Key] = stateDouble + conditionDouble;
267 |                 else if (state[kvp.Key] is long stateLong && kvp.Value is long conditionLong) state[kvp.Key] = stateLong + conditionLong;
268 |                 else if (state[kvp.Key] is decimal stateDecimal && kvp.Value is decimal conditionDecimal) state[kvp.Key] = stateDecimal + conditionDecimal;
269 |                 else if (state[kvp.Key] is DateTime stateDateTime && kvp.Value is TimeSpan conditionTimeSpan) state[kvp.Key] = stateDateTime + conditionTimeSpan;
270 |             }
271 |             foreach (var kvp in parameterPostconditions) {
272 |                 if (!parameters.ContainsKey(kvp.Key)) continue;
273 |                 state[kvp.Value] = parameters[kvp.Key];
274 |             }
275 |             stateMutator?.Invoke(this, state);
276 |         }
277 |
278 |         /// <summary>
279 |         /// Sets all parameters to the action.
280 |         /// </summary>
281 |         /// <param name="parameters">Dictionary of parameters to be passed to the action.</param>
282 |         internal void SetParameters(Dictionary<string, object?> parameters) {
283 |             this.parameters = parameters;
284 |         }
285 |
286 |         private static bool IndicesAtMaximum(List<int> indices, List<int> counts) {
287 |             for (int i = 0; i < indices.Count; i++) if (indices[i] < counts[i] - 1) return false;
288 |             return true;
289 |         }
290 |
291 |         private static void IncrementIndices(List<int> indices, List<int> counts) {
292 |             if (IndicesAtMaximum(indices, counts)) return;
293 |             for (int i = 0; i < indices.Count; i++) {
294 |                 if (indices[i] == counts[i] - 1) indices[i] = 0;
295 |                 else {
296 |                     indices[i]++;
297 |                     return;
298 |                 }
299 |             }
300 |         }
301 |
302 |         /// <summary>
303 |         /// Default executor callback to be used if no callback is passed in.
304 |         /// </summary>
305 |         /// <param name="agent">Agent executing the action.</param>
306 |         /// <param name="action">Action to be executed.</param>
307 |         /// <returns>A Failed status, since the action cannot execute without a callback.</returns>
308 |         private static ExecutionStatus DefaultExecutorCallback(Agent agent, Action action) {
309 |             return ExecutionStatus.Failed;
310 |         }
311 |
312 | #pragma warning disable S1172 // Unused method parameters should be removed
313 |         private static float DefaultCostCallback(Action action, ConcurrentDictionary<string, object?> currentState) {
314 |             return action.cost;
315 |         }
316 | #pragma warning restore S1172 // Unused method parameters should be removed
317 |     }
318 | }

--------------------------------------------------------------------------------

/MountainGoap/Agent.cs
--------------------------------------------------------------------------------

  1 | ﻿// <copyright file="Agent.cs" company="Chris Muller">
  2 | // Copyright (c) Chris Muller. All rights reserved.
  3 | // </copyright>
  4 |
  5 | namespace MountainGoap {
  6 |     using System;
  7 |     using System.Collections.Concurrent;
  8 |     using System.Collections.Generic;
  9 |     using System.Threading;
 10 |
 11 |     /// <summary>
 12 |     /// GOAP agent.
 13 |     /// </summary>
 14 |     public class Agent {
 15 |         /// <summary>
 16 |         /// Name of the agent.
 17 |         /// </summary>
 18 |         public readonly string Name;
 19 |
 20 |         /// <summary>
 21 |         /// Initializes a new instance of the <see cref="Agent"/> class.
 22 |         /// </summary>
 23 |         /// <param name="name">Name of the agent.</param>
 24 |         /// <param name="state">Initial agent state.</param>
 25 |         /// <param name="memory">Initial agent memory.</param>
 26 |         /// <param name="goals">Initial agent goals.</param>
 27 |         /// <param name="actions">Actions available to the agent.</param>
 28 |         /// <param name="sensors">Sensors available to the agent.</param>
 29 |         /// <param name="costMaximum">Maximum cost of an allowable plan.</param>
 30 |         /// <param name="stepMaximum">Maximum steps in an allowable plan.</param>
 31 |         public Agent(string? name = null, ConcurrentDictionary<string, object?>? state = null, Dictionary<string, object?>? memory = null, List<BaseGoal>? goals = null, List<Action>? actions = null, List<Sensor>? sensors = null, float costMaximum = float.MaxValue, int stepMaximum = int.MaxValue) {
 32 |             Name = name ??
quot;Agent {Guid.NewGuid()}";
 33 |             if (state != null) State = state;
 34 |             if (memory != null) Memory = memory;
 35 |             if (goals != null) Goals = goals;
 36 |             if (actions != null) Actions = actions;
 37 |             if (sensors != null) Sensors = sensors;
 38 |             CostMaximum = costMaximum;
 39 |             StepMaximum = stepMaximum;
 40 |         }
 41 |
 42 |         /// <summary>
 43 |         /// Event that fires when the agent executes a step of work.
 44 |         /// </summary>
 45 |         public static event AgentStepEvent OnAgentStep = (agent) => { };
 46 |
 47 |         /// <summary>
 48 |         /// Event that fires when an action sequence completes.
 49 |         /// </summary>
 50 |         public static event AgentActionSequenceCompletedEvent OnAgentActionSequenceCompleted = (agent) => { };
 51 |
 52 |         /// <summary>
 53 |         /// Event that fires when planning begins.
 54 |         /// </summary>
 55 |         public static event PlanningStartedEvent OnPlanningStarted = (agent) => { };
 56 |
 57 |         /// <summary>
 58 |         /// Event that fires when planning for a single goal starts.
 59 |         /// </summary>
 60 |         public static event PlanningStartedForSingleGoalEvent OnPlanningStartedForSingleGoal = (agent, goal) => { };
 61 |
 62 |         /// <summary>
 63 |         /// Event that fires when planning for a single goal finishes.
 64 |         /// </summary>
 65 |         public static event PlanningFinishedForSingleGoalEvent OnPlanningFinishedForSingleGoal = (agent, goal, utility) => { };
 66 |
 67 |         /// <summary>
 68 |         /// Event that fires when planning finishes.
 69 |         /// </summary>
 70 |         public static event PlanningFinishedEvent OnPlanningFinished = (agent, goal, utility) => { };
 71 |
 72 |         /// <summary>
 73 |         /// Event that fires when a new plan is finalized for the agent.
 74 |         /// </summary>
 75 |         public static event PlanUpdatedEvent OnPlanUpdated = (agent, actionList) => { };
 76 |
 77 |         /// <summary>
 78 |         /// Event that fires when the pathfinder evaluates a single node in the action graph.
 79 |         /// </summary>
 80 |         public static event EvaluatedActionNodeEvent OnEvaluatedActionNode = (node, nodes) => { };
 81 |
 82 |         /// <summary>
 83 |         /// Gets the chains of actions currently being performed by the agent.
 84 |         /// </summary>
 85 |         public List<List<Action>> CurrentActionSequences { get; } = new();
 86 |
 87 |         /// <summary>
 88 |         /// Gets or sets the current world state from the agent perspective.
 89 |         /// </summary>
 90 |         public ConcurrentDictionary<string, object?> State { get; set; } = new();
 91 |
 92 |         /// <summary>
 93 |         /// Gets or sets the memory storage object for the agent.
 94 |         /// </summary>
 95 |         public Dictionary<string, object?> Memory { get; set; } = new();
 96 |
 97 |         /// <summary>
 98 |         /// Gets or sets the list of active goals for the agent.
 99 |         /// </summary>
100 |         public List<BaseGoal> Goals { get; set; } = new();
101 |
102 |         /// <summary>
103 |         /// Gets or sets the actions available to the agent.
104 |         /// </summary>
105 |         public List<Action> Actions { get; set; } = new();
106 |
107 |         /// <summary>
108 |         /// Gets or sets the sensors available to the agent.
109 |         /// </summary>
110 |         public List<Sensor> Sensors { get; set; } = new();
111 |
112 |         /// <summary>
113 |         /// Gets or sets the plan cost maximum for the agent.
114 |         /// </summary>
115 |         public float CostMaximum { get; set; }
116 |
117 |         /// <summary>
118 |         /// Gets or sets the step maximum for the agent.
119 |         /// </summary>
120 |         public int StepMaximum { get; set; }
121 |
122 |         /// <summary>
123 |         /// Gets or sets a value indicating whether the agent is currently executing one or more actions.
124 |         /// </summary>
125 |         public bool IsBusy { get; set; } = false;
126 |
127 |         /// <summary>
128 |         /// Gets or sets a value indicating whether the agent is currently planning.
129 |         /// </summary>
130 |         public bool IsPlanning { get; set; } = false;
131 |
132 |         /// <summary>
133 |         /// You should call this every time your game state updates.
134 |         /// </summary>
135 |         /// <param name="mode">Mode to be used for executing the step of work.</param>
136 |         public void Step(StepMode mode = StepMode.Default) {
137 |             OnAgentStep(this);
138 |             foreach (var sensor in Sensors) sensor.Run(this);
139 |             if (mode == StepMode.Default) {
140 |                 StepAsync();
141 |                 return;
142 |             }
143 |             if (!IsBusy) Planner.Plan(this, CostMaximum, StepMaximum);
144 |             if (mode == StepMode.OneAction) Execute();
145 |             else if (mode == StepMode.AllActions) while (IsBusy) Execute();
146 |         }
147 |
148 |         /// <summary>
149 |         /// Clears the current action sequences (also known as plans).
150 |         /// </summary>
151 |         public void ClearPlan() {
152 |             CurrentActionSequences.Clear();
153 |         }
154 |
155 |         /// <summary>
156 |         /// Makes a plan.
157 |         /// </summary>
158 |         public void Plan() {
159 |             if (!IsBusy && !IsPlanning) {
160 |                 IsPlanning = true;
161 |                 Planner.Plan(this, CostMaximum, StepMaximum);
162 |             }
163 |         }
164 |
165 |         /// <summary>
166 |         /// Makes a plan asynchronously.
167 |         /// </summary>
168 |         public void PlanAsync() {
169 |             if (!IsBusy && !IsPlanning) {
170 |                 IsPlanning = true;
171 |                 var t = new Thread(new ThreadStart(() => { Planner.Plan(this, CostMaximum, StepMaximum); }));
172 |                 t.Start();
173 |             }
174 |         }
175 |
176 |         /// <summary>
177 |         /// Executes the current plan.
178 |         /// </summary>
179 |         public void ExecutePlan() {
180 |             if (!IsPlanning) Execute();
181 |         }
182 |
183 |         /// <summary>
184 |         /// Triggers OnPlanningStarted event.
185 |         /// </summary>
186 |         /// <param name="agent">Agent that started planning.</param>
187 |         internal static void TriggerOnPlanningStarted(Agent agent) {
188 |             OnPlanningStarted(agent);
189 |         }
190 |
191 |         /// <summary>
192 |         /// Triggers OnPlanningStartedForSingleGoal event.
193 |         /// </summary>
194 |         /// <param name="agent">Agent that started planning.</param>
195 |         /// <param name="goal">Goal for which planning was started.</param>
196 |         internal static void TriggerOnPlanningStartedForSingleGoal(Agent agent, BaseGoal goal) {
197 |             OnPlanningStartedForSingleGoal(agent, goal);
198 |         }
199 |
200 |         /// <summary>
201 |         /// Triggers OnPlanningFinishedForSingleGoal event.
202 |         /// </summary>
203 |         /// <param name="agent">Agent that finished planning.</param>
204 |         /// <param name="goal">Goal for which planning was completed.</param>
205 |         /// <param name="utility">Utility of the plan.</param>
206 |         internal static void TriggerOnPlanningFinishedForSingleGoal(Agent agent, BaseGoal goal, float utility) {
207 |             OnPlanningFinishedForSingleGoal(agent, goal, utility);
208 |         }
209 |
210 |         /// <summary>
211 |         /// Triggers OnPlanningFinished event.
212 |         /// </summary>
213 |         /// <param name="agent">Agent that finished planning.</param>
214 |         /// <param name="goal">Goal that was selected.</param>
215 |         /// <param name="utility">Utility of the plan.</param>
216 |         internal static void TriggerOnPlanningFinished(Agent agent, BaseGoal? goal, float utility) {
217 |             OnPlanningFinished(agent, goal, utility);
218 |         }
219 |
220 |         /// <summary>
221 |         /// Triggers OnPlanUpdated event.
222 |         /// </summary>
223 |         /// <param name="agent">Agent for which the plan was updated.</param>
224 |         /// <param name="actionList">New action list for the agent.</param>
225 |         internal static void TriggerOnPlanUpdated(Agent agent, List<Action> actionList) {
226 |             OnPlanUpdated(agent, actionList);
227 |         }
228 |
229 |         /// <summary>
230 |         /// Triggers OnEvaluatedActionNode event.
231 |         /// </summary>
232 |         /// <param name="node">Action node being evaluated.</param>
233 |         /// <param name="nodes">List of nodes in the path that led to this point.</param>
234 |         internal static void TriggerOnEvaluatedActionNode(ActionNode node, ConcurrentDictionary<ActionNode, ActionNode> nodes) {
235 |             OnEvaluatedActionNode(node, nodes);
236 |         }
237 |
238 |         /// <summary>
239 |         /// Executes an asynchronous step of agent work.
240 |         /// </summary>
241 |         private void StepAsync() {
242 |             if (!IsBusy && !IsPlanning) {
243 |                 IsPlanning = true;
244 |                 var t = new Thread(new ThreadStart(() => { Planner.Plan(this, CostMaximum, StepMaximum); }));
245 |                 t.Start();
246 |             }
247 |             else if (!IsPlanning) Execute();
248 |         }
249 |
250 |         /// <summary>
251 |         /// Executes the current action sequences.
252 |         /// </summary>
253 |         private void Execute() {
254 |             if (CurrentActionSequences.Count > 0) {
255 |                 List<List<Action>> cullableSequences = new();
256 |                 foreach (var sequence in CurrentActionSequences) {
257 |                     if (sequence.Count > 0) {
258 |                         var executionStatus = sequence[0].Execute(this);
259 |                         if (executionStatus != ExecutionStatus.Executing) sequence.RemoveAt(0);
260 |                     }
261 |                     else cullableSequences.Add(sequence);
262 |                 }
263 |                 foreach (var sequence in cullableSequences) {
264 |                     CurrentActionSequences.Remove(sequence);
265 |                     OnAgentActionSequenceCompleted(this);
266 |                 }
267 |             }
268 |             else IsBusy = false;
269 |         }
270 |     }
271 | }
272 |

--------------------------------------------------------------------------------

/MountainGoap/BaseGoal.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="BaseGoal.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System;
 7 |
 8 |     /// <summary>
 9 |     /// Represents an abstract class for a goal to be achieved for an agent.
10 |     /// </summary>
11 |     public abstract class BaseGoal {
12 |         /// <summary>
13 |         /// Name of the goal.
14 |         /// </summary>
15 |         public readonly string Name;
16 |
17 |         /// <summary>
18 |         /// Weight to give the goal.
19 |         /// </summary>
20 |         internal readonly float Weight;
21 |
22 |         /// <summary>
23 |         /// Initializes a new instance of the <see cref="BaseGoal"/> class.
24 |         /// </summary>
25 |         /// <param name="name">Name of the goal.</param>
26 |         /// <param name="weight">Weight to give the goal.</param>
27 |         protected BaseGoal(string? name = null, float weight = 1f) {
28 |             Name = name ??
quot;Goal {Guid.NewGuid()}";
29 |             Weight = weight;
30 |         }
31 |     }
32 | }
33 |

--------------------------------------------------------------------------------

/MountainGoap/CallbackDelegates/CostCallback.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="CostCallback.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Concurrent;
 7 |
 8 |     /// <summary>
 9 |     /// Delegate type for a callback that defines the cost of an action.
10 |     /// </summary>
11 |     /// <param name="action">Action being executed.</param>
12 |     /// <param name="currentState">State as it will be when cost is relevant.</param>
13 |     /// <returns>Cost of the action.</returns>
14 |     public delegate float CostCallback(Action action, ConcurrentDictionary<string, object?> currentState);
15 | }
16 |

--------------------------------------------------------------------------------

/MountainGoap/CallbackDelegates/ExecutorCallback.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="ExecutorCallback.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Delegate type for a callback that defines a list of all possible parameter states for the given state.
 8 |     /// </summary>
 9 |     /// <param name="agent">Agent executing the action.</param>
10 |     /// <param name="action">Action being executed.</param>
11 |     /// <returns>New execution status of the action.</returns>
12 |     public delegate ExecutionStatus ExecutorCallback(Agent agent, Action action);
13 | }
14 |

--------------------------------------------------------------------------------

/MountainGoap/CallbackDelegates/PermutationSelectorCallback.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="PermutationSelectorCallback.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Concurrent;
 7 |     using System.Collections.Generic;
 8 |
 9 |     /// <summary>
10 |     /// Delegate type for a callback that defines a list of all possible parameter states for the given state.
11 |     /// </summary>
12 |     /// <param name="state">Current world state.</param>
13 |     /// <returns>A list with each parameter set to be tried for the action.</returns>
14 |     public delegate List<object> PermutationSelectorCallback(ConcurrentDictionary<string, object?> state);
15 | }
16 |

--------------------------------------------------------------------------------

/MountainGoap/CallbackDelegates/SensorRunCallback.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="SensorRunCallback.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Delegate type for a callback that runs a sensor during a game loop.
 8 |     /// </summary>
 9 |     /// <param name="agent">Agent using the sensor.</param>
10 |     public delegate void SensorRunCallback(Agent agent);
11 | }
12 |

--------------------------------------------------------------------------------

/MountainGoap/CallbackDelegates/StateCheckerCallback.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="StateCheckerCallback.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Concurrent;
 7 |
 8 |     /// <summary>
 9 |     /// Delegate type for a callback that checks state before action execution or evaluation (the latter during planning).
10 |     /// </summary>
11 |     /// <param name="action">Action being executed or evaluated.</param>
12 |     /// <param name="currentState">State as it will be when the action is executed or evaluated.</param>
13 |     /// <returns>True if the state is okay for executing the action, otherwise false.</returns>
14 |     public delegate bool StateCheckerCallback(Action action, ConcurrentDictionary<string, object?> currentState);
15 | }
16 |

--------------------------------------------------------------------------------

/MountainGoap/CallbackDelegates/StateCostDeltaMultiplierCallback.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="StateMutatorCallback.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Delegate type for a callback that provides multiplier for delta value of the respective key to obtain delta cost to use with ExtremeGoal and ComparativeGoal.
 8 |     /// </summary>
 9 |     /// <param name="action">Action being executed or evaluated.</param>
10 |     /// <param name="stateKey">Key to provide multiplier for</param>
11 |     /// <returns>Multiplier for the delta value to get delta cost</returns>
12 |     public delegate float StateCostDeltaMultiplierCallback(Action? action, string stateKey);
13 | }
14 |

--------------------------------------------------------------------------------

/MountainGoap/CallbackDelegates/StateMutatorCallback.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="StateMutatorCallback.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Concurrent;
 7 |
 8 |     /// <summary>
 9 |     /// Delegate type for a callback that mutates state following action execution or evaluation (the latter during planning).
10 |     /// </summary>
11 |     /// <param name="action">Action being executed or evaluated.</param>
12 |     /// <param name="currentState">State as it will be when the action is executed or evaluated.</param>
13 |     public delegate void StateMutatorCallback(Action action, ConcurrentDictionary<string, object?> currentState);
14 | }
15 |

--------------------------------------------------------------------------------

/MountainGoap/ComparativeGoal.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="ComparativeGoal.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Generic;
 7 |
 8 |     /// <summary>
 9 |     /// Represents a goal to be achieved for an agent.
10 |     /// </summary>
11 |     public class ComparativeGoal : BaseGoal {
12 |         /// <summary>
13 |         /// Desired state for the comparative goal.
14 |         /// </summary>
15 |         internal readonly Dictionary<string, ComparisonValuePair> DesiredState;
16 |
17 |         /// <summary>
18 |         /// Initializes a new instance of the <see cref="ComparativeGoal"/> class.
19 |         /// </summary>
20 |         /// <param name="name">Name of the goal.</param>
21 |         /// <param name="weight">Weight to give the goal.</param>
22 |         /// <param name="desiredState">Desired state for the comparative goal.</param>
23 |         public ComparativeGoal(string? name = null, float weight = 1f, Dictionary<string, ComparisonValuePair>? desiredState = null)
24 |             : base(name, weight) {
25 |             DesiredState = desiredState ?? new();
26 |         }
27 |     }
28 | }
29 |

--------------------------------------------------------------------------------

/MountainGoap/ComparisonOperator.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="ComparisonOperator.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// List of operators that can be used for comparison.
 8 |     /// </summary>
 9 |     public enum ComparisonOperator {
10 |         /// <summary>
11 |         /// Undefined comparison operator (will not do anything).
12 |         /// </summary>
13 |         Undefined = 0,
14 |
15 |         /// <summary>
16 |         /// Equality (==) operator.
17 |         /// </summary>
18 |         Equals = 1,
19 |
20 |         /// <summary>
21 |         /// Less than (&lt;) operator.
22 |         /// </summary>
23 |         LessThan = 2,
24 |
25 |         /// <summary>
26 |         /// Less than or equals (&lt;=) operator.
27 |         /// </summary>
28 |         LessThanOrEquals = 3,
29 |
30 |         /// <summary>
31 |         /// Greater than (>) operator).
32 |         /// </summary>
33 |         GreaterThan = 4,
34 |
35 |         /// <summary>
36 |         /// Greater than or equals (>=) operator.
37 |         /// </summary>
38 |         GreaterThanOrEquals = 5
39 |     }
40 | }

--------------------------------------------------------------------------------

/MountainGoap/ComparisonValuePair.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="ComparisonValuePair.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// List of operators that can be used for comparison.
 8 |     /// </summary>
 9 |     public class ComparisonValuePair {
10 |         /// <summary>
11 |         /// Gets or sets the value to be compared against.
12 |         /// </summary>
13 |         public object? Value { get; set; } = null;
14 |
15 |         /// <summary>
16 |         /// Gets or sets the operator to be used for comparison.
17 |         /// </summary>
18 |         public ComparisonOperator Operator { get; set; } = ComparisonOperator.Undefined;
19 |     }
20 | }

--------------------------------------------------------------------------------

/MountainGoap/Events/AgentActionSequenceCompletedEvent.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="AgentActionSequenceCompletedEvent.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Delegate type for a listener to the event that fires when an agent completes an action sequence.
 8 |     /// </summary>
 9 |     /// <param name="agent">Agent executing the action sequence.</param>
10 |     public delegate void AgentActionSequenceCompletedEvent(Agent agent);
11 | }
12 |

--------------------------------------------------------------------------------

/MountainGoap/Events/AgentStepEvent.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="AgentStepEvent.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Delegate type for a listener to the event that fires when an agent executes a step of work.
 8 |     /// </summary>
 9 |     /// <param name="agent">Agent executing the step of work.</param>
10 |     public delegate void AgentStepEvent(Agent agent);
11 | }
12 |

--------------------------------------------------------------------------------

/MountainGoap/Events/BeginExecuteActionEvent.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="BeginExecuteActionEvent.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Generic;
 7 |
 8 |     /// <summary>
 9 |     /// Delegate type for a listener to the event that fires when an action begins executing.
10 |     /// </summary>
11 |     /// <param name="agent">Agent executing the action.</param>
12 |     /// <param name="action">Action being executed.</param>
13 |     /// <param name="parameters">Parameters to the action being executed.</param>
14 |     public delegate void BeginExecuteActionEvent(Agent agent, Action action, Dictionary<string, object?> parameters);
15 | }
16 |

--------------------------------------------------------------------------------

/MountainGoap/Events/EvaluatedActionNodeEvent.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="EvaluatedActionNodeEvent.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Concurrent;
 7 |
 8 |     /// <summary>
 9 |     /// Delegate type for a listener to the event that fires when an agent is evaluating a path for a potential action plan.
10 |     /// </summary>
11 |     /// <param name="node">Node being evaluated.</param>
12 |     /// <param name="nodes">All nodes in the plan being evaluated.</param>
13 |     public delegate void EvaluatedActionNodeEvent(ActionNode node, ConcurrentDictionary<ActionNode, ActionNode> nodes);
14 | }
15 |

--------------------------------------------------------------------------------

/MountainGoap/Events/FinishExecuteActionEvent.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="FinishExecuteActionEvent.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Generic;
 7 |
 8 |     /// <summary>
 9 |     /// Delegate type for a listener to the event that fires when an action finishes executing.
10 |     /// </summary>
11 |     /// <param name="agent">Agent executing the action.</param>
12 |     /// <param name="action">Action being executed.</param>
13 |     /// <param name="status">Execution status of the action.</param>
14 |     /// <param name="parameters">Parameters to the action being executed.</param>
15 |     public delegate void FinishExecuteActionEvent(Agent agent, Action action, ExecutionStatus status, Dictionary<string, object?> parameters);
16 | }
17 |

--------------------------------------------------------------------------------

/MountainGoap/Events/PlanUpdatedEvent.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="PlanUpdatedEvent.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Delegate type for a listener to the event that fires when an agent has a new plan.
 8 |     /// </summary>
 9 |     /// <param name="agent">Agent executing the step of work.</param>
10 |     /// <param name="plan">Plan determined to be optimal for the agent.</param>
11 |     public delegate void PlanUpdatedEvent(Agent agent, List<Action> plan);
12 | }
13 |

--------------------------------------------------------------------------------

/MountainGoap/Events/PlanningFinishedEvent.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="PlanningFinishedEvent.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Delegate type for a listener to the event that fires when an agent finishes planning.
 8 |     /// </summary>
 9 |     /// <param name="agent">Agent doing the planning.</param>
10 |     /// /// <param name="goal">Goal selected, or null if no valid plan was selected.</param>
11 |     /// <param name="utility">Calculated utility of the plan.</param>
12 |     public delegate void PlanningFinishedEvent(Agent agent, BaseGoal? goal, float utility);
13 | }
14 |

--------------------------------------------------------------------------------

/MountainGoap/Events/PlanningFinishedForSingleGoalEvent.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="PlanningFinishedForSingleGoalEvent.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Delegate type for a listener to the event that fires when an agent finishes planning for a single goal.
 8 |     /// </summary>
 9 |     /// <param name="agent">Agent doing the planning.</param>
10 |     /// <param name="goal">Goal for which planning was finished.</param>
11 |     /// <param name="utility">Calculated utility of the plan.</param>
12 |     public delegate void PlanningFinishedForSingleGoalEvent(Agent agent, BaseGoal goal, float utility);
13 | }
14 |

--------------------------------------------------------------------------------

/MountainGoap/Events/PlanningStartedEvent.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="PlanningStartedEvent.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Delegate type for a listener to the event that fires when an agent begins planning.
 8 |     /// </summary>
 9 |     /// <param name="agent">Agent doing the planning.</param>
10 |     public delegate void PlanningStartedEvent(Agent agent);
11 | }
12 |

--------------------------------------------------------------------------------

/MountainGoap/Events/PlanningStartedForSingleGoalEvent.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="PlanningStartedForSingleGoalEvent.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Delegate type for a listener to the event that fires when an agent starts planning for a single goal.
 8 |     /// </summary>
 9 |     /// <param name="agent">Agent doing the planning.</param>
10 |     /// <param name="goal">Goal for which planning was started.</param>
11 |     public delegate void PlanningStartedForSingleGoalEvent(Agent agent, BaseGoal goal);
12 | }
13 |

--------------------------------------------------------------------------------

/MountainGoap/Events/SensorRunningEvent.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="SensorRunningEvent.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Delegate type for a listener to the event that fires when an agent sensor is about to run.
 8 |     /// </summary>
 9 |     /// <param name="agent">Agent running the sensor.</param>
10 |     /// <param name="sensor">Sensor that is about to run.</param>
11 |     public delegate void SensorRunEvent(Agent agent, Sensor sensor);
12 | }
13 |

--------------------------------------------------------------------------------

/MountainGoap/ExecutionStatus.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="ExecutionStatus.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Possible execution status for an action.
 8 |     /// </summary>
 9 |     public enum ExecutionStatus {
10 |         /// <summary>
11 |         /// Indicates that the action is not currently executing.
12 |         /// </summary>
13 |         NotYetExecuted = 1,
14 |
15 |         /// <summary>
16 |         /// Indicates that the action is currently executing.
17 |         /// </summary>
18 |         Executing = 2,
19 |
20 |         /// <summary>
21 |         /// Indicates that the action has succeeded.
22 |         /// </summary>
23 |         Succeeded = 3,
24 |
25 |         /// <summary>
26 |         /// Indicates that the action has failed.
27 |         /// </summary>
28 |         Failed = 4,
29 |
30 |         /// <summary>
31 |         /// Indicates that the action is not possible due to preconditions.
32 |         /// </summary>
33 |         NotPossible = 5
34 |     }
35 | }
36 |

--------------------------------------------------------------------------------

/MountainGoap/ExtremeGoal.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="ExtremeGoal.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Generic;
 7 |
 8 |     /// <summary>
 9 |     /// Represents a goal requiring an extreme value to be achieved for an agent.
10 |     /// </summary>
11 |     public class ExtremeGoal : BaseGoal {
12 |         /// <summary>
13 |         /// Dictionary of states to be maximized or minimized. A value of true indicates to maximize the goal, a value of false indicates to minimize it.
14 |         /// </summary>
15 |         internal readonly Dictionary<string, bool> DesiredState;
16 |
17 |         /// <summary>
18 |         /// Initializes a new instance of the <see cref="ExtremeGoal"/> class.
19 |         /// </summary>
20 |         /// <param name="name">Name of the goal.</param>
21 |         /// <param name="weight">Weight to give the goal.</param>
22 |         /// <param name="desiredState">States to be maximized or minimized.</param>
23 |         public ExtremeGoal(string? name = null, float weight = 1f, Dictionary<string, bool>? desiredState = null)
24 |             : base(name, weight) {
25 |             DesiredState = desiredState ?? new();
26 |         }
27 |     }
28 | }
29 |

--------------------------------------------------------------------------------

/MountainGoap/Goal.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="Goal.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Generic;
 7 |
 8 |     /// <summary>
 9 |     /// Represents a goal to be achieved for an agent.
10 |     /// </summary>
11 |     public class Goal : BaseGoal {
12 |         /// <summary>
13 |         /// Desired world state to be achieved.
14 |         /// </summary>
15 |         internal readonly Dictionary<string, object?> DesiredState;
16 |
17 |         /// <summary>
18 |         /// Initializes a new instance of the <see cref="Goal"/> class.
19 |         /// </summary>
20 |         /// <param name="name">Name of the goal.</param>
21 |         /// <param name="weight">Weight to give the goal.</param>
22 |         /// <param name="desiredState">Desired end state of the goal.</param>
23 |         public Goal(string? name = null, float weight = 1f, Dictionary<string, object?>? desiredState = null)
24 |             : base(name, weight) {
25 |             DesiredState = desiredState ?? new();
26 |         }
27 |     }
28 | }
29 |

--------------------------------------------------------------------------------

/MountainGoap/Internals/ActionAStar.cs
--------------------------------------------------------------------------------

  1 | ﻿// <copyright file="ActionAStar.cs" company="Chris Muller">
  2 | // Copyright (c) Chris Muller. All rights reserved.
  3 | // </copyright>
  4 |
  5 | namespace MountainGoap {
  6 |     using System;
  7 |     using System.Collections.Concurrent;
  8 |     using Priority_Queue;
  9 |
 10 |     /// <summary>
 11 |     /// AStar calculator for an action graph.
 12 |     /// </summary>
 13 |     internal class ActionAStar {
 14 |         /// <summary>
 15 |         /// Final point at which the calculation arrived.
 16 |         /// </summary>
 17 |         internal readonly ActionNode? FinalPoint = null;
 18 |
 19 |         /// <summary>
 20 |         /// Cost so far to get to each node.
 21 |         /// </summary>
 22 |         internal readonly ConcurrentDictionary<ActionNode, float> CostSoFar = new();
 23 |
 24 |         /// <summary>
 25 |         /// Steps so far to get to each node.
 26 |         /// </summary>
 27 |         internal readonly ConcurrentDictionary<ActionNode, int> StepsSoFar = new();
 28 |
 29 |         /// <summary>
 30 |         /// Dictionary giving the path from start to goal.
 31 |         /// </summary>
 32 |         internal readonly ConcurrentDictionary<ActionNode, ActionNode> CameFrom = new();
 33 |
 34 |         /// <summary>
 35 |         /// Goal state that AStar is trying to achieve.
 36 |         /// </summary>
 37 |         private readonly BaseGoal goal;
 38 |
 39 |         /// <summary>
 40 |         /// Initializes a new instance of the <see cref="ActionAStar"/> class.
 41 |         /// </summary>
 42 |         /// <param name="graph">Graph to be traversed.</param>
 43 |         /// <param name="start">Action from which to start.</param>
 44 |         /// <param name="goal">Goal state to be achieved.</param>
 45 |         /// <param name="costMaximum">Maximum allowable cost for a plan.</param>
 46 |         /// <param name="stepMaximum">Maximum allowable steps for a plan.</param>
 47 |         internal ActionAStar(ActionGraph graph, ActionNode start, BaseGoal goal, float costMaximum, int stepMaximum) {
 48 |             this.goal = goal;
 49 |             FastPriorityQueue<ActionNode> frontier = new(100000);
 50 |             frontier.Enqueue(start, 0);
 51 |             CameFrom[start] = start;
 52 |             CostSoFar[start] = 0;
 53 |             StepsSoFar[start] = 0;
 54 |             while (frontier.Count > 0) {
 55 |                 var current = frontier.Dequeue();
 56 |                 if (MeetsGoal(current, start)) {
 57 |                     FinalPoint = current;
 58 |                     break;
 59 |                 }
 60 |                 foreach (var next in graph.Neighbors(current)) {
 61 |                     float newCost = CostSoFar[current] + next.Cost(current.State);
 62 |                     int newStepCount = StepsSoFar[current] + 1;
 63 |                     if (newCost > costMaximum || newStepCount > stepMaximum) continue;
 64 |                     if (!CostSoFar.ContainsKey(next) || newCost < CostSoFar[next]) {
 65 |                         CostSoFar[next] = newCost;
 66 |                         StepsSoFar[next] = newStepCount;
 67 |                         float priority = newCost + Heuristic(next, goal, current);
 68 |                         frontier.Enqueue(next, priority);
 69 |                         CameFrom[next] = current;
 70 |                         Agent.TriggerOnEvaluatedActionNode(next, CameFrom);
 71 |                     }
 72 |                 }
 73 |             }
 74 |         }
 75 |
 76 |         private static float Heuristic(ActionNode actionNode, BaseGoal goal, ActionNode current) {
 77 |             var cost = 0f;
 78 |             if (goal is Goal normalGoal) {
 79 |                 normalGoal.DesiredState.Select(kvp => kvp.Key).ToList().ForEach(key => {
 80 |                     if (!actionNode.State.ContainsKey(key)) cost++;
 81 |                     else if (actionNode.State[key] == null && actionNode.State[key] != normalGoal.DesiredState[key]) cost++;
 82 |                     else if (actionNode.State[key] is object obj && !obj.Equals(normalGoal.DesiredState[key])) cost++;
 83 |                 });
 84 |             }
 85 |             else if (goal is ExtremeGoal extremeGoal) {
 86 |                 foreach (var kvp in extremeGoal.DesiredState) {
 87 |                     var valueDiff = 0f;
 88 |                     var valueDiffMultiplier = (actionNode?.Action?.StateCostDeltaMultiplier ?? Action.DefaultStateCostDeltaMultiplier).Invoke(actionNode?.Action, kvp.Key);
 89 |                     if (actionNode.State.ContainsKey(kvp.Key) && actionNode.State[kvp.Key] == null) {
 90 |                         cost += float.PositiveInfinity;
 91 |                         continue;
 92 |                     }
 93 |                     if (actionNode.State.ContainsKey(kvp.Key) && extremeGoal.DesiredState.ContainsKey(kvp.Key)) valueDiff = Convert.ToSingle(actionNode.State[kvp.Key]) - Convert.ToSingle(current.State[kvp.Key]);
 94 |                     if (!actionNode.State.ContainsKey(kvp.Key)) cost += float.PositiveInfinity;
 95 |                     else if (!current.State.ContainsKey(kvp.Key)) cost += float.PositiveInfinity;
 96 |                     else if (!kvp.Value && actionNode.State[kvp.Key] is object a && current.State[kvp.Key] is object b && IsLowerThanOrEquals(a, b)) cost += valueDiff *valueDiffMultiplier;
 97 |                     else if (kvp.Value && actionNode.State[kvp.Key] is object a2 && current.State[kvp.Key] is object b2 && IsHigherThanOrEquals(a2, b2)) cost -= valueDiff* valueDiffMultiplier;
 98 |                 }
 99 |             }
100 |             else if (goal is ComparativeGoal comparativeGoal) {
101 |                 foreach (var kvp in comparativeGoal.DesiredState) {
102 |                     var valueDiff2 = 0f;
103 |                     var valueDiffMultiplier = (actionNode?.Action?.StateCostDeltaMultiplier ?? Action.DefaultStateCostDeltaMultiplier).Invoke(actionNode?.Action, kvp.Key);
104 |                     if (actionNode.State.ContainsKey(kvp.Key) && comparativeGoal.DesiredState.ContainsKey(kvp.Key)) valueDiff2 = Math.Abs(Convert.ToSingle(actionNode.State[kvp.Key]) - Convert.ToSingle(current.State[kvp.Key]));
105 |                     if (!actionNode.State.ContainsKey(kvp.Key)) cost += float.PositiveInfinity;
106 |                     else if (!current.State.ContainsKey(kvp.Key)) cost += float.PositiveInfinity;
107 |                     else if (kvp.Value.Operator == ComparisonOperator.Undefined) cost += float.PositiveInfinity;
108 |                     else if (kvp.Value.Operator == ComparisonOperator.Equals && actionNode.State[kvp.Key] is object obj && !obj.Equals(comparativeGoal.DesiredState[kvp.Key].Value)) cost += valueDiff2 *valueDiffMultiplier;
109 |                     else if (kvp.Value.Operator == ComparisonOperator.LessThan && actionNode.State[kvp.Key] is object a && comparativeGoal.DesiredState[kvp.Key].Value is object b && !IsLowerThan(a, b)) cost += valueDiff2* valueDiffMultiplier;
110 |                     else if (kvp.Value.Operator == ComparisonOperator.GreaterThan && actionNode.State[kvp.Key] is object a2 && comparativeGoal.DesiredState[kvp.Key].Value is object b2 && !IsHigherThan(a2, b2)) cost += valueDiff2 *valueDiffMultiplier;
111 |                     else if (kvp.Value.Operator == ComparisonOperator.LessThanOrEquals && actionNode.State[kvp.Key] is object a3 && comparativeGoal.DesiredState[kvp.Key].Value is object b3 && !IsLowerThanOrEquals(a3, b3)) cost += valueDiff2* valueDiffMultiplier;
112 |                     else if (kvp.Value.Operator == ComparisonOperator.GreaterThanOrEquals && actionNode.State[kvp.Key] is object a4 && comparativeGoal.DesiredState[kvp.Key].Value is object b4 && !IsHigherThanOrEquals(a4, b4)) cost += valueDiff2 * valueDiffMultiplier;
113 |                 }
114 |             }
115 |             return cost;
116 |         }
117 |
118 |         private static bool IsLowerThan(object a, object b) {
119 |             return Utils.IsLowerThan(a, b);
120 |         }
121 |
122 |         private static bool IsHigherThan(object a, object b) {
123 |             return Utils.IsHigherThan(a, b);
124 |         }
125 |
126 |         private static bool IsLowerThanOrEquals(object a, object b) {
127 |             return Utils.IsLowerThanOrEquals(a, b);
128 |         }
129 |
130 |         private static bool IsHigherThanOrEquals(object a, object b) {
131 |             return Utils.IsHigherThanOrEquals(a, b);
132 |         }
133 |
134 |         private bool MeetsGoal(ActionNode actionNode, ActionNode current) {
135 |             return Utils.MeetsGoal(goal, actionNode, current);
136 |         }
137 |     }
138 | }
139 |

--------------------------------------------------------------------------------

/MountainGoap/Internals/ActionGraph.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="ActionGraph.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Concurrent;
 7 |     using System.Collections.Generic;
 8 |
 9 |     /// <summary>
10 |     /// Represents a traversable action graph.
11 |     /// </summary>
12 |     internal class ActionGraph {
13 |         /// <summary>
14 |         /// The set of actions for the graph.
15 |         /// </summary>
16 |         internal List<ActionNode> ActionNodes = new();
17 |
18 |         /// <summary>
19 |         /// Initializes a new instance of the <see cref="ActionGraph"/> class.
20 |         /// </summary>
21 |         /// <param name="actions">List of actions to include in the graph.</param>
22 |         /// <param name="state">Initial state to be used.</param>
23 |         internal ActionGraph(List<Action> actions, ConcurrentDictionary<string, object?> state) {
24 |             foreach (var action in actions) {
25 |                 var permutations = action.GetPermutations(state);
26 |                 foreach (var permutation in permutations) ActionNodes.Add(new(action, state, permutation));
27 |             }
28 |         }
29 |
30 |         /// <summary>
31 |         /// Gets the list of neighbors for a node.
32 |         /// </summary>
33 |         /// <param name="node">Node for which to retrieve neighbors.</param>
34 |         /// <returns>The set of action/state combinations that can be executed after the current action/state combination.</returns>
35 |         internal IEnumerable<ActionNode> Neighbors(ActionNode node) {
36 |             foreach (var otherNode in ActionNodes) {
37 |                 if (otherNode.Action is not null && otherNode.Action.IsPossible(node.State)) {
38 |                     var newNode = new ActionNode(otherNode.Action.Copy(), node.State.Copy(), otherNode.Parameters.Copy());
39 |                     newNode.Action?.ApplyEffects(newNode.State);
40 |                     yield return newNode;
41 |                 }
42 |             }
43 |         }
44 |     }
45 | }

--------------------------------------------------------------------------------

/MountainGoap/Internals/ActionNode.cs
--------------------------------------------------------------------------------

  1 | ﻿// <copyright file="ActionNode.cs" company="Chris Muller">
  2 | // Copyright (c) Chris Muller. All rights reserved.
  3 | // </copyright>
  4 |
  5 | namespace MountainGoap {
  6 |     using System.Collections.Concurrent;
  7 |     using System.Collections.Generic;
  8 |     using Priority_Queue;
  9 |
 10 |     /// <summary>
 11 |     /// Represents an action node in an action graph.
 12 |     /// </summary>
 13 |     public class ActionNode : FastPriorityQueueNode {
 14 |         /// <summary>
 15 |         /// Initializes a new instance of the <see cref="ActionNode"/> class.
 16 |         /// </summary>
 17 |         /// <param name="action">Action to be assigned to the node.</param>
 18 |         /// <param name="state">State to be assigned to the node.</param>
 19 |         /// <param name="parameters">Paramters to be passed to the action in the node.</param>
 20 |         internal ActionNode(Action? action, ConcurrentDictionary<string, object?> state, Dictionary<string, object?> parameters) {
 21 |             if (action != null) Action = action.Copy();
 22 |             State = state.Copy();
 23 |             Parameters = parameters.Copy();
 24 |             Action?.SetParameters(Parameters);
 25 |         }
 26 |
 27 |         /// <summary>
 28 |         /// Gets or sets the state of the world for this action node.
 29 |         /// </summary>
 30 |         public ConcurrentDictionary<string, object?> State { get; set; }
 31 |
 32 |         /// <summary>
 33 |         /// Gets or sets parameters to be passed to the action.
 34 |         /// </summary>
 35 |         public Dictionary<string, object?> Parameters { get; set; }
 36 |
 37 |         /// <summary>
 38 |         /// Gets or sets the action to be executed when the world is in the defined <see cref="State"/>.
 39 |         /// </summary>
 40 |         public Action? Action { get; set; }
 41 |
 42 | #pragma warning disable S3875 // "operator==" should not be overloaded on reference types
 43 |         /// <summary>
 44 |         /// Overrides the equality operator on ActionNodes.
 45 |         /// </summary>
 46 |         /// <param name="node1">First node to be compared.</param>
 47 |         /// <param name="node2">Second node to be compared.</param>
 48 |         /// <returns>True if equal, otherwise false.</returns>
 49 |         public static bool operator ==(ActionNode? node1, ActionNode? node2) {
 50 |             if (node1 is null) return node2 is null;
 51 |             if (node2 is null) return node1 is null;
 52 |             if (node1.Action == null || node2.Action == null) return (node1.Action == node2.Action) && node1.StateMatches(node2);
 53 |             return node1.Action.Equals(node2.Action) && node1.StateMatches(node2);
 54 |         }
 55 | #pragma warning restore S3875 // "operator==" should not be overloaded on reference types
 56 |
 57 |         /// <summary>
 58 |         /// Overrides the inequality operator on ActionNodes.
 59 |         /// </summary>
 60 |         /// <param name="node1">First node to be compared.</param>
 61 |         /// <param name="node2">Second node to be compared.</param>
 62 |         /// <returns>True if unequal, otherwise false.</returns>
 63 |         public static bool operator !=(ActionNode? node1, ActionNode? node2) {
 64 |             if (node1 is null) return node2 is not null;
 65 |             if (node2 is null) return node1 is not null;
 66 |             if (node1.Action is not null) return !node1.Action.Equals(node2.Action) || !node1.StateMatches(node2);
 67 |             return node2.Action is null;
 68 |         }
 69 |
 70 |         /// <inheritdoc/>
 71 |         public override bool Equals(object? obj) {
 72 |             if (obj is not ActionNode item) return false;
 73 |             return this == item;
 74 |         }
 75 |
 76 |         /// <inheritdoc/>
 77 |         public override int GetHashCode() {
 78 |             var hashCode = 629302477;
 79 |             if (Action != null) hashCode = (hashCode *-1521134295) + EqualityComparer<Action>.Default.GetHashCode(Action);
 80 |             else hashCode*= -1521134295;
 81 |             hashCode = (hashCode * -1521134295) + EqualityComparer<ConcurrentDictionary<string, object?>>.Default.GetHashCode(State);
 82 |             return hashCode;
 83 |         }
 84 |
 85 |         /// <summary>
 86 |         /// Cost to traverse this node.
 87 |         /// </summary>
 88 |         /// <param name="currentState">Current state after previous node is executed.</param>
 89 |         /// <returns>The cost of the action to be executed.</returns>
 90 |         internal float Cost(ConcurrentDictionary<string, object?> currentState) {
 91 |             if (Action == null) return float.MaxValue;
 92 |             return Action.GetCost(currentState);
 93 |         }
 94 |
 95 |         private bool StateMatches(ActionNode otherNode) {
 96 |             foreach (var kvp in State) {
 97 |                 if (!otherNode.State.ContainsKey(kvp.Key)) return false;
 98 |                 if (otherNode.State[kvp.Key] == null && otherNode.State[kvp.Key] != kvp.Value) return false;
 99 |                 if (otherNode.State[kvp.Key] == null && otherNode.State[kvp.Key] == kvp.Value) continue;
100 |                 if (otherNode.State[kvp.Key] is object obj && !obj.Equals(kvp.Value)) return false;
101 |             }
102 |             foreach (var kvp in otherNode.State) {
103 |                 if (!State.ContainsKey(kvp.Key)) return false;
104 |                 if (State[kvp.Key] == null && State[kvp.Key] != kvp.Value) return false;
105 |                 if (State[kvp.Key] == null && State[kvp.Key] == kvp.Value) continue;
106 |                 if (otherNode.State[kvp.Key] is object obj && !obj.Equals(kvp.Value)) return false;
107 |             }
108 |             return true;
109 |         }
110 |     }
111 | }

--------------------------------------------------------------------------------

/MountainGoap/Internals/DictionaryExtensionMethods.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="DictionaryExtensionMethods.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Concurrent;
 7 |     using System.Collections.Generic;
 8 |     using System.Linq;
 9 |
10 |     /// <summary>
11 |     /// Extension method to copy a dictionary of strings and objects.
12 |     /// </summary>
13 |     public static class DictionaryExtensionMethods {
14 |         /// <summary>
15 |         /// Add functionality for ConcurrentDictionary.
16 |         /// </summary>
17 |         /// <param name="dictionary">Dictionary to which to add an item.</param>
18 |         /// <param name="key">Key to add.</param>
19 |         /// <param name="value">Value to add.</param>
20 |         public static void Add(this ConcurrentDictionary<string, object?> dictionary, string key, object? value) {
21 |             dictionary.TryAdd(key, value);
22 |         }
23 |
24 |         /// <summary>
25 |         /// Copies the dictionary to a shallow clone.
26 |         /// </summary>
27 |         /// <param name="dictionary">Dictionary to be copied.</param>
28 |         /// <returns>A shallow copy of the dictionary.</returns>
29 |         internal static Dictionary<string, object?> Copy(this Dictionary<string, object?> dictionary) {
30 |             return dictionary.ToDictionary(entry => entry.Key, entry => entry.Value);
31 |         }
32 |
33 |         /// <summary>
34 |         /// Copies the concurrent dictionary to a shallow clone.
35 |         /// </summary>
36 |         /// <param name="dictionary">Dictionary to be copied.</param>
37 |         /// <returns>A shallow copy of the dictionary.</returns>
38 |         internal static ConcurrentDictionary<string, object?> Copy(this ConcurrentDictionary<string, object?> dictionary) {
39 |             return new ConcurrentDictionary<string, object?>(dictionary);
40 |         }
41 |
42 |         /// <summary>
43 |         /// Copies the dictionary to a shallow clone.
44 |         /// </summary>
45 |         /// <param name="dictionary">Dictionary to be copied.</param>
46 |         /// <returns>A shallow copy of the dictionary.</returns>
47 |         internal static Dictionary<string, ComparisonValuePair> Copy(this Dictionary<string, ComparisonValuePair> dictionary) {
48 |             return dictionary.ToDictionary(entry => entry.Key, entry => entry.Value);
49 |         }
50 |
51 |         /// <summary>
52 |         /// Copies the dictionary to a shallow clone.
53 |         /// </summary>
54 |         /// <param name="dictionary">Dictionary to be copied.</param>
55 |         /// <returns>A shallow copy of the dictionary.</returns>
56 |         internal static Dictionary<string, string> Copy(this Dictionary<string, string> dictionary) {
57 |             return dictionary.ToDictionary(entry => entry.Key, entry => entry.Value);
58 |         }
59 |
60 |         /// <summary>
61 |         /// Copies the dictionary to a shallow clone.
62 |         /// </summary>
63 |         /// <param name="dictionary">Dictionary to be copied.</param>
64 |         /// <returns>A shallow copy of the dictionary.</returns>
65 |         internal static Dictionary<string, object> CopyNonNullable(this Dictionary<string, object> dictionary) {
66 |             return dictionary.ToDictionary(entry => entry.Key, entry => entry.Value);
67 |         }
68 |     }
69 | }

--------------------------------------------------------------------------------

/MountainGoap/Internals/Planner.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="Planner.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System.Collections.Generic;
 7 |
 8 |     /// <summary>
 9 |     /// Planner for an agent.
10 |     /// </summary>
11 |     internal static class Planner {
12 |         /// <summary>
13 |         /// Makes a plan to achieve the agent's goals.
14 |         /// </summary>
15 |         /// <param name="agent">Agent using the planner.</param>
16 |         /// <param name="costMaximum">Maximum allowable cost for a plan.</param>
17 |         /// <param name="stepMaximum">Maximum allowable steps for a plan.</param>
18 |         internal static void Plan(Agent agent, float costMaximum, int stepMaximum) {
19 |             Agent.TriggerOnPlanningStarted(agent);
20 |             float bestPlanUtility = 0;
21 |             ActionAStar? astar;
22 |             ActionNode? cursor;
23 |             ActionAStar? bestAstar = null;
24 |             BaseGoal? bestGoal = null;
25 |             foreach (var goal in agent.Goals) {
26 |                 Agent.TriggerOnPlanningStartedForSingleGoal(agent, goal);
27 |                 ActionGraph graph = new(agent.Actions, agent.State);
28 |                 ActionNode start = new(null, agent.State, new());
29 |                 astar = new(graph, start, goal, costMaximum, stepMaximum);
30 |                 cursor = astar.FinalPoint;
31 |                 if (cursor is not null && astar.CostSoFar[cursor] == 0) Agent.TriggerOnPlanningFinishedForSingleGoal(agent, goal, 0);
32 |                 else if (cursor is not null) Agent.TriggerOnPlanningFinishedForSingleGoal(agent, goal, goal.Weight / astar.CostSoFar[cursor]);
33 |                 if (cursor is not null && cursor.Action is not null && astar.CostSoFar.ContainsKey(cursor) && goal.Weight / astar.CostSoFar[cursor] > bestPlanUtility) {
34 |                     bestPlanUtility = goal.Weight / astar.CostSoFar[cursor];
35 |                     bestAstar = astar;
36 |                     bestGoal = goal;
37 |                 }
38 |             }
39 |             if (bestPlanUtility > 0 && bestAstar is not null && bestGoal is not null && bestAstar.FinalPoint is not null) {
40 |                 UpdateAgentActionList(bestAstar.FinalPoint, bestAstar, agent);
41 |                 agent.IsBusy = true;
42 |                 Agent.TriggerOnPlanningFinished(agent, bestGoal, bestPlanUtility);
43 |             }
44 |             else Agent.TriggerOnPlanningFinished(agent, null, 0);
45 |             agent.IsPlanning = false;
46 |         }
47 |
48 |         /// <summary>
49 |         /// Updates the agent action list with the new plan. Only supports executing one sequence of events at a time for now.
50 |         /// </summary>
51 |         /// <param name="start">Starting node.</param>
52 |         /// <param name="astar">AStar object used to calculate plan.</param>
53 |         /// <param name="agent">Agent that will implement the plan.</param>
54 |         private static void UpdateAgentActionList(ActionNode start, ActionAStar astar, Agent agent) {
55 |             ActionNode? cursor = start;
56 |             List<Action> actionList = new();
57 |             while (cursor != null && cursor.Action != null && astar.CameFrom.ContainsKey(cursor)) {
58 |                 actionList.Add(cursor.Action);
59 |                 cursor = astar.CameFrom[cursor];
60 |             }
61 |             actionList.Reverse();
62 |             agent.CurrentActionSequences.Add(actionList);
63 |             Agent.TriggerOnPlanUpdated(agent, actionList);
64 |         }
65 |     }
66 | }

--------------------------------------------------------------------------------

/MountainGoap/Internals/Utils.cs
--------------------------------------------------------------------------------

  1 | ﻿// <copyright file="Utils.cs" company="Chris Muller">
  2 | // Copyright (c) Chris Muller. All rights reserved.
  3 | // </copyright>
  4 |
  5 | namespace MountainGoap {
  6 |     /// <summary>
  7 |     /// Utilities for the MountainGoap library.
  8 |     /// </summary>
  9 |     internal static class Utils {
 10 |         /// <summary>
 11 |         /// Indicates whether a is lower than b.
 12 |         /// </summary>
 13 |         /// <param name="a">First element to be compared.</param>
 14 |         /// <param name="b">Second element to be compared.</param>
 15 |         /// <returns>True if lower, false otherwise.</returns>
 16 |         internal static bool IsLowerThan(object a, object b) {
 17 |             if (a == null || b == null) return false;
 18 |             if (a is int intA && b is int intB) return intA < intB;
 19 |             if (a is long longA && b is long longB) return longA < longB;
 20 |             if (a is float floatA && b is float floatB) return floatA < floatB;
 21 |             if (a is double doubleA && b is double doubleB) return doubleA < doubleB;
 22 |             if (a is decimal decimalA && b is decimal decimalB) return decimalA < decimalB;
 23 |             if (a is DateTime dateTimeA && b is DateTime dateTimeB) return dateTimeA < dateTimeB;
 24 |             return false;
 25 |         }
 26 |
 27 |         /// <summary>
 28 |         /// Indicates whether a is higher than b.
 29 |         /// </summary>
 30 |         /// <param name="a">First element to be compared.</param>
 31 |         /// <param name="b">Second element to be compared.</param>
 32 |         /// <returns>True if higher, false otherwise.</returns>
 33 |         internal static bool IsHigherThan(object a, object b) {
 34 |             if (a == null || b == null) return false;
 35 |             if (a is int intA && b is int intB) return intA > intB;
 36 |             if (a is long longA && b is long longB) return longA > longB;
 37 |             if (a is float floatA && b is float floatB) return floatA > floatB;
 38 |             if (a is double doubleA && b is double doubleB) return doubleA > doubleB;
 39 |             if (a is decimal decimalA && b is decimal decimalB) return decimalA > decimalB;
 40 |             if (a is DateTime dateTimeA && b is DateTime dateTimeB) return dateTimeA > dateTimeB;
 41 |             return false;
 42 |         }
 43 |
 44 |         /// <summary>
 45 |         /// Indicates whether a is lower than or equal to b.
 46 |         /// </summary>
 47 |         /// <param name="a">First element to be compared.</param>
 48 |         /// <param name="b">Second element to be compared.</param>
 49 |         /// <returns>True if lower or equal, false otherwise.</returns>
 50 |         internal static bool IsLowerThanOrEquals(object a, object b) {
 51 |             if (a == null || b == null) return false;
 52 |             if (a is int intA && b is int intB) return intA <= intB;
 53 |             if (a is long longA && b is long longB) return longA <= longB;
 54 |             if (a is float floatA && b is float floatB) return floatA <= floatB;
 55 |             if (a is double doubleA && b is double doubleB) return doubleA <= doubleB;
 56 |             if (a is decimal decimalA && b is decimal decimalB) return decimalA <= decimalB;
 57 |             if (a is DateTime dateTimeA && b is DateTime dateTimeB) return dateTimeA <= dateTimeB;
 58 |             return false;
 59 |         }
 60 |
 61 |         /// <summary>
 62 |         /// Indicates whether a is higher than or equal to b.
 63 |         /// </summary>
 64 |         /// <param name="a">First element to be compared.</param>
 65 |         /// <param name="b">Second element to be compared.</param>
 66 |         /// <returns>True if higher or equal, false otherwise.</returns>
 67 |         internal static bool IsHigherThanOrEquals(object a, object b) {
 68 |             if (a == null || b == null) return false;
 69 |             if (a is int intA && b is int intB) return intA >= intB;
 70 |             if (a is long longA && b is long longB) return longA >= longB;
 71 |             if (a is float floatA && b is float floatB) return floatA >= floatB;
 72 |             if (a is double doubleA && b is double doubleB) return doubleA >= doubleB;
 73 |             if (a is decimal decimalA && b is decimal decimalB) return decimalA >= decimalB;
 74 |             if (a is DateTime dateTimeA && b is DateTime dateTimeB) return dateTimeA >= dateTimeB;
 75 |             return false;
 76 |         }
 77 |
 78 |         /// <summary>
 79 |         /// Indicates whether or not a goal is met by an action node.
 80 |         /// </summary>
 81 |         /// <param name="goal">Goal to be met.</param>
 82 |         /// <param name="actionNode">Action node being tested.</param>
 83 |         /// <param name="current">Prior node in the action chain.</param>
 84 |         /// <returns>True if the goal is met, otherwise false.</returns>
 85 |         internal static bool MeetsGoal(BaseGoal goal, ActionNode actionNode, ActionNode current) {
 86 |             if (goal is Goal normalGoal) {
 87 | #pragma warning disable S3267 // Loops should be simplified with "LINQ" expressions
 88 |                 foreach (var kvp in normalGoal.DesiredState) {
 89 |                     if (!actionNode.State.ContainsKey(kvp.Key)) return false;
 90 |                     else if (actionNode.State[kvp.Key] == null && actionNode.State[kvp.Key] != normalGoal.DesiredState[kvp.Key]) return false;
 91 |                     else if (actionNode.State[kvp.Key] is object obj && obj != null && !obj.Equals(normalGoal.DesiredState[kvp.Key])) return false;
 92 |                 }
 93 | #pragma warning restore S3267 // Loops should be simplified with "LINQ" expressions
 94 |             }
 95 |             else if (goal is ExtremeGoal extremeGoal) {
 96 |                 if (actionNode.Action == null) return false;
 97 |                 foreach (var kvp in extremeGoal.DesiredState) {
 98 |                     if (!actionNode.State.ContainsKey(kvp.Key)) return false;
 99 |                     else if (!current.State.ContainsKey(kvp.Key)) return false;
100 |                     else if (kvp.Value && actionNode.State[kvp.Key] is object a && current.State[kvp.Key] is object b && IsLowerThanOrEquals(a, b)) return false;
101 |                     else if (!kvp.Value && actionNode.State[kvp.Key] is object a2 && current.State[kvp.Key] is object b2 && IsHigherThanOrEquals(a2, b2)) return false;
102 |                 }
103 |             }
104 |             else if (goal is ComparativeGoal comparativeGoal) {
105 |                 if (actionNode.Action == null) return false;
106 |                 foreach (var kvp in comparativeGoal.DesiredState) {
107 |                     if (!actionNode.State.ContainsKey(kvp.Key)) return false;
108 |                     else if (!current.State.ContainsKey(kvp.Key)) return false;
109 |                     else if (kvp.Value.Operator == ComparisonOperator.Undefined) return false;
110 |                     else if (kvp.Value.Operator == ComparisonOperator.Equals && actionNode.State[kvp.Key] is object obj && !obj.Equals(comparativeGoal.DesiredState[kvp.Key].Value)) return false;
111 |                     else if (kvp.Value.Operator == ComparisonOperator.LessThan && actionNode.State[kvp.Key] is object a && comparativeGoal.DesiredState[kvp.Key].Value is object b && !IsLowerThan(a, b)) return false;
112 |                     else if (kvp.Value.Operator == ComparisonOperator.GreaterThan && actionNode.State[kvp.Key] is object a2 && comparativeGoal.DesiredState[kvp.Key].Value is object b2 && !IsHigherThan(a2, b2)) return false;
113 |                     else if (kvp.Value.Operator == ComparisonOperator.LessThanOrEquals && actionNode.State[kvp.Key] is object a3 && comparativeGoal.DesiredState[kvp.Key].Value is object b3 && !IsLowerThanOrEquals(a3, b3)) return false;
114 |                     else if (kvp.Value.Operator == ComparisonOperator.GreaterThanOrEquals && actionNode.State[kvp.Key] is object a4 && comparativeGoal.DesiredState[kvp.Key].Value is object b4 && !IsHigherThanOrEquals(a4, b4)) return false;
115 |                 }
116 |             }
117 |             return true;
118 |         }
119 |     }
120 | }
121 |

--------------------------------------------------------------------------------

/MountainGoap/MountainGoap.csproj
--------------------------------------------------------------------------------

 1 | ﻿<Project Sdk="Microsoft.NET.Sdk">
 2 |
 3 |   <PropertyGroup>
 4 |     <TargetFramework>netstandard2.1</TargetFramework>
 5 |  <LangVersion>10.0</LangVersion>
 6 |     <ImplicitUsings>enable</ImplicitUsings>
 7 |     <Nullable>enable</Nullable>
 8 |     <GenerateDocumentationFile>True</GenerateDocumentationFile>
 9 |  <VersionPrefix>1.1.1</VersionPrefix>
10 |  <GeneratePackageOnBuild>True</GeneratePackageOnBuild>
11 |  <Description>A simple GOAP (Goal Oriented Action Planning) library.</Description>
12 |  <Copyright>MIT licensed 2022</Copyright>
13 |  <PackageProjectUrl>https://github.com/caesuric/mountain-goap</PackageProjectUrl>
14 |  <PackageIcon>logo.png</PackageIcon>
15 |  <PackageReadmeFile>README.md</PackageReadmeFile>
16 |  <RepositoryUrl>https://github.com/caesuric/mountain-goap</RepositoryUrl>
17 |  <PackageTags>goap;ai;games;simulation;sim;gamedev</PackageTags>
18 |  <PackageReleaseNotes>Initial release.</PackageReleaseNotes>
19 |  <PackageLicenseExpression>MIT</PackageLicenseExpression>
20 |  <GenerateAssemblyInfo>false</GenerateAssemblyInfo>
21 |   </PropertyGroup>
22 |
23 |   <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|AnyCPU'">
24 |     <NoWarn>1701;1702;SA1500;SA1401;SA1501;SA1503;SA1101;SA1513;SA1520;SA1413;SA0001;SA1000;SA1127</NoWarn>
25 |   </PropertyGroup>
26 |
27 |   <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|AnyCPU'">
28 |     <NoWarn>1701;1702;SA1500;SA1401;SA1501;SA1503;SA1101;SA1513;SA1520;SA1413;SA0001;SA1000;SA1127</NoWarn>
29 |   </PropertyGroup>
30 |
31 |   <ItemGroup>
32 |     <None Remove="stylecop.json" />
33 |   </ItemGroup>
34 |
35 |   <ItemGroup>
36 |     <AdditionalFiles Include="stylecop.json" />
37 |   </ItemGroup>
38 |
39 |   <ItemGroup>
40 |     <None Include="..\logo.png">
41 |       <Pack>True</Pack>
42 |       <PackagePath>\</PackagePath>
43 |     </None>
44 |     <None Include="..\README.md">
45 |       <Pack>True</Pack>
46 |       <PackagePath>\</PackagePath>
47 |     </None>
48 |   </ItemGroup>
49 |
50 |   <ItemGroup>
51 |     <PackageReference Include="StyleCop.Analyzers" Version="1.1.118">
52 |       <PrivateAssets>all</PrivateAssets>
53 |       <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
54 |     </PackageReference>
55 |   </ItemGroup>
56 |
57 | </Project>
58 |

--------------------------------------------------------------------------------

/MountainGoap/PermutationSelectorGenerators.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="PermutationSelectorGenerators.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | #pragma warning disable S3267 // Loops should be simplified with "LINQ" expressions
 6 | namespace MountainGoap {
 7 |     using System.Collections.Concurrent;
 8 |     using System.Collections.Generic;
 9 |
10 |     /// <summary>
11 |     /// Generators for default permutation selectors for convenience.
12 |     /// </summary>
13 |     public static class PermutationSelectorGenerators {
14 |         /// <summary>
15 |         /// Generates a permutation selector that returns all elements of an enumerable.
16 |         /// </summary>
17 |         /// <typeparam name="T">Type of the <see cref="IEnumerable{T}"/>.</typeparam>
18 |         /// <param name="values">Set of values to be included in permutations.</param>
19 |         /// <returns>A lambda function that returns all elements from the collection passed in.</returns>
20 |         public static PermutationSelectorCallback SelectFromCollection<T>(IEnumerable<T> values) {
21 |             return (ConcurrentDictionary<string, object?> state) => {
22 |                 List<object> output = new();
23 |                 foreach (var item in values) if (item is not null) output.Add(item);
24 |                 return output;
25 |             };
26 |         }
27 |
28 |         /// <summary>
29 |         /// Generates a permutation selector that returns all elements of an enumerable within the agent state.
30 |         /// </summary>
31 |         /// <typeparam name="T">Type of the <see cref="IEnumerable{T}"/>.</typeparam>
32 |         /// <param name="key">Key of the state to check for the collection.</param>
33 |         /// <returns>A lambda function that returns all elements from the collection in the state.</returns>
34 |         public static PermutationSelectorCallback SelectFromCollectionInState<T>(string key) {
35 |             return (ConcurrentDictionary<string, object?> state) => {
36 |                 List<object> output = new();
37 |                 if (state[key] is not IEnumerable<T> values) return output;
38 |                 foreach (var item in values) if (item is not null) output.Add(item);
39 |                 return output;
40 |             };
41 |         }
42 |
43 |         /// <summary>
44 |         /// Generates a permutation selector that returns all integer elements in a range.
45 |         /// </summary>
46 |         /// <param name="lowerBound">Lower bound from which to start.</param>
47 |         /// <param name="upperBound">Upper bound, non-inclusive.</param>
48 |         /// <returns>A lambda function that returns all elements in the range given.</returns>
49 |         public static PermutationSelectorCallback SelectFromIntegerRange(int lowerBound, int upperBound) {
50 |             return (ConcurrentDictionary<string, object?> state) => {
51 |                 List<object> output = new();
52 |                 for (int i = lowerBound; i < upperBound; i++) output.Add(i);
53 |                 return output;
54 |             };
55 |         }
56 |     }
57 | }
58 | #pragma warning restore S3267 // Loops should be simplified with "LINQ" expressions

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/FastPriorityQueue.cs
--------------------------------------------------------------------------------

  1 | ﻿#pragma warning disable
  2 | using System;
  3 | using System.Collections;
  4 | using System.Collections.Generic;
  5 | using System.Runtime.CompilerServices;
  6 |
  7 | namespace Priority_Queue
  8 | {
  9 |     /// <summary>
 10 |     /// An implementation of a min-Priority Queue using a heap.  Has O(1) .Contains()!
 11 |     /// See https://github.com/BlueRaja/High-Speed-Priority-Queue-for-C-Sharp/wiki/Getting-Started for more information
 12 |     /// </summary>
 13 |     /// <typeparam name="T">The values in the queue.  Must extend the FastPriorityQueueNode class</typeparam>
 14 |     public sealed class FastPriorityQueue<T> : IFixedSizePriorityQueue<T, float>
 15 |         where T : FastPriorityQueueNode
 16 |     {
 17 |         private int_numNodes;
 18 |         private T[] _nodes;
 19 |
 20 |         /// <summary>
 21 |         /// Instantiate a new Priority Queue
 22 |         /// </summary>
 23 |         /// <param name="maxNodes">The max nodes ever allowed to be enqueued (going over this will cause undefined behavior)</param>
 24 |         public FastPriorityQueue(int maxNodes)
 25 |         {
 26 | #if DEBUG
 27 |             if (maxNodes <= 0)
 28 |             {
 29 |                 throw new InvalidOperationException("New queue size cannot be smaller than 1");
 30 |             }
 31 | #endif
 32 |
 33 |_numNodes = 0;
 34 |             _nodes = new T[maxNodes + 1];
 35 |         }
 36 |
 37 |         /// <summary>
 38 |         /// Returns the number of nodes in the queue.
 39 |         /// O(1)
 40 |         /// </summary>
 41 |         public int Count
 42 |         {
 43 |             get
 44 |             {
 45 |                 return_numNodes;
 46 |             }
 47 |         }
 48 |
 49 |         /// <summary>
 50 |         /// Returns the maximum number of items that can be enqueued at once in this queue.  Once you hit this number (ie. once Count == MaxSize),
 51 |         /// attempting to enqueue another item will cause undefined behavior.  O(1)
 52 |         /// </summary>
 53 |         public int MaxSize
 54 |         {
 55 |             get
 56 |             {
 57 |                 return _nodes.Length - 1;
 58 |             }
 59 |         }
 60 |
 61 |         /// <summary>
 62 |         /// Removes every node from the queue.
 63 |         /// O(n) (So, don't do this often!)
 64 |         /// </summary>
 65 | #if NET_VERSION_4_5
 66 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
 67 | #endif
 68 |         public void Clear()
 69 |         {
 70 |             Array.Clear(_nodes, 1,_numNodes);
 71 |             _numNodes = 0;
 72 |         }
 73 |
 74 |         /// <summary>
 75 |         /// Returns (in O(1)!) whether the given node is in the queue.
 76 |         /// If node is or has been previously added to another queue, the result is undefined unless oldQueue.ResetNode(node) has been called
 77 |         /// O(1)
 78 |         /// </summary>
 79 | #if NET_VERSION_4_5
 80 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
 81 | #endif
 82 |         public bool Contains(T node)
 83 |         {
 84 | #if DEBUG
 85 |             if(node == null)
 86 |             {
 87 |                 throw new ArgumentNullException("node");
 88 |             }
 89 |             if (node.Queue != null && !Equals(node.Queue))
 90 |             {
 91 |                 throw new InvalidOperationException("node.Contains was called on a node from another queue.  Please call originalQueue.ResetNode() first");
 92 |             }
 93 |             if(node.QueueIndex < 0 || node.QueueIndex >= _nodes.Length)
 94 |             {
 95 |                 throw new InvalidOperationException("node.QueueIndex has been corrupted. Did you change it manually? Or add this node to another queue?");
 96 |             }
 97 | #endif
 98 |
 99 |             return (_nodes[node.QueueIndex] == node);
100 |         }
101 |
102 |         /// <summary>
103 |         /// Enqueue a node to the priority queue.  Lower values are placed in front. Ties are broken arbitrarily.
104 |         /// If the queue is full, the result is undefined.
105 |         /// If the node is already enqueued, the result is undefined.
106 |         /// If node is or has been previously added to another queue, the result is undefined unless oldQueue.ResetNode(node) has been called
107 |         /// O(log n)
108 |         /// </summary>
109 | #if NET_VERSION_4_5
110 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
111 | #endif
112 |         public void Enqueue(T node, float priority)
113 |         {
114 | #if DEBUG
115 |             if(node == null)
116 |             {
117 |                 throw new ArgumentNullException("node");
118 |             }
119 |             if(_numNodes >= _nodes.Length - 1)
120 |             {
121 |                 throw new InvalidOperationException("Queue is full - node cannot be added: " + node);
122 |             }
123 |             if (node.Queue != null && !Equals(node.Queue))
124 |             {
125 |                 throw new InvalidOperationException("node.Enqueue was called on a node from another queue.  Please call originalQueue.ResetNode() first");
126 |             }
127 |             if (Contains(node))
128 |             {
129 |                 throw new InvalidOperationException("Node is already enqueued: " + node);
130 |             }
131 |             node.Queue = this;
132 | #endif
133 |
134 |             node.Priority = priority;
135 |_numNodes++;
136 |             _nodes[_numNodes] = node;
137 |             node.QueueIndex = _numNodes;
138 |             CascadeUp(node);
139 |         }
140 |
141 | #if NET_VERSION_4_5
142 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
143 | #endif
144 |         private void CascadeUp(T node)
145 |         {
146 |             //aka Heapify-up
147 |             int parent;
148 |             if(node.QueueIndex > 1)
149 |             {
150 |                 parent = node.QueueIndex >> 1;
151 |                 T parentNode = _nodes[parent];
152 |                 if(HasHigherOrEqualPriority(parentNode, node))
153 |                     return;
154 |
155 |                 //Node has lower priority value, so move parent down the heap to make room
156 |_nodes[node.QueueIndex] = parentNode;
157 |                 parentNode.QueueIndex = node.QueueIndex;
158 |
159 |                 node.QueueIndex = parent;
160 |             }
161 |             else
162 |             {
163 |                 return;
164 |             }
165 |             while(parent > 1)
166 |             {
167 |                 parent >>= 1;
168 |                 T parentNode = _nodes[parent];
169 |                 if(HasHigherOrEqualPriority(parentNode, node))
170 |                     break;
171 |
172 |                 //Node has lower priority value, so move parent down the heap to make room
173 |_nodes[node.QueueIndex] = parentNode;
174 |                 parentNode.QueueIndex = node.QueueIndex;
175 |
176 |                 node.QueueIndex = parent;
177 |             }
178 |             _nodes[node.QueueIndex] = node;
179 |         }
180 |
181 | #if NET_VERSION_4_5
182 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
183 | #endif
184 |         private void CascadeDown(T node)
185 |         {
186 |             //aka Heapify-down
187 |             int finalQueueIndex = node.QueueIndex;
188 |             int childLeftIndex = 2 *finalQueueIndex;
189 |
190 |             // If leaf node, we're done
191 |             if(childLeftIndex > _numNodes)
192 |             {
193 |                 return;
194 |             }
195 |
196 |             // Check if the left-child is higher-priority than the current node
197 |             int childRightIndex = childLeftIndex + 1;
198 |             T childLeft =_nodes[childLeftIndex];
199 |             if(HasHigherPriority(childLeft, node))
200 |             {
201 |                 // Check if there is a right child. If not, swap and finish.
202 |                 if(childRightIndex > _numNodes)
203 |                 {
204 |                     node.QueueIndex = childLeftIndex;
205 |                     childLeft.QueueIndex = finalQueueIndex;
206 |_nodes[finalQueueIndex] = childLeft;
207 |                     _nodes[childLeftIndex] = node;
208 |                     return;
209 |                 }
210 |                 // Check if the left-child is higher-priority than the right-child
211 |                 T childRight =_nodes[childRightIndex];
212 |                 if(HasHigherPriority(childLeft, childRight))
213 |                 {
214 |                     // left is highest, move it up and continue
215 |                     childLeft.QueueIndex = finalQueueIndex;
216 |                     _nodes[finalQueueIndex] = childLeft;
217 |                     finalQueueIndex = childLeftIndex;
218 |                 }
219 |                 else
220 |                 {
221 |                     // right is even higher, move it up and continue
222 |                     childRight.QueueIndex = finalQueueIndex;
223 |_nodes[finalQueueIndex] = childRight;
224 |                     finalQueueIndex = childRightIndex;
225 |                 }
226 |             }
227 |             // Not swapping with left-child, does right-child exist?
228 |             else if(childRightIndex > _numNodes)
229 |             {
230 |                 return;
231 |             }
232 |             else
233 |             {
234 |                 // Check if the right-child is higher-priority than the current node
235 |                 T childRight =_nodes[childRightIndex];
236 |                 if(HasHigherPriority(childRight, node))
237 |                 {
238 |                     childRight.QueueIndex = finalQueueIndex;
239 |                     _nodes[finalQueueIndex] = childRight;
240 |                     finalQueueIndex = childRightIndex;
241 |                 }
242 |                 // Neither child is higher-priority than current, so finish and stop.
243 |                 else
244 |                 {
245 |                     return;
246 |                 }
247 |             }
248 |
249 |             while(true)
250 |             {
251 |                 childLeftIndex = 2* finalQueueIndex;
252 |
253 |                 // If leaf node, we're done
254 |                 if(childLeftIndex >_numNodes)
255 |                 {
256 |                     node.QueueIndex = finalQueueIndex;
257 |                     _nodes[finalQueueIndex] = node;
258 |                     break;
259 |                 }
260 |
261 |                 // Check if the left-child is higher-priority than the current node
262 |                 childRightIndex = childLeftIndex + 1;
263 |                 childLeft =_nodes[childLeftIndex];
264 |                 if(HasHigherPriority(childLeft, node))
265 |                 {
266 |                     // Check if there is a right child. If not, swap and finish.
267 |                     if(childRightIndex > _numNodes)
268 |                     {
269 |                         node.QueueIndex = childLeftIndex;
270 |                         childLeft.QueueIndex = finalQueueIndex;
271 |_nodes[finalQueueIndex] = childLeft;
272 |                         _nodes[childLeftIndex] = node;
273 |                         break;
274 |                     }
275 |                     // Check if the left-child is higher-priority than the right-child
276 |                     T childRight =_nodes[childRightIndex];
277 |                     if(HasHigherPriority(childLeft, childRight))
278 |                     {
279 |                         // left is highest, move it up and continue
280 |                         childLeft.QueueIndex = finalQueueIndex;
281 |                         _nodes[finalQueueIndex] = childLeft;
282 |                         finalQueueIndex = childLeftIndex;
283 |                     }
284 |                     else
285 |                     {
286 |                         // right is even higher, move it up and continue
287 |                         childRight.QueueIndex = finalQueueIndex;
288 |_nodes[finalQueueIndex] = childRight;
289 |                         finalQueueIndex = childRightIndex;
290 |                     }
291 |                 }
292 |                 // Not swapping with left-child, does right-child exist?
293 |                 else if(childRightIndex > _numNodes)
294 |                 {
295 |                     node.QueueIndex = finalQueueIndex;
296 |_nodes[finalQueueIndex] = node;
297 |                     break;
298 |                 }
299 |                 else
300 |                 {
301 |                     // Check if the right-child is higher-priority than the current node
302 |                     T childRight = _nodes[childRightIndex];
303 |                     if(HasHigherPriority(childRight, node))
304 |                     {
305 |                         childRight.QueueIndex = finalQueueIndex;
306 |_nodes[finalQueueIndex] = childRight;
307 |                         finalQueueIndex = childRightIndex;
308 |                     }
309 |                     // Neither child is higher-priority than current, so finish and stop.
310 |                     else
311 |                     {
312 |                         node.QueueIndex = finalQueueIndex;
313 |                         _nodes[finalQueueIndex] = node;
314 |                         break;
315 |                     }
316 |                 }
317 |             }
318 |         }
319 |
320 |         /// <summary>
321 |         /// Returns true if 'higher' has higher priority than 'lower', false otherwise.
322 |         /// Note that calling HasHigherPriority(node, node) (ie. both arguments the same node) will return false
323 |         /// </summary>
324 | #if NET_VERSION_4_5
325 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
326 | #endif
327 |         private bool HasHigherPriority(T higher, T lower)
328 |         {
329 |             return (higher.Priority < lower.Priority);
330 |         }
331 |
332 |         /// <summary>
333 |         /// Returns true if 'higher' has higher priority than 'lower', false otherwise.
334 |         /// Note that calling HasHigherOrEqualPriority(node, node) (ie. both arguments the same node) will return true
335 |         /// </summary>
336 | #if NET_VERSION_4_5
337 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
338 | #endif
339 |         private bool HasHigherOrEqualPriority(T higher, T lower)
340 |         {
341 |             return (higher.Priority <= lower.Priority);
342 |         }
343 |
344 |         /// <summary>
345 |         /// Removes the head of the queue and returns it.
346 |         /// If queue is empty, result is undefined
347 |         /// O(log n)
348 |         /// </summary>
349 | #if NET_VERSION_4_5
350 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
351 | #endif
352 |         public T Dequeue()
353 |         {
354 | #if DEBUG
355 |             if(_numNodes <= 0)
356 |             {
357 |                 throw new InvalidOperationException("Cannot call Dequeue() on an empty queue");
358 |             }
359 |
360 |             if(!IsValidQueue())
361 |             {
362 |                 throw new InvalidOperationException("Queue has been corrupted (Did you update a node priority manually instead of calling UpdatePriority()?" +
363 |                                                     "Or add the same node to two different queues?)");
364 |             }
365 | #endif
366 |
367 |             T returnMe =_nodes[1];
368 |             //If the node is already the last node, we can remove it immediately
369 |             if(_numNodes == 1)
370 |             {
371 |_nodes[1] = null;
372 |                 _numNodes = 0;
373 |                 return returnMe;
374 |             }
375 |
376 |             //Swap the node with the last node
377 |             T formerLastNode =_nodes[_numNodes];
378 |_nodes[1] = formerLastNode;
379 |             formerLastNode.QueueIndex = 1;
380 |             _nodes[_numNodes] = null;
381 |             _numNodes--;
382 |
383 |             //Now bubble formerLastNode (which is no longer the last node) down
384 |             CascadeDown(formerLastNode);
385 |             return returnMe;
386 |         }
387 |
388 |         /// <summary>
389 |         /// Resize the queue so it can accept more nodes.  All currently enqueued nodes are remain.
390 |         /// Attempting to decrease the queue size to a size too small to hold the existing nodes results in undefined behavior
391 |         /// O(n)
392 |         /// </summary>
393 |         public void Resize(int maxNodes)
394 |         {
395 | #if DEBUG
396 |             if (maxNodes <= 0)
397 |             {
398 |                 throw new InvalidOperationException("Queue size cannot be smaller than 1");
399 |             }
400 |
401 |             if (maxNodes <_numNodes)
402 |             {
403 |                 throw new InvalidOperationException("Called Resize(" + maxNodes + "), but current queue contains " + _numNodes + " nodes");
404 |             }
405 | #endif
406 |
407 |             T[] newArray = new T[maxNodes + 1];
408 |             int highestIndexToCopy = Math.Min(maxNodes,_numNodes);
409 |             Array.Copy(_nodes, newArray, highestIndexToCopy + 1);
410 |_nodes = newArray;
411 |         }
412 |
413 |         /// <summary>
414 |         /// Returns the head of the queue, without removing it (use Dequeue() for that).
415 |         /// If the queue is empty, behavior is undefined.
416 |         /// O(1)
417 |         /// </summary>
418 |         public T First
419 |         {
420 |             get
421 |             {
422 | #if DEBUG
423 |                 if(_numNodes <= 0)
424 |                 {
425 |                     throw new InvalidOperationException("Cannot call .First on an empty queue");
426 |                 }
427 | #endif
428 |
429 |                 return_nodes[1];
430 |             }
431 |         }
432 |
433 |         /// <summary>
434 |         /// This method must be called on a node every time its priority changes while it is in the queue.  
435 |         /// <b>Forgetting to call this method will result in a corrupted queue!</b>
436 |         /// Calling this method on a node not in the queue results in undefined behavior
437 |         /// O(log n)
438 |         /// </summary>
439 | #if NET_VERSION_4_5
440 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
441 | #endif
442 |         public void UpdatePriority(T node, float priority)
443 |         {
444 | #if DEBUG
445 |             if(node == null)
446 |             {
447 |                 throw new ArgumentNullException("node");
448 |             }
449 |             if (node.Queue != null && !Equals(node.Queue))
450 |             {
451 |                 throw new InvalidOperationException("node.UpdatePriority was called on a node from another queue");
452 |             }
453 |             if (!Contains(node))
454 |             {
455 |                 throw new InvalidOperationException("Cannot call UpdatePriority() on a node which is not enqueued: " + node);
456 |             }
457 | #endif
458 |
459 |             node.Priority = priority;
460 |             OnNodeUpdated(node);
461 |         }
462 |
463 | #if NET_VERSION_4_5
464 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
465 | #endif
466 |         private void OnNodeUpdated(T node)
467 |         {
468 |             //Bubble the updated node up or down as appropriate
469 |             int parentIndex = node.QueueIndex >> 1;
470 |
471 |             if(parentIndex > 0 && HasHigherPriority(node, _nodes[parentIndex]))
472 |             {
473 |                 CascadeUp(node);
474 |             }
475 |             else
476 |             {
477 |                 //Note that CascadeDown will be called if parentNode == node (that is, node is the root)
478 |                 CascadeDown(node);
479 |             }
480 |         }
481 |
482 |         /// <summary>
483 |         /// Removes a node from the queue.  The node does not need to be the head of the queue.  
484 |         /// If the node is not in the queue, the result is undefined.  If unsure, check Contains() first
485 |         /// O(log n)
486 |         /// </summary>
487 | #if NET_VERSION_4_5
488 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
489 | #endif
490 |         public void Remove(T node)
491 |         {
492 | #if DEBUG
493 |             if(node == null)
494 |             {
495 |                 throw new ArgumentNullException("node");
496 |             }
497 |             if (node.Queue != null && !Equals(node.Queue))
498 |             {
499 |                 throw new InvalidOperationException("node.Remove was called on a node from another queue");
500 |             }
501 |             if (!Contains(node))
502 |             {
503 |                 throw new InvalidOperationException("Cannot call Remove() on a node which is not enqueued: " + node);
504 |             }
505 | #endif
506 |
507 |             //If the node is already the last node, we can remove it immediately
508 |             if(node.QueueIndex == _numNodes)
509 |             {
510 |_nodes[_numNodes] = null;
511 |_numNodes--;
512 |                 return;
513 |             }
514 |
515 |             //Swap the node with the last node
516 |             T formerLastNode = _nodes[_numNodes];
517 |             _nodes[node.QueueIndex] = formerLastNode;
518 |             formerLastNode.QueueIndex = node.QueueIndex;
519 |_nodes[_numNodes] = null;
520 |_numNodes--;
521 |
522 |             //Now bubble formerLastNode (which is no longer the last node) up or down as appropriate
523 |             OnNodeUpdated(formerLastNode);
524 |         }
525 |
526 |         /// <summary>
527 |         /// By default, nodes that have been previously added to one queue cannot be added to another queue.
528 |         /// If you need to do this, please call originalQueue.ResetNode(node) before attempting to add it in the new queue
529 |         /// If the node is currently in the queue or belongs to another queue, the result is undefined
530 |         /// </summary>
531 | #if NET_VERSION_4_5
532 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
533 | #endif
534 |         public void ResetNode(T node)
535 |         {
536 | #if DEBUG
537 |             if (node == null)
538 |             {
539 |                 throw new ArgumentNullException("node");
540 |             }
541 |             if (node.Queue != null && !Equals(node.Queue))
542 |             {
543 |                 throw new InvalidOperationException("node.ResetNode was called on a node from another queue");
544 |             }
545 |             if (Contains(node))
546 |             {
547 |                 throw new InvalidOperationException("node.ResetNode was called on a node that is still in the queue");
548 |             }
549 |
550 |             node.Queue = null;
551 | #endif
552 |
553 |             node.QueueIndex = 0;
554 |         }
555 |
556 |         public IEnumerator<T> GetEnumerator()
557 |         {
558 | #if NET_VERSION_4_5 // ArraySegment does not implement IEnumerable before 4.5
559 |             IEnumerable<T> e = new ArraySegment<T>(_nodes, 1,_numNodes);
560 |             return e.GetEnumerator();
561 | #else
562 |             for(int i = 1; i <= _numNodes; i++)
563 |                 yield return_nodes[i];
564 | #endif
565 |         }
566 |
567 |         IEnumerator IEnumerable.GetEnumerator()
568 |         {
569 |             return GetEnumerator();
570 |         }
571 |
572 |         /// <summary>
573 |         /// <b>Should not be called in production code.</b>
574 |         /// Checks to make sure the queue is still in a valid state.  Used for testing/debugging the queue.
575 |         /// </summary>
576 |         public bool IsValidQueue()
577 |         {
578 |             for(int i = 1; i < _nodes.Length; i++)
579 |             {
580 |                 if(_nodes[i] != null)
581 |                 {
582 |                     int childLeftIndex = 2 * i;
583 |                     if(childLeftIndex < _nodes.Length &&_nodes[childLeftIndex] != null && HasHigherPriority(_nodes[childLeftIndex],_nodes[i]))
584 |                         return false;
585 |
586 |                     int childRightIndex = childLeftIndex + 1;
587 |                     if(childRightIndex < _nodes.Length &&_nodes[childRightIndex] != null && HasHigherPriority(_nodes[childRightIndex],_nodes[i]))
588 |                         return false;
589 |                 }
590 |             }
591 |             return true;
592 |         }
593 |     }
594 | }
595 | #pragma warning restore

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/FastPriorityQueueNode.cs
--------------------------------------------------------------------------------

 1 | ﻿#pragma warning disable
 2 | using System;
 3 |
 4 | namespace Priority_Queue
 5 | {
 6 |     public class FastPriorityQueueNode
 7 |     {
 8 |         /// <summary>
 9 |         /// The Priority to insert this node at.
10 |         /// Cannot be manually edited - see queue.Enqueue() and queue.UpdatePriority() instead
11 |         /// </summary>
12 |         public float Priority { get; protected internal set; }
13 |
14 |         /// <summary>
15 |         /// Represents the current position in the queue
16 |         /// </summary>
17 |         public int QueueIndex { get; internal set; }
18 |
19 | #if DEBUG
20 |         /// <summary>
21 |         /// The queue this node is tied to. Used only for debug builds.
22 |         /// </summary>
23 |         public object Queue { get; internal set; }
24 | #endif
25 |     }
26 | }
27 | #pragma warning restore

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/GenericPriorityQueue.cs
--------------------------------------------------------------------------------

  1 | ﻿#pragma warning disable
  2 | using System;
  3 | using System.Collections;
  4 | using System.Collections.Generic;
  5 | using System.Runtime.CompilerServices;
  6 |
  7 | namespace Priority_Queue
  8 | {
  9 |     /// <summary>
 10 |     /// A copy of StablePriorityQueue which also has generic priority-type
 11 |     /// </summary>
 12 |     /// <typeparam name="TItem">The values in the queue.  Must extend the GenericPriorityQueueNode class</typeparam>
 13 |     /// <typeparam name="TPriority">The priority-type.  Must extend IComparable&lt;TPriority&gt;</typeparam>
 14 |     public sealed class GenericPriorityQueue<TItem, TPriority> : IFixedSizePriorityQueue<TItem, TPriority>
 15 |         where TItem : GenericPriorityQueueNode<TPriority>
 16 |     {
 17 |         private int_numNodes;
 18 |         private TItem[] _nodes;
 19 |         private long_numNodesEverEnqueued;
 20 |         private readonly Comparison<TPriority> _comparer;
 21 |
 22 |         /// <summary>
 23 |         /// Instantiate a new Priority Queue
 24 |         /// </summary>
 25 |         /// <param name="maxNodes">The max nodes ever allowed to be enqueued (going over this will cause undefined behavior)</param>
 26 |         public GenericPriorityQueue(int maxNodes) : this(maxNodes, Comparer<TPriority>.Default) { }
 27 |
 28 |         /// <summary>
 29 |         /// Instantiate a new Priority Queue
 30 |         /// </summary>
 31 |         /// <param name="maxNodes">The max nodes ever allowed to be enqueued (going over this will cause undefined behavior)</param>
 32 |         /// <param name="comparer">The comparer used to compare TPriority values.</param>
 33 |         public GenericPriorityQueue(int maxNodes, IComparer<TPriority> comparer) : this(maxNodes, comparer.Compare) { }
 34 |
 35 |         /// <summary>
 36 |         /// Instantiate a new Priority Queue
 37 |         /// </summary>
 38 |         /// <param name="maxNodes">The max nodes ever allowed to be enqueued (going over this will cause undefined behavior)</param>
 39 |         /// <param name="comparer">The comparison function to use to compare TPriority values</param>
 40 |         public GenericPriorityQueue(int maxNodes, Comparison<TPriority> comparer)
 41 |         {
 42 | #if DEBUG
 43 |             if (maxNodes <= 0)
 44 |             {
 45 |                 throw new InvalidOperationException("New queue size cannot be smaller than 1");
 46 |             }
 47 | #endif
 48 |
 49 |_numNodes = 0;
 50 |             _nodes = new TItem[maxNodes + 1];
 51 |_numNodesEverEnqueued = 0;
 52 |             _comparer = comparer;
 53 |         }
 54 |
 55 |         /// <summary>
 56 |         /// Returns the number of nodes in the queue.
 57 |         /// O(1)
 58 |         /// </summary>
 59 |         public int Count
 60 |         {
 61 |             get
 62 |             {
 63 |                 return_numNodes;
 64 |             }
 65 |         }
 66 |
 67 |         /// <summary>
 68 |         /// Returns the maximum number of items that can be enqueued at once in this queue.  Once you hit this number (ie. once Count == MaxSize),
 69 |         /// attempting to enqueue another item will cause undefined behavior.  O(1)
 70 |         /// </summary>
 71 |         public int MaxSize
 72 |         {
 73 |             get
 74 |             {
 75 |                 return _nodes.Length - 1;
 76 |             }
 77 |         }
 78 |
 79 |         /// <summary>
 80 |         /// Removes every node from the queue.
 81 |         /// O(n) (So, don't do this often!)
 82 |         /// </summary>
 83 | #if NET_VERSION_4_5
 84 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
 85 | #endif
 86 |         public void Clear()
 87 |         {
 88 |             Array.Clear(_nodes, 1,_numNodes);
 89 |             _numNodes = 0;
 90 |         }
 91 |
 92 |         /// <summary>
 93 |         /// Returns (in O(1)!) whether the given node is in the queue.
 94 |         /// If node is or has been previously added to another queue, the result is undefined unless oldQueue.ResetNode(node) has been called
 95 |         /// O(1)
 96 |         /// </summary>
 97 | #if NET_VERSION_4_5
 98 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
 99 | #endif
100 |         public bool Contains(TItem node)
101 |         {
102 | #if DEBUG
103 |             if(node == null)
104 |             {
105 |                 throw new ArgumentNullException("node");
106 |             }
107 |             if (node.Queue != null && !Equals(node.Queue))
108 |             {
109 |                 throw new InvalidOperationException("node.Contains was called on a node from another queue.  Please call originalQueue.ResetNode() first");
110 |             }
111 |             if (node.QueueIndex < 0 || node.QueueIndex >= _nodes.Length)
112 |             {
113 |                 throw new InvalidOperationException("node.QueueIndex has been corrupted. Did you change it manually?");
114 |             }
115 | #endif
116 |
117 |             return (_nodes[node.QueueIndex] == node);
118 |         }
119 |
120 |         /// <summary>
121 |         /// Enqueue a node to the priority queue.  Lower values are placed in front. Ties are broken by first-in-first-out.
122 |         /// If the queue is full, the result is undefined.
123 |         /// If the node is already enqueued, the result is undefined.
124 |         /// If node is or has been previously added to another queue, the result is undefined unless oldQueue.ResetNode(node) has been called
125 |         /// O(log n)
126 |         /// </summary>
127 | #if NET_VERSION_4_5
128 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
129 | #endif
130 |         public void Enqueue(TItem node, TPriority priority)
131 |         {
132 | #if DEBUG
133 |             if(node == null)
134 |             {
135 |                 throw new ArgumentNullException("node");
136 |             }
137 |             if(_numNodes >= _nodes.Length - 1)
138 |             {
139 |                 throw new InvalidOperationException("Queue is full - node cannot be added: " + node);
140 |             }
141 |             if (node.Queue != null && !Equals(node.Queue))
142 |             {
143 |                 throw new InvalidOperationException("node.Enqueue was called on a node from another queue.  Please call originalQueue.ResetNode() first");
144 |             }
145 |             if (Contains(node))
146 |             {
147 |                 throw new InvalidOperationException("Node is already enqueued: " + node);
148 |             }
149 |             node.Queue = this;
150 | #endif
151 |
152 |             node.Priority = priority;
153 |_numNodes++;
154 |             _nodes[_numNodes] = node;
155 |             node.QueueIndex = _numNodes;
156 |             node.InsertionIndex =_numNodesEverEnqueued++;
157 |             CascadeUp(node);
158 |         }
159 |
160 | #if NET_VERSION_4_5
161 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
162 | #endif
163 |         private void CascadeUp(TItem node)
164 |         {
165 |             //aka Heapify-up
166 |             int parent;
167 |             if (node.QueueIndex > 1)
168 |             {
169 |                 parent = node.QueueIndex >> 1;
170 |                 TItem parentNode =_nodes[parent];
171 |                 if(HasHigherPriority(parentNode, node))
172 |                     return;
173 |
174 |                 //Node has lower priority value, so move parent down the heap to make room
175 |                 _nodes[node.QueueIndex] = parentNode;
176 |                 parentNode.QueueIndex = node.QueueIndex;
177 |
178 |                 node.QueueIndex = parent;
179 |             }
180 |             else
181 |             {
182 |                 return;
183 |             }
184 |             while(parent > 1)
185 |             {
186 |                 parent >>= 1;
187 |                 TItem parentNode =_nodes[parent];
188 |                 if(HasHigherPriority(parentNode, node))
189 |                     break;
190 |
191 |                 //Node has lower priority value, so move parent down the heap to make room
192 |                 _nodes[node.QueueIndex] = parentNode;
193 |                 parentNode.QueueIndex = node.QueueIndex;
194 |
195 |                 node.QueueIndex = parent;
196 |             }
197 |_nodes[node.QueueIndex] = node;
198 |         }
199 |
200 | #if NET_VERSION_4_5
201 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
202 | #endif
203 |         private void CascadeDown(TItem node)
204 |         {
205 |             //aka Heapify-down
206 |             int finalQueueIndex = node.QueueIndex;
207 |             int childLeftIndex = 2 *finalQueueIndex;
208 |
209 |             // If leaf node, we're done
210 |             if(childLeftIndex >_numNodes)
211 |             {
212 |                 return;
213 |             }
214 |
215 |             // Check if the left-child is higher-priority than the current node
216 |             int childRightIndex = childLeftIndex + 1;
217 |             TItem childLeft = _nodes[childLeftIndex];
218 |             if(HasHigherPriority(childLeft, node))
219 |             {
220 |                 // Check if there is a right child. If not, swap and finish.
221 |                 if(childRightIndex >_numNodes)
222 |                 {
223 |                     node.QueueIndex = childLeftIndex;
224 |                     childLeft.QueueIndex = finalQueueIndex;
225 |                     _nodes[finalQueueIndex] = childLeft;
226 |_nodes[childLeftIndex] = node;
227 |                     return;
228 |                 }
229 |                 // Check if the left-child is higher-priority than the right-child
230 |                 TItem childRight = _nodes[childRightIndex];
231 |                 if(HasHigherPriority(childLeft, childRight))
232 |                 {
233 |                     // left is highest, move it up and continue
234 |                     childLeft.QueueIndex = finalQueueIndex;
235 |_nodes[finalQueueIndex] = childLeft;
236 |                     finalQueueIndex = childLeftIndex;
237 |                 }
238 |                 else
239 |                 {
240 |                     // right is even higher, move it up and continue
241 |                     childRight.QueueIndex = finalQueueIndex;
242 |                     _nodes[finalQueueIndex] = childRight;
243 |                     finalQueueIndex = childRightIndex;
244 |                 }
245 |             }
246 |             // Not swapping with left-child, does right-child exist?
247 |             else if(childRightIndex >_numNodes)
248 |             {
249 |                 return;
250 |             }
251 |             else
252 |             {
253 |                 // Check if the right-child is higher-priority than the current node
254 |                 TItem childRight = _nodes[childRightIndex];
255 |                 if(HasHigherPriority(childRight, node))
256 |                 {
257 |                     childRight.QueueIndex = finalQueueIndex;
258 |_nodes[finalQueueIndex] = childRight;
259 |                     finalQueueIndex = childRightIndex;
260 |                 }
261 |                 // Neither child is higher-priority than current, so finish and stop.
262 |                 else
263 |                 {
264 |                     return;
265 |                 }
266 |             }
267 |
268 |             while(true)
269 |             {
270 |                 childLeftIndex = 2* finalQueueIndex;
271 |
272 |                 // If leaf node, we're done
273 |                 if(childLeftIndex > _numNodes)
274 |                 {
275 |                     node.QueueIndex = finalQueueIndex;
276 |_nodes[finalQueueIndex] = node;
277 |                     break;
278 |                 }
279 |
280 |                 // Check if the left-child is higher-priority than the current node
281 |                 childRightIndex = childLeftIndex + 1;
282 |                 childLeft = _nodes[childLeftIndex];
283 |                 if(HasHigherPriority(childLeft, node))
284 |                 {
285 |                     // Check if there is a right child. If not, swap and finish.
286 |                     if(childRightIndex >_numNodes)
287 |                     {
288 |                         node.QueueIndex = childLeftIndex;
289 |                         childLeft.QueueIndex = finalQueueIndex;
290 |                         _nodes[finalQueueIndex] = childLeft;
291 |_nodes[childLeftIndex] = node;
292 |                         break;
293 |                     }
294 |                     // Check if the left-child is higher-priority than the right-child
295 |                     TItem childRight = _nodes[childRightIndex];
296 |                     if(HasHigherPriority(childLeft, childRight))
297 |                     {
298 |                         // left is highest, move it up and continue
299 |                         childLeft.QueueIndex = finalQueueIndex;
300 |_nodes[finalQueueIndex] = childLeft;
301 |                         finalQueueIndex = childLeftIndex;
302 |                     }
303 |                     else
304 |                     {
305 |                         // right is even higher, move it up and continue
306 |                         childRight.QueueIndex = finalQueueIndex;
307 |                         _nodes[finalQueueIndex] = childRight;
308 |                         finalQueueIndex = childRightIndex;
309 |                     }
310 |                 }
311 |                 // Not swapping with left-child, does right-child exist?
312 |                 else if(childRightIndex >_numNodes)
313 |                 {
314 |                     node.QueueIndex = finalQueueIndex;
315 |                     _nodes[finalQueueIndex] = node;
316 |                     break;
317 |                 }
318 |                 else
319 |                 {
320 |                     // Check if the right-child is higher-priority than the current node
321 |                     TItem childRight =_nodes[childRightIndex];
322 |                     if(HasHigherPriority(childRight, node))
323 |                     {
324 |                         childRight.QueueIndex = finalQueueIndex;
325 |                         _nodes[finalQueueIndex] = childRight;
326 |                         finalQueueIndex = childRightIndex;
327 |                     }
328 |                     // Neither child is higher-priority than current, so finish and stop.
329 |                     else
330 |                     {
331 |                         node.QueueIndex = finalQueueIndex;
332 |_nodes[finalQueueIndex] = node;
333 |                         break;
334 |                     }
335 |                 }
336 |             }
337 |         }
338 |
339 |         /// <summary>
340 |         /// Returns true if 'higher' has higher priority than 'lower', false otherwise.
341 |         /// Note that calling HasHigherPriority(node, node) (ie. both arguments the same node) will return false
342 |         /// </summary>
343 | #if NET_VERSION_4_5
344 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
345 | #endif
346 |         private bool HasHigherPriority(TItem higher, TItem lower)
347 |         {
348 |             var cmp =_comparer(higher.Priority, lower.Priority);
349 |             return (cmp < 0 || (cmp == 0 && higher.InsertionIndex < lower.InsertionIndex));
350 |         }
351 |
352 |         /// <summary>
353 |         /// Removes the head of the queue (node with minimum priority; ties are broken by order of insertion), and returns it.
354 |         /// If queue is empty, result is undefined
355 |         /// O(log n)
356 |         /// </summary>
357 | #if NET_VERSION_4_5
358 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
359 | #endif
360 |         public TItem Dequeue()
361 |         {
362 | #if DEBUG
363 |             if(_numNodes <= 0)
364 |             {
365 |                 throw new InvalidOperationException("Cannot call Dequeue() on an empty queue");
366 |             }
367 |
368 |             if(!IsValidQueue())
369 |             {
370 |                 throw new InvalidOperationException("Queue has been corrupted (Did you update a node priority manually instead of calling UpdatePriority()?" +
371 |                                                     "Or add the same node to two different queues?)");
372 |             }
373 | #endif
374 |
375 |             TItem returnMe = _nodes[1];
376 |             //If the node is already the last node, we can remove it immediately
377 |             if(_numNodes == 1)
378 |             {
379 |                 _nodes[1] = null;
380 |_numNodes = 0;
381 |                 return returnMe;
382 |             }
383 |
384 |             //Swap the node with the last node
385 |             TItem formerLastNode = _nodes[_numNodes];
386 |             _nodes[1] = formerLastNode;
387 |             formerLastNode.QueueIndex = 1;
388 |_nodes[_numNodes] = null;
389 |_numNodes--;
390 |
391 |             //Now bubble formerLastNode (which is no longer the last node) down
392 |             CascadeDown(formerLastNode);
393 |             return returnMe;
394 |         }
395 |
396 |         /// <summary>
397 |         /// Resize the queue so it can accept more nodes.  All currently enqueued nodes are remain.
398 |         /// Attempting to decrease the queue size to a size too small to hold the existing nodes results in undefined behavior
399 |         /// O(n)
400 |         /// </summary>
401 |         public void Resize(int maxNodes)
402 |         {
403 | #if DEBUG
404 |             if (maxNodes <= 0)
405 |             {
406 |                 throw new InvalidOperationException("Queue size cannot be smaller than 1");
407 |             }
408 |
409 |             if (maxNodes < _numNodes)
410 |             {
411 |                 throw new InvalidOperationException("Called Resize(" + maxNodes + "), but current queue contains " +_numNodes + " nodes");
412 |             }
413 | #endif
414 |
415 |             TItem[] newArray = new TItem[maxNodes + 1];
416 |             int highestIndexToCopy = Math.Min(maxNodes, _numNodes);
417 |             Array.Copy(_nodes, newArray, highestIndexToCopy + 1);
418 |             _nodes = newArray;
419 |         }
420 |
421 |         /// <summary>
422 |         /// Returns the head of the queue, without removing it (use Dequeue() for that).
423 |         /// If the queue is empty, behavior is undefined.
424 |         /// O(1)
425 |         /// </summary>
426 |         public TItem First
427 |         {
428 |             get
429 |             {
430 | #if DEBUG
431 |                 if(_numNodes <= 0)
432 |                 {
433 |                     throw new InvalidOperationException("Cannot call .First on an empty queue");
434 |                 }
435 | #endif
436 |
437 |                 return _nodes[1];
438 |             }
439 |         }
440 |
441 |         /// <summary>
442 |         /// This method must be called on a node every time its priority changes while it is in the queue.  
443 |         /// <b>Forgetting to call this method will result in a corrupted queue!</b>
444 |         /// Calling this method on a node not in the queue results in undefined behavior
445 |         /// O(log n)
446 |         /// </summary>
447 | #if NET_VERSION_4_5
448 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
449 | #endif
450 |         public void UpdatePriority(TItem node, TPriority priority)
451 |         {
452 | #if DEBUG
453 |             if(node == null)
454 |             {
455 |                 throw new ArgumentNullException("node");
456 |             }
457 |             if (node.Queue != null && !Equals(node.Queue))
458 |             {
459 |                 throw new InvalidOperationException("node.UpdatePriority was called on a node from another queue");
460 |             }
461 |             if (!Contains(node))
462 |             {
463 |                 throw new InvalidOperationException("Cannot call UpdatePriority() on a node which is not enqueued: " + node);
464 |             }
465 | #endif
466 |
467 |             node.Priority = priority;
468 |             OnNodeUpdated(node);
469 |         }
470 |
471 | #if NET_VERSION_4_5
472 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
473 | #endif
474 |         private void OnNodeUpdated(TItem node)
475 |         {
476 |             //Bubble the updated node up or down as appropriate
477 |             int parentIndex = node.QueueIndex >> 1;
478 |
479 |             if(parentIndex > 0 && HasHigherPriority(node,_nodes[parentIndex]))
480 |             {
481 |                 CascadeUp(node);
482 |             }
483 |             else
484 |             {
485 |                 //Note that CascadeDown will be called if parentNode == node (that is, node is the root)
486 |                 CascadeDown(node);
487 |             }
488 |         }
489 |
490 |         /// <summary>
491 |         /// Removes a node from the queue.  The node does not need to be the head of the queue.  
492 |         /// If the node is not in the queue, the result is undefined.  If unsure, check Contains() first
493 |         /// O(log n)
494 |         /// </summary>
495 | #if NET_VERSION_4_5
496 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
497 | #endif
498 |         public void Remove(TItem node)
499 |         {
500 | #if DEBUG
501 |             if(node == null)
502 |             {
503 |                 throw new ArgumentNullException("node");
504 |             }
505 |             if (node.Queue != null && !Equals(node.Queue))
506 |             {
507 |                 throw new InvalidOperationException("node.Remove was called on a node from another queue");
508 |             }
509 |             if (!Contains(node))
510 |             {
511 |                 throw new InvalidOperationException("Cannot call Remove() on a node which is not enqueued: " + node);
512 |             }
513 | #endif
514 |
515 |             //If the node is already the last node, we can remove it immediately
516 |             if(node.QueueIndex ==_numNodes)
517 |             {
518 |                 _nodes[_numNodes] = null;
519 |                 _numNodes--;
520 |                 return;
521 |             }
522 |
523 |             //Swap the node with the last node
524 |             TItem formerLastNode =_nodes[_numNodes];
525 |_nodes[node.QueueIndex] = formerLastNode;
526 |             formerLastNode.QueueIndex = node.QueueIndex;
527 |             _nodes[_numNodes] = null;
528 |             _numNodes--;
529 |
530 |             //Now bubble formerLastNode (which is no longer the last node) up or down as appropriate
531 |             OnNodeUpdated(formerLastNode);
532 |         }
533 |
534 |         /// <summary>
535 |         /// By default, nodes that have been previously added to one queue cannot be added to another queue.
536 |         /// If you need to do this, please call originalQueue.ResetNode(node) before attempting to add it in the new queue
537 |         /// </summary>
538 | #if NET_VERSION_4_5
539 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
540 | #endif
541 |         public void ResetNode(TItem node)
542 |         {
543 | #if DEBUG
544 |             if (node == null)
545 |             {
546 |                 throw new ArgumentNullException("node");
547 |             }
548 |             if (node.Queue != null && !Equals(node.Queue))
549 |             {
550 |                 throw new InvalidOperationException("node.ResetNode was called on a node from another queue");
551 |             }
552 |             if (Contains(node))
553 |             {
554 |                 throw new InvalidOperationException("node.ResetNode was called on a node that is still in the queue");
555 |             }
556 |
557 |             node.Queue = null;
558 | #endif
559 |
560 |             node.QueueIndex = 0;
561 |         }
562 |
563 |
564 |         public IEnumerator<TItem> GetEnumerator()
565 |         {
566 | #if NET_VERSION_4_5 // ArraySegment does not implement IEnumerable before 4.5
567 |             IEnumerable<TItem> e = new ArraySegment<TItem>(_nodes, 1, _numNodes);
568 |             return e.GetEnumerator();
569 | #else
570 |             for(int i = 1; i <=_numNodes; i++)
571 |                 yield return _nodes[i];
572 | #endif
573 |         }
574 |
575 |         IEnumerator IEnumerable.GetEnumerator()
576 |         {
577 |             return GetEnumerator();
578 |         }
579 |
580 |         /// <summary>
581 |         /// <b>Should not be called in production code.</b>
582 |         /// Checks to make sure the queue is still in a valid state.  Used for testing/debugging the queue.
583 |         /// </summary>
584 |         public bool IsValidQueue()
585 |         {
586 |             for(int i = 1; i <_nodes.Length; i++)
587 |             {
588 |                 if(_nodes[i] != null)
589 |                 {
590 |                     int childLeftIndex = 2 * i;
591 |                     if(childLeftIndex <_nodes.Length && _nodes[childLeftIndex] != null && HasHigherPriority(_nodes[childLeftIndex], _nodes[i]))
592 |                         return false;
593 |
594 |                     int childRightIndex = childLeftIndex + 1;
595 |                     if(childRightIndex <_nodes.Length && _nodes[childRightIndex] != null && HasHigherPriority(_nodes[childRightIndex], _nodes[i]))
596 |                         return false;
597 |                 }
598 |             }
599 |             return true;
600 |         }
601 |     }
602 | }
603 | #pragma warning restore

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/GenericPriorityQueueNode.cs
--------------------------------------------------------------------------------

 1 | ﻿#pragma warning disable
 2 | namespace Priority_Queue
 3 | {
 4 |     public class GenericPriorityQueueNode<TPriority>
 5 |     {
 6 |         /// <summary>
 7 |         /// The Priority to insert this node at.
 8 |         /// Cannot be manually edited - see queue.Enqueue() and queue.UpdatePriority() instead
 9 |         /// </summary>
10 |         public TPriority Priority { get; protected internal set; }
11 |
12 |         /// <summary>
13 |         /// Represents the current position in the queue
14 |         /// </summary>
15 |         public int QueueIndex { get; internal set; }
16 |
17 |         /// <summary>
18 |         /// Represents the order the node was inserted in
19 |         /// </summary>
20 |         public long InsertionIndex { get; internal set; }
21 |
22 |
23 | #if DEBUG
24 |         /// <summary>
25 |         /// The queue this node is tied to. Used only for debug builds.
26 |         /// </summary>
27 |         public object Queue { get; internal set; }
28 | #endif
29 |     }
30 | }
31 | #pragma warning restore

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/IFixedSizePriorityQueue.cs
--------------------------------------------------------------------------------

 1 | ﻿#pragma warning disable
 2 | using System;
 3 | using System.Collections.Generic;
 4 | using System.Text;
 5 |
 6 | namespace Priority_Queue
 7 | {
 8 |     /// <summary>
 9 |     /// A helper-interface only needed to make writing unit tests a bit easier (hence the 'internal' access modifier)
10 |     /// </summary>
11 |     internal interface IFixedSizePriorityQueue<TItem, in TPriority> : IPriorityQueue<TItem, TPriority>
12 |     {
13 |         /// <summary>
14 |         /// Resize the queue so it can accept more nodes.  All currently enqueued nodes are remain.
15 |         /// Attempting to decrease the queue size to a size too small to hold the existing nodes results in undefined behavior
16 |         /// </summary>
17 |         void Resize(int maxNodes);
18 |
19 |         /// <summary>
20 |         /// Returns the maximum number of items that can be enqueued at once in this queue.  Once you hit this number (ie. once Count == MaxSize),
21 |         /// attempting to enqueue another item will cause undefined behavior.
22 |         /// </summary>
23 |         int MaxSize { get; }
24 |
25 |         /// <summary>
26 |         /// By default, nodes that have been previously added to one queue cannot be added to another queue.
27 |         /// If you need to do this, please call originalQueue.ResetNode(node) before attempting to add it in the new queue
28 |         /// </summary>
29 |         void ResetNode(TItem node);
30 |     }
31 | }
32 | #pragma warning restore

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/IPriorityQueue.cs
--------------------------------------------------------------------------------

 1 | ﻿#pragma warning disable
 2 | using System;
 3 | using System.Collections.Generic;
 4 |
 5 | namespace Priority_Queue
 6 | {
 7 |     /// <summary>
 8 |     /// The IPriorityQueue interface.  This is mainly here for purists, and in case I decide to add more implementations later.
 9 |     /// For speed purposes, it is actually recommended that you *don't* access the priority queue through this interface, since the JIT can
10 |     /// (theoretically?) optimize method calls from concrete-types slightly better.
11 |     /// </summary>
12 |     public interface IPriorityQueue<TItem, in TPriority> : IEnumerable<TItem>
13 |     {
14 |         /// <summary>
15 |         /// Enqueue a node to the priority queue.  Lower values are placed in front. Ties are broken by first-in-first-out.
16 |         /// See implementation for how duplicates are handled.
17 |         /// </summary>
18 |         void Enqueue(TItem node, TPriority priority);
19 |
20 |         /// <summary>
21 |         /// Removes the head of the queue (node with minimum priority; ties are broken by order of insertion), and returns it.
22 |         /// </summary>
23 |         TItem Dequeue();
24 |
25 |         /// <summary>
26 |         /// Removes every node from the queue.
27 |         /// </summary>
28 |         void Clear();
29 |
30 |         /// <summary>
31 |         /// Returns whether the given node is in the queue.
32 |         /// </summary>
33 |         bool Contains(TItem node);
34 |
35 |         /// <summary>
36 |         /// Removes a node from the queue.  The node does not need to be the head of the queue.  
37 |         /// </summary>
38 |         void Remove(TItem node);
39 |
40 |         /// <summary>
41 |         /// Call this method to change the priority of a node.  
42 |         /// </summary>
43 |         void UpdatePriority(TItem node, TPriority priority);
44 |
45 |         /// <summary>
46 |         /// Returns the head of the queue, without removing it (use Dequeue() for that).
47 |         /// </summary>
48 |         TItem First { get; }
49 |
50 |         /// <summary>
51 |         /// Returns the number of nodes in the queue.
52 |         /// </summary>
53 |         int Count { get; }
54 |     }
55 | }
56 | #pragma warning restore

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/Priority Queue.csproj
--------------------------------------------------------------------------------

 1 | ﻿<?xml version="1.0" encoding="utf-8"?>
 2 | <Project ToolsVersion="12.0" DefaultTargets="Build" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
 3 |   <Import Project="$(MSBuildExtensionsPath)\$(MSBuildToolsVersion)\Microsoft.Common.props" Condition="Exists('$(MSBuildExtensionsPath)\$(MSBuildToolsVersion)\Microsoft.Common.props')" />
 4 |   <PropertyGroup>
 5 |     <Configuration Condition=" '$(Configuration)' == '' ">Debug</Configuration>
 6 |     <Platform Condition=" '$(Platform)' == '' ">AnyCPU</Platform>
 7 |     <ProjectGuid>{1531C1EA-BD53-41D1-A34B-CFCDF79D2651}</ProjectGuid>
 8 |     <OutputType>Library</OutputType>
 9 |     <AppDesignerFolder>Properties</AppDesignerFolder>
10 |     <RootNamespace>Priority_Queue</RootNamespace>
11 |     <AssemblyName>PriorityQueue</AssemblyName>
12 |     <TargetFrameworkVersion>v4.5</TargetFrameworkVersion>
13 |     <FileAlignment>512</FileAlignment>
14 |     <CustomConstants Condition=" '$(TargetFrameworkVersion)' == 'v4.5' ">NET_VERSION_4_5</CustomConstants>
15 |     <DefineConstants>$(DefineConstants);$(CustomConstants)</DefineConstants>
16 |     <TargetFrameworkProfile>
17 |     </TargetFrameworkProfile>
18 |   </PropertyGroup>
19 |   <PropertyGroup Condition=" '$(Configuration)|$(Platform)' == 'Debug|AnyCPU' ">
20 |     <DebugSymbols>true</DebugSymbols>
21 |     <DebugType>full</DebugType>
22 |     <Optimize>false</Optimize>
23 |     <OutputPath>bin\Debug\</OutputPath>
24 |     <DefineConstants>DEBUG;TRACE</DefineConstants>
25 |     <ErrorReport>prompt</ErrorReport>
26 |     <WarningLevel>4</WarningLevel>
27 |     <CustomConstants Condition=" '$(TargetFrameworkVersion)' == 'v4.5' ">NET_VERSION_4_5</CustomConstants>
28 |     <DefineConstants>$(DefineConstants);$(CustomConstants)</DefineConstants>
29 |     <Prefer32Bit>false</Prefer32Bit>
30 |   </PropertyGroup>
31 |   <PropertyGroup Condition=" '$(Configuration)|$(Platform)' == 'Release|AnyCPU' ">
32 |     <DebugType>pdbonly</DebugType>
33 |     <Optimize>true</Optimize>
34 |     <OutputPath>bin\Release\</OutputPath>
35 |     <DefineConstants>TRACE</DefineConstants>
36 |     <ErrorReport>prompt</ErrorReport>
37 |     <WarningLevel>4</WarningLevel>
38 |     <CustomConstants Condition=" '$(TargetFrameworkVersion)' == 'v4.5' ">NET_VERSION_4_5</CustomConstants>
39 |     <DefineConstants>$(DefineConstants);$(CustomConstants)</DefineConstants>
40 |     <Prefer32Bit>false</Prefer32Bit>
41 |   </PropertyGroup>
42 |   <PropertyGroup Condition=" '$(Configuration)|$(Platform)' == 'Release 4.5|AnyCPU' ">
43 |     <DebugType>pdbonly</DebugType>
44 |     <Optimize>true</Optimize>
45 |     <DefineConstants>TRACE;NET_VERSION_4_5</DefineConstants>
46 |     <ErrorReport>prompt</ErrorReport>
47 |     <WarningLevel>4</WarningLevel>
48 |     <Prefer32Bit>false</Prefer32Bit>
49 |     <OutputPath>bin\Release\net45\</OutputPath>
50 |     <TargetFrameworkVersion>v4.5</TargetFrameworkVersion>
51 |     <DocumentationFile>bin\Release\net45\PriorityQueue.xml</DocumentationFile>
52 |   </PropertyGroup>
53 |   <PropertyGroup Condition="'$(Configuration)|$(Platform)' == 'Release 2.0|AnyCPU'">
54 |     <DebugType>pdbonly</DebugType>
55 |     <Optimize>true</Optimize>
56 |     <DefineConstants>TRACE</DefineConstants>
57 |     <ErrorReport>prompt</ErrorReport>
58 |     <WarningLevel>4</WarningLevel>
59 |     <Prefer32Bit>false</Prefer32Bit>
60 |     <OutputPath>bin\Release\net20\</OutputPath>
61 |     <TargetFrameworkVersion>v2.0</TargetFrameworkVersion>
62 |     <DocumentationFile>bin\Release\net20\PriorityQueue.xml</DocumentationFile>
63 |   </PropertyGroup>
64 |   <PropertyGroup>
65 |     <SignAssembly>true</SignAssembly>
66 |   </PropertyGroup>
67 |   <PropertyGroup>
68 |     <AssemblyOriginatorKeyFile>Priority Queue.snk</AssemblyOriginatorKeyFile>
69 |   </PropertyGroup>
70 |   <ItemGroup>
71 |     <Reference Include="System" />
72 |     <Reference Include="System.Data" />
73 |     <Reference Include="System.Xml" />
74 |   </ItemGroup>
75 |   <ItemGroup>
76 |     <Compile Include="GenericPriorityQueue.cs" />
77 |     <Compile Include="GenericPriorityQueueNode.cs" />
78 |     <Compile Include="IFixedSizePriorityQueue.cs" />
79 |     <Compile Include="StablePriorityQueue.cs" />
80 |     <Compile Include="FastPriorityQueue.cs" />
81 |     <Compile Include="StablePriorityQueueNode.cs" />
82 |     <Compile Include="IPriorityQueue.cs" />
83 |     <Compile Include="FastPriorityQueueNode.cs" />
84 |     <Compile Include="Properties\AssemblyInfo.cs" />
85 |     <Compile Include="SimplePriorityQueue.cs" />
86 |   </ItemGroup>
87 |   <ItemGroup>
88 |     <None Include="Priority Queue.snk" />
89 |   </ItemGroup>
90 |   <Import Project="$(MSBuildToolsPath)\Microsoft.CSharp.targets" />
91 |   <!-- To modify your build process, add your task inside one of the targets below and uncomment it. 
92 |        Other similar extension points exist, see Microsoft.Common.targets.
93 |   <Target Name="BeforeBuild">
94 |   </Target>
95 |   <Target Name="AfterBuild">
96 |   </Target>
97 |   -->
98 | </Project>

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/Priority Queue.nuspec
--------------------------------------------------------------------------------

 1 | <?xml version="1.0"?>
 2 | <package >
 3 |   <metadata>
 4 |     <id>OptimizedPriorityQueue</id>
 5 |     <version>5.1.0</version>
 6 |     <title>Highly Optimized Priority Queue</title>
 7 |     <authors>BlueRaja</authors>
 8 |     <owners>BlueRaja</owners>
 9 |     <licenseUrl>https://github.com/BlueRaja/High-Speed-Priority-Queue-for-C-Sharp/blob/master/LICENSE.txt</licenseUrl>
10 |     <projectUrl>https://github.com/BlueRaja/High-Speed-Priority-Queue-for-C-Sharp</projectUrl>
11 |     <requireLicenseAcceptance>false</requireLicenseAcceptance>
12 |     <description>A highly optimized Priority Queue for path-finding and related applications</description>
13 |     <releaseNotes>Added strong names</releaseNotes>
14 |     <copyright>Copyright 2021</copyright>
15 |     <tags>C# priority-queue pathfinding optimized</tags>
16 |   </metadata>
17 |   <files>
18 |     <file src="bin\Release\net20\PriorityQueue.dll" target="lib\net20\PriorityQueue.dll" />
19 |     <file src="bin\Release\net20\PriorityQueue.pdb" target="lib\net20\PriorityQueue.pdb" />
20 |     <file src="bin\Release\net20\PriorityQueue.xml" target="lib\net20\PriorityQueue.xml" />
21 |
22 |     <file src="bin\Release\net45\PriorityQueue.dll" target="lib\net45\PriorityQueue.dll" />
23 |     <file src="bin\Release\net45\PriorityQueue.pdb" target="lib\net45\PriorityQueue.pdb" />
24 |     <file src="bin\Release\net45\PriorityQueue.xml" target="lib\net45\PriorityQueue.xml" />
25 |
26 |     <file src="..\Priority Queue Net Standard\bin\Release\netstandard1.0\PriorityQueue.dll" target="lib\netstandard1.0\PriorityQueue.dll" />
27 |     <file src="..\Priority Queue Net Standard\bin\Release\netstandard1.0\PriorityQueue.pdb" target="lib\netstandard1.0\PriorityQueue.pdb" />
28 |     <file src="..\Priority Queue Net Standard\bin\Release\netstandard1.0\PriorityQueue.xml" target="lib\netstandard1.0\PriorityQueue.xml" />
29 |
30 |     <file src="..\Priority Queue PCL\bin\Release\PriorityQueue.dll" target="lib\portable-net40+sl5+win8+wpa81+wp8\PriorityQueue.dll" />
31 |     <file src="..\Priority Queue PCL\bin\Release\PriorityQueue.pdb" target="lib\portable-net40+sl5+win8+wpa81+wp8\PriorityQueue.pdb" />
32 |     <file src="..\Priority Queue PCL\bin\Release\PriorityQueue.xml" target="lib\portable-net40+sl5+win8+wpa81+wp8\PriorityQueue.xml" />
33 |
34 |     <file src="..\Priority Queue Unity Full\bin\Release\PriorityQueue.dll" target="lib\net35-unity full v3.5\PriorityQueue.dll" />
35 |     <file src="..\Priority Queue Unity Full\bin\Release\PriorityQueue.pdb" target="lib\net35-unity full v3.5\PriorityQueue.pdb" />
36 |     <file src="..\Priority Queue Unity Full\bin\Release\PriorityQueue.xml" target="lib\net35-unity full v3.5\PriorityQueue.xml" />
37 |
38 |     <file src="..\Priority Queue Unity Subset\bin\Release\PriorityQueue.dll" target="lib\net35-unity subset v3.5\PriorityQueue.dll" />
39 |     <file src="..\Priority Queue Unity Subset\bin\Release\PriorityQueue.pdb" target="lib\net35-unity subset v3.5\PriorityQueue.pdb" />
40 |     <file src="..\Priority Queue Unity Subset\bin\Release\PriorityQueue.xml" target="lib\net35-unity subset v3.5\PriorityQueue.xml" />
41 |   </files>
42 | </package>

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/Priority Queue.snk
--------------------------------------------------------------------------------
<https://raw.githubusercontent.com/caesuric/mountain-goap/main/MountainGoap/PriorityQueue/Priority> Queue.snk

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/Properties/AssemblyInfo.cs
--------------------------------------------------------------------------------

 1 | ﻿#pragma warning disable
 2 | using System.Reflection;
 3 | using System.Runtime.CompilerServices;
 4 | using System.Runtime.InteropServices;
 5 |
 6 | // General Information about an assembly is controlled through the following
 7 | // set of attributes. Change these attribute values to modify the information
 8 | // associated with an assembly.
 9 | [assembly: AssemblyTitle("Highly Optimized Priority Queue")]
10 | [assembly: AssemblyDescription("A highly optimized Priority Queue for path-finding and related applications")]
11 | [assembly: AssemblyConfiguration("")]
12 | [assembly: AssemblyCompany("")]
13 | [assembly: AssemblyProduct("Highly Optimized Priority Queue")]
14 | [assembly: AssemblyCopyright("Copyright © BlueRaja 2017")]
15 | [assembly: AssemblyTrademark("")]
16 | [assembly: AssemblyCulture("")]
17 |
18 | // Setting ComVisible to false makes the types in this assembly not visible
19 | // to COM components.  If you need to access a type in this assembly from
20 | // COM, set the ComVisible attribute to true on that type.
21 | [assembly: ComVisible(false)]
22 |
23 | // The following GUID is for the ID of the typelib if this project is exposed to COM
24 | [assembly: Guid("3eee6b54-af8a-494b-9121-3d46ed09a58b")]
25 |
26 | [assembly: InternalsVisibleTo("Priority Queue Tests, PublicKey=0024000004800000940000000602000000240000525341310004000001000100794a91e4cf03eda7c3406cbc7247bdae9f498905b805173bbd3bb97613cb2afa69311aef40119245618d08a9c84edae6b545795f2b8dc81a9ed2f70598e341b4a67d9e96fe23dfa80f61db1dd47cb2d58992c2cd3dc8d6f4744aeda94c21c018d5e63e1cc9ff5ded1030e9b092315e00c04391429bc311e4f2597114cee1efae")]
27 |
28 | // Version information for an assembly consists of the following four values:
29 | //
30 | //      Major Version
31 | //      Minor Version
32 | //      Build Number
33 | //      Revision
34 | //
35 | // You can specify all the values or you can default the Build and Revision Numbers
36 | // by using the '*' as shown below:
37 | // [assembly: AssemblyVersion("1.0.*")]
38 | [assembly: AssemblyVersion("5.1.0")]
39 | [assembly: AssemblyFileVersion("5.1.0")]
40 | #pragma warning restore

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/SimplePriorityQueue.cs
--------------------------------------------------------------------------------

  1 | ﻿#pragma warning disable
  2 | using System;
  3 | using System.Collections;
  4 | using System.Collections.Generic;
  5 |
  6 | namespace Priority_Queue
  7 | {
  8 |     /// <summary>
  9 |     /// A simplified priority queue implementation.  Is stable, auto-resizes, and thread-safe, at the cost of being slightly slower than
 10 |     /// FastPriorityQueue
 11 |     /// Methods tagged as O(1) or O(log n) are assuming there are no duplicates.  Duplicates may increase the algorithmic complexity.
 12 |     /// </summary>
 13 |     /// <typeparam name="TItem">The type to enqueue</typeparam>
 14 |     /// <typeparam name="TPriority">The priority-type to use for nodes.  Must extend IComparable&lt;TPriority&gt;</typeparam>
 15 |     public class SimplePriorityQueue<TItem, TPriority> : IPriorityQueue<TItem, TPriority>
 16 |     {
 17 |         private class SimpleNode : GenericPriorityQueueNode<TPriority>
 18 |         {
 19 |             public TItem Data { get; private set; }
 20 |
 21 |             public SimpleNode(TItem data)
 22 |             {
 23 |                 Data = data;
 24 |             }
 25 |         }
 26 |
 27 |         private const int INITIAL_QUEUE_SIZE = 10;
 28 |         private readonly GenericPriorityQueue<SimpleNode, TPriority>_queue;
 29 |         private readonly Dictionary<TItem, IList<SimpleNode>> _itemToNodesCache;
 30 |         private readonly IList<SimpleNode>_nullNodesCache;
 31 |
 32 |         #region Constructors
 33 |         /// <summary>
 34 |         /// Instantiate a new Priority Queue
 35 |         /// </summary>
 36 |         public SimplePriorityQueue() : this(Comparer<TPriority>.Default, EqualityComparer<TItem>.Default) { }
 37 |
 38 |         /// <summary>
 39 |         /// Instantiate a new Priority Queue
 40 |         /// </summary>
 41 |         /// <param name="priorityComparer">The comparer used to compare TPriority values.  Defaults to Comparer&lt;TPriority&gt;.default</param>
 42 |         public SimplePriorityQueue(IComparer<TPriority> priorityComparer) : this(priorityComparer.Compare, EqualityComparer<TItem>.Default) { }
 43 |
 44 |         /// <summary>
 45 |         /// Instantiate a new Priority Queue
 46 |         /// </summary>
 47 |         /// <param name="priorityComparer">The comparison function to use to compare TPriority values</param>
 48 |         public SimplePriorityQueue(Comparison<TPriority> priorityComparer) : this(priorityComparer, EqualityComparer<TItem>.Default) { }
 49 |
 50 |         /// <summary>
 51 |         /// Instantiate a new Priority Queue
 52 |         /// </summary>
 53 |         /// <param name="itemEquality">The equality comparison function to use to compare TItem values</param>
 54 |         public SimplePriorityQueue(IEqualityComparer<TItem> itemEquality) : this(Comparer<TPriority>.Default, itemEquality) { }
 55 |
 56 |         /// <summary>
 57 |         /// Instantiate a new Priority Queue
 58 |         /// </summary>
 59 |         /// <param name="priorityComparer">The comparer used to compare TPriority values.  Defaults to Comparer&lt;TPriority&gt;.default</param>
 60 |         /// <param name="itemEquality">The equality comparison function to use to compare TItem values</param>
 61 |         public SimplePriorityQueue(IComparer<TPriority> priorityComparer, IEqualityComparer<TItem> itemEquality) : this(priorityComparer.Compare, itemEquality) { }
 62 |
 63 |         /// <summary>
 64 |         /// Instantiate a new Priority Queue
 65 |         /// </summary>
 66 |         /// <param name="priorityComparer">The comparison function to use to compare TPriority values</param>
 67 |         /// <param name="itemEquality">The equality comparison function to use to compare TItem values</param>
 68 |         public SimplePriorityQueue(Comparison<TPriority> priorityComparer, IEqualityComparer<TItem> itemEquality)
 69 |         {
 70 |             _queue = new GenericPriorityQueue<SimpleNode, TPriority>(INITIAL_QUEUE_SIZE, priorityComparer);
 71 |_itemToNodesCache = new Dictionary<TItem, IList<SimpleNode>>(itemEquality);
 72 |             _nullNodesCache = new List<SimpleNode>();
 73 |         }
 74 |         #endregion
 75 |
 76 |         /// <summary>
 77 |         /// Given an item of type T, returns the existing SimpleNode in the queue
 78 |         /// </summary>
 79 |         private SimpleNode GetExistingNode(TItem item)
 80 |         {
 81 |             if (item == null)
 82 |             {
 83 |                 return_nullNodesCache.Count > 0 ? _nullNodesCache[0] : null;
 84 |             }
 85 |
 86 |             IList<SimpleNode> nodes;
 87 |             if (!_itemToNodesCache.TryGetValue(item, out nodes))
 88 |             {
 89 |                 return null;
 90 |             }
 91 |             return nodes[0];
 92 |         }
 93 |
 94 |         /// <summary>
 95 |         /// Adds an item to the Node-cache to allow for many methods to be O(1) or O(log n)
 96 |         /// </summary>
 97 |         private void AddToNodeCache(SimpleNode node)
 98 |         {
 99 |             if (node.Data == null)
100 |             {
101 |                 _nullNodesCache.Add(node);
102 |                 return;
103 |             }
104 |
105 |             IList<SimpleNode> nodes;
106 |             if (!_itemToNodesCache.TryGetValue(node.Data, out nodes))
107 |             {
108 |                 nodes = new List<SimpleNode>();
109 |                 _itemToNodesCache[node.Data] = nodes;
110 |             }
111 |             nodes.Add(node);
112 |         }
113 |
114 |         /// <summary>
115 |         /// Removes an item to the Node-cache to allow for many methods to be O(1) or O(log n) (assuming no duplicates)
116 |         /// </summary>
117 |         private void RemoveFromNodeCache(SimpleNode node)
118 |         {
119 |             if (node.Data == null)
120 |             {
121 |_nullNodesCache.Remove(node);
122 |                 return;
123 |             }
124 |
125 |             IList<SimpleNode> nodes;
126 |             if (!_itemToNodesCache.TryGetValue(node.Data, out nodes))
127 |             {
128 |                 return;
129 |             }
130 |             nodes.Remove(node);
131 |             if (nodes.Count == 0)
132 |             {
133 |_itemToNodesCache.Remove(node.Data);
134 |             }
135 |         }
136 |
137 |         /// <summary>
138 |         /// Returns the number of nodes in the queue.
139 |         /// O(1)
140 |         /// </summary>
141 |         public int Count
142 |         {
143 |             get
144 |             {
145 |                 lock(_queue)
146 |                 {
147 |                     return_queue.Count;
148 |                 }
149 |             }
150 |         }
151 |
152 |         /// <summary>
153 |         /// Returns the head of the queue, without removing it (use Dequeue() for that).
154 |         /// Throws an exception when the queue is empty.
155 |         /// O(1)
156 |         /// </summary>
157 |         public TItem First
158 |         {
159 |             get
160 |             {
161 |                 lock(_queue)
162 |                 {
163 |                     if(_queue.Count <= 0)
164 |                     {
165 |                         throw new InvalidOperationException("Cannot call .First on an empty queue");
166 |                     }
167 |
168 |                     return _queue.First.Data;
169 |                 }
170 |             }
171 |         }
172 |
173 |         /// <summary>
174 |         /// Removes every node from the queue.
175 |         /// O(n)
176 |         /// </summary>
177 |         public void Clear()
178 |         {
179 |             lock(_queue)
180 |             {
181 |                 _queue.Clear();
182 |_itemToNodesCache.Clear();
183 |                 _nullNodesCache.Clear();
184 |             }
185 |         }
186 |
187 |         /// <summary>
188 |         /// Returns whether the given item is in the queue.
189 |         /// O(1)
190 |         /// </summary>
191 |         public bool Contains(TItem item)
192 |         {
193 |             lock(_queue)
194 |             {
195 |                 return item == null ? _nullNodesCache.Count > 0 :_itemToNodesCache.ContainsKey(item);
196 |             }
197 |         }
198 |
199 |         /// <summary>
200 |         /// Removes the head of the queue (node with minimum priority; ties are broken by order of insertion), and returns it.
201 |         /// If queue is empty, throws an exception
202 |         /// O(log n)
203 |         /// </summary>
204 |         public TItem Dequeue()
205 |         {
206 |             lock(_queue)
207 |             {
208 |                 if(_queue.Count <= 0)
209 |                 {
210 |                     throw new InvalidOperationException("Cannot call Dequeue() on an empty queue");
211 |                 }
212 |
213 |                 SimpleNode node =_queue.Dequeue();
214 |                 RemoveFromNodeCache(node);
215 |                 return node.Data;
216 |             }
217 |         }
218 |
219 |         /// <summary>
220 |         /// Enqueue the item with the given priority, without calling lock(_queue) or AddToNodeCache(node)
221 |         /// </summary>
222 |         /// <param name="item"></param>
223 |         /// <param name="priority"></param>
224 |         /// <returns></returns>
225 |         private SimpleNode EnqueueNoLockOrCache(TItem item, TPriority priority)
226 |         {
227 |             SimpleNode node = new SimpleNode(item);
228 |             if (_queue.Count ==_queue.MaxSize)
229 |             {
230 |                 _queue.Resize(_queue.MaxSize *2 + 1);
231 |             }
232 |             _queue.Enqueue(node, priority);
233 |             return node;
234 |         }
235 |
236 |         /// <summary>
237 |         /// Enqueue a node to the priority queue.  Lower values are placed in front. Ties are broken by first-in-first-out.
238 |         /// This queue automatically resizes itself, so there's no concern of the queue becoming 'full'.
239 |         /// Duplicates and null-values are allowed.
240 |         /// O(log n)
241 |         /// </summary>
242 |         public void Enqueue(TItem item, TPriority priority)
243 |         {
244 |             lock(_queue)
245 |             {
246 |                 IList<SimpleNode> nodes;
247 |                 if (item == null)
248 |                 {
249 |                     nodes = _nullNodesCache;
250 |                 }
251 |                 else if (!_itemToNodesCache.TryGetValue(item, out nodes))
252 |                 {
253 |                     nodes = new List<SimpleNode>();
254 |                     _itemToNodesCache[item] = nodes;
255 |                 }
256 |                 SimpleNode node = EnqueueNoLockOrCache(item, priority);
257 |                 nodes.Add(node);
258 |             }
259 |         }
260 |
261 |         /// <summary>
262 |         /// Enqueue a node to the priority queue if it doesn't already exist.  Lower values are placed in front. Ties are broken by first-in-first-out.
263 |         /// This queue automatically resizes itself, so there's no concern of the queue becoming 'full'.  Null values are allowed.
264 |         /// Returns true if the node was successfully enqueued; false if it already exists.
265 |         /// O(log n)
266 |         /// </summary>
267 |         public bool EnqueueWithoutDuplicates(TItem item, TPriority priority)
268 |         {
269 |             lock(_queue)
270 |             {
271 |                 IList<SimpleNode> nodes;
272 |                 if (item == null)
273 |                 {
274 |                     if (_nullNodesCache.Count > 0)
275 |                     {
276 |                         return false;
277 |                     }
278 |                     nodes =_nullNodesCache;
279 |                 }
280 |                 else if (_itemToNodesCache.ContainsKey(item))
281 |                 {
282 |                     return false;
283 |                 }
284 |                 else
285 |                 {
286 |                     nodes = new List<SimpleNode>();
287 |_itemToNodesCache[item] = nodes;
288 |                 }
289 |                 SimpleNode node = EnqueueNoLockOrCache(item, priority);
290 |                 nodes.Add(node);
291 |                 return true;
292 |             }
293 |         }
294 |
295 |         /// <summary>
296 |         /// Removes an item from the queue.  The item does not need to be the head of the queue.  
297 |         /// If the item is not in the queue, an exception is thrown.  If unsure, check Contains() first.
298 |         /// If multiple copies of the item are enqueued, only the first one is removed.
299 |         /// O(log n)
300 |         /// </summary>
301 |         public void Remove(TItem item)
302 |         {
303 |             lock(_queue)
304 |             {
305 |                 SimpleNode removeMe;
306 |                 IList<SimpleNode> nodes;
307 |                 if (item == null)
308 |                 {
309 |                     if (_nullNodesCache.Count == 0)
310 |                     {
311 |                         throw new InvalidOperationException("Cannot call Remove() on a node which is not enqueued: " + item);
312 |                     }
313 |                     removeMe = _nullNodesCache[0];
314 |                     nodes =_nullNodesCache;
315 |                 }
316 |                 else
317 |                 {
318 |                     if (!_itemToNodesCache.TryGetValue(item, out nodes))
319 |                     {
320 |                         throw new InvalidOperationException("Cannot call Remove() on a node which is not enqueued: " + item);
321 |                     }
322 |                     removeMe = nodes[0];
323 |                     if (nodes.Count == 1)
324 |                     {
325 |_itemToNodesCache.Remove(item);
326 |                     }
327 |                 }
328 |                 _queue.Remove(removeMe);
329 |                 nodes.Remove(removeMe);
330 |             }
331 |         }
332 |
333 |         /// <summary>
334 |         /// Call this method to change the priority of an item.
335 |         /// Calling this method on a item not in the queue will throw an exception.
336 |         /// If the item is enqueued multiple times, only the first one will be updated.
337 |         /// (If your requirements are complex enough that you need to enqueue the same item multiple times <i>and</i> be able
338 |         /// to update all of them, please wrap your items in a wrapper class so they can be distinguished).
339 |         /// O(log n)
340 |         /// </summary>
341 |         public void UpdatePriority(TItem item, TPriority priority)
342 |         {
343 |             lock (_queue)
344 |             {
345 |                 SimpleNode updateMe = GetExistingNode(item);
346 |                 if (updateMe == null)
347 |                 {
348 |                     throw new InvalidOperationException("Cannot call UpdatePriority() on a node which is not enqueued: " + item);
349 |                 }
350 |                 _queue.UpdatePriority(updateMe, priority);
351 |             }
352 |         }
353 |
354 |         /// <summary>
355 |         /// Returns the priority of the given item.
356 |         /// Calling this method on a item not in the queue will throw an exception.
357 |         /// If the item is enqueued multiple times, only the priority of the first will be returned.
358 |         /// (If your requirements are complex enough that you need to enqueue the same item multiple times <i>and</i> be able
359 |         /// to query all their priorities, please wrap your items in a wrapper class so they can be distinguished).
360 |         /// O(1)
361 |         /// </summary>
362 |         public TPriority GetPriority(TItem item)
363 |         {
364 |             lock (_queue)
365 |             {
366 |                 SimpleNode findMe = GetExistingNode(item);
367 |                 if(findMe == null)
368 |                 {
369 |                     throw new InvalidOperationException("Cannot call GetPriority() on a node which is not enqueued: " + item);
370 |                 }
371 |                 return findMe.Priority;
372 |             }
373 |         }
374 |
375 |         #region Try* methods for multithreading
376 |         /// Get the head of the queue, without removing it (use TryDequeue() for that).
377 |         /// Useful for multi-threading, where the queue may become empty between calls to Contains() and First
378 |         /// Returns true if successful, false otherwise
379 |         /// O(1)
380 |         public bool TryFirst(out TItem first)
381 |         {
382 |             if (_queue.Count > 0)
383 |             {
384 |                 lock (_queue)
385 |                 {
386 |                     if (_queue.Count > 0)
387 |                     {
388 |                         first =_queue.First.Data;
389 |                         return true;
390 |                     }
391 |                 }
392 |             }
393 |
394 |             first = default(TItem);
395 |             return false;
396 |         }
397 |
398 |         /// <summary>
399 |         /// Removes the head of the queue (node with minimum priority; ties are broken by order of insertion), and sets it to first.
400 |         /// Useful for multi-threading, where the queue may become empty between calls to Contains() and Dequeue()
401 |         /// Returns true if successful; false if queue was empty
402 |         /// O(log n)
403 |         /// </summary>
404 |         public bool TryDequeue(out TItem first)
405 |         {
406 |             if (_queue.Count > 0)
407 |             {
408 |                 lock (_queue)
409 |                 {
410 |                     if (_queue.Count > 0)
411 |                     {
412 |                         SimpleNode node =_queue.Dequeue();
413 |                         first = node.Data;
414 |                         RemoveFromNodeCache(node);
415 |                         return true;
416 |                     }
417 |                 }
418 |             }
419 |
420 |             first = default(TItem);
421 |             return false;
422 |         }
423 |
424 |         /// <summary>
425 |         /// Attempts to remove an item from the queue.  The item does not need to be the head of the queue.  
426 |         /// Useful for multi-threading, where the queue may become empty between calls to Contains() and Remove()
427 |         /// Returns true if the item was successfully removed, false if it wasn't in the queue.
428 |         /// If multiple copies of the item are enqueued, only the first one is removed.
429 |         /// O(log n)
430 |         /// </summary>
431 |         public bool TryRemove(TItem item)
432 |         {
433 |             lock(_queue)
434 |             {
435 |                 SimpleNode removeMe;
436 |                 IList<SimpleNode> nodes;
437 |                 if (item == null)
438 |                 {
439 |                     if (_nullNodesCache.Count == 0)
440 |                     {
441 |                         return false;
442 |                     }
443 |                     removeMe = _nullNodesCache[0];
444 |                     nodes =_nullNodesCache;
445 |                 }
446 |                 else
447 |                 {
448 |                     if (!_itemToNodesCache.TryGetValue(item, out nodes))
449 |                     {
450 |                         return false;
451 |                     }
452 |                     removeMe = nodes[0];
453 |                     if (nodes.Count == 1)
454 |                     {
455 |_itemToNodesCache.Remove(item);
456 |                     }
457 |                 }
458 |                 _queue.Remove(removeMe);
459 |                 nodes.Remove(removeMe);
460 |                 return true;
461 |             }
462 |         }
463 |
464 |         /// <summary>
465 |         /// Call this method to change the priority of an item.
466 |         /// Useful for multi-threading, where the queue may become empty between calls to Contains() and UpdatePriority()
467 |         /// If the item is enqueued multiple times, only the first one will be updated.
468 |         /// (If your requirements are complex enough that you need to enqueue the same item multiple times <i>and</i> be able
469 |         /// to update all of them, please wrap your items in a wrapper class so they can be distinguished).
470 |         /// Returns true if the item priority was updated, false otherwise.
471 |         /// O(log n)
472 |         /// </summary>
473 |         public bool TryUpdatePriority(TItem item, TPriority priority)
474 |         {
475 |             lock(_queue)
476 |             {
477 |                 SimpleNode updateMe = GetExistingNode(item);
478 |                 if(updateMe == null)
479 |                 {
480 |                     return false;
481 |                 }
482 |                 _queue.UpdatePriority(updateMe, priority);
483 |                 return true;
484 |             }
485 |         }
486 |
487 |         /// <summary>
488 |         /// Attempt to get the priority of the given item.
489 |         /// Useful for multi-threading, where the queue may become empty between calls to Contains() and GetPriority()
490 |         /// If the item is enqueued multiple times, only the priority of the first will be returned.
491 |         /// (If your requirements are complex enough that you need to enqueue the same item multiple times <i>and</i> be able
492 |         /// to query all their priorities, please wrap your items in a wrapper class so they can be distinguished).
493 |         /// Returns true if the item was found in the queue, false otherwise
494 |         /// O(1)
495 |         /// </summary>
496 |         public bool TryGetPriority(TItem item, out TPriority priority)
497 |         {
498 |             lock(_queue)
499 |             {
500 |                 SimpleNode findMe = GetExistingNode(item);
501 |                 if(findMe == null)
502 |                 {
503 |                     priority = default(TPriority);
504 |                     return false;
505 |                 }
506 |                 priority = findMe.Priority;
507 |                 return true;
508 |             }
509 |         }
510 |         #endregion
511 |
512 |         public IEnumerator<TItem> GetEnumerator()
513 |         {
514 |             List<TItem> queueData = new List<TItem>();
515 |             lock (_queue)
516 |             {
517 |                 //Copy to a separate list because we don't want to 'yield return' inside a lock
518 |                 foreach(var node in_queue)
519 |                 {
520 |                     queueData.Add(node.Data);
521 |                 }
522 |             }
523 |
524 |             return queueData.GetEnumerator();
525 |         }
526 |
527 |         IEnumerator IEnumerable.GetEnumerator()
528 |         {
529 |             return GetEnumerator();
530 |         }
531 |
532 |         public bool IsValidQueue()
533 |         {
534 |             lock(_queue)
535 |             {
536 |                 // Check all items in cache are in the queue
537 |                 foreach (IList<SimpleNode> nodes in_itemToNodesCache.Values)
538 |                 {
539 |                     foreach (SimpleNode node in nodes)
540 |                     {
541 |                         if (!_queue.Contains(node))
542 |                         {
543 |                             return false;
544 |                         }
545 |                     }
546 |                 }
547 |
548 |                 // Check all items in queue are in cache
549 |                 foreach (SimpleNode node in_queue)
550 |                 {
551 |                     if (GetExistingNode(node.Data) == null)
552 |                     {
553 |                         return false;
554 |                     }
555 |                 }
556 |
557 |                 // Check queue structure itself
558 |                 return _queue.IsValidQueue();
559 |             }
560 |         }
561 |     }
562 |
563 |     /// <summary>
564 |     /// A simplified priority queue implementation.  Is stable, auto-resizes, and thread-safe, at the cost of being slightly slower than
565 |     /// FastPriorityQueue
566 |     /// This class is kept here for backwards compatibility.  It's recommended you use SimplePriorityQueue&lt;TItem, TPriority&gt;
567 |     /// </summary>
568 |     /// <typeparam name="TItem">The type to enqueue</typeparam>
569 |     public class SimplePriorityQueue<TItem> : SimplePriorityQueue<TItem, float>
570 |     {
571 |         /// <summary>
572 |         /// Instantiate a new Priority Queue
573 |         /// </summary>
574 |         public SimplePriorityQueue() { }
575 |
576 |         /// <summary>
577 |         /// Instantiate a new Priority Queue
578 |         /// </summary>
579 |         /// <param name="comparer">The comparer used to compare priority values.  Defaults to Comparer&lt;float&gt;.default</param>
580 |         public SimplePriorityQueue(IComparer<float> comparer) : base(comparer) { }
581 |
582 |         /// <summary>
583 |         /// Instantiate a new Priority Queue
584 |         /// </summary>
585 |         /// <param name="comparer">The comparison function to use to compare priority values</param>
586 |         public SimplePriorityQueue(Comparison<float> comparer) : base(comparer) { }
587 |     }
588 | }
589 | #pragma warning restore

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/StablePriorityQueue.cs
--------------------------------------------------------------------------------

  1 | ﻿#pragma warning disable
  2 | using System;
  3 | using System.Collections;
  4 | using System.Collections.Generic;
  5 | using System.Runtime.CompilerServices;
  6 |
  7 | namespace Priority_Queue
  8 | {
  9 |     /// <summary>
 10 |     /// A copy of FastPriorityQueue which is also stable - that is, when two nodes are enqueued with the same priority, they
 11 |     /// are always dequeued in the same order.
 12 |     /// See https://github.com/BlueRaja/High-Speed-Priority-Queue-for-C-Sharp/wiki/Getting-Started for more information
 13 |     /// </summary>
 14 |     /// <typeparam name="T">The values in the queue.  Must extend the StablePriorityQueueNode class</typeparam>
 15 |     public sealed class StablePriorityQueue<T> : IFixedSizePriorityQueue<T, float>
 16 |         where T : StablePriorityQueueNode
 17 |     {
 18 |         private int_numNodes;
 19 |         private T[] _nodes;
 20 |         private long_numNodesEverEnqueued;
 21 |
 22 |         /// <summary>
 23 |         /// Instantiate a new Priority Queue
 24 |         /// </summary>
 25 |         /// <param name="maxNodes">The max nodes ever allowed to be enqueued (going over this will cause undefined behavior)</param>
 26 |         public StablePriorityQueue(int maxNodes)
 27 |         {
 28 |             #if DEBUG
 29 |             if (maxNodes <= 0)
 30 |             {
 31 |                 throw new InvalidOperationException("New queue size cannot be smaller than 1");
 32 |             }
 33 |             #endif
 34 |
 35 |             _numNodes = 0;
 36 |_nodes = new T[maxNodes + 1];
 37 |             _numNodesEverEnqueued = 0;
 38 |         }
 39 |
 40 |         /// <summary>
 41 |         /// Returns the number of nodes in the queue.
 42 |         /// O(1)
 43 |         /// </summary>
 44 |         public int Count
 45 |         {
 46 |             get
 47 |             {
 48 |                 return_numNodes;
 49 |             }
 50 |         }
 51 |
 52 |         /// <summary>
 53 |         /// Returns the maximum number of items that can be enqueued at once in this queue.  Once you hit this number (ie. once Count == MaxSize),
 54 |         /// attempting to enqueue another item will cause undefined behavior.  O(1)
 55 |         /// </summary>
 56 |         public int MaxSize
 57 |         {
 58 |             get
 59 |             {
 60 |                 return _nodes.Length - 1;
 61 |             }
 62 |         }
 63 |
 64 |         /// <summary>
 65 |         /// Removes every node from the queue.
 66 |         /// O(n) (So, don't do this often!)
 67 |         /// </summary>
 68 |         #if NET_VERSION_4_5
 69 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
 70 |         #endif
 71 |         public void Clear()
 72 |         {
 73 |             Array.Clear(_nodes, 1,_numNodes);
 74 |             _numNodes = 0;
 75 |         }
 76 |
 77 |         /// <summary>
 78 |         /// Returns (in O(1)!) whether the given node is in the queue.
 79 |         /// If node is or has been previously added to another queue, the result is undefined unless oldQueue.ResetNode(node) has been called
 80 |         /// O(1)
 81 |         /// </summary>
 82 |         #if NET_VERSION_4_5
 83 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
 84 |         #endif
 85 |         public bool Contains(T node)
 86 |         {
 87 |             #if DEBUG
 88 |             if(node == null)
 89 |             {
 90 |                 throw new ArgumentNullException("node");
 91 |             }
 92 |             if (node.Queue != null && !Equals(node.Queue))
 93 |             {
 94 |                 throw new InvalidOperationException("node.Contains was called on a node from another queue.  Please call originalQueue.ResetNode() first");
 95 |             }
 96 |             if (node.QueueIndex < 0 || node.QueueIndex >= _nodes.Length)
 97 |             {
 98 |                 throw new InvalidOperationException("node.QueueIndex has been corrupted. Did you change it manually?");
 99 |             }
100 |             #endif
101 |
102 |             return (_nodes[node.QueueIndex] == node);
103 |         }
104 |
105 |         /// <summary>
106 |         /// Enqueue a node to the priority queue.  Lower values are placed in front. Ties are broken by first-in-first-out.
107 |         /// If the queue is full, the result is undefined.
108 |         /// If the node is already enqueued, the result is undefined.
109 |         /// If node is or has been previously added to another queue, the result is undefined unless oldQueue.ResetNode(node) has been called
110 |         /// O(log n)
111 |         /// </summary>
112 |         #if NET_VERSION_4_5
113 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
114 |         #endif
115 |         public void Enqueue(T node, float priority)
116 |         {
117 |             #if DEBUG
118 |             if(node == null)
119 |             {
120 |                 throw new ArgumentNullException("node");
121 |             }
122 |             if(_numNodes >= _nodes.Length - 1)
123 |             {
124 |                 throw new InvalidOperationException("Queue is full - node cannot be added: " + node);
125 |             }
126 |             if (node.Queue != null && !Equals(node.Queue))
127 |             {
128 |                 throw new InvalidOperationException("node.Enqueue was called on a node from another queue.  Please call originalQueue.ResetNode() first");
129 |             }
130 |             if (Contains(node))
131 |             {
132 |                 throw new InvalidOperationException("Node is already enqueued: " + node);
133 |             }
134 |             node.Queue = this;
135 |             #endif
136 |
137 |             node.Priority = priority;
138 |_numNodes++;
139 |             _nodes[_numNodes] = node;
140 |             node.QueueIndex = _numNodes;
141 |             node.InsertionIndex =_numNodesEverEnqueued++;
142 |             CascadeUp(node);
143 |         }
144 |
145 |         //Performance appears to be slightly better when this is NOT inlined o_O
146 |         #if NET_VERSION_4_5
147 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
148 |         #endif
149 |         private void CascadeUp(T node)
150 |         {
151 |             //aka Heapify-up
152 |             int parent;
153 |             if(node.QueueIndex > 1)
154 |             {
155 |                 parent = node.QueueIndex >> 1;
156 |                 T parentNode = _nodes[parent];
157 |                 if(HasHigherPriority(parentNode, node))
158 |                     return;
159 |
160 |                 //Node has lower priority value, so move parent down the heap to make room
161 |_nodes[node.QueueIndex] = parentNode;
162 |                 parentNode.QueueIndex = node.QueueIndex;
163 |
164 |                 node.QueueIndex = parent;
165 |             }
166 |             else
167 |             {
168 |                 return;
169 |             }
170 |             while(parent > 1)
171 |             {
172 |                 parent >>= 1;
173 |                 T parentNode = _nodes[parent];
174 |                 if(HasHigherPriority(parentNode, node))
175 |                     break;
176 |
177 |                 //Node has lower priority value, so move parent down the heap to make room
178 |_nodes[node.QueueIndex] = parentNode;
179 |                 parentNode.QueueIndex = node.QueueIndex;
180 |
181 |                 node.QueueIndex = parent;
182 |             }
183 |             _nodes[node.QueueIndex] = node;
184 |         }
185 |
186 | #if NET_VERSION_4_5
187 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
188 | #endif
189 |         private void CascadeDown(T node)
190 |         {
191 |             //aka Heapify-down
192 |             int finalQueueIndex = node.QueueIndex;
193 |             int childLeftIndex = 2 *finalQueueIndex;
194 |
195 |             // If leaf node, we're done
196 |             if(childLeftIndex > _numNodes)
197 |             {
198 |                 return;
199 |             }
200 |
201 |             // Check if the left-child is higher-priority than the current node
202 |             int childRightIndex = childLeftIndex + 1;
203 |             T childLeft =_nodes[childLeftIndex];
204 |             if(HasHigherPriority(childLeft, node))
205 |             {
206 |                 // Check if there is a right child. If not, swap and finish.
207 |                 if(childRightIndex > _numNodes)
208 |                 {
209 |                     node.QueueIndex = childLeftIndex;
210 |                     childLeft.QueueIndex = finalQueueIndex;
211 |_nodes[finalQueueIndex] = childLeft;
212 |                     _nodes[childLeftIndex] = node;
213 |                     return;
214 |                 }
215 |                 // Check if the left-child is higher-priority than the right-child
216 |                 T childRight =_nodes[childRightIndex];
217 |                 if(HasHigherPriority(childLeft, childRight))
218 |                 {
219 |                     // left is highest, move it up and continue
220 |                     childLeft.QueueIndex = finalQueueIndex;
221 |                     _nodes[finalQueueIndex] = childLeft;
222 |                     finalQueueIndex = childLeftIndex;
223 |                 }
224 |                 else
225 |                 {
226 |                     // right is even higher, move it up and continue
227 |                     childRight.QueueIndex = finalQueueIndex;
228 |_nodes[finalQueueIndex] = childRight;
229 |                     finalQueueIndex = childRightIndex;
230 |                 }
231 |             }
232 |             // Not swapping with left-child, does right-child exist?
233 |             else if(childRightIndex > _numNodes)
234 |             {
235 |                 return;
236 |             }
237 |             else
238 |             {
239 |                 // Check if the right-child is higher-priority than the current node
240 |                 T childRight =_nodes[childRightIndex];
241 |                 if(HasHigherPriority(childRight, node))
242 |                 {
243 |                     childRight.QueueIndex = finalQueueIndex;
244 |                     _nodes[finalQueueIndex] = childRight;
245 |                     finalQueueIndex = childRightIndex;
246 |                 }
247 |                 // Neither child is higher-priority than current, so finish and stop.
248 |                 else
249 |                 {
250 |                     return;
251 |                 }
252 |             }
253 |
254 |             while(true)
255 |             {
256 |                 childLeftIndex = 2* finalQueueIndex;
257 |
258 |                 // If leaf node, we're done
259 |                 if(childLeftIndex >_numNodes)
260 |                 {
261 |                     node.QueueIndex = finalQueueIndex;
262 |                     _nodes[finalQueueIndex] = node;
263 |                     break;
264 |                 }
265 |
266 |                 // Check if the left-child is higher-priority than the current node
267 |                 childRightIndex = childLeftIndex + 1;
268 |                 childLeft =_nodes[childLeftIndex];
269 |                 if(HasHigherPriority(childLeft, node))
270 |                 {
271 |                     // Check if there is a right child. If not, swap and finish.
272 |                     if(childRightIndex > _numNodes)
273 |                     {
274 |                         node.QueueIndex = childLeftIndex;
275 |                         childLeft.QueueIndex = finalQueueIndex;
276 |_nodes[finalQueueIndex] = childLeft;
277 |                         _nodes[childLeftIndex] = node;
278 |                         break;
279 |                     }
280 |                     // Check if the left-child is higher-priority than the right-child
281 |                     T childRight =_nodes[childRightIndex];
282 |                     if(HasHigherPriority(childLeft, childRight))
283 |                     {
284 |                         // left is highest, move it up and continue
285 |                         childLeft.QueueIndex = finalQueueIndex;
286 |                         _nodes[finalQueueIndex] = childLeft;
287 |                         finalQueueIndex = childLeftIndex;
288 |                     }
289 |                     else
290 |                     {
291 |                         // right is even higher, move it up and continue
292 |                         childRight.QueueIndex = finalQueueIndex;
293 |_nodes[finalQueueIndex] = childRight;
294 |                         finalQueueIndex = childRightIndex;
295 |                     }
296 |                 }
297 |                 // Not swapping with left-child, does right-child exist?
298 |                 else if(childRightIndex > _numNodes)
299 |                 {
300 |                     node.QueueIndex = finalQueueIndex;
301 |_nodes[finalQueueIndex] = node;
302 |                     break;
303 |                 }
304 |                 else
305 |                 {
306 |                     // Check if the right-child is higher-priority than the current node
307 |                     T childRight = _nodes[childRightIndex];
308 |                     if(HasHigherPriority(childRight, node))
309 |                     {
310 |                         childRight.QueueIndex = finalQueueIndex;
311 |_nodes[finalQueueIndex] = childRight;
312 |                         finalQueueIndex = childRightIndex;
313 |                     }
314 |                     // Neither child is higher-priority than current, so finish and stop.
315 |                     else
316 |                     {
317 |                         node.QueueIndex = finalQueueIndex;
318 |                         _nodes[finalQueueIndex] = node;
319 |                         break;
320 |                     }
321 |                 }
322 |             }
323 |         }
324 |
325 |         /// <summary>
326 |         /// Returns true if 'higher' has higher priority than 'lower', false otherwise.
327 |         /// Note that calling HasHigherPriority(node, node) (ie. both arguments the same node) will return false
328 |         /// </summary>
329 | #if NET_VERSION_4_5
330 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
331 |         #endif
332 |         private bool HasHigherPriority(T higher, T lower)
333 |         {
334 |             return (higher.Priority < lower.Priority ||
335 |                 (higher.Priority == lower.Priority && higher.InsertionIndex < lower.InsertionIndex));
336 |         }
337 |
338 |         /// <summary>
339 |         /// Removes the head of the queue (node with minimum priority; ties are broken by order of insertion), and returns it.
340 |         /// If queue is empty, result is undefined
341 |         /// O(log n)
342 |         /// </summary>
343 | #if NET_VERSION_4_5
344 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
345 | #endif
346 |         public T Dequeue()
347 |         {
348 |             #if DEBUG
349 |             if(_numNodes <= 0)
350 |             {
351 |                 throw new InvalidOperationException("Cannot call Dequeue() on an empty queue");
352 |             }
353 |
354 |             if(!IsValidQueue())
355 |             {
356 |                 throw new InvalidOperationException("Queue has been corrupted (Did you update a node priority manually instead of calling UpdatePriority()?" +
357 |                                                     "Or add the same node to two different queues?)");
358 |             }
359 |             #endif
360 |
361 |             T returnMe = _nodes[1];
362 |             //If the node is already the last node, we can remove it immediately
363 |             if(_numNodes == 1)
364 |             {
365 |                 _nodes[1] = null;
366 |_numNodes = 0;
367 |                 return returnMe;
368 |             }
369 |
370 |             //Swap the node with the last node
371 |             T formerLastNode = _nodes[_numNodes];
372 |             _nodes[1] = formerLastNode;
373 |             formerLastNode.QueueIndex = 1;
374 |_nodes[_numNodes] = null;
375 |_numNodes--;
376 |
377 |             //Now bubble formerLastNode (which is no longer the last node) down
378 |             CascadeDown(formerLastNode);
379 |             return returnMe;
380 |         }
381 |
382 |         /// <summary>
383 |         /// Resize the queue so it can accept more nodes.  All currently enqueued nodes are remain.
384 |         /// Attempting to decrease the queue size to a size too small to hold the existing nodes results in undefined behavior
385 |         /// O(n)
386 |         /// </summary>
387 |         public void Resize(int maxNodes)
388 |         {
389 |             #if DEBUG
390 |             if (maxNodes <= 0)
391 |             {
392 |                 throw new InvalidOperationException("Queue size cannot be smaller than 1");
393 |             }
394 |
395 |             if (maxNodes < _numNodes)
396 |             {
397 |                 throw new InvalidOperationException("Called Resize(" + maxNodes + "), but current queue contains " +_numNodes + " nodes");
398 |             }
399 |             #endif
400 |
401 |             T[] newArray = new T[maxNodes + 1];
402 |             int highestIndexToCopy = Math.Min(maxNodes, _numNodes);
403 |             Array.Copy(_nodes, newArray, highestIndexToCopy + 1);
404 |             _nodes = newArray;
405 |         }
406 |
407 |         /// <summary>
408 |         /// Returns the head of the queue, without removing it (use Dequeue() for that).
409 |         /// If the queue is empty, behavior is undefined.
410 |         /// O(1)
411 |         /// </summary>
412 |         public T First
413 |         {
414 |             get
415 |             {
416 |                 #if DEBUG
417 |                 if(_numNodes <= 0)
418 |                 {
419 |                     throw new InvalidOperationException("Cannot call .First on an empty queue");
420 |                 }
421 |                 #endif
422 |
423 |                 return _nodes[1];
424 |             }
425 |         }
426 |
427 |         /// <summary>
428 |         /// This method must be called on a node every time its priority changes while it is in the queue.  
429 |         /// <b>Forgetting to call this method will result in a corrupted queue!</b>
430 |         /// Calling this method on a node not in the queue results in undefined behavior
431 |         /// O(log n)
432 |         /// </summary>
433 |         #if NET_VERSION_4_5
434 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
435 |         #endif
436 |         public void UpdatePriority(T node, float priority)
437 |         {
438 |             #if DEBUG
439 |             if(node == null)
440 |             {
441 |                 throw new ArgumentNullException("node");
442 |             }
443 |             if (node.Queue != null && !Equals(node.Queue))
444 |             {
445 |                 throw new InvalidOperationException("node.UpdatePriority was called on a node from another queue");
446 |             }
447 |             if (!Contains(node))
448 |             {
449 |                 throw new InvalidOperationException("Cannot call UpdatePriority() on a node which is not enqueued: " + node);
450 |             }
451 |             #endif
452 |
453 |             node.Priority = priority;
454 |             OnNodeUpdated(node);
455 |         }
456 |
457 | #if NET_VERSION_4_5
458 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
459 | #endif
460 |         private void OnNodeUpdated(T node)
461 |         {
462 |             //Bubble the updated node up or down as appropriate
463 |             int parentIndex = node.QueueIndex >> 1;
464 |
465 |             if(parentIndex > 0 && HasHigherPriority(node,_nodes[parentIndex]))
466 |             {
467 |                 CascadeUp(node);
468 |             }
469 |             else
470 |             {
471 |                 //Note that CascadeDown will be called if parentNode == node (that is, node is the root)
472 |                 CascadeDown(node);
473 |             }
474 |         }
475 |
476 |         /// <summary>
477 |         /// Removes a node from the queue.  The node does not need to be the head of the queue.  
478 |         /// If the node is not in the queue, the result is undefined.  If unsure, check Contains() first
479 |         /// O(log n)
480 |         /// </summary>
481 | #if NET_VERSION_4_5
482 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
483 | #endif
484 |         public void Remove(T node)
485 |         {
486 | #if DEBUG
487 |             if(node == null)
488 |             {
489 |                 throw new ArgumentNullException("node");
490 |             }
491 |             if (node.Queue != null && !Equals(node.Queue))
492 |             {
493 |                 throw new InvalidOperationException("node.Remove was called on a node from another queue");
494 |             }
495 |             if (!Contains(node))
496 |             {
497 |                 throw new InvalidOperationException("Cannot call Remove() on a node which is not enqueued: " + node);
498 |             }
499 | #endif
500 |
501 |             //If the node is already the last node, we can remove it immediately
502 |             if(node.QueueIndex ==_numNodes)
503 |             {
504 |                 _nodes[_numNodes] = null;
505 |                 _numNodes--;
506 |                 return;
507 |             }
508 |
509 |             //Swap the node with the last node
510 |             T formerLastNode =_nodes[_numNodes];
511 |_nodes[node.QueueIndex] = formerLastNode;
512 |             formerLastNode.QueueIndex = node.QueueIndex;
513 |             _nodes[_numNodes] = null;
514 |             _numNodes--;
515 |
516 |             //Now bubble formerLastNode (which is no longer the last node) up or down as appropriate
517 |             OnNodeUpdated(formerLastNode);
518 |         }
519 |
520 |         /// <summary>
521 |         /// By default, nodes that have been previously added to one queue cannot be added to another queue.
522 |         /// If you need to do this, please call originalQueue.ResetNode(node) before attempting to add it in the new queue
523 |         /// </summary>
524 | #if NET_VERSION_4_5
525 |         [MethodImpl(MethodImplOptions.AggressiveInlining)]
526 | #endif
527 |         public void ResetNode(T node)
528 |         {
529 | #if DEBUG
530 |             if (node == null)
531 |             {
532 |                 throw new ArgumentNullException("node");
533 |             }
534 |             if (node.Queue != null && !Equals(node.Queue))
535 |             {
536 |                 throw new InvalidOperationException("node.ResetNode was called on a node from another queue");
537 |             }
538 |             if (Contains(node))
539 |             {
540 |                 throw new InvalidOperationException("node.ResetNode was called on a node that is still in the queue");
541 |             }
542 |
543 |             node.Queue = null;
544 | #endif
545 |
546 |             node.QueueIndex = 0;
547 |         }
548 |
549 |
550 |         public IEnumerator<T> GetEnumerator()
551 |         {
552 | #if NET_VERSION_4_5 // ArraySegment does not implement IEnumerable before 4.5
553 |             IEnumerable<T> e = new ArraySegment<T>(_nodes, 1, _numNodes);
554 |             return e.GetEnumerator();
555 | #else
556 |             for(int i = 1; i <=_numNodes; i++)
557 |                 yield return _nodes[i];
558 | #endif
559 |         }
560 |
561 |         IEnumerator IEnumerable.GetEnumerator()
562 |         {
563 |             return GetEnumerator();
564 |         }
565 |
566 |         /// <summary>
567 |         /// <b>Should not be called in production code.</b>
568 |         /// Checks to make sure the queue is still in a valid state.  Used for testing/debugging the queue.
569 |         /// </summary>
570 |         public bool IsValidQueue()
571 |         {
572 |             for(int i = 1; i <_nodes.Length; i++)
573 |             {
574 |                 if(_nodes[i] != null)
575 |                 {
576 |                     int childLeftIndex = 2 * i;
577 |                     if(childLeftIndex <_nodes.Length && _nodes[childLeftIndex] != null && HasHigherPriority(_nodes[childLeftIndex], _nodes[i]))
578 |                         return false;
579 |
580 |                     int childRightIndex = childLeftIndex + 1;
581 |                     if(childRightIndex <_nodes.Length && _nodes[childRightIndex] != null && HasHigherPriority(_nodes[childRightIndex], _nodes[i]))
582 |                         return false;
583 |                 }
584 |             }
585 |             return true;
586 |         }
587 |     }
588 | }
589 | #pragma warning restore

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/StablePriorityQueueNode.cs
--------------------------------------------------------------------------------

 1 | ﻿#pragma warning disable
 2 | namespace Priority_Queue
 3 | {
 4 |     public class StablePriorityQueueNode : FastPriorityQueueNode
 5 |     {
 6 |         /// <summary>
 7 |         /// Represents the order the node was inserted in
 8 |         /// </summary>
 9 |         public long InsertionIndex { get; internal set; }
10 |     }
11 | }
12 | #pragma warning restore

--------------------------------------------------------------------------------

/MountainGoap/PriorityQueue/packages.config
--------------------------------------------------------------------------------

1 | ﻿<?xml version="1.0" encoding="utf-8"?>
2 | <packages>
3 |   <package id="NuGet.CommandLine" version="2.8.6" targetFramework="net45" developmentDependency="true" />
4 | </packages>

--------------------------------------------------------------------------------

/MountainGoap/Sensor.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="Sensor.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     using System;
 7 |     using System.Reflection;
 8 |
 9 |     /// <summary>
10 |     /// Sensor for getting information about world state.
11 |     /// </summary>
12 |     public class Sensor {
13 |         /// <summary>
14 |         /// Name of the sensor.
15 |         /// </summary>
16 |         public readonly string Name;
17 |
18 |         /// <summary>
19 |         /// Callback to be executed when the sensor runs.
20 |         /// </summary>
21 |         private readonly SensorRunCallback runCallback;
22 |
23 |         /// <summary>
24 |         /// Initializes a new instance of the <see cref="Sensor"/> class.
25 |         /// </summary>
26 |         /// <param name="runCallback">Callback to be executed when the sensor runs.</param>
27 |         /// <param name="name">Name of the sensor.</param>
28 |         public Sensor(SensorRunCallback runCallback, string? name = null) {
29 |             Name = name ??
quot;Sensor {Guid.NewGuid()} ({runCallback.GetMethodInfo().Name})";
30 |             this.runCallback = runCallback;
31 |         }
32 |
33 |         /// <summary>
34 |         /// Event that triggers when a sensor runs.
35 |         /// </summary>
36 |         public static event SensorRunEvent OnSensorRun = (agent, sensor) => { };
37 |
38 |         /// <summary>
39 |         /// Runs the sensor during a game loop.
40 |         /// </summary>
41 |         /// <param name="agent">Agent for which the sensor is being run.</param>
42 |         public void Run(Agent agent) {
43 |             OnSensorRun(agent, this);
44 |             runCallback(agent);
45 |         }
46 |     }
47 | }

--------------------------------------------------------------------------------

/MountainGoap/StepMode.cs
--------------------------------------------------------------------------------

 1 | ﻿// <copyright file="StepMode.cs" company="Chris Muller">
 2 | // Copyright (c) Chris Muller. All rights reserved.
 3 | // </copyright>
 4 |
 5 | namespace MountainGoap {
 6 |     /// <summary>
 7 |     /// Different modes with which MountainGoap can execute an agent step.
 8 |     /// </summary>
 9 |     public enum StepMode {
10 |         /// <summary>
11 |         /// Default step mode. Runs async, doesn't necessitate taking action.
12 |         /// </summary>
13 |         Default = 1,
14 |
15 |         /// <summary>
16 |         /// Turn-based step mode, plans synchronously, executes at least one action if possible.
17 |         /// </summary>
18 |         OneAction = 2,
19 |
20 |         /// <summary>
21 |         /// Turn-based step mode, plans synchronously, executes all actions in planned action sequence.
22 |         /// </summary>
23 |         AllActions = 3
24 |     }
25 | }
26 |

--------------------------------------------------------------------------------

/MountainGoap/stylecop.json
--------------------------------------------------------------------------------

 1 | ﻿{
 2 |   // ACTION REQUIRED: This file was automatically added to your project, but it
 3 |   // will not take effect until additional steps are taken to enable it. See the
 4 |   // following page for additional information:
 5 |   //
 6 |   // <https://github.com/DotNetAnalyzers/StyleCopAnalyzers/blob/master/documentation/EnableConfiguration.md>
 7 |
 8 |   "$schema": "<https://raw.githubusercontent.com/DotNetAnalyzers/StyleCopAnalyzers/master/StyleCop.Analyzers/StyleCop.Analyzers/Settings/stylecop.schema.json>",
 9 |   "settings": {
10 |     "documentationRules": {
11 |       "companyName": "Chris Muller",
12 |       "copyrightText": "Copyright (c) Chris Muller. All rights reserved."
13 |     }
14 |   }
15 | }
16 |

--------------------------------------------------------------------------------

/MountainGoapLogging/DefaultLogger.cs
--------------------------------------------------------------------------------

 1 | ﻿namespace MountainGoapLogging {
 2 |     using MountainGoap;
 3 |     using Serilog;
 4 |     using Serilog.Core;
 5 |     using System.Collections.Concurrent;
 6 |
 7 |     public class DefaultLogger {
 8 |         private readonly Logger logger;
 9 |
10 |         public DefaultLogger(bool logToConsole = true, string? loggingFile = null) {
11 |             var config = new LoggerConfiguration();
12 |             if (logToConsole) config.WriteTo.Console();
13 |             if (loggingFile != null) config.WriteTo.File(loggingFile);
14 |             Agent.OnAgentActionSequenceCompleted += OnAgentActionSequenceCompleted;
15 |             Agent.OnAgentStep += OnAgentStep;
16 |             Agent.OnPlanningStarted += OnPlanningStarted;
17 |             Agent.OnPlanningStartedForSingleGoal += OnPlanningStartedForSingleGoal;
18 |             Agent.OnPlanningFinished += OnPlanningFinished;
19 |             Agent.OnPlanningFinishedForSingleGoal += OnPlanningFinishedForSingleGoal;
20 |             Agent.OnPlanUpdated += OnPlanUpdated;
21 |             Agent.OnEvaluatedActionNode += OnEvaluatedActionNode;
22 |             Action.OnBeginExecuteAction += OnBeginExecuteAction;
23 |             Action.OnFinishExecuteAction += OnFinishExecuteAction;
24 |             Sensor.OnSensorRun += OnSensorRun;
25 |             logger = config.CreateLogger();
26 |         }
27 |
28 |         private void OnEvaluatedActionNode(ActionNode node, ConcurrentDictionary<ActionNode, ActionNode> nodes) {
29 |             var cameFromList = new List<ActionNode>();
30 |             var traceback = node;
31 |             while (nodes.ContainsKey(traceback) && traceback.Action != nodes[traceback].Action) {
32 |                 cameFromList.Add(traceback);
33 |                 traceback = nodes[traceback];
34 |             }
35 |             cameFromList.Reverse();
36 |             logger.Information("Evaluating node {node} with {count} nodes leading to it.", node.Action?.Name, cameFromList.Count - 1);
37 |         }
38 |
39 |         private void OnPlanUpdated(Agent agent, List<Action> actionList) {
40 |             logger.Information("Agent {agent} has a new plan:", agent.Name);
41 |             var count = 1;
42 |             foreach (var action in actionList) {
43 |                 logger.Information("\tStep #{count}: {action}", count, action.Name);
44 |                 count++;
45 |             }
46 |         }
47 |
48 |         private void OnAgentActionSequenceCompleted(Agent agent) {
49 |             logger.Information("Agent {agent} completed action sequence.", agent.Name);
50 |         }
51 |
52 |         private void OnAgentStep(Agent agent) {
53 |             logger.Information("Agent {agent} is working.", agent.Name);
54 |         }
55 |
56 |         private void OnBeginExecuteAction(Agent agent, Action action, Dictionary<string, object?> parameters) {
57 |             logger.Information("Agent {agent} began executing action {action}.", agent.Name, action.Name);
58 |             if (parameters.Count == 0) return;
59 |             logger.Information("\tAction parameters:");
60 |             foreach (var kvp in parameters) logger.Information("\t\t{key}: {value}", kvp.Key, kvp.Value);
61 |         }
62 |
63 |         private void OnFinishExecuteAction(Agent agent, Action action, ExecutionStatus status, Dictionary<string, object?> parameters) {
64 |             logger.Information("Agent {agent} finished executing action {action} with status {status}.", agent.Name, action.Name, status);
65 |         }
66 |
67 |         private void OnPlanningFinished(Agent agent, BaseGoal? goal, float utility) {
68 |             if (goal is null) logger.Warning("Agent {agent} finished planning and found no possible goal.", agent.Name);
69 |             else logger.Information("Agent {agent} finished planning with goal {goal}, utility value {utility}.", agent.Name, goal.Name, utility);
70 |         }
71 |
72 |         private void OnPlanningStartedForSingleGoal(Agent agent, BaseGoal goal) {
73 |             logger.Information("Agent {agent} started planning for goal {goal}.", agent.Name, goal.Name);
74 |         }
75 |         private void OnPlanningFinishedForSingleGoal(Agent agent, BaseGoal goal, float utility) {
76 |             logger.Information("Agent {agent} finished planning for goal {goal}, utility value {utility}.", agent.Name, goal.Name, utility);
77 |         }
78 |
79 |         private void OnPlanningStarted(Agent agent) {
80 |             logger.Information("Agent {agent} started planning.", agent.Name);
81 |         }
82 |
83 |         private void OnSensorRun(Agent agent, Sensor sensor) {
84 |             logger.Information("Agent {agent} ran sensor {sensor}.", agent.Name, sensor.Name);
85 |         }
86 |     }
87 | }
88 |

--------------------------------------------------------------------------------

/MountainGoapLogging/MountainGoapLogging.csproj
--------------------------------------------------------------------------------

 1 | ﻿<Project Sdk="Microsoft.NET.Sdk">
 2 |
 3 |   <PropertyGroup>
 4 |  <TargetFramework>netstandard2.1</TargetFramework>
 5 |  <LangVersion>10.0</LangVersion>
 6 |     <ImplicitUsings>enable</ImplicitUsings>
 7 |     <Nullable>enable</Nullable>
 8 |  <GenerateAssemblyInfo>false</GenerateAssemblyInfo>
 9 |   </PropertyGroup>
10 |
11 |   <ItemGroup>
12 |     <PackageReference Include="Serilog" Version="2.12.0" />
13 |     <PackageReference Include="Serilog.Sinks.Console" Version="4.1.0" />
14 |     <PackageReference Include="Serilog.Sinks.File" Version="5.0.0" />
15 |   </ItemGroup>
16 |
17 |   <ItemGroup>
18 |     <ProjectReference Include="..\MountainGoap\MountainGoap.csproj" />
19 |   </ItemGroup>
20 |
21 | </Project>
22 |

--------------------------------------------------------------------------------

/MountainGoapTest/ActionContinuationTests.cs
--------------------------------------------------------------------------------

 1 | ﻿namespace MountainGoapTest {
 2 |     using System.Collections.Concurrent;
 3 |     using System.Collections.Generic;
 4 |
 5 |     public class ActionContinuationTests {
 6 |         [Fact]
 7 |         public void ItCanContinueActions() {
 8 |             var timesExecuted = 0;
 9 |             var agent = new Agent(
10 |                 state: new() {
11 |                     { "key", false },
12 |                     { "progress", 0 }
13 |                 },
14 |                 goals: new List<BaseGoal> {
15 |                     new Goal(
16 |                         desiredState: new() {
17 |                             { "key", true }
18 |                         }
19 |                     )
20 |                 },
21 |                 actions: new List<Action> {
22 |                     new Action(
23 |                         preconditions: new() {
24 |                             { "key", false }
25 |                         },
26 |                         postconditions: new() {
27 |                             { "key", true }
28 |                         },
29 |                         executor: (Agent agent, Action action) => {
30 |                             timesExecuted++;
31 |                             if (agent.State["progress"] is int progress && progress < 3) {
32 |                                 agent.State["progress"] = progress + 1;
33 |                                 return ExecutionStatus.Executing;
34 |                             }
35 |                             else return ExecutionStatus.Succeeded;
36 |                         }
37 |                     )
38 |                 }
39 |             );
40 |             agent.Step(StepMode.OneAction);
41 |             if (agent.State["key"] is bool value) Assert.False(value);
42 |             else Assert.False(true);
43 |             agent.Step(StepMode.OneAction);
44 |             if (agent.State["key"] is bool value2) Assert.False(value2);
45 |             else Assert.False(true);
46 |             agent.Step(StepMode.OneAction);
47 |             if (agent.State["key"] is bool value3) Assert.False(value3);
48 |             else Assert.False(true);
49 |             agent.Step(StepMode.OneAction);
50 |             if (agent.State["key"] is bool value4) Assert.True(value4);
51 |             else Assert.False(true);
52 |             Assert.Equal(4, timesExecuted);
53 |         }
54 |     }
55 | }
56 |

--------------------------------------------------------------------------------

/MountainGoapTest/ActionNodeTests.cs
--------------------------------------------------------------------------------

  1 | ﻿namespace MountainGoapTest {
  2 |     using System.Collections.Generic;
  3 |
  4 |     public class AgentTests {
  5 |         [Fact]
  6 |         public void ItHandlesInitialNullStateValuesCorrectly() {
  7 |             var agent = new Agent(
  8 |                 state: new() {
  9 |                     { "key", null }
 10 |                 },
 11 |                 goals: new List<BaseGoal> {
 12 |                     new Goal(
 13 |                         desiredState: new() {
 14 |                             { "key", "non-null value" }
 15 |                         }
 16 |                     )
 17 |                 },
 18 |                 actions: new List<Action> {
 19 |                     new Action(
 20 |                         preconditions: new() {
 21 |                             { "key", null }
 22 |                         },
 23 |                         postconditions: new() {
 24 |                             { "key", "non-null value" }
 25 |                         },
 26 |                         executor: (Agent agent, Action action) => {
 27 |                             return ExecutionStatus.Succeeded;
 28 |                         }
 29 |                     )
 30 |                 }
 31 |             );
 32 |             agent.Step(StepMode.OneAction);
 33 |             Assert.NotNull(agent.State["key"]);
 34 |         }
 35 |
 36 |         [Fact]
 37 |         public void ItHandlesNullGoalsCorrectly() {
 38 |             var agent = new Agent(
 39 |                 state: new() {
 40 |                     { "key", "non-null value" }
 41 |                 },
 42 |                 goals: new List<BaseGoal> {
 43 |                     new Goal(
 44 |                         desiredState: new() {
 45 |                             { "key", null }
 46 |                         }
 47 |                     )
 48 |                 },
 49 |                 actions: new List<Action> {
 50 |                     new Action(
 51 |                         preconditions: new() {
 52 |                             { "key", "non-null value" }
 53 |                         },
 54 |                         postconditions: new() {
 55 |                             { "key", null }
 56 |                         },
 57 |                         executor: (Agent agent, Action action) => {
 58 |                             return ExecutionStatus.Succeeded;
 59 |                         }
 60 |                     )
 61 |                 }
 62 |             );
 63 |             agent.Step(StepMode.OneAction);
 64 |             Assert.Null(agent.State["key"]);
 65 |         }
 66 |
 67 |         [Fact]
 68 |         public void ItHandlesNonNullStateValuesCorrectly() {
 69 |             var agent = new Agent(
 70 |                 state: new() {
 71 |                     { "key", "value" }
 72 |                 },
 73 |                 goals: new List<BaseGoal> {
 74 |                     new Goal(
 75 |                         desiredState: new() {
 76 |                             { "key", "new value" }
 77 |                         }
 78 |                     )
 79 |                 },
 80 |                 actions: new List<Action> {
 81 |                     new Action(
 82 |                         preconditions: new() {
 83 |                             { "key", "value" }
 84 |                         },
 85 |                         postconditions: new() {
 86 |                             { "key", "new value" }
 87 |                         },
 88 |                         executor: (Agent agent, Action action) => {
 89 |                             return ExecutionStatus.Succeeded;
 90 |                         }
 91 |                     )
 92 |                 }
 93 |             );
 94 |             agent.Step(StepMode.OneAction);
 95 |             object? value = agent.State["key"];
 96 |             Assert.NotNull(value);
 97 |             if (value is not null) Assert.Equal("new value", (string)value);
 98 |         }
 99 |
100 |         [Fact]
101 |         public void ItExecutesOneActionInOneActionStepMode() {
102 |             var actionCount = 0;
103 |             var agent = new Agent(
104 |                 state: new() {
105 |                     { "key", "value" }
106 |                 },
107 |                 goals: new List<BaseGoal> {
108 |                     new Goal(
109 |                         desiredState: new() {
110 |                             { "key", "new value" }
111 |                         }
112 |                     )
113 |                 },
114 |                 actions: new List<Action> {
115 |                     new Action(
116 |                         preconditions: new() {
117 |                             { "key", "value" }
118 |                         },
119 |                         postconditions: new() {
120 |                             { "key", "new value" }
121 |                         },
122 |                         executor: (Agent agent, Action action) => {
123 |                             actionCount++;
124 |                             return ExecutionStatus.Succeeded;
125 |                         }
126 |                     )
127 |                 }
128 |             );
129 |             agent.Step(StepMode.OneAction);
130 |             Assert.Equal(1, actionCount);
131 |         }
132 |
133 |         [Fact]
134 |         public void ItExecutesAllActionsInAllActionsStepMode() {
135 |             var actionCount = 0;
136 |             var agent = new Agent(
137 |                 state: new() {
138 |                     { "key", "value" }
139 |                 },
140 |                 goals: new List<BaseGoal> {
141 |                     new Goal(
142 |                         desiredState: new() {
143 |                             { "key", "new value" }
144 |                         }
145 |                     )
146 |                 },
147 |                 actions: new List<Action> {
148 |                     new Action(
149 |                         preconditions: new() {
150 |                             { "key", "value" }
151 |                         },
152 |                         postconditions: new() {
153 |                             { "key", "intermediate value" }
154 |                         },
155 |                         executor: (Agent agent, Action action) => {
156 |                             actionCount++;
157 |                             return ExecutionStatus.Succeeded;
158 |                         }
159 |                     ),
160 |                     new Action(
161 |                         preconditions: new() {
162 |                             { "key", "intermediate value" }
163 |                         },
164 |                         postconditions: new() {
165 |                             { "key", "new value" }
166 |                         },
167 |                         executor: (Agent agent, Action action) => {
168 |                             actionCount++;
169 |                             return ExecutionStatus.Succeeded;
170 |                         }
171 |                     )
172 |                 }
173 |             );
174 |             agent.Step(StepMode.AllActions);
175 |             Assert.Equal(2, actionCount);
176 |         }
177 |     }
178 | }
179 |

--------------------------------------------------------------------------------

/MountainGoapTest/ArithmeticPostconditionsTests.cs
--------------------------------------------------------------------------------

 1 | ﻿using System;
 2 | using System.Collections.Generic;
 3 | using System.Linq;
 4 | using System.Text;
 5 | using System.Threading.Tasks;
 6 |
 7 | namespace MountainGoapTest
 8 | {
 9 |     public class ArithmeticPostconditionsTests
10 |     {
11 |         [Fact]
12 |         public void MinimalExampleTest()
13 |         {
14 |
15 |             List<BaseGoal> goals = new() {
16 |                 new ComparativeGoal(
17 |                     name: "Goal1",
18 |                     desiredState: new() {
19 |                         { "i", new ComparisonValuePair {
20 |                             Value = 100,
21 |                             Operator = ComparisonOperator.GreaterThan
22 |                         } }
23 |                     },
24 |                     weight: 1f
25 |                 ),
26 |             };
27 |
28 |             List<MountainGoap.Action> actions = new() {
29 |                 new MountainGoap.Action(
30 |                     name: "Action1",
31 |                     executor: (Agent agent, MountainGoap.Action action) => {
32 |                         return ExecutionStatus.Succeeded;
33 |                     },
34 |                     arithmeticPostconditions: new Dictionary<string, object> {
35 |                         { "i", 10 }
36 |                     },
37 |                     cost: 0.5f
38 |                 ),
39 |             };
40 |
41 |             Agent agent = new(
42 |                 goals: goals,
43 |                 actions: actions,
44 |                 state: new() {
45 |                     { "i", 0 }
46 |                 }
47 |             );
48 |
49 |             agent.Step(StepMode.OneAction);
50 |             Assert.Equal(10, agent.State["i"]);
51 |             agent.Step(StepMode.OneAction);
52 |             Assert.Equal(20, agent.State["i"]);
53 |         }
54 |     }
55 | }
56 |

--------------------------------------------------------------------------------

/MountainGoapTest/MountainGoapTest.csproj
--------------------------------------------------------------------------------

 1 | <Project Sdk="Microsoft.NET.Sdk">
 2 |
 3 |   <PropertyGroup>
 4 |     <TargetFramework>net6.0</TargetFramework>
 5 |     <Nullable>enable</Nullable>
 6 |
 7 |     <IsPackable>false</IsPackable>
 8 |   </PropertyGroup>
 9 |
10 |   <ItemGroup>
11 |     <PackageReference Include="Microsoft.NET.Test.Sdk" Version="16.11.0" />
12 |     <PackageReference Include="xunit" Version="2.4.1" />
13 |     <PackageReference Include="xunit.runner.visualstudio" Version="2.4.3">
14 |       <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
15 |       <PrivateAssets>all</PrivateAssets>
16 |     </PackageReference>
17 |     <PackageReference Include="coverlet.collector" Version="3.1.0">
18 |       <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
19 |       <PrivateAssets>all</PrivateAssets>
20 |     </PackageReference>
21 |   </ItemGroup>
22 |
23 |   <ItemGroup>
24 |     <ProjectReference Include="..\MountainGoap\MountainGoap.csproj" />
25 |   </ItemGroup>
26 |
27 | </Project>
28 |

--------------------------------------------------------------------------------

/MountainGoapTest/PermutationSelectorGeneratorTests.cs
--------------------------------------------------------------------------------

 1 | ﻿namespace MountainGoapTest {
 2 |     using System.Collections.Concurrent;
 3 |     using System.Collections.Generic;
 
 4 |
 5 |     public class PermutationSelectorGeneratorTests {
 6 |         [Fact]
 7 |         public void ItSelectsFromACollection() {
 8 |             var collection = new List<int> { 1, 2, 3 };
 9 |             var selector = PermutationSelectorGenerators.SelectFromCollection(collection);
10 |             List<object> permutations = selector(new ConcurrentDictionary<string, object?>());
11 |             Assert.Equal(3, permutations.Count);
12 |         }
13 |
14 |         [Fact]
15 |         public void ItSelectsFromACollectionInState() {
16 |             var collection = new List<int> { 1, 2, 3 };
17 |             var selector = PermutationSelectorGenerators.SelectFromCollectionInState<int>("collection");
18 |             List<object> permutations = selector(new ConcurrentDictionary<string, object?> { { "collection", collection } });
19 |             Assert.Equal(3, permutations.Count);
20 |         }
21 |
22 |         [Fact]
23 |         public void ItSelectsFromAnIntegerRange() {
24 |             var selector = PermutationSelectorGenerators.SelectFromIntegerRange(1, 4);
25 |             List<object> permutations = selector(new ConcurrentDictionary<string, object?>());
26 |             Assert.Equal(3, permutations.Count);
27 |         }
28 |     }
29 | }
30 |

--------------------------------------------------------------------------------

/MountainGoapTest/PermutationSelectorTests.cs
--------------------------------------------------------------------------------

 1 | ﻿namespace MountainGoapTest {
 2 |     using System.Collections.Generic;
 3 |
 4 |     public class PermutationSelectorTests {
 5 |         [Fact]
 6 |         public void ItSelectsFromADynamicallyGeneratedCollectionInState() {
 7 |             var collection = new List<int> { 1, 2, 3 };
 8 |             var selector = PermutationSelectorGenerators.SelectFromCollectionInState<int>("collection");
 9 |             var agent = new Agent(
10 |                 name: "sample agent",
11 |                 state: new() {
12 |                     { "collection", collection },
13 |                     { "goalAchieved", false }
14 |                 },
15 |                 goals: new() {
16 |                     new Goal(
17 |                         name: "sample goal",
18 |                         desiredState: new Dictionary<string, object?> {
19 |                             { "goalAchieved", true }
20 |                         }
21 |                     )
22 |                 },
23 |                 actions: new() {
24 |                     new(
25 |                         name: "sample action",
26 |                         cost: 1f,
27 |                         preconditions: new() {
28 |                             { "goalAchieved", false }
29 |                         },
30 |                         postconditions: new() {
31 |                             { "goalAchieved", true }
32 |                         },
33 |                         executor: (agent, action) => { return ExecutionStatus.Succeeded; }
34 |                     )
35 |                 },
36 |                 sensors: new() {
37 |                     new(
38 |                         (agent) => {
39 |                             if (agent.State["collection"] is List<int> collection) {
40 |                                 collection.Add(4);
41 |                             }
42 |                         },
43 |                         name: "sample sensor"
44 |                     )
45 |                 }
46 |             );
47 |             List<object> permutations = selector(agent.State);
48 |             Assert.Equal(3, permutations.Count);
49 |             agent.Step(StepMode.OneAction);
50 |             permutations = selector(agent.State);
51 |             Assert.Equal(4, permutations.Count);
52 |             agent.Step(StepMode.OneAction);
53 |             permutations = selector(agent.State);
54 |             Assert.Equal(5, permutations.Count);
55 |         }
56 |     }
57 | }
58 |

--------------------------------------------------------------------------------

/MountainGoapTest/Usings.cs
--------------------------------------------------------------------------------

1 | global using Xunit;
2 | global using MountainGoap;
3 |

--------------------------------------------------------------------------------

</csharp>
