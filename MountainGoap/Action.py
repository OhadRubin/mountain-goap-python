# // <copyright file="Action.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import uuid
from typing import Dict, Any, Optional, List, Callable, Tuple, cast
from datetime import datetime, timedelta

from .CallbackDelegates.CostCallback import CostCallback
from .CallbackDelegates.ExecutorCallback import ExecutorCallback
from .CallbackDelegates.PermutationSelectorCallback import PermutationSelectorCallback
from .CallbackDelegates.StateCheckerCallback import StateCheckerCallback
from .CallbackDelegates.StateCostDeltaMultiplierCallback import StateCostDeltaMultiplierCallback
from .CallbackDelegates.StateMutatorCallback import StateMutatorCallback

from .ComparisonOperator import ComparisonOperator
from .ComparisonValuePair import ComparisonValuePair
from .ExecutionStatus import ExecutionStatus
from .Internals.DictionaryExtensionMethods import DictionaryExtensionMethods
from .Internals.Utils import Utils

from .Events.BeginExecuteActionEvent import BeginExecuteActionEvent
from .Events.FinishExecuteActionEvent import FinishExecuteActionEvent

# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

class Action:
    """
    Represents an action in a GOAP system.
    """

    Name: str

    _cost_base: float

    _permutation_selectors: Dict[str, PermutationSelectorCallback]

    _executor: ExecutorCallback

    _cost_callback: CostCallback

    _preconditions: Dict[str, Optional[Any]]

    _comparative_preconditions: Dict[str, ComparisonValuePair]

    _postconditions: Dict[str, Optional[Any]]

    _arithmetic_postconditions: Dict[str, Any] # Non-nullable in C#

    _parameter_postconditions: Dict[str, str]

    _state_mutator: Optional[StateMutatorCallback]

    _state_checker: Optional[StateCheckerCallback]

    _parameters: Dict[str, Optional[Any]]

    StateCostDeltaMultiplier: Optional[StateCostDeltaMultiplierCallback]

    # Events (static in C#)
    OnBeginExecuteAction: BeginExecuteActionEvent
    OnFinishExecuteAction: FinishExecuteActionEvent

    ExecutionStatus: ExecutionStatus = ExecutionStatus.NotYetExecuted

    def __init__(self,
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
                 state_cost_delta_multiplier: Optional[StateCostDeltaMultiplierCallback] = None):
        """
        Initializes a new instance of the Action class.
        """
        self._permutation_selectors = permutation_selectors if permutation_selectors is not None else {}
        self._executor = executor if executor is not None else Action._default_executor_callback
        
        # In C#, GetMethodInfo().Name is used for default name.
        # In Python, we can get the function's __name__ attribute.
        executor_name = self._executor.__name__ if hasattr(self._executor, '__name__') else str(self._executor)
        self.Name = name if name is not None else f"Action {uuid.uuid4()} ({executor_name})"
        
        self._cost_base = cost
        self._cost_callback = cost_callback if cost_callback is not None else Action._default_cost_callback
        
        self._preconditions = preconditions if preconditions is not None else {}
        self._comparative_preconditions = comparative_preconditions if comparative_preconditions is not None else {}
        self._postconditions = postconditions if postconditions is not None else {}
        self._arithmetic_postconditions = arithmetic_postconditions if arithmetic_postconditions is not None else {}
        self._parameter_postconditions = parameter_postconditions if parameter_postconditions is not None else {}
        
        self._state_mutator = state_mutator
        self._state_checker = state_checker
        self.StateCostDeltaMultiplier = state_cost_delta_multiplier if state_cost_delta_multiplier is not None else Action.default_state_cost_delta_multiplier

        self._parameters = {}

        # Initialize static events (class attributes in Python)
        # Note: Event handling in Python is often done via simple callable lists or a custom Event class.
        # Here, we'll use a callable that calls into a list of registered handlers.
        # This setup needs to be done once, typically at the module level or by a dedicated event manager.
        # In C#, `+= (agent, action, parameters) => { }` means if no handler is registered, it's an empty anonymous method.
        # In Python, an empty list of handlers implies no action, or a dummy default handler.

    # Static event-like attributes (class variables)
    _on_begin_execute_action_handlers: List[BeginExecuteActionEvent] = []
    _on_finish_execute_action_handlers: List[FinishExecuteActionEvent] = []

    @classmethod
    def OnBeginExecuteAction(cls, agent: 'Agent', action: 'Action', parameters: Dict[str, Optional[Any]]) -> None:
        for handler in cls._on_begin_execute_action_handlers:
            handler(agent, action, parameters)

    @classmethod
    def OnFinishExecuteAction(cls, agent: 'Agent', action: 'Action', status: ExecutionStatus, parameters: Dict[str, Optional[Any]]) -> None:
        for handler in cls._on_finish_execute_action_handlers:
            handler(agent, action, status, parameters)

    # Static registration methods for events
    @classmethod
    def register_on_begin_execute_action(cls, handler: BeginExecuteActionEvent):
        cls._on_begin_execute_action_handlers.append(handler)

    @classmethod
    def register_on_finish_execute_action(cls, handler: FinishExecuteActionEvent):
        cls._on_finish_execute_action_handlers.append(handler)

    # Default callbacks (static in C#)
    @staticmethod
    def default_state_cost_delta_multiplier(action: Optional['Action'], state_key: str) -> float:
        return 1.0

    @staticmethod
    def _default_executor_callback(agent: 'Agent', action: 'Action') -> ExecutionStatus:
        # from ..Agent import Agent # Local import to avoid circular dependency if not TYPE_CHECKING
        return ExecutionStatus.Failed

    @staticmethod
    def _default_cost_callback(action: 'Action', current_state: StateDictionary) -> float:
        # #pragma warning disable S1172 // Unused method parameters should be removed
        return action._cost_base
        # #pragma warning restore S1172 // Unused method parameters should be removed


    def copy(self) -> 'Action':
        """
        Makes a copy of the action.
        """
        new_action = Action(
            name=self.Name,
            permutation_selectors=self._permutation_selectors.copy(),
            executor=self._executor,
            cost=self._cost_base,
            cost_callback=self._cost_callback,
            preconditions=DictionaryExtensionMethods.copy_dict(self._preconditions),
            comparative_preconditions=DictionaryExtensionMethods.copy_comparison_value_pair_dict(self._comparative_preconditions),
            postconditions=DictionaryExtensionMethods.copy_dict(self._postconditions),
            arithmetic_postconditions=DictionaryExtensionMethods.copy_non_nullable_dict(self._arithmetic_postconditions),
            parameter_postconditions=DictionaryExtensionMethods.copy_string_dict(self._parameter_postconditions),
            state_mutator=self._state_mutator,
            state_checker=self._state_checker,
            state_cost_delta_multiplier=self.StateCostDeltaMultiplier
        )
        new_action._parameters = DictionaryExtensionMethods.copy_dict(self._parameters) # Set after init
        return new_action

    def set_parameter(self, key: str, value: Any) -> None:
        """
        Sets a parameter to the action.
        """
        self._parameters[key] = value

    def get_parameter(self, key: str) -> Optional[Any]:
        """
        Gets a parameter to the action.
        """
        return self._parameters.get(key)

    def get_cost(self, current_state: StateDictionary) -> float:
        """
        Gets the cost of the action.
        """
        try:
            return self._cost_callback(self, current_state)
        except Exception:
            return float('inf') # float.MaxValue in C#

    def execute(self, agent: 'Agent') -> ExecutionStatus:
        """
        Executes a step of work for the agent.
        """
        # Local import to avoid circular dependency
        from .Agent import Agent

        Action.OnBeginExecuteAction(agent, self, self._parameters)
        if self.is_possible(agent.State):
            new_status = self._executor(agent, self)
            if new_status == ExecutionStatus.Succeeded:
                self.apply_effects(agent.State)
            self.ExecutionStatus = new_status
            Action.OnFinishExecuteAction(agent, self, self.ExecutionStatus, self._parameters)
            return new_status
        else:
            self.ExecutionStatus = ExecutionStatus.NotPossible
            Action.OnFinishExecuteAction(agent, self, self.ExecutionStatus, self._parameters)
            return ExecutionStatus.NotPossible

    def is_possible(self, state: StateDictionary) -> bool:
        """
        Determines whether or not an action is possible.
        """
        for key, value in self._preconditions.items():
            if key not in state:
                return False
            # C# `state[kvp.Key] == null && state[kvp.Key] != kvp.Value` is a bit redundant if kvp.Key refers to a key that exists.
            # It simplifies to: if the current state value for this key is not equal to the required precondition value.
            if state[key] != value:
                return False

        for key, comp_value_pair in self._comparative_preconditions.items():
            if key not in state or state[key] is None:
                return False
            
            current_val = state[key]
            desired_val = comp_value_pair.Value
            operator = comp_value_pair.Operator

            # C# `is object obj && kvp.Value.Value is object obj2` check:
            # In Python, we rely on type hints and runtime checks for actual values.
            # If desired_val is None, it implies a malformed comparison pair if operator is not Undefined,
            # or if it's a numeric comparison.
            if desired_val is None and operator != ComparisonOperator.Undefined:
                # If the desired value for comparison is None, but the operator implies a comparison
                # that requires a non-None value, then it's not possible.
                # Example: checking if 'x < None' won't work numerically.
                # This could be made more robust by checking if current_val and desired_val are comparable types.
                # For now, following the C# logic.
                return False

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
            # For ComparisonOperator.Equals, it's covered by the regular preconditions loop if `ComparisonValuePair`
            # had an "Equals" equivalent. But in C# `ComparisonOperator.Equals` is separate.
            # However, the `is_possible` only checks `comparativePreconditions` for `<`, `<=`, `>`, `>=`.
            # A direct equality check would be `state[key] != desired_val` which is already in the first loop.

        if self._state_checker is not None and not self._state_checker(self, state):
            return False
        return True

    def get_permutations(self, state: StateDictionary) -> List[Dict[str, Optional[Any]]]:
        """
        Gets all permutations of parameters possible for an action.
        """
        combined_outputs: List[Dict[str, Optional[Any]]] = []
        outputs: Dict[str, List[Any]] = {}

        for key, selector_callback in self._permutation_selectors.items():
            outputs[key] = selector_callback(state)

        permutation_parameters = list(outputs.keys())
        indices = [0] * len(permutation_parameters)
        counts = [len(outputs[param]) for param in permutation_parameters]

        # If any parameter list is empty, no permutations are possible.
        if any(c == 0 for c in counts):
            return combined_outputs

        while True:
            single_output: Dict[str, Optional[Any]] = {}
            for i in range(len(indices)):
                if indices[i] >= counts[i]:
                    # This 'continue' from C# logic would mean skipping this parameter,
                    # which is usually not desired in a permutation, but verbatim implies this.
                    # A more common permutation generation would stop if indices[i] is out of bounds.
                    # For verbatim translation, we'll keep the continue.
                    continue
                param_key = permutation_parameters[i]
                single_output[param_key] = outputs[param_key][indices[i]]
            
            combined_outputs.append(single_output)

            if Action._indices_at_maximum(indices, counts):
                return combined_outputs
            
            Action._increment_indices(indices, counts)

    def apply_effects(self, state: StateDictionary) -> None:
        """
        Applies the effects of the action.
        """
        for key, value in self._postconditions.items():
            state[key] = value

        for key, value_to_add in self._arithmetic_postconditions.items():
            if key not in state:
                continue

            current_value = state[key]

            # Python handles arithmetic operations for mixed numeric types automatically.
            # For datetime + timedelta, we need specific handling.
            if isinstance(current_value, (int, float)) and isinstance(value_to_add, (int, float)):
                state[key] = current_value + value_to_add
            elif isinstance(current_value, datetime) and isinstance(value_to_add, timedelta):
                state[key] = current_value + value_to_add
            # Add other specific type combinations if they exist in C# (e.g. long, decimal not native in Python as distinct types)
            # Python's `int` handles arbitrary precision integers, so it covers `long`.
            # `float` covers `double`. `decimal` would require `Decimal` type from `decimal` module.
            else:
                # If types are not directly addable or known, skip.
                # For more strict verbatim, convert to float if possible for addition.
                try:
                    state[key] = cast(Any, current_value) + cast(Any, value_to_add)
                except TypeError:
                    pass # Or log a warning/error

        for param_key, state_key in self._parameter_postconditions.items():
            if param_key not in self._parameters:
                continue
            state[state_key] = self._parameters[param_key]

        if self._state_mutator is not None:
            self._state_mutator(self, state)

    def set_parameters(self, parameters: Dict[str, Optional[Any]]) -> None:
        """
        Sets all parameters to the action.
        """
        self._parameters = parameters

    @staticmethod
    def _indices_at_maximum(indices: List[int], counts: List[int]) -> bool:
        """
        Checks if all indices are at their maximum allowed value (last element of their respective list).
        """
        for i in range(len(indices)):
            if indices[i] < counts[i] - 1:
                return False
        return True

    @staticmethod
    def _increment_indices(indices: List[int], counts: List[int]) -> None:
        """
        Increments indices to generate the next permutation.
        """
        if Action._indices_at_maximum(indices, counts):
            return # All combinations exhausted

        for i in range(len(indices)):
            if indices[i] == counts[i] - 1:
                indices[i] = 0 # Wrap around
            else:
                indices[i] += 1
                return # Found the position to increment, done for this step

    def __hash__(self) -> int:
        """
        Provides a hash for the Action instance.
        Necessary for ActionNode equality and hashing.
        """
        # Hash based on Name, which should be unique enough for most purposes.
        return hash(self.Name)

    def __eq__(self, other: object) -> bool:
        """
        Provides equality comparison for Action instances.
        Necessary for ActionNode equality.
        """
        if not isinstance(other, Action):
            return NotImplemented
        return self.Name == other.Name

