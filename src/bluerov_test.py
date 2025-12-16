import holoocean
import numpy as np
import cv2
import time

from controllers.keyboard_controller import KeyboardController
from lib.scenario_builder import ScenarioConfig
from lib.worlds import World
from lib.rover import Rover
from utils.sonar_viz import PolarSonarVisualizerAsync


# ============================================================
# CONFIG
# ============================================================
RUNNING = True

# Last valid sensor values (raw)
last_valid = {
    "Pose": None,
    "Velocity": None,
    "IMU": None,
    "DVL": None,
    "RangeFinder": None,
    "Collision": None,
}

SENSOR_MAP = {
    "Pose": "PoseSensor",
    "Velocity": "VelocitySensor",
    "IMU": "IMUSensor",
    "DVL": "DVLSensor",
    "RangeFinder": "RangeFinderSensor",
    "Collision": "CollisionSensor",
}

# Derived telemetry (interpretable)
pose_info = None
speed_ms = None
vertical_speed = None
altitude = None
front_range = None
motion_state = "STABLE"


# ============================================================
# PARSING & ESTIMATION UTILS
# ============================================================
def parse_pose(T):
    """Extract position and RPY from homogeneous transform."""
    if T is None:
        return None

    T = np.array(T)
    x, y, z = T[0, 3], T[1, 3], T[2, 3]
    R = T[:3, :3]

    yaw = np.degrees(np.arctan2(R[1, 0], R[0, 0]))
    pitch = np.degrees(np.arctan2(-R[2, 0], np.sqrt(R[2, 1]**2 + R[2, 2]**2)))
    roll = np.degrees(np.arctan2(R[2, 1], R[2, 2]))

    return x, y, z, roll, pitch, yaw


def estimate_velocity(vel):
    if vel is None:
        return None, None
    v = np.array(vel)
    speed = float(np.linalg.norm(v[:2]))
    vz = float(v[2])
    return speed, vz


def estimate_altitude_from_dvl(dvl):
    if dvl is None:
        return None
    dvl = np.array(dvl).reshape(-1)
    if len(dvl) <= 3:
        return None

    ranges = dvl[3:]
    valid = ranges[ranges > 0]
    return float(np.min(valid)) if len(valid) > 0 else None


def estimate_motion_state(imu):
    if imu is None:
        return "STABLE"
    imu = np.array(imu).reshape(-1)
    acc = imu[:3]
    return "MANEUVERING" if np.linalg.norm(acc + np.array([0, 0, 9.8])) > 0.5 else "STABLE"


def estimate_front_obstacle(rf):
    if rf is None or len(rf) == 0:
        return None
    return float(rf[0])


# ============================================================
# TELEMETRY HUD
# ============================================================
def draw_telemetry_hud():
    hud = np.zeros((420, 900, 3), dtype=np.uint8)

    lines = [
        "=== ROV TELEMETRY ===",

        f"Position: ({pose_info[0]:.1f}, {pose_info[1]:.1f}, {pose_info[2]:.1f}) m"
            if pose_info else "Position: None",

        f"Attitude: R={pose_info[3]:.1f}°  P={pose_info[4]:.1f}°  Y={pose_info[5]:.1f}°"
            if pose_info else "Attitude: None",

        f"Speed: {speed_ms:.2f} m/s" if speed_ms is not None else "Speed: None",
        f"Vertical speed: {vertical_speed:.2f} m/s" if vertical_speed is not None else "Vertical speed: None",

        f"Altitude (DVL): {altitude:.2f} m" if altitude is not None else "Altitude (DVL): None",
        f"Front obstacle: {front_range:.2f} m" if front_range is not None else "Front obstacle: None",

        f"Motion: {motion_state}",
        "COLLISION DETECTED!" if last_valid["Collision"] else "Collision: none",

        "",
        "Q: quit",
    ]

    y = 30
    for line in lines:
        cv2.putText(hud, line, (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 0), 1, cv2.LINE_AA)
        y += 26

    cv2.imshow("Telemetry HUD", hud)


# ============================================================
# BUILD SCENARIO
# ============================================================
rov0 = Rover.BlueROV2(
    name="rov0",
    location=[0, 0, -4],
    rotation=[0, 0, 0],
    control_scheme=0,
)

scenario = (
    ScenarioConfig(name="BlueROV_Keyboard")
    .set_package("Ocean")
    .set_world(World.Dam)
    .set_main_agent("rov0")
    .add_agent(rov0)
)

scenario_dict = scenario.to_dict()

sonar_viz = PolarSonarVisualizerAsync(
    azimuth_deg=90.0,
    range_min=1.0,
    range_max=30.0,
    plot_hz=5.0,
    use_cuda=True
)


# ============================================================
# MAIN LOOP
# ============================================================
print("Avvio HoloOcean...")
controller = KeyboardController()

with holoocean.make(
    scenario_cfg=scenario_dict,
    show_viewport=False,
    ticks_per_sec=30,
    frames_per_sec=True
) as env:

    print("Simulazione in esecuzione...")

    try:
        while RUNNING:

            cmd = controller.get_command()
            if cmd is None:
                break

            state = env.step(cmd)

            # Cache raw sensors
            for alias, holo_name in SENSOR_MAP.items():
                if holo_name in state:
                    last_valid[alias] = state[holo_name]

            # Derive telemetry
            pose_info = parse_pose(last_valid["Pose"])
            speed_ms, vertical_speed = estimate_velocity(last_valid["Velocity"])
            altitude = estimate_altitude_from_dvl(last_valid["DVL"])
            front_range = estimate_front_obstacle(last_valid["RangeFinder"])
            motion_state = estimate_motion_state(last_valid["IMU"])

            # Cameras
            if "FrontCamera" in state:
                cv2.imshow("Front Camera", state["FrontCamera"][:, :, :3])
            if "SonarCamera" in state:
                cv2.imshow("Sonar Camera", state["SonarCamera"][:, :, :3])

            # Sonar
            if "ImagingSonar" in state:
                sonar_viz.submit(state["ImagingSonar"])
            sonar_viz.update_plot()

            draw_telemetry_hud()

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        pass

sonar_viz.close()
cv2.destroyAllWindows()
print("Simulazione terminata.")
