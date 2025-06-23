import threading
import uuid
from typing import Any, Dict, List, Optional

from .types import (
    AgentActionSequenceCompletedEvent, AgentStepEvent,
    BeginExecuteActionEvent, FinishExecuteActionEvent, PlanUpdatedEvent,
    PlanningFinishedEvent, PlanningFinishedForSingleGoalEvent,
    PlanningStartedEvent, PlanningStartedForSingleGoalEvent, EvaluatedActionNodeEvent,
    StateDictionary
)
from .actions import Action, StepMode, ExecutionStatus
from .goals import BaseGoal
from .sensors import Sensor
from .planning import Planner, ActionNode

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
                    print(f"{self.Name} executing action: {action_to_execute.Name}")
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
            print(f"DEBUG: {self.Name} has no action sequences to execute")
            # IsBusy is only set to False if there were no sequences to start with.
            self.IsBusy = False


