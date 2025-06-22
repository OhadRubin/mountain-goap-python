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

# --- Callback Delegates (Consolidated) ---
CostCallback = Callable[["Action", StateDictionary], float]
ExecutorCallback = Callable[["Agent", "Action"], "ExecutionStatus"]
PermutationSelectorCallback = Callable[[StateDictionary], List[Any]]
SensorRunCallback = Callable[["Agent"], None]
StateCheckerCallback = Callable[["Action", StateDictionary], bool]
StateCostDeltaMultiplierCallback = Callable[[Optional["Action"], str], float]
StateMutatorCallback = Callable[["Action", StateDictionary], None]

# --- Event Delegates (Consolidated) ---
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
class FastPriorityQueueNode:
    Priority: float
    QueueIndex: int

    def __init__(self):
        self.Priority = 0.0
        self.QueueIndex = 0


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
            # if action_node.Action is None:
            #     return False
            for key, comparison_value_pair in goal.DesiredState.items():
                # C# explicitly checks for key in both actionNode.State and current.State
                if key not in action_node.State:
                    return False  # Key must exist in action_node's state
                if key not in current.State:
                    print(f"FIX4 DEBUG: ComparativeGoal key '{key}' missing from current.State - would cause KeyError")
                    assert False
                    return False  # Added check for current.State - this is the fix!
                
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
        
        # Add debugging for A* search
        is_debug_search = False
        if hasattr(start.State, 'get') and (start.State.get('faction') == 'enemy' or start.State.get('faction') == 'player'):
            is_debug_search = start.State.get("food_eaten") == 4
            if is_debug_search:
                print(f"    A* DEBUG: Starting search for goal {goal.Name}")
                print(f"      Start state: food_eaten={start.State.get('food_eaten')}, well_rested={start.State.get('well_rested')}, stretched={start.State.get('stretched')}")
                print(f"      Limits: cost_maximum={cost_maximum}, step_maximum={step_maximum}")
                print(f"      Available actions: {[node.Action.Name for node in graph.ActionNodes if node.Action]}")
                print(f"      Actions that could work for this state:")
                for node in graph.ActionNodes:
                    if node.Action and node.Action.is_possible(start.State):
                        print(f"        {node.Action.Name} - preconditions satisfied")
                    else:
                        print(f"        {node.Action.Name} - preconditions NOT satisfied")
        
        frontier = FastPriorityQueue(100000)  # Increased from 100k to 1M
        frontier.enqueue(start, 0.0)
        self.CameFrom[start] = start
        self.CostSoFar[start] = 0.0
        self.StepsSoFar[start] = 0
        nodes_explored = 0
        
        while frontier.count > 0:
            current = frontier.dequeue()
            nodes_explored += 1
            
            if is_debug_search and nodes_explored <= 5:
                print(f"      A* exploring node {nodes_explored}: action={current.Action.Name if current.Action else 'START'}")
                print(f"        State: food_eaten={current.State.get('food_eaten')}, well_rested={current.State.get('well_rested')}, stretched={current.State.get('stretched')}")
                
            if self._meets_goal(current, start):
                if is_debug_search:
                    print(f"      A* FOUND GOAL at node {nodes_explored}!")
                self.FinalPoint = current
                break
                
            neighbor_count = 0
            for next_node in graph.neighbors(current):
                neighbor_count += 1
                if is_debug_search and nodes_explored <= 3:
                    print(f"        Neighbor {neighbor_count}: {next_node.Action.Name if next_node.Action else 'None'}")
                    
                action_cost = next_node.cost(current.State)
                new_cost = self.CostSoFar[current] + action_cost
                new_step_count = self.StepsSoFar[current] + 1
                if new_cost > cost_maximum or new_step_count > step_maximum:
                    if is_debug_search and nodes_explored <= 3:
                        print(f"          Rejected: cost {new_cost} > {cost_maximum} or steps {new_step_count} > {step_maximum}")
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
                    if is_debug_search and nodes_explored <= 3:
                        print(f"          Added to frontier with priority {priority}")
                        
            if is_debug_search and nodes_explored <= 5:
                print(f"        Generated {neighbor_count} neighbors, frontier size: {frontier.count}")
                
        if is_debug_search:
            print(f"      A* search complete: explored {nodes_explored} nodes, final frontier size: {frontier.count}")
            print(f"      Goal found: {self.FinalPoint is not None}")
            if self.FinalPoint is None:
                print(f"      Search ended without finding goal - no more nodes to explore")
        elif nodes_explored > 100:
            print(f"    A* WARNING: Explored {nodes_explored} nodes, might be infinite loop!")

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
                    print(f"FIX4 DEBUG: Heuristic - key '{key}' missing from states, adding inf cost")
                    assert False
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


class Planner:
    """
    Planner for an agent.
    """

    @staticmethod
    def plan(agent: "Agent", cost_maximum: float, step_maximum: int) -> None:
        if "Monster" in agent.Name or "Player" in agent.Name:
            print(f"PLANNER DEBUG: Starting planning for {agent.Name}")
            if "Player" in agent.Name:
                print(f"  Player state: food_eaten={agent.State.get('food_eaten')}, well_rested={agent.State.get('well_rested')}, stretched={agent.State.get('stretched')}")
        Agent.OnPlanningStarted(agent)
        best_plan_utility = 0.0
        best_astar: Optional[ActionAStar] = None
        best_goal: Optional["BaseGoal"] = None
        for goal in agent.Goals:
            if "Monster" in agent.Name or "Player" in agent.Name:
                print(f"  Planning for goal: {goal.Name}")
            Agent.OnPlanningStartedForSingleGoal(agent, goal)
            graph = ActionGraph(agent.Actions, agent.State)
            start_node = ActionNode(None, agent.State, {})
            astar_result = ActionAStar(
                graph, start_node, goal, cost_maximum, step_maximum
            )
            cursor = astar_result.FinalPoint
            current_goal_utility = 0.0
            if cursor is not None:
                if "Monster" in agent.Name or "Player" in agent.Name:
                    print(f"    A* found solution for {goal.Name}")
            else:
                if "Monster" in agent.Name or "Player" in agent.Name:
                    print(f"    A* found NO solution for {goal.Name}")
            if cursor is not None:
                plan_cost = astar_result.CostSoFar.get(cursor, 0.0)

                if "Monster" in agent.Name or "Player" in agent.Name:
                    print(f"    UTILITY DEBUG: {goal.Name} - plan_cost={plan_cost}, goal.Weight={goal.Weight}")
                    print(f"    UTILITY DEBUG: cursor.Action={cursor.Action.Name if cursor.Action else 'None'}")

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

                if "Monster" in agent.Name or "Player" in agent.Name:
                    print(f"    UTILITY DEBUG: comparison_utility={comparison_utility}, best_plan_utility={best_plan_utility}")
                    print(f"    UTILITY DEBUG: cursor.Action is not None: {cursor.Action is not None}")
                    print(f"    UTILITY DEBUG: comparison_utility > best_plan_utility: {comparison_utility > best_plan_utility}")

                if cursor.Action is not None and comparison_utility > best_plan_utility:
                    if "Monster" in agent.Name or "Player" in agent.Name:
                        print(f"    UTILITY DEBUG: NEW BEST PLAN SELECTED for {goal.Name}")
                    best_plan_utility = comparison_utility
                    best_astar = astar_result
                    best_goal = goal
                else:
                    if "Monster" in agent.Name or "Player" in agent.Name:
                        print(f"    UTILITY DEBUG: Plan REJECTED for {goal.Name}")
                        if cursor.Action is None:
                            print(f"      Reason: cursor.Action is None")
                        elif not (comparison_utility > best_plan_utility):
                            print(f"      Reason: utility {comparison_utility} <= best {best_plan_utility}")
            else:
                Agent.OnPlanningFinishedForSingleGoal(agent, goal, 0.0)
        if "Monster" in agent.Name:
            print(f"  FINAL PLAN SELECTION: best_plan_utility={best_plan_utility}")
            print(f"    best_plan_utility > 0: {best_plan_utility > 0}")
            print(f"    best_astar is not None: {best_astar is not None}")
            print(f"    best_goal is not None: {best_goal is not None}")
            print(f"    best_astar.FinalPoint is not None: {best_astar.FinalPoint is not None if best_astar else 'N/A'}")
            
        if (
            best_plan_utility > 0
            and best_astar is not None
            and best_goal is not None
            and best_astar.FinalPoint is not None
        ):
            if "Monster" in agent.Name:
                print(f"  PLAN ACCEPTED: Updating action list for {best_goal.Name}")
            Planner._update_agent_action_list(best_astar.FinalPoint, best_astar, agent)
            agent.IsBusy = True
            Agent.OnPlanningFinished(agent, best_goal, best_plan_utility)
        else:
            if "Monster" in agent.Name:
                print(f"  PLAN REJECTED: No valid plan found")
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
class BaseGoal:
    Name: str
    Weight: float

    def __init__(self, name: str = None, weight: float = 1.0):
        self.Name = name if name is not None else f"Goal {uuid.uuid4()}"
        self.Weight = weight


class ComparisonOperator(Enum):
    Undefined = 0
    Equals = 1
    LessThan = 2
    LessThanOrEquals = 3
    GreaterThan = 4
    GreaterThanOrEquals = 5


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


class ExecutionStatus(Enum):
    NotYetExecuted = 1
    Executing = 2
    Succeeded = 3
    Failed = 4
    NotPossible = 5


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


class StepMode(Enum):
    Default = 1
    OneAction = 2
    AllActions = 3


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
            return [{}]  # Actions without selectors get one empty permutation

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
        print(f"DEBUG: {self.Name} step() called, mode={mode}")
        Agent.OnAgentStep(self)
        for sensor in self.Sensors:
            sensor.run(self)
        if mode == StepMode.Default:
            print(f"DEBUG: {self.Name} taking default async path")
            self._step_async()
            return
        print(f"DEBUG: {self.Name} IsBusy={self.IsBusy}, will plan if not busy")
        if not self.IsBusy:
            print(f"DEBUG: {self.Name} calling planner")
            if "Monster" in self.Name:
                print(f"  Monster state: canSeeEnemies={self.State.get('canSeeEnemies')}, canSeeFood={self.State.get('canSeeFood')}, nearEnemy={self.State.get('nearEnemy')}, nearFood={self.State.get('nearFood')}")
                print(f"  Monster goals: {[g.Name for g in self.Goals]}")
                print(f"  Monster actions: {[a.Name for a in self.Actions]}")
            Planner.plan(self, self.CostMaximum, self.StepMaximum)
        if mode == StepMode.OneAction:
            print(f"DEBUG: {self.Name} executing one action")
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
        print(f"DEBUG: {self.Name}._execute() called, sequences count: {len(self.CurrentActionSequences)}")
        if len(self.CurrentActionSequences) > 0:
            cullable_sequences = []
            for sequence in self.CurrentActionSequences:
                if len(sequence) > 0:
                    action_to_execute = sequence[0]
                    print(f"{self.Name} executing action: {action_to_execute.Name}")
                    execution_status = action_to_execute.execute(self)
                    print(f"{self.Name} action {action_to_execute.Name} status: {execution_status}")
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
            print(f"DEBUG: {self.Name} has no action sequences to execute")
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
            print(f"{agent_instance.Name} moving toward {target_agent.Name} from {agent_position} to {new_position}")
            if RpgUtils.in_distance(new_position, target_position, 1.0):
                print(f"{agent_instance.Name} reached {target_agent.Name}!")
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
            new_position = Vector2(new_x, new_y)
            agent_instance.State["position"] = new_position
            print(f"{agent_instance.Name} searching for food, moved from {agent_position} to {new_position}")
        can_see_food = agent_instance.State.get("canSeeFood")
        if isinstance(can_see_food, bool) and can_see_food:
            print(f"{agent_instance.Name} found food!")
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
                agent_instance.State["food_eaten"] = food_eaten + 1
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
                name="Get exactly 5 food",
                weight=1.0,
                desired_state={
                    "food_eaten": ComparisonValuePair(
                        operator=ComparisonOperator.Equals, value=3
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
        def rest_executor(agent_instance, action_instance):
            print(f"{agent_instance.Name} is resting")
            return ExecutionStatus.Succeeded
            
        rest_action = Action(
            name="Rest",
            executor=rest_executor,
            preconditions={"well_rested": False},
            postconditions={"well_rested": True, "stretched": False},
        )
        
        def walk_around_executor(agent_instance, action_instance):
            print(f"{agent_instance.Name} is walking around")
            return ExecutionStatus.Succeeded
            
        walk_around_action = Action(
            name="Walk Around",
            executor=walk_around_executor,
            preconditions={"stretched": False},
            postconditions={"stretched": True, "well_rested": False},
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
                "well_rested": False,
                "stretched": False,
                "sight_range": 10.0,
                "food_sight_range": 20.0,
            },
            goals=[
                food_goal,
                remove_enemies_goal,
                Goal(
                    name="Get well rested", weight=0.11, desired_state={"well_rested": True}
                ),
                Goal(
                    name="Get stretched", weight=0.1, desired_state={"stretched": True}
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
                walk_around_action,
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
        # Initialize monster state
        agent.State.update({
            "canSeeFood": False,
            "nearFood": False,
            "eatingFood": False,
            "foodPositions": food_positions,
            "hp": 2,
            "sight_range": 5.0,
            "food_sight_range": 5.0
        })

        agent.Goals.append(eat_food_goal)
        agent.Sensors.extend([see_food_sensor, food_proximity_sensor])
        agent.Actions.extend([go_to_food_action, look_for_food_action, eat_action])
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

        for _ in range(3):
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
                        print(f"DEBUG: Processing agent {agent.Name}, IsBusy={agent.IsBusy}, IsPlanning={agent.IsPlanning}")
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
