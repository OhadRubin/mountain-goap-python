from typing import Any, Dict, Iterable, Optional, List
from .types import StateDictionary
from .utils import PriorityQueueNode, PriorityQueue, DictionaryExtensionMethods, Utils
from .actions import Action
from .goals import BaseGoal, Goal, ExtremeGoal, ComparativeGoal, ComparisonOperator

class ActionNode(PriorityQueueNode):
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

        frontier = PriorityQueue(100000)
        frontier.enqueue(start, 0.0)
        self.CameFrom[start] = start
        self.CostSoFar[start] = 0.0
        self.StepsSoFar[start] = 0
        nodes_explored = 0

        while frontier.count > 0:
            current = frontier.dequeue()
            nodes_explored += 1

            if self._meets_goal(current, start):
                self.FinalPoint = current
                break

            neighbor_count = 0
            for next_node in graph.neighbors(current):
                neighbor_count += 1

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
                    (__import__(".agent", fromlist=["Agent"]).Agent.OnEvaluatedActionNode)(next_node, self.CameFrom)

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
                else:  # minimize
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

    @staticmethod
    def plan(agent: "Agent", cost_maximum: float, step_maximum: int) -> None:
        from .agent import Agent
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
                    comparison_utility = float("inf")
                elif (
                    plan_cost == 0 and goal.Weight <= 0
                ):  # Handle Weight 0 or negative with 0 cost, resulting in NaN or -inf in C#
                    comparison_utility = (
                        float("nan") if goal.Weight == 0 else float("-inf")
                    )

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
        from .agent import Agent
        action_list: List["Action"] = []
        while (
            cursor is not None
            and cursor.Action is not None
            and cursor in astar.CameFrom
        ):
            action_list.append(cursor.Action)
            prev_cursor = astar.CameFrom.get(cursor)
            # C# relies on `cursor.Action != null` (where start node has null action) to terminate.
            # Remove the extra check for `cursor == prev_cursor` to match C#'s more implicit termination.
            cursor = prev_cursor
        action_list.reverse()
        agent.CurrentActionSequences.append(action_list)
        Agent.OnPlanUpdated(agent, action_list)


