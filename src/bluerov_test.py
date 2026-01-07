import holoocean
import cv2

from controllers.keyboard_controller import KeyboardController
from lib.scenario_builder import ScenarioConfig
from lib.worlds import World
from lib.rover import Rover
from utils.sonar_viz import PolarSonarVisualizer
from utils.camera_viz import show_camera


from telemetry.parsing import parse_pose
from telemetry.estimation import (
    parse_velocity,
    estimate_motion_state,
    parse_depth,
    estimate_depth_from_seabed,
)
from telemetry.hud import draw_telemetry_hud


SENSOR_MAP = {
    "Pose": "PoseSensor",
    "Velocity": "VelocitySensor",
    "IMU": "IMUSensor",
    "DVL": "DVLSensor",
    "RangeFinder": "RangeFinderSensor",
    "Collision": "CollisionSensor",
    "Depth": "DepthSensor",
}


rov0 = Rover.BlueROV2(
    name="rov0",
    location=[0, 0, 0],
    rotation=[0, 0, 0],
    control_scheme=0,
)

scenario = (
    ScenarioConfig("BlueROV_CustomOctree")
    .set_world(World.Dam)
    .add_agent(rov0)
)


sonar_viz = PolarSonarVisualizer(
    azimuth_deg=90,
    range_min=1,
    range_max=30,
    plot_hz=5,
    ema_alpha=0.1
)


controller = KeyboardController()

with holoocean.make(
    scenario_cfg=scenario.to_dict(),
    show_viewport=False,
    ticks_per_sec=30,
    frames_per_sec=True
) as env:

    last = {}

    while True:
        cmd = controller.get_command()
        if cmd is None:
            break

        state = env.step(cmd)

        for k, v in SENSOR_MAP.items():
            if v in state:
                last[k] = state[v]

        telemetry = {
            "pose": parse_pose(last.get("Pose")),
            "velocity": parse_velocity(last.get("Velocity")),
            "altitude": parse_depth(last.get("Depth")),
            "under_range": estimate_depth_from_seabed(last.get("RangeFinder")),
            "motion": estimate_motion_state(last.get("IMU")),
            "collision": last.get("Collision"),
        }

        show_camera(state, "FrontCamera", "Front Camera")
        show_camera(state, "SonarCamera", "Sonar Camera")

        if "ImagingSonar" in state:
            sonar_viz.submit(state["ImagingSonar"])
        sonar_viz.update_plot()

        draw_telemetry_hud(telemetry)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

sonar_viz.close()
cv2.destroyAllWindows()
