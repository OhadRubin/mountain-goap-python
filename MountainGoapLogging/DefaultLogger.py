# // <copyright file="DefaultLogger.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Any, Optional, List
import logging
import sys

# Assume MountainGoap is installed or accessible via PYTHONPATH
# from MountainGoap import Agent, Action, Sensor, ExecutionStatus, BaseGoal
# from MountainGoap.Internals.ActionNode import ActionNode
# For this structure, we'll use relative imports assuming the project root is the base.
from MountainGoap.Agent import Agent
from MountainGoap.Action import Action
from MountainGoap.Sensor import Sensor
from MountainGoap.ExecutionStatus import ExecutionStatus
from MountainGoap.BaseGoal import BaseGoal
from MountainGoap.Internals.ActionNode import ActionNode

# Instead of Serilog, we'll use Python's built-in `logging` module.
# Serilog's structured logging features can be mimicked using f-strings or extra dict in Python's logging.
class DefaultLogger:
    def __init__(self, log_to_console: bool = True, logging_file: Optional[str] = None):
        # Configure basic logging. In a real application, you might want more sophisticated setup.
        # Python's logging.Logger is not directly analogous to Serilog.Core.Logger
        # Serilog's Logger configures sinks, while Python's Logger manages handlers.
        self.logger = logging.getLogger("MountainGoapLogger")
        self.logger.setLevel(logging.INFO)
        # Prevent adding handlers multiple times if instantiated repeatedly
        if not self.logger.handlers:
            if log_to_console:
                console_handler = logging.StreamHandler(sys.stdout)
                formatter = logging.Formatter('%(levelname)s: %(message)s')
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)

            if logging_file is not None:
                file_handler = logging.FileHandler(logging_file)
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
        
        # Register Python methods to C# static events
        Agent.register_on_agent_action_sequence_completed(self._on_agent_action_sequence_completed)
        Agent.register_on_agent_step(self._on_agent_step)
        Agent.register_on_planning_started(self._on_planning_started)
        Agent.register_on_planning_started_for_single_goal(self._on_planning_started_for_single_goal)
        Agent.register_on_planning_finished(self._on_planning_finished)
        Agent.register_on_planning_finished_for_single_goal(self._on_planning_finished_for_single_goal)
        Agent.register_on_plan_updated(self._on_plan_updated)
        Agent.register_on_evaluated_action_node(self._on_evaluated_action_node)
        
        Action.register_on_begin_execute_action(self._on_begin_execute_action)
        Action.register_on_finish_execute_action(self._on_finish_execute_action)
        
        Sensor.register_on_sensor_run(self._on_sensor_run)


    def _on_evaluated_action_node(self, node: ActionNode, nodes: Dict[ActionNode, ActionNode]) -> None:
        came_from_list: List[ActionNode] = []
        traceback_node: Optional[ActionNode] = node
        
        # Reconstruct path. The C# logic `traceback.Action != nodes[traceback].Action` is tricky.
        # In astar.CameFrom, `CameFrom[start] = start`.
        # So we trace back until we hit the start node (where its predecessor is itself).
        # Or until the action is None (for the conceptual start node).
        while traceback_node is not None and traceback_node in nodes and traceback_node != nodes[traceback_node]:
            came_from_list.append(traceback_node)
            traceback_node = nodes[traceback_node]
        
        # Add the start node itself if it was the origin of the path
        if traceback_node is not None and traceback_node not in came_from_list:
            came_from_list.append(traceback_node)

        came_from_list.reverse() # Order from start to current node
        
        # C# logs count - 1, likely excluding the 'start' node or the evaluated node itself.
        # If came_from_list includes start and end, path length is len - 1.
        # If 'node' itself is counted as the end, and we're looking at steps leading *to* it.
        # The start node itself has 0 steps leading to it.
        # Example: start -> A -> B. Evaluating B. Path [start, A, B]. Count is 3. Path steps: 2.
        num_steps_leading_to_it = len(came_from_list) - 1
        
        self.logger.info(f"Evaluating node {node.Action.Name if node.Action else 'No Action'} with {num_steps_leading_to_it} nodes leading to it.")


    def _on_plan_updated(self, agent: Agent, action_list: List[Action]) -> None:
        self.logger.info(f"Agent {agent.Name} has a new plan:")
        for i, action in enumerate(action_list):
            self.logger.info(f"\tStep #{i+1}: {action.Name}")

    def _on_agent_action_sequence_completed(self, agent: Agent) -> None:
        self.logger.info(f"Agent {agent.Name} completed action sequence.")

    def _on_agent_step(self, agent: Agent) -> None:
        self.logger.info(f"Agent {agent.Name} is working.")

    def _on_begin_execute_action(self, agent: Agent, action: Action, parameters: Dict[str, Optional[Any]]) -> None:
        self.logger.info(f"Agent {agent.Name} began executing action {action.Name}.")
        if parameters:
            self.logger.info("\tAction parameters:")
            for key, value in parameters.items():
                self.logger.info(f"\t\t{key}: {value}")

    def _on_finish_execute_action(self, agent: Agent, action: Action, status: ExecutionStatus, parameters: Dict[str, Optional[Any]]) -> None:
        self.logger.info(f"Agent {agent.Name} finished executing action {action.Name} with status {status.name}.")

    def _on_planning_finished(self, agent: Agent, goal: Optional[BaseGoal], utility: float) -> None:
        if goal is None:
            self.logger.warning(f"Agent {agent.Name} finished planning and found no possible goal.")
        else:
            self.logger.info(f"Agent {agent.Name} finished planning with goal {goal.Name}, utility value {utility}.")

    def _on_planning_started_for_single_goal(self, agent: Agent, goal: BaseGoal) -> None:
        self.logger.info(f"Agent {agent.Name} started planning for goal {goal.Name}.")

    def _on_planning_finished_for_single_goal(self, agent: Agent, goal: BaseGoal, utility: float) -> None:
        self.logger.info(f"Agent {agent.Name} finished planning for goal {goal.Name}, utility value {utility}.")

    def _on_planning_started(self, agent: Agent) -> None:
        self.logger.info(f"Agent {agent.Name} started planning.")

    def _on_sensor_run(self, agent: Agent, sensor: Sensor) -> None:
        self.logger.info(f"Agent {agent.Name} ran sensor {sensor.Name}.")

