"""
base.py
-------

Defines the base class for all HoloOcean sensors.
This class provides a flexible configuration interface allowing each
sensor to include arbitrary parameters via keyword arguments.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class BaseSensor:
    """
    Generic base class for configurable HoloOcean sensors.

    This class is used as the foundation for defining all sensor types,
    supporting both structured configuration dictionaries and dynamic
    keyword arguments. It is designed to be serialized directly into
    a HoloOcean-compatible format through `to_dict()`.

    Parameters
    ----------
    sensor_type : str
        Type of the sensor (e.g., "DepthSensor", "RGBCamera", "IMUSensor").
    socket : str, optional
        Socket name for sensor data connection. Default is ``"COM"``.
    Hz : int, optional
        Sensor update frequency in Hertz. Default is ``30``.
    sensor_name : str, optional
        Custom name for the sensor (e.g., "FrontCamera").
    configuration : dict, optional
        Dictionary of additional configuration parameters.
    **kwargs
        Arbitrary key–value pairs to include or override in the configuration.

    Examples
    --------
    >>> from lib.sensors.base import BaseSensor
    >>> sensor = BaseSensor(
    ...     sensor_type="DepthSensor",
    ...     socket="DepthSocket",
    ...     Hz=20,
    ...     Sigma=0.1
    ... )
    >>> print(sensor.to_dict())
    {'sensor_type': 'DepthSensor', 'socket': 'DepthSocket', 'Hz': 20,
     'configuration': {'Sigma': 0.1}}
    """

    sensor_type: str
    socket: str = "COM"
    Hz: int = 30
    sensor_name: str = None
    configuration: Dict[str, Any] = field(default_factory=dict)

    def __init__(
        self,
        sensor_type: str,
        socket: str = "COM",
        Hz: int = 30,
        sensor_name: str = None,
        configuration: Dict[str, Any] = None,
        **kwargs
    ):
        self.sensor_type = sensor_type
        self.socket = socket
        self.Hz = Hz
        self.sensor_name = sensor_name

        # Merge configuration dictionary and additional keyword arguments
        self.configuration = {}
        if configuration:
            self.configuration.update(configuration)
        if kwargs:
            self.configuration.update(kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the sensor configuration into a HoloOcean-compatible dictionary.

        Returns
        -------
        dict
            A dictionary containing all relevant sensor parameters.
        """
        data = {
            "sensor_type": self.sensor_type,
            "socket": self.socket,
            "Hz": self.Hz,
        }

        if self.sensor_name:
            data["sensor_name"] = self.sensor_name

        if self.configuration:
            data["configuration"] = self.configuration

        return data
