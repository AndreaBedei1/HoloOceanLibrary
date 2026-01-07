import numpy as np

def rpy_deg_to_quaternion(rpy_deg):
    """
    Convert roll-pitch-yaw (deg) to quaternion (x, y, z, w)
    using XYZ convention.
    """
    roll, pitch, yaw = np.deg2rad(rpy_deg)

    cr = np.cos(roll * 0.5)
    sr = np.sin(roll * 0.5)
    cp = np.cos(pitch * 0.5)
    sp = np.sin(pitch * 0.5)
    cy = np.cos(yaw * 0.5)
    sy = np.sin(yaw * 0.5)

    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy

    return [qx, qy, qz, qw]

def pose_to_csv_fields(pose_dict):
    """
    Converts the output of parse_pose into:
    pose_x, pose_y, pose_z, qx, qy, qz, qw
    """
    if pose_dict is None:
        return None

    pos = pose_dict["pos"]          
    rpy = pose_dict["rpy"]          

    qx, qy, qz, qw = rpy_deg_to_quaternion(rpy)

    return [
        pos[0], pos[1], pos[2],
        qx, qy, qz, qw
    ]

def velocity_to_csv_fields(vel_dict):
    """
    Converts the output of estimate_velocity into:
    vel_x, vel_y, vel_z
    """
    if vel_dict is None:
        return None

    return [
        vel_dict.get("vx", 0.0),
        vel_dict.get("vy", 0.0),
        vel_dict.get("vz", 0.0),
    ]
