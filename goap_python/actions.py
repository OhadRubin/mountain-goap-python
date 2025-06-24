import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Iterable
from typing import cast
from enum import Enum

from .types import (
    PermutationSelectorCallback, ExecutorCallback, CostCallback,
    StateCheckerCallback, StateMutatorCallback, StateCostDeltaMultiplierCallback,
    BeginExecuteActionEvent, FinishExecuteActionEvent,
    StateDictionary
)
from .goals import ComparisonValuePair, ComparisonOperator, ExecutionStatus
from .utils import DictionaryExtensionMethods

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
            else:  # current_value is not None
                if (
                    current_value != value
                ):  # In Python, `!=` calls `__ne__`, which is the correct equivalent to C#'s `!Equals()`
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


