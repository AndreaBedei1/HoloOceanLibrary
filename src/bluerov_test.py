# main_bluerov.py
# -----------------------------------------------------------
# BlueROV2 Keyboard Control Demo with Multiple HoloOcean Sensors
# -----------------------------------------------------------

import holoocean
import numpy as np
import cv2
import time
from controllers.keyboard_controller import KeyboardController

from lib.scenario_builder import ScenarioConfig
from lib.worlds import World
from lib.rover import Rover
from lib.sensors import Sensor


# --- Create the agent (BlueROV2) with all required sensors ---
rov0 = Rover.BlueROV2(
    name="rov0",
    location=[0, 0, -4],
    rotation=[0, 0, 0],
    control_scheme=0,
    sensors=[
        # --- Core navigation ---
        Sensor.Pose(socket="COM", Hz=30),
        Sensor.Depth(socket="DepthSocket", Hz=30, Sigma=0.2),
        Sensor.IMU(socket="IMUSocket", Hz=30),

        # --- Visual sensors ---
        Sensor.RGBCamera(
            name="FrontCamera",
            socket="CameraSocket",
            Hz=30,
            width=640,
            height=480,
            FOV=90.0,
        ),

        # --- Acoustic & navigation sensors ---
        Sensor.ImagingSonar(     # sostituisce SinglebeamSonar
            socket="SonarSocket",
            Hz=30,
            Azimuth=60.0,         # da 120 → 60 (campo dimezzato)
            Elevation=10.0,       # da 20 → 10
            RangeMin=1.0,
            RangeMax=20.0,        # da 30 → 20
            RangeBins=128,        # da 512 → 128
            AzimuthBins=128,      # da 512 → 128
            AddSigma=0.05,
            MultSigma=0.05,
            MultiPath=False,
            ScaleNoise=False,
        ),
        Sensor.DVL(
            socket="DVLSocket",
            Hz=30,
            Elevation=22.5,
            VelSigma=0.02,
            ReturnRange=True,
            MaxRange=40,
        ),

        # --- Proximity and environmental sensors ---
        Sensor.RangeFinder(
            socket="RangeSocket",
            Hz=30,
            Range=25.0,
            FOV=20.0,
            NoiseSigma=0.05,
        ),
        Sensor.Collision(
            socket="CollisionSocket",
            Hz=30,
        ),
        Sensor.Velocity(socket="COM", Hz=30),
    ],
)


# --- Build the scenario ---
scenario = (
    ScenarioConfig(name="BlueROV_Keyboard_Sonar")
    .set_package("Ocean")
    .set_world(World.Dam)
    .set_main_agent("rov0")
    .add_agent(rov0)
)

scenario_dict = scenario.to_dict()

# --- Print summary of the scenario ---
print("\n=== Scenario Summary ===")
print(f"Name: {scenario_dict['name']}")
print(f"World: {scenario_dict['world']}")
print(f"Main Agent: {scenario_dict['main_agent']}")
print("Sensors attached:")
for s in scenario_dict["agents"][0]["sensors"]:
    s_name = s.get("sensor_name", s["sensor_type"])
    print(f"  - {s_name:25s} | Type: {s['sensor_type']:<25s} | Hz: {s['Hz']}")
print("==========================\n")

# --- Start simulation ---
print("Avvio HoloOcean...")
with holoocean.make(scenario_cfg=scenario_dict, show_viewport=True) as env:
    controller = KeyboardController()
    print("\n Keyboard control active (WASD + ↑↓, R/F, Q/E — press Q in camera window to quit)\n")

    try:
        last_print = time.time()
        while True:
            cmd = controller.get_command()
            if cmd is None:
                break

            state = env.step(cmd)

            # Show front camera
            if "FrontCamera" in state:
                frame = state["FrontCamera"]
                cv2.imshow("Front Camera", frame[:, :, :3])

            # Show Imaging Sonar (2D)
            if "ImagingSonar" in state:
                sonar_img = state["ImagingSonar"]
                sonar_img = (255 * sonar_img / np.max(sonar_img + 1e-6)).astype(np.uint8)
                cv2.imshow("Imaging Sonar", sonar_img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Print depth and forward velocity occasionally
            if time.time() - last_print > 1.0:
                depth = state.get("DepthSensor", [np.nan])[0]
                vel = state.get("VelocitySensor", [np.nan, np.nan, np.nan])
                print(f"Depth: {depth:6.2f} m | Velocity: {vel}")
                last_print = time.time()

            time.sleep(0.03)

    except KeyboardInterrupt:
        print("\n Manual exit requested.")

cv2.destroyAllWindows()
print("\nSimulazione terminata.")
