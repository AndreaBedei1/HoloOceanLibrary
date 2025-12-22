# HoloOceanLibrary

An object-oriented Python library for building **HoloOcean** scenarios without manually writing JSON files.
Define worlds, agents, and sensors programmatically, export directly to the structure expected by `holoocean.make()`, and control a **BlueROV2** interactively via keyboard.

This library is designed for rapid prototyping, sensor-fusion experiments, and reproducible simulation setups.

---

## Key Features

- **Scenario builder (`ScenarioConfig`)**  
  Compose complete HoloOcean scenarios in Python and export validated dictionaries.

- **World catalog (`World`)**  
  Predefined, validated world identifiers (e.g., `PierHarbor`, `Dam`, `SimpleUnderwater`).

- **Agent & rover factories**  
  High-level constructors such as `Rover.BlueROV2` with sensible default sensors.

- **Unified sensor factory (`Sensor`)**  
  Cameras, sonar variants, navigation sensors, proximity sensors, and lidar—configured in a consistent way.

- **Keyboard controller**  
  Pygame-based thruster control for manual BlueROV2 operation.

- **End-to-end demo**  
  A runnable example showing scenario creation, rendering, sensor visualization, and control.

---

## Requirements

- Python **3.x**
- Python packages:
  - `holoocean`
  - `numpy`
  - `pygame`
  - `opencv-python`
- HoloOcean assets installed locally  
  (follow the official HoloOcean documentation for asset installation)

### Install dependencies

```bash
pip install holoocean numpy pygame opencv-python
pip install -r requirements.txt
```

---

## Quick Start

Create a scenario programmatically and launch HoloOcean:

```python
from lib.scenario_builder import ScenarioConfig
from lib.worlds import World
from lib.rover import Rover
from lib.sensors import Sensor
import holoocean

rov = Rover.BlueROV2(
    name="rov0",
    sensors=[
        Sensor.Pose(),
        Sensor.Depth(sigma=0.2),
        Sensor.IMU(),
        Sensor.RGBCamera(
            name="FrontCamera",
            width=640,
            height=480,
            FOV=90,
        ),
    ],
)

scenario = (
    ScenarioConfig(name="BlueROV_Keyboard")
    .set_world(World.PierHarbor)
    .set_main_agent("rov0")
    .add_agent(rov)
)

with holoocean.make(
    scenario_cfg=scenario.to_dict(),
    show_viewport=True,
) as env:
    while True:
        # Call env.step(thruster_commands)
        ...
```

---

## Demo: Keyboard-Driven BlueROV2

The bundled demo builds a sonar-heavy scenario and maps keyboard input to the BlueROV2 thrusters.

```bash
python src/bluerov_test.py
```

### What the demo does

- Opens the HoloOcean viewport
- Displays OpenCV windows for:
  - Front RGB camera
  - Imaging sonar
- Sends real-time thruster commands using a keyboard controller

---

## Keyboard Mapping

| Motion | Keys |
|------|------|
| Surge (forward/backward) | **W / S** |
| Strafe (left/right) | **A / D** |
| Heave (up/down) | **↑ / ↓** |
| Yaw (rotate left/right) | **Q / E** |
| Pitch (nose up/down) | **R / F** |
| Quit | Close the pygame window or press **q** in an OpenCV window |

---

## Library Structure

```text
lib/
├── scenario_builder.py        # ScenarioConfig: package, world, agents, export
├── worlds.py                  # World catalog (PierHarbor, Dam, etc.)
├── agents.py                  # AgentConfig base class
├── rover.py                   # Rover.BlueROV2 factory with default sensors
├── sensors/
│   └── __init__.py            # Sensor registry and constructors
controllers/
├── keyboard_controller.py     # Pygame-based thruster controller
src/
├── bluerov_test.py            # End-to-end runnable demo
```

---

## Available Sensors

### Core Sensors
- `Pose`
- `Depth`
- `IMU`
- `RGBCamera`
- `StereoCamera`
- `RGBD`
- `SemanticSegmentation`

### Acoustic & Navigation
- `SinglebeamSonar`
- `SidescanSonar`
- `ImagingSonar`
- `ProfilingSonar`
- `DVL`
- `Magnetometer`
- `GPS`
- `Beacon`
- `OpticalModem`

### Environment & Physics
- `BST`
- `Dynamics`

### Proximity & Motion
- `RangeFinder`
- `Collision`
- `Velocity`

### Lidar
- `RaycastLidar`
- `RaycastSemanticLidar`

---

## Customizing Sensors

All sensors accept keyword arguments and export **HoloOcean-compatible dictionaries**.

```python
from lib.sensors import Sensor

custom_sonar = Sensor.ImagingSonar(
    Hz=15,
    Azimuth=90.0,
    Elevation=15.0,
    RangeMax=25.0,
    RangeBins=256,
    AzimuthBins=256,
    MultiPath=False,
)

print(custom_sonar.to_dict())
```

---

## License

MIT License — see the `LICENSE` file for details.

