# // <copyright file="PlanningFinishedForSingleGoalEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..BaseGoal import BaseGoal

PlanningFinishedForSingleGoalEvent = Callable[['Agent', 'BaseGoal', float], None]

