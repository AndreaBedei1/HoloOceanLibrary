import numpy as np


def parse_pose(T):
    """Extract position (m) and RPY (deg) from homogeneous transform."""
    if T is None:
        return None

    T = np.asarray(T)
    x, y, z = T[0, 3], T[1, 3], T[2, 3]
    R = T[:3, :3]

    yaw = np.degrees(np.arctan2(R[1, 0], R[0, 0]))
    pitch = np.degrees(
        np.arctan2(-R[2, 0], np.sqrt(R[2, 1]**2 + R[2, 2]**2))
    )
    roll = np.degrees(np.arctan2(R[2, 1], R[2, 2]))

    return {
        "pos": (x, y, z),
        "rpy": (roll, pitch, yaw),
    }
