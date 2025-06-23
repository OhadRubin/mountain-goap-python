from typing import Any, Callable, Dict, List, Optional

StateDictionary = Dict[str, Optional[Any]]

# Callback types
CostCallback = Callable[["Action", StateDictionary], float]
ExecutorCallback = Callable[["Agent", "Action"], "ExecutionStatus"]
PermutationSelectorCallback = Callable[[StateDictionary], List[Any]]
SensorRunCallback = Callable[["Agent"], None]
StateCheckerCallback = Callable[["Action", StateDictionary], bool]
StateCostDeltaMultiplierCallback = Callable[[Optional["Action"], str], float]
StateMutatorCallback = Callable[["Action", StateDictionary], None]

# Event types
AgentActionSequenceCompletedEvent = Callable[["Agent"], None]
AgentStepEvent = Callable[["Agent"], None]
BeginExecuteActionEvent = Callable[["Agent", "Action", Dict[str, Any]], None]
EvaluatedActionNodeEvent = Callable[["ActionNode", Dict["ActionNode", "ActionNode"]], None]
FinishExecuteActionEvent = Callable[["Agent", "Action", "ExecutionStatus", Dict[str, Any]], None]
PlanUpdatedEvent = Callable[["Agent", List["Action"]], None]
PlanningFinishedEvent = Callable[["Agent", Optional["BaseGoal"], float], None]
PlanningFinishedForSingleGoalEvent = Callable[["Agent", "BaseGoal", float], None]
PlanningStartedEvent = Callable[["Agent"], None]
PlanningStartedForSingleGoalEvent = Callable[["Agent", "BaseGoal"], None]
SensorRunEvent = Callable[["Agent", "Sensor"], None]
