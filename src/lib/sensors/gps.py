"""
gps.py
------

Defines the GPS Sensor for HoloOcean simulations.
This sensor provides simulated global positioning data, optionally including
depth and noise to emulate underwater surface or buoy-based GPS systems.
"""

from lib.sensors.base import BaseSensor


class GPSSensor(BaseSensor):
    """
    Global Positioning System (GPS) sensor configuration.

    This sensor simulates a GPS receiver that reports global position data
    in latitude, longitude, and altitude (or depth). It can include
    configurable Gaussian noise and a fixed depth offset to emulate
    surface buoys or shallow water GPS readings.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``1``.
    socket : str, optional
        Data connection socket name. Default is ``"GPSSocket"``.
    Sigma : float, optional
        Standard deviation of position noise (meters). Default is ``0.0``.
    Depth : float, optional
        Fixed depth offset below the surface (meters). Default is ``2.0``.
    DepthSigma : float, optional
        Standard deviation of depth measurement noise (meters). Default is ``0.0``.
    **kwargs
        Additional configuration parameters forwarded to the base sensor.

    Examples
    --------
    >>> from lib.sensors.gps import GPSSensor
    >>> gps = GPSSensor(Hz=2, Sigma=0.5, Depth=1.5)
    >>> print(gps.to_dict())
    {'sensor_type': 'GPSSensor', 'socket': 'GPSSocket', 'Hz': 2,
     'configuration': {'Sigma': 0.5, 'Depth': 1.5, 'DepthSigma': 0.0}}
    """

    def __init__(
        self,
        Hz: int = 1,
        socket: str = "GPSSocket",
        Sigma: float = 0.0,
        Depth: float = 2.0,
        DepthSigma: float = 0.0,
        **kwargs
    ):
        super().__init__(
            sensor_type="GPSSensor",
            socket=socket,
            Hz=Hz,
            Sigma=Sigma,
            Depth=Depth,
            DepthSigma=DepthSigma,
            **kwargs
        )
