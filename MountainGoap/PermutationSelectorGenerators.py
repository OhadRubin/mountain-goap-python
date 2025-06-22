# // <copyright file="PermutationSelectorGenerators.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

# #pragma warning disable S3267 // Loops should be simplified with "LINQ" expressions

from typing import Iterable, List, Any, TypeVar, Callable, Dict, Optional
from .CallbackDelegates.PermutationSelectorCallback import PermutationSelectorCallback

T = TypeVar('T')

# A type alias for the state dictionary (from CallbackDelegates.py)
StateDictionary = Dict[str, Optional[Any]]


class PermutationSelectorGenerators:
    """
    Generators for default permutation selectors for convenience.
    """

    @staticmethod
    def select_from_collection(values: Iterable[T]) -> PermutationSelectorCallback:
        """
        Generates a permutation selector that returns all elements of an enumerable.
        """
        def selector(state: StateDictionary) -> List[Any]:
            output: List[Any] = []
            for item in values:
                if item is not None:
                    output.append(item)
            return output
        return selector

    @staticmethod
    def select_from_collection_in_state(key: str) -> PermutationSelectorCallback:
        """
        Generates a permutation selector that returns all elements of an enumerable within the agent state.
        """
        def selector(state: StateDictionary) -> List[Any]:
            output: List[Any] = []
            if key in state and isinstance(state[key], Iterable):
                values = state[key]
                for item in values:
                    if item is not None:
                        output.append(item)
            return output
        return selector

    @staticmethod
    def select_from_integer_range(lower_bound: int, upper_bound: int) -> PermutationSelectorCallback:
        """
        Generates a permutation selector that returns all integer elements in a range.
        """
        def selector(state: StateDictionary) -> List[Any]:
            output: List[Any] = []
            for i in range(lower_bound, upper_bound):
                output.append(i)
            return output
        return selector

