"""
rangefinder.py
--------------

Defines the Range Finder sensor for HoloOcean simulations.
This sensor measures distances to nearby objects along one or more
laser beams, useful for obstacle detection, mapping, or collision avoidance.
"""

from lib.sensors.base import BaseSensor


class RangeFinderSensor(BaseSensor):
    """
    Range Finder sensor configuration.

    This sensor emits one or more laser beams in predefined directions
    and reports the distance to the first detected collision along each beam.
    It can be used for proximity sensing, obstacle avoidance, or environment
    mapping tasks. Multiple beams can be configured to simulate multi-ray
    range sensors or scanning lidar-like devices.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``10``.
    socket : str, optional
        Data connection socket name. Default is ``"RangeSocket"``.
    LaserMaxDistance : float, optional
        Maximum measurable range in meters. Default is ``10.0``.
    LaserCount : int, optional
        Number of laser beams emitted. Default is ``1``.
    LaserAngle : float, optional
        Angular spread between beams in degrees. Default is ``0.0``.
    LaserDebug : bool, optional
        If True, enables visual debugging of the laser beams in the simulator.
        Default is ``False``.
    **kwargs
        Additional configuration parameters forwarded to the base sensor.

    Examples
    --------
    >>> from lib.sensors.rangefinder import RangeFinderSensor
    >>> rf = RangeFinderSensor(LaserCount=3, LaserMaxDistance=20.0, LaserAngle=15.0)
    >>> print(rf.to_dict())
    {'sensor_type': 'RangeFinderSensor', 'socket': 'RangeSocket', 'Hz': 10,
     'configuration': {'LaserMaxDistance': 20.0, 'LaserCount': 3,
                       'LaserAngle': 15.0, 'LaserDebug': False}}
    """

    def __init__(
        self,
        Hz: int = 10,
        socket: str = "RangeSocket",
        LaserMaxDistance: float = 10.0,
        LaserCount: int = 1,
        LaserAngle: float = 0.0,
        LaserDebug: bool = False,
        **kwargs
    ):
        super().__init__(
            sensor_type="RangeFinderSensor",
            socket=socket,
            Hz=Hz,
            LaserMaxDistance=LaserMaxDistance,
            LaserCount=LaserCount,
            LaserAngle=LaserAngle,
            LaserDebug=LaserDebug,
            **kwargs
        )
