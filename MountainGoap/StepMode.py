# // <copyright file="StepMode.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from enum import Enum

class StepMode(Enum):
    """
    Different modes with which MountainGoap can execute an agent step.
    """

    Default = 1

    OneAction = 2

    AllActions = 3

