# // <copyright file="ActionGraph.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import List, Any, Optional, Dict, Iterable, TYPE_CHECKING
from .DictionaryExtensionMethods import DictionaryExtensionMethods
from .ActionNode import ActionNode

if TYPE_CHECKING:
    from ..Action import Action

# A type alias for the state dictionary
StateDictionary = Dict[str, Optional[Any]]

class ActionGraph:
    """
    Represents a traversable action graph.
    """

    ActionNodes: List[ActionNode]

    def __init__(self, actions: List['Action'], state: StateDictionary):
        """
        Initializes a new instance of the ActionGraph class.
        """
        self.ActionNodes = []
        for action in actions:
            permutations = action.get_permutations(state)
            # If no permutations are returned (e.g., empty selector lists),
            # the action with that permutation context isn't added.
            # If permutations are always expected to return at least one empty dict if no params,
            # then this logic is fine.
            # In C#, `GetPermutations` returns an empty list if any selector yields no values,
            # so the outer loop over `permutations` will skip.
            for permutation in permutations:
                # Create a new ActionNode for each action-permutation combination.
                # Important: Pass a *copy* of the action and initial state to the node.
                # The ActionNode constructor already handles copying the action.
                self.ActionNodes.append(ActionNode(action, state, permutation))

    def neighbors(self, node: ActionNode) -> Iterable[ActionNode]:
        """
        Gets the list of neighbors for a node.
        """
        for other_node_template in self.ActionNodes:
            # `other_node_template` here refers to the initial ActionNodes created based on the agent's initial state.
            # When we generate neighbors, we are essentially looking for actions that can be applied
            # given the `node.State` (which is the state *after* the current node's action is applied).

            if other_node_template.Action is not None and \
               other_node_template.Action.is_possible(node.State): # Check possibility against the current node's resulting state
                
                # Create a new ActionNode representing the *next* state after applying `other_node_template.Action`
                # Its action is a copy of the other_node_template's action
                # Its initial state is a copy of the *current* node's state
                # Its parameters are a copy of the other_node_template's parameters (which were determined for the base state or for general use)
                new_action = other_node_template.Action.copy()
                new_state = DictionaryExtensionMethods.copy_concurrent_dict(node.State)
                new_parameters = DictionaryExtensionMethods.copy_dict(other_node_template.Parameters)

                new_node = ActionNode(new_action, new_state, new_parameters)
                
                # Apply the effects of the new action to the new node's state
                if new_node.Action is not None:
                    new_node.Action.apply_effects(new_node.State)

                yield new_node

