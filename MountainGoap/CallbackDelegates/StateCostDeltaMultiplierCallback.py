# // <copyright file="StateMutatorCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..Action import Action

# Define the delegate type using Callable
# The first parameter is Optional['Action'] (forward reference for Action or None)
# The second parameter is str
# The return type is float
StateCostDeltaMultiplierCallback = Callable[[Optional['Action'], str], float]

