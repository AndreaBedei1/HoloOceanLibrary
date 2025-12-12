"""
velocity.py
------------

Defines the Velocity Sensor for HoloOcean simulations.
This sensor reports the linear velocity of the agent in the global reference frame.
It is typically used for motion estimation, feedback control, and logging.
"""

from lib.sensors.base import BaseSensor


class VelocitySensor(BaseSensor):
    """
    Velocity sensor configuration.

    This sensor measures the linear velocity components (x, y, z)
    of the vehicle or agent in the global coordinate frame. It is
    commonly used in control loops, navigation algorithms, or as
    ground-truth data for evaluating estimators such as DVL- or
    IMU-based velocity reconstruction.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``30``.
    socket : str, optional
        Data connection socket name. Default is ``"COM"``.
    **kwargs
        Additional parameters forwarded to the base configuration.

    Examples
    --------
    >>> from lib.sensors.velocity import VelocitySensor
    >>> vel = VelocitySensor(Hz=60)
    >>> print(vel.to_dict())
    {'sensor_type': 'VelocitySensor', 'socket': 'COM', 'Hz': 60}
    """

    def __init__(
        self,
        Hz: int = 30,
        socket: str = "COM",
        **kwargs
    ):
        super().__init__(
            sensor_type="VelocitySensor",
            socket=socket,
            Hz=Hz,
            **kwargs
        )
