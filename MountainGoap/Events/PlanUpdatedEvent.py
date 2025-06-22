# // <copyright file="PlanUpdatedEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..Action import Action

PlanUpdatedEvent = Callable[['Agent', List['Action']], None]

