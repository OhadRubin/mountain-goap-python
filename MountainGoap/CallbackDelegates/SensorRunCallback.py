# // <copyright file="SensorRunCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent

# Define the delegate type using Callable
# The parameter is 'Agent' (forward reference)
# The return type is None (void in C#)
SensorRunCallback = Callable[['Agent'], None]

