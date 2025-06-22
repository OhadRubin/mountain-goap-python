# // <copyright file="PlanningFinishedEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..BaseGoal import BaseGoal

PlanningFinishedEvent = Callable[['Agent', Optional['BaseGoal'], float], None]

