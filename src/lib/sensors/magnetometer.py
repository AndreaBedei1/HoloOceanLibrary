"""
magnetometer.py
----------------

Defines the Magnetometer sensor for HoloOcean simulations.
This sensor measures the direction of a reference magnetic vector
(e.g., the global X-axis or Earth’s magnetic field) expressed
in the vehicle’s local coordinate frame.
"""

from lib.sensors.base import BaseSensor


class MagnetometerSensor(BaseSensor):
    """
    Magnetometer sensor configuration.

    This sensor simulates a 3-axis magnetometer that measures the projection
    of a global magnetic field vector into the vehicle’s local body frame.
    It can include Gaussian noise and a customizable magnetic field vector,
    allowing simulation of different orientations or environments.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``30``.
    socket : str, optional
        Data connection socket name. Default is ``"MagSocket"``.
    Sigma : float, optional
        Standard deviation of measurement noise (Tesla). Default is ``0.0``.
    MagneticVector : list of float, optional
        Reference magnetic vector in global coordinates ``[x, y, z]``.
        Default is ``[1, 0, 0]`` (aligned with the global X-axis).
    **kwargs
        Additional configuration parameters forwarded to the base sensor.

    Examples
    --------
    >>> from lib.sensors.magnetometer import MagnetometerSensor
    >>> mag = MagnetometerSensor(Sigma=0.01, MagneticVector=[0.3, 0.1, 0.9])
    >>> print(mag.to_dict())
    {'sensor_type': 'MagnetometerSensor', 'socket': 'MagSocket', 'Hz': 30,
     'configuration': {'Sigma': 0.01, 'MagneticVector': [0.3, 0.1, 0.9]}}
    """

    def __init__(
        self,
        Hz: int = 30,
        socket: str = "MagSocket",
        Sigma: float = 0.0,
        MagneticVector: list = None,
        **kwargs
    ):
        super().__init__(
            sensor_type="MagnetometerSensor",
            socket=socket,
            Hz=Hz,
            Sigma=Sigma,
            MagneticVector=MagneticVector or [1, 0, 0],
            **kwargs
        )
