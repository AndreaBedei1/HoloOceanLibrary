import cv2
import numpy as np


def _fmt_vec3(pos):
    return f"({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})"


def draw_telemetry_hud(data, *, window_name="Telemetry HUD"):
    """
    data expected keys (all optional):
      - pose: {"pos": (x,y,z), "rpy": (roll,pitch,yaw)}
      - velocity: {"vx":..,"vy":..,"vz":..}  (optionally also speed_xy/speed_3d)
      - altitude: float (m)
      - front_range: float (m)
      - motion: str
      - collision: bool
    """
    pose = data.get("pose") or None
    vel = data.get("velocity") or None

    # Velocity derived metrics (robust to missing fields)
    speed_xy = None
    speed_3d = None
    if isinstance(vel, dict):
        vx = vel.get("vx")
        vy = vel.get("vy")
        vz = vel.get("vz")
        if isinstance(vx, (int, float)) and isinstance(vy, (int, float)):
            speed_xy = float(np.hypot(vx, vy))
        if (
            isinstance(vx, (int, float))
            and isinstance(vy, (int, float))
            and isinstance(vz, (int, float))
        ):
            speed_3d = float(np.sqrt(vx * vx + vy * vy + vz * vz))

    altitude = data.get("altitude", None)
    under_range = data.get("under_range", None)
    motion = data.get("motion", "UNKNOWN")
    collision = bool(data.get("collision", False))

    lines = [
        "=== ROV TELEMETRY ===",
        "",
        f"Position: {_fmt_vec3(pose['pos'])} m" if pose else "Position: None",
        (
            f"Attitude: R={pose['rpy'][0]:.1f} deg  P={pose['rpy'][1]:.1f} deg  Y={pose['rpy'][2]:.1f} deg"
            if pose else "Attitude: None"
        ),
        "",
        (
            f"Velocity: vx={vel.get('vx', float('nan')):.2f}  vy={vel.get('vy', float('nan')):.2f}  vz={vel.get('vz', float('nan')):.2f} m/s"
            if isinstance(vel, dict) else "Velocity: None"
        ),
        f"Speed XY: {speed_xy:.2f} m/s" if speed_xy is not None else "Speed XY: None",
        f"Speed 3D: {speed_3d:.2f} m/s" if speed_3d is not None else "Speed 3D: None",
        "",
        f"Depth: {altitude:.2f} m" if isinstance(altitude, (int, float)) else "Altitude: None",
        f"Distance from seabed: {under_range:.2f} m" if isinstance(under_range, (int, float)) else "Distance from seabed: None",
        f"Motion: {motion}",
        "",
        ("COLLISION DETECTED!" if collision else "Collision: none"),
        "",
        "Q: quit",
    ]

    # Create HUD image sized to content
    h = 30 + 26 * len(lines) + 10
    w = 900
    hud = np.zeros((h, w, 3), dtype=np.uint8)

    y = 30
    for line in lines:
        color = (0, 255, 0)
        if "COLLISION" in line:
            color = (0, 0, 255)  # red
        cv2.putText(
            hud,
            line,
            (10, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            1,
            cv2.LINE_AA,
        )
        y += 26

    cv2.imshow(window_name, hud)
    return hud
