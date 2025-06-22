# // <copyright file="ActionNode.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Any, Optional, TYPE_CHECKING
from ..PriorityQueue.FastPriorityQueueNode import FastPriorityQueueNode
from .DictionaryExtensionMethods import DictionaryExtensionMethods

if TYPE_CHECKING:
    from ..Action import Action

class ActionNode(FastPriorityQueueNode):
    """
    Represents an action node in an action graph.
    """

    State: Dict[str, Optional[Any]]

    Parameters: Dict[str, Optional[Any]]

    Action: Optional['Action']

    def __init__(self, action: Optional['Action'], state: Dict[str, Optional[Any]], parameters: Dict[str, Optional[Any]]):
        """
        Initializes a new instance of the ActionNode class.
        """
        super().__init__()
        self.Action = action.copy() if action is not None else None
        self.State = DictionaryExtensionMethods.copy_concurrent_dict(state) # Simulating ConcurrentDictionary copy
        self.Parameters = DictionaryExtensionMethods.copy_dict(parameters)

        if self.Action is not None:
            self.Action.set_parameters(self.Parameters)

    def __eq__(self, other: object) -> bool:
        """
        Overrides the equality operator on ActionNodes.
        """
        if not isinstance(other, ActionNode):
            return NotImplemented # Or return False directly if strict type comparison is desired

        if self is other: # Optimization: if same object
            return True

        # Check Action equality
        if self.Action is None:
            if other.Action is not None:
                return False
        elif other.Action is None:
            return False
        elif not self.Action.__eq__(other.Action): # Assuming Action class implements __eq__
            return False

        # Check State equality
        return self._state_matches(other)


    def __ne__(self, other: object) -> bool:
        """
        Overrides the inequality operator on ActionNodes.
        """
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """
        Overrides the hash code generation for ActionNodes.
        A hashable representation of the state is needed.
        """
        def _make_hashable(value: Any) -> Any:
            """Recursively convert lists/dicts to tuples for hashing."""
            if isinstance(value, dict):
                return tuple(sorted((k, _make_hashable(v)) for k, v in value.items()))
            if isinstance(value, list):
                return tuple(_make_hashable(v) for v in value)
            if isinstance(value, set):
                return tuple(sorted(_make_hashable(v) for v in value))
            return value

        # Convert state dictionary to a hashable representation
        state_tuple = tuple(sorted((k, _make_hashable(v)) for k, v in self.State.items()))
        
        # Ensure action is hashable, or use its hash directly if it has one.
        # If Action is a custom object and not hashable, we'd need to define its __hash__
        # For now, if Action.Name is unique enough, we can use that, or a default hash.
        action_hash = hash(self.Action) if self.Action is not None else hash(None)
        
        return hash((action_hash, state_tuple))

    def cost(self, current_state: Dict[str, Optional[Any]]) -> float:
        """
        Cost to traverse this node.
        """
        if self.Action is None:
            return float('inf') # float.MaxValue in C#
        return self.Action.get_cost(current_state)

    def _state_matches(self, other_node: 'ActionNode') -> bool:
        """
        Compares the state of this node with another node for equality.
        """
        # A simpler way to check if two dictionaries have the same keys and values
        # This handles cases where values might be None correctly.
        # It also handles different types (int vs float) correctly if Python's `==` allows it.
        return self.State == other_node.State

