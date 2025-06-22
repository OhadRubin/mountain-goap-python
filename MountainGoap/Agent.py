# // <copyright file="Agent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import uuid
from typing import Dict, Any, Optional, List
import threading # For Thread and ConcurrentDictionary behavior (though we use plain dict)

from .BaseGoal import BaseGoal
from .Action import Action
from .Sensor import Sensor
from .StepMode import StepMode
from .ExecutionStatus import ExecutionStatus
from .Internals.Planner import Planner
from .Internals.ActionNode import ActionNode # For event type hints

from .Events.AgentActionSequenceCompletedEvent import AgentActionSequenceCompletedEvent
from .Events.AgentStepEvent import AgentStepEvent
from .Events.PlanningStartedEvent import PlanningStartedEvent
from .Events.PlanningStartedForSingleGoalEvent import PlanningStartedForSingleGoalEvent
from .Events.PlanningFinishedForSingleGoalEvent import PlanningFinishedForSingleGoalEvent
from .Events.PlanningFinishedEvent import PlanningFinishedEvent
from .Events.PlanUpdatedEvent import PlanUpdatedEvent
from .Events.EvaluatedActionNodeEvent import EvaluatedActionNodeEvent

# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

class Agent:
    """
    GOAP agent.
    """

    Name: str

    CurrentActionSequences: List[List[Action]]

    State: StateDictionary

    Memory: Dict[str, Optional[Any]]

    Goals: List[BaseGoal]

    Actions: List[Action]

    Sensors: List[Sensor]

    CostMaximum: float

    StepMaximum: int

    IsBusy: bool = False

    IsPlanning: bool = False

    # Events (class attributes, handlers stored in lists)
    _on_agent_step_handlers: List[AgentStepEvent] = []
    _on_agent_action_sequence_completed_handlers: List[AgentActionSequenceCompletedEvent] = []
    _on_planning_started_handlers: List[PlanningStartedEvent] = []
    _on_planning_started_for_single_goal_handlers: List[PlanningStartedForSingleGoalEvent] = []
    _on_planning_finished_for_single_goal_handlers: List[PlanningFinishedForSingleGoalEvent] = []
    _on_planning_finished_handlers: List[PlanningFinishedEvent] = []
    _on_plan_updated_handlers: List[PlanUpdatedEvent] = []
    _on_evaluated_action_node_handlers: List[EvaluatedActionNodeEvent] = []

    # C# events are public static, Python equivalent is a classmethod that invokes handlers
    @classmethod
    def OnAgentStep(cls, agent: 'Agent'):
        for handler in cls._on_agent_step_handlers:
            handler(agent)

    @classmethod
    def OnAgentActionSequenceCompleted(cls, agent: 'Agent'):
        for handler in cls._on_agent_action_sequence_completed_handlers:
            handler(agent)

    @classmethod
    def OnPlanningStarted(cls, agent: 'Agent'):
        for handler in cls._on_planning_started_handlers:
            handler(agent)

    @classmethod
    def OnPlanningStartedForSingleGoal(cls, agent: 'Agent', goal: BaseGoal):
        for handler in cls._on_planning_started_for_single_goal_handlers:
            handler(agent, goal)

    @classmethod
    def OnPlanningFinishedForSingleGoal(cls, agent: 'Agent', goal: BaseGoal, utility: float):
        for handler in cls._on_planning_finished_for_single_goal_handlers:
            handler(agent, goal, utility)

    @classmethod
    def OnPlanningFinished(cls, agent: 'Agent', goal: Optional[BaseGoal], utility: float):
        for handler in cls._on_planning_finished_handlers:
            handler(agent, goal, utility)

    @classmethod
    def OnPlanUpdated(cls, agent: 'Agent', action_list: List[Action]):
        for handler in cls._on_plan_updated_handlers:
            handler(agent, action_list)

    @classmethod
    def OnEvaluatedActionNode(cls, node: ActionNode, nodes: Dict[ActionNode, ActionNode]):
        for handler in cls._on_evaluated_action_node_handlers:
            handler(node, nodes)
    
    # Registration methods for external logging/monitoring to attach handlers
    @classmethod
    def register_on_agent_step(cls, handler: AgentStepEvent): cls._on_agent_step_handlers.append(handler)
    @classmethod
    def register_on_agent_action_sequence_completed(cls, handler: AgentActionSequenceCompletedEvent): cls._on_agent_action_sequence_completed_handlers.append(handler)
    @classmethod
    def register_on_planning_started(cls, handler: PlanningStartedEvent): cls._on_planning_started_handlers.append(handler)
    @classmethod
    def register_on_planning_started_for_single_goal(cls, handler: PlanningStartedForSingleGoalEvent): cls._on_planning_started_for_single_goal_handlers.append(handler)
    @classmethod
    def register_on_planning_finished_for_single_goal(cls, handler: PlanningFinishedForSingleGoalEvent): cls._on_planning_finished_for_single_goal_handlers.append(handler)
    @classmethod
    def register_on_planning_finished(cls, handler: PlanningFinishedEvent): cls._on_planning_finished_handlers.append(handler)
    @classmethod
    def register_on_plan_updated(cls, handler: PlanUpdatedEvent): cls._on_plan_updated_handlers.append(handler)
    @classmethod
    def register_on_evaluated_action_node(cls, handler: EvaluatedActionNodeEvent): cls._on_evaluated_action_node_handlers.append(handler)


    def __init__(self,
                 name: Optional[str] = None,
                 state: Optional[StateDictionary] = None,
                 memory: Optional[Dict[str, Optional[Any]]] = None,
                 goals: Optional[List[BaseGoal]] = None,
                 actions: Optional[List[Action]] = None,
                 sensors: Optional[List[Sensor]] = None,
                 cost_maximum: float = float('inf'), # float.MaxValue in C#
                 step_maximum: int = float('inf') # int.MaxValue in C# (using float('inf') for consistency, though int limit is high)
                 ):
        """
        Initializes a new instance of the Agent class.
        """
        self.Name = name if name is not None else f"Agent {uuid.uuid4()}"
        self.State = state if state is not None else {}
        self.Memory = memory if memory is not None else {}
        self.Goals = goals if goals is not None else []
        self.Actions = actions if actions is not None else []
        self.Sensors = sensors if sensors is not None else []
        self.CostMaximum = cost_maximum
        self.StepMaximum = step_maximum

        self.CurrentActionSequences = []
        self.IsBusy = False
        self.IsPlanning = False


    def step(self, mode: StepMode = StepMode.Default) -> None:
        """
        You should call this every time your game state updates.
        """
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
            # In OneAction mode we want the agent to yield control back to the caller
            # after executing a single action, even if there are more actions left.
            # The remaining plan is kept for the next step, so mark the agent as
            # not busy to allow planning or execution in the following frame.
            self.IsBusy = False
        elif mode == StepMode.AllActions:
            while self.IsBusy: # Loop until plan is fully executed or becomes impossible
                self._execute()
                # Important: After each execute, re-check IsBusy, which is updated by _execute itself.
                # Also, if a plan becomes impossible, it will stop setting IsBusy to True.
                # If a plan is exhausted, IsBusy will be False.


    def clear_plan(self) -> None:
        """
        Clears the current action sequences (also known as plans).
        """
        self.CurrentActionSequences.clear()

    def plan(self) -> None:
        """
        Makes a plan.
        """
        if not self.IsBusy and not self.IsPlanning:
            self.IsPlanning = True
            Planner.plan(self, self.CostMaximum, self.StepMaximum)

    def plan_async(self) -> None:
        """
        Makes a plan asynchronously.
        """
        if not self.IsBusy and not self.IsPlanning:
            self.IsPlanning = True
            thread = threading.Thread(target=Planner.plan, args=(self, self.CostMaximum, self.StepMaximum))
            thread.start()

    def execute_plan(self) -> None:
        """
        Executes the current plan.
        """
        if not self.IsPlanning:
            self._execute()

    def _step_async(self) -> None:
        """
        Executes an asynchronous step of agent work.
        """
        if not self.IsBusy and not self.IsPlanning:
            self.IsPlanning = True
            thread = threading.Thread(target=Planner.plan, args=(self, self.CostMaximum, self.StepMaximum))
            thread.start()
        elif not self.IsPlanning:
            self._execute()

    def _execute(self) -> None:
        """
        Executes the current action sequences.
        """
        if len(self.CurrentActionSequences) > 0:
            cullable_sequences = []
            for sequence in self.CurrentActionSequences:
                if len(sequence) > 0:
                    action_to_execute = sequence[0]
                    execution_status = action_to_execute.execute(self) # Pass self (agent) to action's execute method
                    if execution_status != ExecutionStatus.Executing:
                        sequence.pop(0) # Remove the action if it's done (succeeded, failed, not possible)
                    if len(sequence) == 0:
                        cullable_sequences.append(sequence)
                else:
                    cullable_sequences.append(sequence) # Mark sequence as empty for removal

            for sequence in cullable_sequences:
                self.CurrentActionSequences.remove(sequence)
                Agent.OnAgentActionSequenceCompleted(self) # Trigger event for completed sequence

            # If after execution, all sequences are empty, agent is no longer busy.
            # Otherwise, it might still be busy.
            self.IsBusy = any(len(seq) > 0 for seq in self.CurrentActionSequences)
        else:
            self.IsBusy = False # No current action sequences, so not busy

