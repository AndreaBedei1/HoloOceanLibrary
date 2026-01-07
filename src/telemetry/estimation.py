import numpy as np


def parse_velocity(vel):
    """
    Returns raw body/world velocity as vx, vy, vz
    """
    if vel is None:
        return None

    v = np.asarray(vel).reshape(-1)

    if v.shape[0] < 3:
        return None

    return {
        "vx": float(v[0]),
        "vy": float(v[1]),
        "vz": float(v[2]),
    }


def parse_depth(rangefinder):
    """
    Parses the depth value from a rangefinder sensor reading.
    Args:
        rangefinder (list or None): A list containing rangefinder readings, or None.
    Returns:
        float or None: The first value in the rangefinder list as a float, or None if the input is None or empty.
    """
    if rangefinder is None or len(rangefinder) == 0:
        return None
    return float(rangefinder[0])


def estimate_motion_state(imu, threshold=0.4):
    """
    Estimates the motion state of a system based on IMU acceleration data.
    Parameters
    ----------
    imu : array-like or None
        The IMU data containing at least the first three elements as acceleration (x, y, z) in m/s^2.
        If None, the function assumes the system is stable.
    threshold : float, optional
        The acceleration threshold (in m/s^2) above which the system is considered to be maneuvering.
        Default is 0.5.
    Returns
    -------
    str
        "MANEUVERING" if the norm of the acceleration (including gravity compensation) exceeds the threshold,
        otherwise "STABLE".
    """
    if imu is None:
        return "STABLE"

    imu = np.asarray(imu).reshape(-1)
    acc = imu[:3]

    return (
        "MANEUVERING"
        if np.linalg.norm(acc + np.array([0, 0, 9.8])) > threshold
        else "STABLE"
    )

def estimate_depth_from_seabed(rangefinder):
    """
    Estimates the depth from the seabed using rangefinder data.
    Parameters:
        rangefinder (list or sequence): A list or sequence containing rangefinder readings,
                                        where the first element represents the measured distance
                                        from the sensor to the seabed.
    Returns:
        float or None: The estimated depth as a float if rangefinder data is available,
                       otherwise None.
    """
    if rangefinder is None or len(rangefinder) == 0:
        return None
    return float(rangefinder[0])

