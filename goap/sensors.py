import uuid
from typing import List, Optional

from .types import SensorRunCallback, SensorRunEvent

class Sensor:
    Name: str
    _run_callback: SensorRunCallback
    _on_sensor_run_handlers: List[SensorRunEvent] = []

    @classmethod
    def OnSensorRun(cls, agent: "Agent", sensor: "Sensor"):
        for handler in cls._on_sensor_run_handlers:
            handler(agent, sensor)

    @classmethod
    def register_on_sensor_run(cls, handler: SensorRunEvent):
        cls._on_sensor_run_handlers.append(handler)

    def __init__(self, run_callback: SensorRunCallback, name: Optional[str] = None):
        callback_name = (
            run_callback.__name__
            if hasattr(run_callback, "__name__")
            else str(run_callback)
        )
        self.Name = (
            name if name is not None else f"Sensor {uuid.uuid4()} ({callback_name})"
        )
        self._run_callback = run_callback

    def run(self, agent: "Agent") -> None:
        Sensor.OnSensorRun(agent, self)
        self._run_callback(agent)

