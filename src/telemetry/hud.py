import cv2
import numpy as np


def draw_telemetry_hud(data):
    hud = np.zeros((420, 900, 3), dtype=np.uint8)

    pose = data.get("pose")
    vel = data.get("velocity")

    lines = [
        "=== ROV TELEMETRY ===",

        f"Position: ({pose['pos'][0]:.1f}, {pose['pos'][1]:.1f}, {pose['pos'][2]:.1f}) m"
        if pose else "Position: None",

        f"Attitude: R={pose['rpy'][0]:.1f}°  P={pose['rpy'][1]:.1f}°  Y={pose['rpy'][2]:.1f}°"
        if pose else "Attitude: None",

        f"Speed: {vel['speed_xy']:.2f} m/s"
        if vel else "Speed: None",

        f"Vertical speed: {vel['vz']:.2f} m/s"
        if vel else "Vertical speed: None",

        f"Altitude: {data.get('altitude'):.2f} m"
        if data.get("altitude") is not None else "Altitude: None",

        f"Front obstacle: {data.get('front_range'):.2f} m"
        if data.get("front_range") is not None else "Front obstacle: None",

        f"Motion: {data.get('motion', 'UNKNOWN')}",
        "COLLISION DETECTED!"
        if data.get("collision") else "Collision: none",

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
        y += 26

    cv2.imshow("Telemetry HUD", hud)
