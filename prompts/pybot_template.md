Convert the following python minecraft bot to use the attached goap framework.

<python_minecraft_bot>
{/Users/ohadr/goap/mountain-goap-python/pybot.md}
</python_minecraft_bot>


<goap_python_code>
{/Users/ohadr/goap/mountain-goap-python/inline_short.py}
</goap_python_code>

Here is an explanation of the state machines of the python minecraft bot:

<state_machines>
{/Users/ohadr/goap/mountain-goap-python/minebot/newfile.md}
</state_machines>



You should use the following worldstate in your port (you don't have to, you can decide not to use some things..). Assume that everything that Rpg example uses is already defined.



{/Users/ohadr/goap/mountain-goap-python/minebot/goap.js}

Additional instructions: You should output the goap-based npc in a single file.
Reminder: you do not need to implement the following function:

lass FastPriorityQueueNode:
    def __init__(self):
class FastPriorityQueue:
    def __init__(self, max_nodes: int):
    def count(self) -> int:
    def max_size(self) -> int:
    def clear(self) -> None:
    def contains(self, node: T) -> bool:
    def enqueue(self, node: T, priority: float) -> None:
    def _cascade_up(self, node: T) -> None:
    def _cascade_down(self, node: T) -> None:
    def _has_higher_priority(self, higher: T, lower: T) -> bool:
    def _has_higher_or_equal_priority(self, higher: T, lower: T) -> bool:
    def dequeue(self) -> T:
    def resize(self, max_nodes: int) -> None:
    def first(self) -> T:
    def update_priority(self, node: T, priority: float) -> None:
    def _on_node_updated(self, node: T) -> None:
    def remove(self, node: T) -> None:
    def reset_node(self, node: T) -> None:
    def __iter__(self) -> Iterable[T]:
    def is_valid_queue(self) -> bool:
class DictionaryExtensionMethods:
    def copy_dict(dictionary: StateDictionary) -> StateDictionary:
    def copy_concurrent_dict(dictionary: StateDictionary) -> StateDictionary:
    def copy_comparison_value_pair_dict(
    def copy_string_dict(dictionary: Dict[str, str]) -> Dict[str, str]:
    def copy_non_nullable_dict(dictionary: Dict[str, Any]) -> Dict[str, Any]:
class ActionNode(FastPriorityQueueNode):
    def __init__(
    def __eq__(self, other: object) -> bool:
    def __ne__(self, other: object) -> bool:
    def __hash__(self) -> int:
        def make_hashable(obj):
    def cost(self, current_state: StateDictionary) -> float:
    def _state_matches(self, other_node: "ActionNode") -> bool:
class ActionGraph:
    def __init__(self, actions: List["Action"], state: StateDictionary):
    def neighbors(self, node: ActionNode) -> Iterable[ActionNode]:
class Utils:
    def is_lower_than(a: Any, b: Any) -> bool:
    def is_higher_than(a: Any, b: Any) -> bool:
    def is_lower_than_or_equals(a: Any, b: Any) -> bool:
    def is_higher_than_or_equals(a: Any, b: Any) -> bool:
    def meets_goal(
class ActionAStar:
    def __init__(
    def _heuristic(
    def _meets_goal(
class Planner:
    def plan(agent: "Agent", cost_maximum: float, step_maximum: int) -> None:
    def _update_agent_action_list(
class BaseGoal:
    def __init__(self, name: str = None, weight: float = 1.0):
class ComparisonOperator(Enum):
class ComparisonValuePair:
    def __init__(
class ComparativeGoal(BaseGoal):
    def __init__(
class ExecutionStatus(Enum):
class ExtremeGoal(BaseGoal):
    def __init__(
class Goal(BaseGoal):
    def __init__(
class PermutationSelectorGenerators:
    def select_from_collection(values: Iterable[T]) -> PermutationSelectorCallback:
        def selector(state: StateDictionary) -> List[Any]:
    def select_from_collection_in_state(key: str) -> PermutationSelectorCallback:
        def selector(state: StateDictionary) -> List[Any]:
    def select_from_integer_range(
        def selector(state: StateDictionary) -> List[Any]:
class Sensor:
    def OnSensorRun(cls, agent: "Agent", sensor: "Sensor"):
    def register_on_sensor_run(cls, handler: SensorRunEvent):
    def __init__(self, run_callback: SensorRunCallback, name: Optional[str] = None):
    def run(self, agent: "Agent") -> None:
class StepMode(Enum):
class Action:
    def __init__(
    def OnBeginExecuteAction(
    def OnFinishExecuteAction(
    def register_on_begin_execute_action(cls, handler: BeginExecuteActionEvent):
    def register_on_finish_execute_action(cls, handler: FinishExecuteActionEvent):
    def default_state_cost_delta_multiplier(
    def _default_executor_callback(agent: "Agent", action: "Action") -> ExecutionStatus:
    def _default_cost_callback(
    def copy(self) -> "Action":
    def set_parameter(self, key: str, value: Any) -> None:
    def get_parameter(self, key: str) -> Optional[Any]:
    def get_cost(self, current_state: StateDictionary) -> float:
    def execute(self, agent: "Agent") -> ExecutionStatus:
    def is_possible(self, state: StateDictionary) -> bool:
    def get_permutations(
    def apply_effects(self, state: StateDictionary) -> None:
    def set_parameters(self, parameters: Dict[str, Optional[Any]]) -> None:
    def _indices_at_maximum(indices: List[int], counts: List[int]) -> bool:
    def _increment_indices(indices: List[int], counts: List[int]) -> None:
    def __hash__(self) -> int:
    def __eq__(self, other: object) -> bool:
class Agent:
    def OnAgentStep(cls, agent: "Agent"):
    def OnAgentActionSequenceCompleted(cls, agent: "Agent"):
    def OnPlanningStarted(cls, agent: "Agent"):
    def OnPlanningStartedForSingleGoal(cls, agent: "Agent", goal: BaseGoal):
    def OnPlanningFinishedForSingleGoal(
    def OnPlanningFinished(
    def OnPlanUpdated(cls, agent: "Agent", action_list: List[Action]):
    def OnEvaluatedActionNode(
    def register_on_agent_step(cls, handler: AgentStepEvent):
    def register_on_agent_action_sequence_completed(
    def register_on_planning_started(cls, handler: PlanningStartedEvent):
    def register_on_planning_started_for_single_goal(
    def register_on_planning_finished_for_single_goal(
    def register_on_planning_finished(cls, handler: PlanningFinishedEvent):
    def register_on_plan_updated(cls, handler: PlanUpdatedEvent):
    def register_on_evaluated_action_node(cls, handler: EvaluatedActionNodeEvent):
    def __init__(
    def step(self, mode: StepMode = StepMode.Default) -> None:
    def clear_plan(self) -> None:
    def plan(self) -> None:
    def plan_async(self) -> None:
    def execute_plan(self) -> None:
    def _step_async(self) -> None:
    def _execute(self) -> None:
