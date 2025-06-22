# // <copyright file="StateMutatorCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Action import Action

# A type alias for the state dictionary
StateDictionary = Dict[str, Any]

# Define the delegate type using Callable
# The first parameter is 'Action' (forward reference)
# The second parameter is 'StateDictionary'
# The return type is None (void in C#)
StateMutatorCallback = Callable[['Action', StateDictionary], None]

