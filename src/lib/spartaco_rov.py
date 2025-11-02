from lib.rover import Rover
from lib.sensors import Sensor

def create_spartaco_rov(name="spartaco_rov", location=[0, 0, -5]):
    """Crea l'agente BlueROV3 Heavy (Spartaco ROV) con sensori realistici e sonar approssimato."""
    return Rover.BlueROV2Heavy(
        name=name,
        location=location,
        rotation=[0, 0, 0],
        control_scheme=0,
        sensors=[
            # --- Core navigation ---
            Sensor.Pose(socket="PoseSocket", Hz=30),
            Sensor.Depth(socket="DepthSocket", Hz=30, Sigma=0.2),
            Sensor.IMU(socket="IMUSocket", Hz=30),
            Sensor.Velocity(socket="VelocitySocket", Hz=30),

            # --- Visual sensors ---
            Sensor.RGBCamera(
                name="FrontCamera",
                socket="CameraSocket",
                Hz=20,
                width=640,
                height=480,
                FOV=90.0,
            ),

            # --- Acoustic & navigation sensors ---
            Sensor.ImagingSonar(
                name="ApproxSideSonar",
                socket="SonarSocket",
                Hz=15,
                Azimuth=90.0,
                Elevation=10.0,
                RangeMin=1.0,
                RangeMax=25.0,
                RangeBins=256,
                AzimuthBins=256,
                AddSigma=0.05,
                MultSigma=0.05,
                MultiPath=False,
                ScaleNoise=False,
            ),

            # --- Motion relative to seabed (DVL) ---
            Sensor.DVL(
                socket="DVLSocket",
                Hz=20,
                Elevation=22.5,
                VelSigma=0.02,
                ReturnRange=True,
                MaxRange=40,
            ),

            # --- Environment & safety ---
            Sensor.RangeFinder(
                socket="RangeSocket",
                Hz=15,
                Range=25.0,
                FOV=20.0,
                NoiseSigma=0.05,
            ),
            Sensor.Collision(socket="CollisionSocket", Hz=10),
        ],
    )
