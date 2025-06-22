# // <copyright file="Planner.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import List, Optional, Dict, TYPE_CHECKING
from .ActionAStar import ActionAStar
from .ActionGraph import ActionGraph
from .ActionNode import ActionNode
from ..Action import Action
from ..BaseGoal import BaseGoal

if TYPE_CHECKING:
    from ..Agent import Agent

class Planner:
    """
    Planner for an agent.
    """

    @staticmethod
    def plan(agent: 'Agent', cost_maximum: float, step_maximum: int) -> None:
        """
        Makes a plan to achieve the agent's goals.
        """
        # Ensure agent is imported to access its static event methods
        # from ..Agent import Agent # Already imported at module level for type hints.

        # Import Agent locally to avoid circular import
        from ..Agent import Agent
        Agent.OnPlanningStarted(agent) # Trigger static event

        best_plan_utility = 0.0
        best_astar: Optional[ActionAStar] = None
        best_goal: Optional[BaseGoal] = None

        for goal in agent.Goals:
            Agent.OnPlanningStartedForSingleGoal(agent, goal) # Trigger static event

            # Create an ActionGraph based on the current agent's state and available actions
            graph = ActionGraph(agent.Actions, agent.State)
            
            # The A* start node represents the initial state with no action yet taken.
            # Its action is None, but its state is the agent's current state.
            start_node = ActionNode(None, agent.State, {})
            
            astar_result = ActionAStar(graph, start_node, goal, cost_maximum, step_maximum)
            
            cursor = astar_result.FinalPoint

            current_goal_utility = 0.0
            if cursor is not None:
                # Calculate utility for this goal's plan
                # Utility = GoalWeight / PlanCost (if cost is not zero)
                plan_cost = astar_result.CostSoFar.get(cursor, 0.0) # Get cost to final point
                if plan_cost == 0.0 and cursor != start_node: # If cost is 0 but it's not the start node (meaning a path exists with 0 cost actions)
                    current_goal_utility = float('inf') # Effectively infinite utility for a free plan
                elif plan_cost > 0.0:
                    current_goal_utility = goal.Weight / plan_cost
                # If plan_cost is 0 and it's just the start_node, it implies goal is already met with 0 cost, so utility should be high.
                # If plan_cost is 0 but path exists (cursor is not start_node), also effectively infinite utility.
                # If plan_cost is 0 and cursor is start_node, meaning goal already met.
                
                # C# logic: if cost is 0, utility is 0. This seems like a simplification.
                # let's follow C# verbatim
                if cursor is not None and plan_cost == 0:
                    current_goal_utility = 0.0 # Strict verbatim for this line
                elif cursor is not None:
                    current_goal_utility = goal.Weight / plan_cost

                # Trigger event for finishing planning for single goal
                Agent.OnPlanningFinishedForSingleGoal(agent, goal, current_goal_utility)

                # Update best plan if current one has higher utility
                if current_goal_utility > best_plan_utility:
                    best_plan_utility = current_goal_utility
                    best_astar = astar_result
                    best_goal = goal
            else:
                # If cursor is None, no path was found for this goal.
                Agent.OnPlanningFinishedForSingleGoal(agent, goal, 0.0) # Utility 0 for no path

        # After checking all goals, finalize the best plan
        if best_plan_utility > 0 and best_astar is not None and best_goal is not None and best_astar.FinalPoint is not None:
            Planner._update_agent_action_list(best_astar.FinalPoint, best_astar, agent)
            agent.IsBusy = True
            Agent.OnPlanningFinished(agent, best_goal, best_plan_utility)
        else:
            Agent.OnPlanningFinished(agent, None, 0.0) # No valid plan found

        agent.IsPlanning = False # Planning is complete

    @staticmethod
    def _update_agent_action_list(start_node: ActionNode, astar: ActionAStar, agent: 'Agent') -> None:
        """
        Updates the agent action list with the new plan.
        """
        # Import Agent lazily to avoid circular dependency at module import time
        from ..Agent import Agent  # noqa: WPS433

        cursor: Optional[ActionNode] = start_node
        action_list: List[Action] = []

        # Reconstruct path by traversing CameFrom dictionary backwards from FinalPoint
        # Stop when cursor is the initial 'start' node (which has a None action)
        while cursor is not None and cursor != astar.CameFrom[cursor]: # astar.CameFrom[start_node] == start_node
            if cursor.Action is not None:
                action_list.append(cursor.Action)
            cursor = astar.CameFrom.get(cursor)
            # If a cycle is detected or path breaks before start_node,
            # this loop might become infinite or stop prematurely.
            # astar.CameFrom guarantees a path back to 'start_node' if 'FinalPoint' is reachable.
            
        action_list.reverse() # Reverse to get actions in chronological order

        agent.CurrentActionSequences.clear() # Clear any existing plans
        agent.CurrentActionSequences.append(action_list)
        Agent.OnPlanUpdated(agent, action_list) # Trigger static event

