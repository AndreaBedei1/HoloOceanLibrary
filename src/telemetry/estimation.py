import numpy as np


def estimate_velocity(vel):
    if vel is None:
        return None

    v = np.asarray(vel).reshape(-1)
    return {
        "speed_xy": float(np.linalg.norm(v[:2])),
        "vz": float(v[2]),
    }

def parse_depth(depth):
    if depth is None:
        return None

    depth = np.asarray(depth)

    if depth.size == 0:
        return None

    return float(depth.reshape(-1)[0])


def estimate_motion_state(imu, threshold=0.5):
    if imu is None:
        return "STABLE"

    imu = np.asarray(imu).reshape(-1)
    acc = imu[:3]

    # euristica volutamente isolata
    return (
        "MANEUVERING"
        if np.linalg.norm(acc + np.array([0, 0, 9.8])) > threshold
        else "STABLE"
    )


def estimate_front_obstacle(rangefinder):
    if rangefinder is None or len(rangefinder) == 0:
        return None
    return float(rangefinder[0])
