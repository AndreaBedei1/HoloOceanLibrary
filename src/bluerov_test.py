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
from lib.spartaco_rov import create_spartaco_rov



# --- Create the agent (BlueROV3 Heavy / Spartaco ROV) ---
rov0 = create_spartaco_rov()


# --- Build the scenario ---
scenario = (
    ScenarioConfig(name="SpartacoROV_HoloOcean")
    .set_package("Ocean")
    .set_world(World.PierHarbor)   # ambiente realistico tipo porto
    .set_main_agent("spartaco_rov")
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
