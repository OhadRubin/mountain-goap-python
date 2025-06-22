# // <copyright file="PermutationSelectorCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, Dict, Any, List

# A type alias for the state dictionary
StateDictionary = Dict[str, Any]

# Define the delegate type using Callable
# The parameter is 'StateDictionary'
# The return type is List[Any] (list of objects)
PermutationSelectorCallback = Callable[[StateDictionary], List[Any]]

