"""
agents.py
---------

Defines the core agent configuration class for HoloOcean.
This class provides a unified structure for all agent types (ROVs/AUVs)
and supports dynamic addition of sensors and conversion to dictionary format.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class AgentConfig:
    """
    Configuration model for a HoloOcean agent.

    This class represents a single autonomous vehicle or robot in a HoloOcean
    scenario, including its position, orientation, control mode, and sensors.
    It serves as the base structure used by factory classes such as `Rover`
    to generate predefined configurations.

    Attributes
    ----------
    agent_name : str
        Unique identifier for the agent (e.g., "rov0").
    agent_type : str
        Type of agent (e.g., "BlueROV2", "HoveringAUV").
    control_scheme : int, optional
        Control mode (0 = manual, 1 = waypoint, etc.). Default is 0.
    location : list of float, optional
        Initial position [x, y, z] in meters. Default is [0, 0, 0].
    rotation : list of float, optional
        Initial orientation [roll, pitch, yaw] in degrees. Default is [0, 0, 0].
    sensors : list of dict, optional
        List of sensor configurations, each represented as a dictionary.

    Examples
    --------
    >>> from lib.agents import AgentConfig
    >>> agent = AgentConfig(agent_name="rov0", agent_type="BlueROV2")
    >>> agent.add_sensor({"sensor_type": "PoseSensor", "Hz": 30})
    >>> print(agent.to_dict())
    """

    agent_name: str
    agent_type: str
    control_scheme: int = 0
    location: List[float] = field(default_factory=lambda: [0, 0, 0])
    rotation: List[float] = field(default_factory=lambda: [0, 0, 0])
    sensors: List[Dict[str, Any]] = field(default_factory=list)

    def add_sensor(self, sensor: Dict[str, Any]) -> "AgentConfig":
        """
        Add a sensor configuration to the agent.

        Parameters
        ----------
        sensor : dict
            Dictionary representing a sensor configuration (type, Hz, socket, etc.).

        Returns
        -------
        AgentConfig
            The current instance, allowing for method chaining.
        """
        self.sensors.append(sensor)
        return self

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the agent configuration to a dictionary.

        Returns
        -------
        dict
            A structure compatible with `ScenarioConfig`, ready to be used
            in `holoocean.make()`.
        """
        return {
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "control_scheme": self.control_scheme,
            "location": self.location,
            "rotation": self.rotation,
            "sensors": self.sensors,
        }
