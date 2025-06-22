# // <copyright file="ExecutorCallback.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..Action import Action
    from ..ExecutionStatus import ExecutionStatus

# Define the delegate type using Callable
# The first parameter is 'Agent' (forward reference)
# The second parameter is 'Action' (forward reference)
# The return type is 'ExecutionStatus' (forward reference)
ExecutorCallback = Callable[['Agent', 'Action'], 'ExecutionStatus']

