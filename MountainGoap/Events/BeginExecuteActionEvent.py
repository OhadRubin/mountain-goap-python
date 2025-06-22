# // <copyright file="BeginExecuteActionEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..Action import Action

BeginExecuteActionEvent = Callable[['Agent', 'Action', Dict[str, Any]], None]

