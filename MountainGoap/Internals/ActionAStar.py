# // <copyright file="ActionAStar.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Any, Optional, List, cast
from math import inf
from datetime import datetime, timedelta

from ..PriorityQueue.FastPriorityQueue import FastPriorityQueue
from ..PriorityQueue.FastPriorityQueueNode import FastPriorityQueueNode # To derive ActionNode from this.
from .ActionNode import ActionNode
from .ActionGraph import ActionGraph
from ..BaseGoal import BaseGoal
from ..Goal import Goal
from ..ExtremeGoal import ExtremeGoal
from ..ComparativeGoal import ComparativeGoal
from ..ComparisonOperator import ComparisonOperator
from .Utils import Utils

# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

class ActionAStar:
    """
    AStar calculator for an action graph.
    """

    FinalPoint: Optional[ActionNode] = None

    CostSoFar: Dict[ActionNode, float] = {} # Using standard dict for simplicity in Python

    StepsSoFar: Dict[ActionNode, int] = {} # Using standard dict for simplicity in Python

    CameFrom: Dict[ActionNode, ActionNode] = {} # Using standard dict for simplicity in Python

    _goal: BaseGoal

    def __init__(self, graph: ActionGraph, start: ActionNode, goal: BaseGoal, cost_maximum: float, step_maximum: int):
        """
        Initializes a new instance of the ActionAStar class.
        """
        from ..Agent import Agent # Local import to avoid circular dependency

        self._goal = goal
        # The C# FastPriorityQueue expects nodes to inherit from FastPriorityQueueNode.
        # ActionNode already does, so this is consistent.
        frontier = FastPriorityQueue[ActionNode](100000) # Max nodes for queue
        frontier.enqueue(start, 0.0)

        self.CameFrom[start] = start # A* uses start to point to itself to signify the beginning
        self.CostSoFar[start] = 0.0
        self.StepsSoFar[start] = 0

        while frontier.count > 0:
            current = frontier.dequeue()

            if self._meets_goal(current, start): # Note: C# original passes 'start' as 'current' to MeetsGoal, which is the prior state.
                                                  # This is a bit confusing but implies current is the state *before* `current.Action` is applied.
                                                  # Let's adjust `_meets_goal` to take `previous_node` appropriately.
                                                  # For the start node, `current` is the `previous_node` for its subsequent actions.
                                                  # The goal condition should be checked on `current.State` (state *after* current action is done).
                self.FinalPoint = current
                break
            
            for next_node in graph.neighbors(current): # graph.neighbors generates nodes where the action's effects are *already applied*
                # The cost of 'next_node' is the cost of its action given the state *before* that action (which is `current.State`)
                action_cost = next_node.cost(current.State) # Cost of the action in `next_node` when taken from `current.State`
                new_cost = self.CostSoFar[current] + action_cost
                new_step_count = self.StepsSoFar[current] + 1

                if new_cost > cost_maximum or new_step_count > step_maximum:
                    continue

                # If `next_node` is not in `CostSoFar` OR a cheaper path to `next_node` is found
                if next_node not in self.CostSoFar or new_cost < self.CostSoFar[next_node]:
                    self.CostSoFar[next_node] = new_cost
                    self.StepsSoFar[next_node] = new_step_count
                    
                    # Heuristic needs to estimate cost from `next_node.State` to goal.
                    # The `current` argument to Heuristic in C# appears to be the *previous* node in the path (e.g., `current` here).
                    # So, `Heuristic(next, goal, current)` means heuristic from `next.State` towards goal, influenced by `current.State` as the immediate prior state.
                    priority = new_cost + self._heuristic(next_node, goal, current)
                    
                    # If next_node is already in frontier but with higher priority, UpdatePriority is called.
                    if frontier.contains(next_node):
                        frontier.update_priority(next_node, priority)
                    else:
                        frontier.enqueue(next_node, priority)
                    
                    self.CameFrom[next_node] = current
                    Agent.OnEvaluatedActionNode(next_node, self.CameFrom) # Trigger static event

    def _heuristic(self, action_node: ActionNode, goal: BaseGoal, previous_node_in_path: ActionNode) -> float:
        """
        Calculates the heuristic cost from actionNode.State to the goal.
        """
        from ..Action import Action # Local import

        cost = 0.0
        
        if isinstance(goal, Goal):
            # For a normal goal, count how many desired state keys are NOT met
            # This is a simple count-mismatch heuristic.
            for key, desired_value in goal.DesiredState.items():
                if key not in action_node.State or action_node.State[key] != desired_value:
                    cost += 1.0 # Each unmet condition adds 1 to heuristic cost
        elif isinstance(goal, ExtremeGoal):
            # For extreme goals, heuristic encourages movement towards the extreme.
            # Reward: subtract cost if moving in desired direction.
            # Penalty: add cost if moving in undesired direction or not moving enough.
            for key, maximize in goal.DesiredState.items():
                value_diff_multiplier = (action_node.Action.StateCostDeltaMultiplier if action_node.Action else Action.default_state_cost_delta_multiplier)(action_node.Action, key)
                
                if key not in action_node.State or key not in previous_node_in_path.State:
                    cost += inf # Cannot determine progress without both states
                    continue

                current_val = action_node.State[key]
                prev_val = previous_node_in_path.State[key]
                
                if current_val is None or prev_val is None:
                    # If any value is None, it's hard to compare numerically, consider it a high cost.
                    cost += inf
                    continue
                
                # Convert to float for numeric comparison, similar to C# Convert.ToSingle
                try:
                    current_val_f = float(current_val)
                    prev_val_f = float(prev_val)
                except (ValueError, TypeError):
                    cost += inf # Not a comparable numeric type
                    continue
                
                value_diff = current_val_f - prev_val_f

                if maximize:
                    if Utils.is_lower_than_or_equals(current_val, prev_val):
                        # Not improving or getting worse, penalize.
                        # C# `cost -= valueDiff * valueDiffMultiplier;` for maximize when is_higher_than_or_equals
                        # This means if current > prev, (current-prev) is positive, so cost reduces.
                        # If current == prev, (current-prev) is 0, no change.
                        # If current < prev, (current-prev) is negative, so cost increases.
                        # This means it's a "reward" for moving in the right direction.
                        # For a heuristic, we want to estimate *remaining* cost.
                        # If we're not moving positively (or maximizing), the "remaining" cost is higher.
                        # So, if not moving toward max, we add penalty proportional to how much we didn't move.
                        # The C# heuristic here is actually a negative "reward" which reduces the priority.
                        # To reflect this, if we're maximizing and the value increased, we subtract, meaning it's "closer".
                        # If we're maximizing and the value decreased, we add, meaning it's "further".
                        cost -= value_diff * value_diff_multiplier # Encourage increase
                    else: # current_val < prev_val
                        # Moving away from the goal, this path is worse.
                        cost += abs(value_diff) * value_diff_multiplier # Penalize decrease
                else: # minimize
                    if Utils.is_higher_than_or_equals(current_val, prev_val):
                        # Not improving or getting worse, penalize.
                        # C# `cost += valueDiff * valueDiffMultiplier;` for minimize when is_lower_than_or_equals
                        # This means if current < prev, (current-prev) is negative, cost reduces.
                        # If current == prev, (current-prev) is 0, no change.
                        # If current > prev, (current-prev) is positive, cost increases.
                        cost += value_diff * value_diff_multiplier # Encourage decrease
                    else: # current_val > prev_val
                        # Moving away from the goal, this path is worse.
                        cost += abs(value_diff) * value_diff_multiplier # Penalize increase


        elif isinstance(goal, ComparativeGoal):
            # For comparative goals, heuristic encourages movement towards meeting the comparison.
            # Penalize by how far away it is or if moving in wrong direction.
            for key, comp_value_pair in goal.DesiredState.items():
                value_diff_multiplier = (action_node.Action.StateCostDeltaMultiplier if action_node.Action else Action.default_state_cost_delta_multiplier)(action_node.Action, key)

                if key not in action_node.State or key not in previous_node_in_path.State:
                    cost += inf
                    continue

                current_val = action_node.State[key]
                desired_val = comp_value_pair.Value
                operator = comp_value_pair.Operator

                if current_val is None or desired_val is None:
                    if operator != ComparisonOperator.Undefined:
                        cost += inf # Cannot compare if values are None
                        continue

                # Ensure values are comparable for arithmetic difference
                try:
                    current_val_f = float(current_val)
                    desired_val_f = float(desired_val) if desired_val is not None else float('nan') # Handle None case for desired_val
                    prev_val_f = float(previous_node_in_path.State[key])
                except (ValueError, TypeError):
                    current_val_f = float('nan') # Mark as non-numeric if conversion fails
                    prev_val_f = float('nan')

                # This valueDiff2 in C# is Math.Abs(Convert.ToSingle(actionNode.State[kvp.Key]) - Convert.ToSingle(current.State[kvp.Key]))
                # It's the absolute change from previous state. This seems more like a penalty for *change* rather than *distance to goal*.
                # Calculate the absolute difference from the previous step so we can penalize moving away from the goal.
                value_diff_from_previous_step = abs(current_val_f - prev_val_f)
                if operator == ComparisonOperator.Undefined:
                    cost += inf
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

    def _meets_goal(self, action_node: ActionNode, previous_node_in_path: ActionNode) -> bool:
        """
        Indicates whether or not a goal is met by an action node.
        This is the terminal condition for A*.
        """
        return Utils.meets_goal(self._goal, action_node, previous_node_in_path)

