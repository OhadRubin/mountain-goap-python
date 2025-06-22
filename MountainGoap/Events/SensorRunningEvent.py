# // <copyright file="SensorRunningEvent.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent import Agent
    from ..Sensor import Sensor

SensorRunEvent = Callable[['Agent', 'Sensor'], None]

