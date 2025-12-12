"""
beacon.py
---------

Defines the Acoustic Beacon Sensor for HoloOcean simulations.
This sensor emulates an underwater acoustic beacon used for localization
or range-based navigation.
"""

from lib.sensors.base import BaseSensor


class AcousticBeaconSensor(BaseSensor):
    """
    Acoustic Beacon Sensor configuration.

    This sensor simulates an underwater acoustic beacon, which can be used
    for positioning, range measurements, or communication with AUVs/ROVs.
    It inherits from `BaseSensor` and allows flexible configuration of
    measurement noise, visibility checks, and maximum detection distance.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``2``.
    socket : str, optional
        Data connection socket name. Default is ``"BeaconSocket"``.
    id : int, optional
        Unique identifier of the beacon. Default is ``0``.
    CheckVisible : bool, optional
        If True, visibility constraints are applied before detection.
        Default is ``False``.
    MaxDistance : float, optional
        Maximum detection range in meters. Default is ``None`` (unlimited).
    DistanceSigma : float, optional
        Standard deviation of distance noise (meters). Default is ``0.0``.
    DistanceCov : float, optional
        Covariance of distance measurements. Default is ``0.0``.
    **kwargs
        Additional parameters forwarded to the base configuration.

    Examples
    --------
    >>> from lib.sensors.beacon import AcousticBeaconSensor
    >>> beacon = AcousticBeaconSensor(id=1, MaxDistance=50.0, DistanceSigma=0.05)
    >>> print(beacon.to_dict())
    {'sensor_type': 'AcousticBeaconSensor', 'socket': 'BeaconSocket', 'Hz': 2,
     'configuration': {'id': 1, 'CheckVisible': False,
                       'MaxDistance': 50.0, 'DistanceSigma': 0.05,
                       'DistanceCov': 0.0}}
    """

    def __init__(
        self,
        Hz: int = 2,
        socket: str = "BeaconSocket",
        id: int = 0,
        CheckVisible: bool = False,
        MaxDistance: float = None,
        DistanceSigma: float = 0.0,
        DistanceCov: float = 0.0,
        **kwargs
    ):
        super().__init__(
            sensor_type="AcousticBeaconSensor",
            socket=socket,
            Hz=Hz,
            id=id,
            CheckVisible=CheckVisible,
            MaxDistance=MaxDistance,
            DistanceSigma=DistanceSigma,
            DistanceCov=DistanceCov,
            **kwargs
        )
