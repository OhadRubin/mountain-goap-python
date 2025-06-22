# // <copyright file="AgentActionSequenceCompletedEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent

AgentActionSequenceCompletedEvent = Callable[['Agent'], None]

