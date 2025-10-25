"""
pose.py
-------

Defines the Pose Sensor for HoloOcean simulations.
This sensor provides ground-truth position and orientation of the vehicle
in the global reference frame, typically used for evaluation or debugging.
"""

from lib.sensors.base import BaseSensor


class PoseSensor(BaseSensor):
    """
    Pose sensor configuration.

    This sensor provides the true 6-DoF pose of the vehicle in the global
    coordinate frame, including position (x, y, z) and orientation (roll,
    pitch, yaw). It is primarily intended for debugging, benchmarking,
    or validation of navigation and state estimation algorithms.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``30``.
    socket : str, optional
        Data connection socket name. Default is ``"COM"``.
    **kwargs
        Additional parameters forwarded to the base sensor configuration.

    Examples
    --------
    >>> from lib.sensors.pose import PoseSensor
    >>> pose = PoseSensor(Hz=60)
    >>> print(pose.to_dict())
    {'sensor_type': 'PoseSensor', 'socket': 'COM', 'Hz': 60}
    """

    def __init__(self, Hz: int = 30, socket: str = "COM", **kwargs):
        super().__init__(
            sensor_type="PoseSensor",
            socket=socket,
            Hz=Hz,
            **kwargs
        )
