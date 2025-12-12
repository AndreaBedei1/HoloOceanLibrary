import holoocean
import numpy as np
import cv2
import time
import threading
from queue import Queue, Empty

from controllers.keyboard_controller import KeyboardController
from lib.scenario_builder import ScenarioConfig
from lib.worlds import World
from lib.rover import Rover
from lib.scanning_sonar import ScanningImagingSonar


# ============================
# THREAD-SAFE SHARED STATE
# ============================
latest_state = {}
lock = threading.Lock()
running = True

# ============================
# FPS COUNTER
# ============================
fps_count = 0
fps_t0 = time.time()

# ============================
# SONAR THREAD STATE
# ============================
sonar_queue = Queue(maxsize=1)     # latest-only
sonar_img_lock = threading.Lock()
latest_sonar_img = None

SONAR_KEY = "SinglebeamSonar"  # nome del sonar nello state


# ============================
# LAST VALID SENSOR VALUES
# ============================
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
# TELEMETRY HUD (MAIN THREAD)
# ============================
def draw_telemetry_hud():

    hud = np.zeros((400, 600, 3), dtype=np.uint8)

    vel = last_valid["Velocity"]
    speed_knots = None
    if vel is not None:
        speed_knots = np.linalg.norm(vel) * 1.94384

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
    ]

    y = 30
    for line in lines:
        cv2.putText(hud, line, (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 0), 1, cv2.LINE_AA)
        y += 35

    cv2.imshow("Telemetry HUD", hud)


# ============================
# SONAR WORKER THREAD
# ============================
def sonar_worker(scanning_sonar, stop_event):
    global latest_sonar_img

    while not stop_event.is_set():
        try:
            profile = sonar_queue.get(timeout=0.1)
        except Empty:
            continue

        try:
            sonar_img = scanning_sonar.step(profile)
            if sonar_img is not None:
                with sonar_img_lock:
                    latest_sonar_img = sonar_img
        finally:
            sonar_queue.task_done()


def get_latest_sonar_image():
    with sonar_img_lock:
        return None if latest_sonar_img is None else latest_sonar_img.copy()


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
    ScenarioConfig(name="BlueROV_Keyboard_Sonar")
    .set_package("Ocean")
    .set_world(World.Dam)
    .set_main_agent("rov0")
    .add_agent(rov0)
)

scenario_dict = scenario.to_dict()


# ============================
# MAIN SIMULATION LOOP
# ============================
print("Avvio HoloOcean...")

with holoocean.make(
    scenario_cfg=scenario_dict,
    show_viewport=False,
    ticks_per_sec=100,
    frames_per_sec=True
) as env:

    scanning_sonar = ScanningImagingSonar(
        azimuth_bins=256,
        range_bins=512,
        range_max=50.0,
        device="cuda"
    )

    controller = KeyboardController()

    sonar_stop_event = threading.Event()
    sonar_thread = threading.Thread(
        target=sonar_worker,
        args=(scanning_sonar, sonar_stop_event),
        daemon=True
    )
    sonar_thread.start()

    print("Simulazione in esecuzione...")

    try:
        while running:

            cmd = controller.get_command()
            if cmd is None:
                break

            state = env.step(cmd)

            # ============================
            # FPS PRINT
            # ============================
            fps_count += 1
            now = time.time()
            if now - fps_t0 >= 1.0:
                print(f"[FPS] {fps_count}")
                fps_count = 0
                fps_t0 = now

            # ============================
            # UPDATE SHARED STATE
            # ============================
            with lock:
                latest_state = state

            # ============================
            # UPDATE LAST VALID VALUES
            # ============================
            for alias, holo_name in SENSOR_MAP.items():
                if holo_name in state:
                    last_valid[alias] = state[holo_name]

            # ============================
            # CAMERA
            # ============================
            if "FrontCamera" in state:
                frame = state["FrontCamera"]
                cv2.imshow("Front Camera", frame[:, :, :3])

            # ============================
            # PUSH SONAR PROFILE (ASYNC)
            # ============================
            if SONAR_KEY in state:
                profile = state[SONAR_KEY]

                if sonar_queue.full():
                    try:
                        sonar_queue.get_nowait()
                        sonar_queue.task_done()
                    except Empty:
                        pass

                sonar_queue.put(profile)

            # ============================
            # SHOW SONAR IMAGE (FROM WORKER)
            # ============================
            sonar_img = get_latest_sonar_image()
            if sonar_img is not None:
                sonar_img = cv2.resize(
                    sonar_img, (600, 400),
                    interpolation=cv2.INTER_NEAREST
                )
                cv2.imshow("Reconstructed Sonar", sonar_img)

            # ============================
            # TELEMETRY HUD
            # ============================
            draw_telemetry_hud()

            # ============================
            # UI LOOP
            # ============================
            if cv2.waitKey(1) & 0xFF == ord("q"):
                running = False
                break

    except KeyboardInterrupt:
        running = False
    finally:
        sonar_stop_event.set()
        sonar_thread.join(timeout=1.0)

cv2.destroyAllWindows()
print("\nSimulazione terminata.")
