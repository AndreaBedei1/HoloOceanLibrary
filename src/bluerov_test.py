import holoocean
import numpy as np
import cv2
import time

from controllers.keyboard_controller import KeyboardController
from lib.scenario_builder import ScenarioConfig
from lib.worlds import World
from lib.rover import Rover
from utils.sonar_viz import PolarSonarVisualizerAsync

# ============================
# CONFIG
# ============================
running = True

# FPS counter
fps_count = 0
fps_t0 = time.time()

# Last valid telemetry values
last_valid = {
    "Pose": None,
    "Depth": None,
    "Velocity": None,
    "IMU": None,
    "DVL": None,
    "Ping2Sonar": None,
    "LaserLeft": None,
    "Collision": None,
}

SENSOR_MAP = {
    "Pose": "PoseSensor",
    "Depth": "DepthSensor",
    "Velocity": "VelocitySensor",
    "IMU": "IMUSensor",
    "DVL": "DVLSensor",
    "Ping2Sonar": "Ping2",
    "LaserLeft": "LaserRangefinderSensor",
    "Collision": "CollisionSensor",
}




# ============================
# TELEMETRY HUD
# ============================
def draw_telemetry_hud():
    hud = np.zeros((400, 700, 3), dtype=np.uint8)

    vel = last_valid["Velocity"]
    speed_knots = None
    if vel is not None:
        # vel può essere 3D; norm -> m/s, converti in knots
        speed_knots = float(np.linalg.norm(vel)) * 1.94384

    lines = [
        "=== TELEMETRIA ROV ===",
        f"Depth:     {last_valid['Depth']}",
        f"Speed:     {speed_knots:.2f} knots" if speed_knots is not None else "Speed:     None",
        f"Pose:      {last_valid['Pose']}",
        f"IMU:       {last_valid['IMU']}",
        f"DVL:       {last_valid['DVL']}",
        f"Ping2:     {last_valid['Ping2Sonar']}",
        f"Laser:     {last_valid['LaserLeft']}",
        f"Collision: {last_valid['Collision']}",
        "",
        "Q: quit",
    ]

    y = 30
    for line in lines:
        cv2.putText(
            hud, line, (10, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
            (0, 255, 0), 1, cv2.LINE_AA
        )
        y += 28

    cv2.imshow("Telemetry HUD", hud)


# ============================
# SONAR VISUALIZATION UTILS
# ============================
def normalize_sonar_to_u8(img):
    """
    Convertiamo a uint8 per mostrarlo bene.
    """
    if img is None:
        return None

    a = img
    if a.dtype != np.float32 and a.dtype != np.float64:
        a = a.astype(np.float32)

    # robust min/max (evita flicker quando ci sono outlier)
    lo = np.percentile(a, 2)
    hi = np.percentile(a, 98)
    if hi - lo < 1e-6:
        hi = lo + 1e-6

    a = (a - lo) / (hi - lo)
    a = np.clip(a, 0.0, 1.0)
    return (a * 255).astype(np.uint8)


# ============================
# BUILD SCENARIO
# ============================
rov0 = Rover.BlueROV2(
    name="rov0",
    location=[0, 0, -4],
    rotation=[0, 0, 0],
    control_scheme=0,
)

scenario = (
    ScenarioConfig(name="BlueROV_Keyboard_ImagingSonar")
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



# ============================
# MAIN LOOP
# ============================
print("Avvio HoloOcean...")

controller = KeyboardController()

# Anti-freeze: ticks alti ok, ma viewport off e sonar Hz basso (nel sensore!)
with holoocean.make(
    scenario_cfg=scenario_dict,
    show_viewport=False,
    ticks_per_sec=30,
    frames_per_sec=True
) as env:

    print("Simulazione in esecuzione...")

    try:
        while running:

            cmd = controller.get_command()
            if cmd is None:
                break

            state = env.step(cmd)

            # FPS print
            fps_count += 1
            now = time.time()
            if now - fps_t0 >= 1.0:
                print(f"[FPS] {fps_count}")
                fps_count = 0
                fps_t0 = now

            # Update telemetry cache
            for alias, holo_name in SENSOR_MAP.items():
                if holo_name in state:
                    last_valid[alias] = state[holo_name]

            # Front camera
            if "FrontCamera" in state:
                frame = state["FrontCamera"]
                cv2.imshow("Front Camera", frame[:, :, :3])

            if "SonarCamera" in state:
                img = state["SonarCamera"]
                cv2.imshow("Camera @ Sonar", img[:, :, :3])

            # Imaging sonar
            if "ImagingSonar" in state:
                sonar_viz.submit(state["ImagingSonar"])

            sonar_viz.update_plot()    

            # Telemetry HUD
            draw_telemetry_hud()

            # UI loop (MAI saltare waitKey, altrimenti OpenCV freeza)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                running = False
                break

    except KeyboardInterrupt:
        running = False

sonar_viz.close()
cv2.destroyAllWindows()
print("\nSimulazione terminata.")
