"""
raycast_lidar.py
----------------

Defines the Raycast LiDAR sensor for HoloOcean simulations.
This sensor emulates a rotating LiDAR device that measures distances
to surrounding objects by casting multiple rays in 3D space.

Note:
    This sensor is currently marked as *Work In Progress* in HoloOcean
    and may have limited or unstable functionality.
"""

import warnings
from lib.sensors.base import BaseSensor


class RaycastLidar(BaseSensor):
    """
    Raycast LiDAR sensor configuration.

    This sensor simulates a multi-channel rotating LiDAR similar to
    Velodyne or Ouster devices. It emits rays across a configurable
    vertical and horizontal field of view and measures the distance
    to the first object hit by each beam.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``10``.
    socket : str, optional
        Data connection socket name. Default is ``"LidarSocket"``.
    Channels : int, optional
        Number of vertical channels (laser emitters). Default is ``32``.
    Range : float, optional
        Maximum detection range in meters. Default is ``500.0``.
    PointsPerSecond : int, optional
        Number of LiDAR points generated per second. Default is ``56000``.
    RotationFrequency : float, optional
        Rotation speed in Hertz (rotations per second). Default is ``10.0``.
    UpperFovLimit : float, optional
        Upper vertical field-of-view limit (degrees). Default is ``10.0``.
    LowerFovLimit : float, optional
        Lower vertical field-of-view limit (degrees). Default is ``-30.0``.
    HorizontalFov : float, optional
        Horizontal field-of-view (degrees). Default is ``360.0``.
    AtmospAttenRate : float, optional
        Atmospheric attenuation rate (1/m). Default is ``0.004``.
    RandomSeed : int, optional
        Random seed for reproducibility. Default is ``0``.
    DropOffGenRate : float, optional
        Probability rate of point drop-off generation. Default is ``0.45``.
    DropOffIntensityLimit : float, optional
        Intensity threshold for point drop-off. Default is ``0.8``.
    DropOffAtZeroIntensity : float, optional
        Probability of drop-off when intensity = 0. Default is ``0.4``.
    ShowDebugPoints : bool, optional
        If True, enables visualization of LiDAR beams in simulation. Default is ``False``.
    NoiseStdDev : float, optional
        Standard deviation of range noise (meters). Default is ``0.0``.
    **kwargs
        Additional parameters forwarded to the base configuration.

    Warnings
    --------
    UserWarning
        Issued when the sensor is initialized, as it is currently marked as
        *Work In Progress* in HoloOcean and may not be fully supported.

    Examples
    --------
    >>> from lib.sensors.raycast_lidar import RaycastLidar
    >>> lidar = RaycastLidar(Channels=16, Range=120.0, RotationFrequency=5.0)
    RaycastLidar is marked as *Work In Progress* in HoloOcean and may not be fully supported.
    >>> print(lidar.to_dict())
    {'sensor_type': 'RaycastLidar', 'socket': 'LidarSocket', 'Hz': 10,
     'configuration': {'Channels': 16, 'Range': 120.0, 'PointsPerSecond': 56000,
                       'RotationFrequency': 5.0, 'UpperFovLimit': 10.0,
                       'LowerFovLimit': -30.0, 'HorizontalFov': 360.0,
                       'AtmospAttenRate': 0.004, 'RandomSeed': 0,
                       'DropOffGenRate': 0.45, 'DropOffIntensityLimit': 0.8,
                       'DropOffAtZeroIntensity': 0.4, 'ShowDebugPoints': False,
                       'NoiseStdDev': 0.0}}
    """

    def __init__(
        self,
        Hz: int = 10,
        socket: str = "LidarSocket",
        Channels: int = 32,
        Range: float = 500.0,
        PointsPerSecond: int = 56000,
        RotationFrequency: float = 10.0,
        UpperFovLimit: float = 10.0,
        LowerFovLimit: float = -30.0,
        HorizontalFov: float = 360.0,
        AtmospAttenRate: float = 0.004,
        RandomSeed: int = 0,
        DropOffGenRate: float = 0.45,
        DropOffIntensityLimit: float = 0.8,
        DropOffAtZeroIntensity: float = 0.4,
        ShowDebugPoints: bool = False,
        NoiseStdDev: float = 0.0,
        **kwargs
    ):
        warnings.warn(
            "RaycastLidar is marked as *Work In Progress* in HoloOcean "
            "and may not be fully supported.",
            UserWarning,
        )

        super().__init__(
            sensor_type="RaycastLidar",
            socket=socket,
            Hz=Hz,
            Channels=Channels,
            Range=Range,
            PointsPerSecond=PointsPerSecond,
            RotationFrequency=RotationFrequency,
            UpperFovLimit=UpperFovLimit,
            LowerFovLimit=LowerFovLimit,
            HorizontalFov=HorizontalFov,
            AtmospAttenRate=AtmospAttenRate,
            RandomSeed=RandomSeed,
            DropOffGenRate=DropOffGenRate,
            DropOffIntensityLimit=DropOffIntensityLimit,
            DropOffAtZeroIntensity=DropOffAtZeroIntensity,
            ShowDebugPoints=ShowDebugPoints,
            NoiseStdDev=NoiseStdDev,
            **kwargs
        )
