"""
dvl.py
------

Defines the Doppler Velocity Log (DVL) sensor for HoloOcean simulations.
This sensor measures the vehicle’s velocity relative to the seafloor
using Doppler shift principles, optionally returning range data and
measurement uncertainty.
"""

from lib.sensors.base import BaseSensor


class DVL(BaseSensor):
    """
    Doppler Velocity Log (DVL) sensor configuration.

    The DVL sensor estimates the vehicle’s linear velocity relative to the
    seabed using acoustic Doppler measurements. It can also return the
    estimated altitude (range) to the bottom and include configurable noise
    models for realistic underwater navigation simulation.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``20``.
    socket : str, optional
        Data connection socket name. Default is ``"DVLSocket"``.
    Elevation : float, optional
        Elevation angle (degrees) between the beams and the vehicle plane.
        Default is ``22.5``.
    DebugLines : bool, optional
        If True, enables visualization of DVL beam traces. Default is ``False``.
    VelSigma : float, optional
        Standard deviation of velocity noise (m/s). Default is ``0.02626``.
    ReturnRange : bool, optional
        If True, returns estimated bottom range (altitude). Default is ``True``.
    MaxRange : float, optional
        Maximum valid range in meters. Default is ``50.0``.
    RangeSigma : float, optional
        Standard deviation of range measurement noise (m). Default is ``0.1``.
    **kwargs
        Additional configuration parameters forwarded to the base sensor.

    Examples
    --------
    >>> from lib.sensors.dvl import DVL
    >>> dvl = DVL(Hz=30, VelSigma=0.02, MaxRange=40)
    >>> print(dvl.to_dict())
    {'sensor_type': 'DVLSensor', 'socket': 'DVLSocket', 'Hz': 30,
     'configuration': {'Elevation': 22.5, 'DebugLines': False,
                       'VelSigma': 0.02, 'ReturnRange': True,
                       'MaxRange': 40.0, 'RangeSigma': 0.1}}
    """

    def __init__(
        self,
        Hz: int = 20,
        socket: str = "DVLSocket",
        Elevation: float = 22.5,
        DebugLines: bool = False,
        VelSigma: float = 0.02626,
        ReturnRange: bool = True,
        MaxRange: float = 50.0,
        RangeSigma: float = 0.1,
        **kwargs
    ):
        super().__init__(
            sensor_type="DVLSensor",
            socket=socket,
            Hz=Hz,
            Elevation=Elevation,
            DebugLines=DebugLines,
            VelSigma=VelSigma,
            ReturnRange=ReturnRange,
            MaxRange=MaxRange,
            RangeSigma=RangeSigma,
            **kwargs
        )
