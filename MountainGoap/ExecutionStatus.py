# // <copyright file="ExecutionStatus.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from enum import Enum

class ExecutionStatus(Enum):
    """
    Possible execution status for an action.
    """

    NotYetExecuted = 1

    Executing = 2

    Succeeded = 3

    Failed = 4

    NotPossible = 5

