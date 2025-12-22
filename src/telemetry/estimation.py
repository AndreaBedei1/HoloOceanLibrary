import numpy as np


def estimate_velocity(vel):
    if vel is None:
        return None

    v = np.asarray(vel).reshape(-1)
    return {
        "speed_xy": float(np.linalg.norm(v[:2])),
        "vz": float(v[2]),
    }


def estimate_altitude_from_dvl(dvl):
    if dvl is None:
        return None

    dvl = np.asarray(dvl).reshape(-1)
    if len(dvl) <= 3:
        return None

    ranges = dvl[3:]
    valid = ranges[ranges > 0]
    return float(np.min(valid)) if len(valid) else None


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
