# // <copyright file="Sensor.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

import uuid
from typing import Optional, List
from .CallbackDelegates.SensorRunCallback import SensorRunCallback
from .Events.SensorRunningEvent import SensorRunEvent # Changed name from SensorRunningEvent.cs to match usage

class Sensor:
    """
    Sensor for getting information about world state.
    """

    Name: str

    _run_callback: SensorRunCallback

    # Events (static in C#)
    _on_sensor_run_handlers: List[SensorRunEvent] = []

    @classmethod
    def OnSensorRun(cls, agent: 'Agent', sensor: 'Sensor'):
        for handler in cls._on_sensor_run_handlers:
            handler(agent, sensor)

    @classmethod
    def register_on_sensor_run(cls, handler: SensorRunEvent):
        cls._on_sensor_run_handlers.append(handler)


    def __init__(self, run_callback: SensorRunCallback, name: Optional[str] = None):
        """
        Initializes a new instance of the Sensor class.
        """
        # In C#, GetMethodInfo().Name is used for default name.
        # In Python, we can get the function's __name__ attribute.
        callback_name = run_callback.__name__ if hasattr(run_callback, '__name__') else str(run_callback)
        self.Name = name if name is not None else f"Sensor {uuid.uuid4()} ({callback_name})"
        self._run_callback = run_callback

    def run(self, agent: 'Agent') -> None:
        """
        Runs the sensor during a game loop.
        """
        from .Agent import Agent # Local import to avoid circular dependency

        Sensor.OnSensorRun(agent, self) # Call the classmethod event
        self._run_callback(agent)

