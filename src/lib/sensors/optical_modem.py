"""
optical_modem.py
----------------

Defines the Optical Modem sensor for HoloOcean simulations.
This sensor simulates underwater optical communication between agents,
allowing data exchange through line-of-sight laser signaling with
configurable range, beam angle, and noise characteristics.
"""

from lib.sensors.base import BaseSensor


class OpticalModemSensor(BaseSensor):
    """
    Optical Modem sensor configuration.

    This sensor models an underwater optical communication device used for
    short-range data exchange between autonomous underwater vehicles (AUVs)
    or static beacons. Communication is possible only when another modem is
    within range and inside the field of view (FOV) cone of the laser beam.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``2``.
    socket : str, optional
        Data connection socket name. Default is ``"OpticalModemSocket"``.
    id : int, optional
        Unique identifier for this modem instance. Default is ``0``.
    MaxDistance : float, optional
        Maximum communication distance in meters. Default is ``50.0``.
    DistanceSigma : float, optional
        Standard deviation of range uncertainty (meters). Default is ``0.0``.
    LaserAngle : float, optional
        Full field of view of the optical cone (degrees). Default is ``60.0``.
    AngleSigma : float, optional
        Standard deviation of angular measurement noise (degrees). Default is ``0.0``.
    LaserDebug : bool, optional
        If True, enables debug visualization of the optical beam cone.
        Default is ``False``.
    DebugNumSides : int, optional
        Number of polygon sides used for debug cone rendering. Default is ``72``.
    **kwargs
        Additional parameters forwarded to the base configuration.

    Examples
    --------
    >>> from lib.sensors.optical_modem import OpticalModemSensor
    >>> modem = OpticalModemSensor(id=1, MaxDistance=40.0, LaserAngle=45.0)
    >>> print(modem.to_dict())
    {'sensor_type': 'OpticalModemSensor', 'socket': 'OpticalModemSocket', 'Hz': 2,
     'configuration': {'id': 1, 'MaxDistance': 40.0, 'DistanceSigma': 0.0,
                       'LaserAngle': 45.0, 'AngleSigma': 0.0,
                       'LaserDebug': False, 'DebugNumSides': 72}}
    """

    def __init__(
        self,
        Hz: int = 2,
        socket: str = "OpticalModemSocket",
        id: int = 0,
        MaxDistance: float = 50.0,
        DistanceSigma: float = 0.0,
        LaserAngle: float = 60.0,
        AngleSigma: float = 0.0,
        LaserDebug: bool = False,
        DebugNumSides: int = 72,
        **kwargs
    ):
        super().__init__(
            sensor_type="OpticalModemSensor",
            socket=socket,
            Hz=Hz,
            id=id,
            MaxDistance=MaxDistance,
            DistanceSigma=DistanceSigma,
            LaserAngle=LaserAngle,
            AngleSigma=AngleSigma,
            LaserDebug=LaserDebug,
            DebugNumSides=DebugNumSides,
            **kwargs
        )
