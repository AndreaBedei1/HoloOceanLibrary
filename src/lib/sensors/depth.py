"""
depth.py
--------

Defines the Depth Sensor for HoloOcean simulations.
This sensor measures the agent’s depth (or pressure) relative to the water surface,
optionally including Gaussian noise to simulate sensor uncertainty.
"""

from lib.sensors.base import BaseSensor


class DepthSensor(BaseSensor):
    """
    Depth or pressure sensor configuration.

    This sensor measures the underwater depth of the vehicle based on pressure
    or vertical position. It can optionally include additive Gaussian noise
    to emulate real-world sensor variability. The data is typically used for
    depth control, buoyancy estimation, or logging purposes.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``30``.
    socket : str, optional
        Data connection socket name. Default is ``"DepthSocket"``.
    Sigma : float, optional
        Standard deviation of simulated measurement noise (meters).
        Default is ``0.0`` (no noise).
    **kwargs
        Additional configuration parameters forwarded to the base sensor.

    Examples
    --------
    >>> from lib.sensors.depth import DepthSensor
    >>> depth = DepthSensor(Hz=20, Sigma=0.2)
    >>> print(depth.to_dict())
    {'sensor_type': 'DepthSensor', 'socket': 'DepthSocket', 'Hz': 20,
     'configuration': {'Sigma': 0.2}}
    """

    def __init__(
        self,
        Hz: int = 30,
        socket: str = "DepthSocket",
        Sigma: float = 0.0,
        **kwargs
    ):
        super().__init__(
            sensor_type="DepthSensor",
            socket=socket,
            Hz=Hz,
            Sigma=Sigma,
            **kwargs
        )
