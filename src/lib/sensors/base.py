"""
base.py
-------

Defines the base class for all HoloOcean sensors.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List


@dataclass
class BaseSensor:
    """
    Generic base class for configurable HoloOcean sensors.
    """

    sensor_type: str
    socket: str = "COM"
    Hz: int = 30
    sensor_name: Optional[str] = None
    location: Optional[List[float]] = None
    rotation: Optional[List[float]] = None
    configuration: Dict[str, Any] = field(default_factory=dict)

    def __init__(
        self,
        sensor_type: str,
        socket: str = "COM",
        Hz: int = 30,
        sensor_name: str = None,
        location: List[float] = None,
        rotation: List[float] = None,
        configuration: Dict[str, Any] = None,
        **kwargs
    ):
        self.sensor_type = sensor_type
        self.socket = socket
        self.Hz = Hz
        self.sensor_name = sensor_name
        self.location = location
        self.rotation = rotation

        # Sensor-specific configuration
        self.configuration = {}
        if configuration:
            self.configuration.update(configuration)
        if kwargs:
            self.configuration.update(kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the sensor configuration into a HoloOcean-compatible dictionary.
        """
        data = {
            "sensor_type": self.sensor_type,
            "socket": self.socket,
            "Hz": self.Hz,
        }

        if self.sensor_name:
            data["sensor_name"] = self.sensor_name

        if self.location is not None:
            data["location"] = self.location

        if self.rotation is not None:
            data["rotation"] = self.rotation

        if self.configuration:
            data["configuration"] = self.configuration

        return data
