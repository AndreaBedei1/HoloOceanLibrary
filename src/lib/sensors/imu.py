"""
imu.py
------

Defines the Inertial Measurement Unit (IMU) sensor for HoloOcean simulations.
This sensor measures linear acceleration and angular velocity along the
vehicle’s local body axes, optionally including configurable noise.
"""

from lib.sensors.base import BaseSensor


class IMUSensor(BaseSensor):
    """
    Inertial Measurement Unit (IMU) sensor configuration.

    This sensor simulates an IMU that reports linear acceleration and
    angular velocity in the vehicle’s local coordinate frame. It is
    typically used for motion estimation, navigation filtering, or control
    feedback. Measurement noise can be configured to emulate real IMU data.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``30``.
    socket : str, optional
        Data connection socket name. Default is ``"IMUSocket"``.
    AccSigma : float, optional
        Standard deviation of acceleration noise (m/s²). Default is ``0.0``.
    GyroSigma : float, optional
        Standard deviation of angular velocity noise (rad/s). Default is ``0.0``.
    **kwargs
        Additional configuration parameters forwarded to the base sensor.

    Examples
    --------
    >>> from lib.sensors.imu import IMUSensor
    >>> imu = IMUSensor(Hz=100, AccSigma=0.02, GyroSigma=0.001)
    >>> print(imu.to_dict())
    {'sensor_type': 'IMUSensor', 'socket': 'IMUSocket', 'Hz': 100,
     'configuration': {'AccSigma': 0.02, 'GyroSigma': 0.001}}
    """

    def __init__(
        self,
        Hz: int = 30,
        socket: str = "IMUSocket",
        AccSigma: float = 0.0,
        GyroSigma: float = 0.0,
        **kwargs
    ):
        super().__init__(
            sensor_type="IMUSensor",
            socket=socket,
            Hz=Hz,
            AccSigma=AccSigma,
            GyroSigma=GyroSigma,
            **kwargs
        )
