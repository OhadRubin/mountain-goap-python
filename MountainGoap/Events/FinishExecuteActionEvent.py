# // <copyright file="FinishExecuteActionEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..Action import Action
    from ..ExecutionStatus import ExecutionStatus

FinishExecuteActionEvent = Callable[['Agent', 'Action', 'ExecutionStatus', Dict[str, Any]], None]

