import holoocean
import numpy as np
import cv2
import time

# ============================
# TRAJECTORY CONTROLLER
# ============================
class TrajectoryController:
    """
    Traiettoria deterministica a due fasi:
    - PRELOAD: allontanamento
    - RUN: ritorno sullo stesso path
    """

    def __init__(self, preload_time=60):
        self.t0 = time.time()
        self.preload_time = preload_time

    def is_run_phase(self):
        return (time.time() - self.t0) >= self.preload_time


    def command(self):
        t = time.time() - self.t0
        cmd = np.zeros(8, dtype=np.float32)

        speed = 25.0

        # ============================
        # PHASE 1 — PRELOAD (BACKWARD)
        # ============================
        if t < self.preload_time:
            cmd[4:] = -speed   # backward
            return cmd

        # ============================
        # PHASE 2 — RUN (FORWARD)
        # ============================
        t2 = t - self.preload_time

        if t2 < 70:
            cmd[4:] = +speed

        else:
            self.t0 = time.time()  # loop completo

        return cmd



# ============================
# BUILD SCENARIO
# ============================
def build_scenario():
    from lib.scenario_builder import ScenarioConfig
    from lib.worlds import World
    from lib.rover import Rover

    rov = Rover.BlueROV2(
        name="rov0",
        location=[0, 0, -50],
        rotation=[0, 0, 0],
        control_scheme=0,
    )

    scenario = (
        ScenarioConfig(name="AutonomousSonarTest")
        .set_package("Ocean")
        .set_world(World.Dam)
        .set_main_agent("rov0")
        .add_agent(rov)
    )

    return scenario.to_dict()


# ============================
# MAIN
# ============================
def main():

    scenario_cfg = build_scenario()

    # preload_time = quanto tempo vai "indietro"
    traj = TrajectoryController(preload_time=60)

    print("🌊 Avvio HoloOcean...")
    with holoocean.make(
        scenario_cfg=scenario_cfg,
        ticks_per_sec=30,
        show_viewport=False,   # niente viewport Unreal
    ) as env:

        print("🔁 Preload (indietro) → Run (avanti) automatico")

        fps_count = 0
        fps_t0 = time.time()

        while True:
            cmd = traj.command()
            state = env.step(cmd)

            # Visualizzi SOLO nella fase RUN
            if traj.is_run_phase():

                if "FrontCamera" in state:
                    cv2.imshow(
                        "Front Camera",
                        state["FrontCamera"][:, :, :3]
                    )

                fps_count += 1
                if fps_count % 60 == 0:
                    now = time.time()
                    fps = fps_count / (now - fps_t0)
                    print(f"FPS ≈ {fps:.1f}")
                    fps_count = 0
                    fps_t0 = now

                if cv2.waitKey(1) & 0xFF == 27:
                    break

    cv2.destroyAllWindows()
    print("🛑 Simulazione terminata")



# ============================
# ENTRY POINT
# ============================
if __name__ == "__main__":
    main()
