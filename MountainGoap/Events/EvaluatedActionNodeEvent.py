# // <copyright file="EvaluatedActionNodeEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Internals.ActionNode import ActionNode

EvaluatedActionNodeEvent = Callable[['ActionNode', Dict['ActionNode', 'ActionNode']], None]

