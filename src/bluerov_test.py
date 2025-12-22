import holoocean
import cv2

from controllers.keyboard_controller import KeyboardController
from lib.scenario_builder import ScenarioConfig
from lib.worlds import World
from lib.rover import Rover
from utils.sonar_viz import PolarSonarVisualizerAsync
from utils.camera_viz import show_camera


from telemetry.parsing import parse_pose
from telemetry.estimation import (
    estimate_velocity,
    estimate_motion_state,
    parse_depth,
    estimate_front_obstacle,
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
    location=[0, 0, -20],
    # location=[14, -23, -276],
    rotation=[0, 0, 0],
    control_scheme=0,
)

scenario = (
    ScenarioConfig("BlueROV_CustomOctree")
    .set_world(World.Dam)
    # .set_env_bounds(
    #     env_min=[-200, -200, -200],
    #     env_max=[0, 0, 0],
    # )
    # .set_octree(
    #     octree_min=0.01,   
    #     octree_max=1.0,
    # )
    .add_agent(rov0)
)


sonar_viz = PolarSonarVisualizerAsync(
    azimuth_deg=90,
    range_min=1,
    range_max=30,
    plot_hz=5,
    use_cuda=True
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
            "velocity": estimate_velocity(last.get("Velocity")),
            "altitude": parse_depth(last.get("Depth")),
            "front_range": estimate_front_obstacle(last.get("RangeFinder")),
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
