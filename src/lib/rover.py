"""
rover.py
--------

Factory interface for creating predefined underwater vehicles (ROVs/AUVs)
in HoloOcean. Each factory method returns an AgentConfig instance populated
with the appropriate sensors and parameters.
"""

from lib.agents import AgentConfig
from lib.sensors import Sensor


class Rover:
    """
    Factory class for generating predefined underwater robot configurations.

    This class provides ready-to-use constructors for common HoloOcean agents,
    such as the BlueROV2. Each method returns an `AgentConfig` object that can
    be directly added to a `ScenarioConfig`.

    Examples
    --------
    >>> from lib.rover import Rover
    >>> from lib.scenario_builder import ScenarioConfig
    >>> from lib.worlds import World
    >>> rov = Rover.BlueROV2(name="rov0")
    >>> scenario = (
    ...     ScenarioConfig(name="TestScenario")
    ...     .set_world(World.PierHarbor)
    ...     .add_agent(rov)
    ... )
    """

    @staticmethod
    def BlueROV2(
        name: str = "rov0",
        location=None,
        rotation=None,
        control_scheme: int = 0,
        sensors=None,
    ) -> AgentConfig:
        """
        Create a BlueROV2 agent configuration.

        Parameters
        ----------
        name : str, optional
            Unique name for the agent. Default is ``"rov0"``.
        location : list of float, optional
            Initial [x, y, z] position in meters. Default is ``[0, 0, -4]``.
        rotation : list of float, optional
            Initial [roll, pitch, yaw] orientation in degrees. Default is ``[0, 0, 0]``.
        control_scheme : int, optional
            Control mode (0 = manual, 1 = waypoint, etc.). Default is ``0``.
        sensors : list, optional
            List of sensor objects (from `lib.sensors.Sensor`). If not provided,
            default sensors (Pose, Depth, IMU, FrontCamera) are attached.

        Returns
        -------
        AgentConfig
            A configured BlueROV2 agent ready to be added to a scenario.
        """
        location = location or [0, 0, -4]
        rotation = rotation or [0, 0, 0]

        sensors = sensors or [
            Sensor.Pose(),
            Sensor.Depth(sigma=0.2),
            Sensor.IMU(),
            Sensor.RGBCamera(name="FrontCamera", width=640, height=480),
        ]

        return AgentConfig(
            agent_name=name,
            agent_type="BlueROV2",
            control_scheme=control_scheme,
            location=location,
            rotation=rotation,
            sensors=[s.to_dict() for s in sensors],
        )
