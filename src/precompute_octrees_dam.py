import holoocean
import numpy as np
import time
from tqdm import tqdm

from lib.scenario_builder import ScenarioConfig
from lib.worlds import World
from lib.rover import Rover


# ============================
# BUILD SCENARIO (stesso mondo + sonar!)
# ============================
rov0 = Rover.BlueROV2(
    name="rov0",
    location=[0, 0, -4],
    rotation=[0, 0, 0],
    control_scheme=0,
)

scenario = (
    ScenarioConfig(name="Precompute_Dam_ImagingSonar")
    .set_package("Ocean")
    .set_world(World.Dam)
    .set_main_agent("rov0")
    .add_agent(rov0)
)

scenario_dict = scenario.to_dict()


# ============================
# DUMMY COMMAND (come da doc)
# ============================
# Non importa cosa fai, basta muoversi un po'
command = np.zeros(8, dtype=np.float32)
command[4:] = -20  # thrusters


print("🔧 Precomputo octree in corso (Dam + ImagingSonar)...")

with holoocean.make(
    scenario_cfg=scenario_dict,
    show_viewport=False,     # 🔴 fondamentale
    ticks_per_sec=30,        # lento va bene
    frames_per_sec=False     # 🔴 niente realtime cap
) as env:

    for i in tqdm(range(1000)):
        env.act("rov0", command)
        env.tick()
        time.sleep(0.01)

print("✅ Octree generate e salvate.")
