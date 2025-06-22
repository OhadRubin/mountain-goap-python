# // <copyright file="CostCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, Dict, Any

# A type alias for the state dictionary
StateDictionary = Dict[str, Any]

# Define the delegate type using Callable
# The first parameter is 'Action' (forward reference)
# The second parameter is 'StateDictionary'
# The return type is float
CostCallback = Callable[['Action', StateDictionary], float]

