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
        Create a BlueROV2 / Spartaco ROV agent configuration
        with FULL default sensor suite unless custom sensors are provided.
        """
        location = location or [0, 0, -4]
        rotation = rotation or [0, 0, 0]

        if sensors is None:
            sensors = [
                # --- Core navigation ---
                Sensor.Pose(socket="PoseSocket", Hz=10), # Ci da la posizione in acqua come il sensore installato nel rover
                Sensor.Depth(socket="DepthSocket", Hz=10),
                Sensor.IMU(socket="IMUSocket", Hz=10),
                Sensor.Velocity(socket="VelocitySocket", Hz=10),

                # --- Visual front camera ---
                Sensor.RGBCamera(
                    name="FrontCamera",
                    socket="CameraSocket",
                    Hz=50,
                    width=640,
                    height=480,
                    FOV=90.0,
                ),

                # --- Acoustic sonar (approx SideScan → ImagingSonar) ---
                Sensor.SinglebeamSonar(
                    name="SurveyorImagingSonar_SB",
                    socket="SonarSocket",
                    Hz=100,
                    OpeningAngle=20.0,      
                    RangeMin=1.0,
                    RangeMax=50.0,
                    RangeBins=512,
                    AddSigma=0.05,
                    MultSigma=0.05,
                    RangeSigma=0.1,
                    UseApprox=True,
                    ShowWarning=False
                ),

                # --- DVL navigation ---
                Sensor.DVL(
                    socket="DVLSocket",
                    Hz=10,
                    Elevation=22.5,
                    VelSigma=0.02,
                    ReturnRange=True,
                    MaxRange=40,
                ),

                # PING2 SONAR (under) -> simulation
                Sensor.RangeFinder(
                    name="Ping2Sonar",
                    socket="DVLSocket",
                    Hz=10,
                    LaserMaxDistance=50.0,
                    LaserCount=1
                ),


                # Front Laser (Merge of right and left laser)
                Sensor.RangeFinder(
                    name="LaserLeft",
                    socket="CameraSocket",
                    Hz=10,
                    LaserMaxDistance=10.0,
                    LaserCount=1
                ),

                Sensor.Collision(
                    socket="CollisionSocket",
                    Hz=10,
                ),
            ]

        # Return complete agent config
        return AgentConfig(
            agent_name=name,
            agent_type="BlueROV2",
            control_scheme=control_scheme,
            location=location,
            rotation=rotation,
            sensors=[s.to_dict() for s in sensors],
        )

