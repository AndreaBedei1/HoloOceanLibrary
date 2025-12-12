"""
rgbd_camera.py
--------------

Defines the RGB-D Camera sensor for HoloOcean simulations.
This sensor captures synchronized color (RGB) and depth images,
allowing visual and geometric perception of the environment.

Note
----
This sensor is currently marked as *Work In Progress* in HoloOcean
and may not function correctly in all worlds.
"""

import warnings
from lib.sensors.base import BaseSensor


class RGBDCamera(BaseSensor):
    """
    RGB-D camera sensor configuration.

    This sensor provides both RGB images and corresponding depth maps,
    simulating a depth camera such as an Intel RealSense or Microsoft Kinect.
    It can be used for visual SLAM, 3D reconstruction, or perception tasks.
    The depth data is generated based on scene geometry and camera intrinsics.

    Parameters
    ----------
    name : str, optional
        Custom sensor name. Default is ``"RGBDCamera"``.
    Hz : int, optional
        Frame capture frequency in Hertz. Default is ``10``.
    socket : str, optional
        Data connection socket name. Default is ``"CameraSocket"``.
    CaptureWidth : int, optional
        Frame width in pixels. Default is ``640``.
    CaptureHeight : int, optional
        Frame height in pixels. Default is ``480``.
    FovAngle : float, optional
        Camera field of view in degrees. Default is ``90.0``.
    TargetGamma : float, optional
        Gamma correction factor for output images. Default is ``1.0``.
    **kwargs
        Additional camera parameters forwarded to the base configuration.

    Warnings
    --------
    UserWarning
        Issued at initialization since this sensor is marked as *Work In Progress*
        in HoloOcean and may not function correctly in all worlds.

    Examples
    --------
    >>> from lib.sensors.rgbd_camera import RGBDCamera
    >>> rgbd = RGBDCamera(Hz=15, FovAngle=100.0)
    RGBDCamera is marked as *Work In Progress* in HoloOcean and may not function correctly in all worlds.
    >>> print(rgbd.to_dict())
    {'sensor_type': 'RGBDCamera', 'sensor_name': 'RGBDCamera', 'socket': 'CameraSocket', 'Hz': 15,
     'configuration': {'CaptureWidth': 640, 'CaptureHeight': 480,
                       'FovAngle': 100.0, 'TargetGamma': 1.0}}
    """

    def __init__(
        self,
        name: str = "RGBDCamera",
        Hz: int = 10,
        socket: str = "CameraSocket",
        CaptureWidth: int = 640,
        CaptureHeight: int = 480,
        FovAngle: float = 90.0,
        TargetGamma: float = 1.0,
        **kwargs
    ):
        warnings.warn(
            "RGBDCamera is marked as *Work In Progress* in HoloOcean "
            "and may not function correctly in all worlds.",
            UserWarning,
        )

        super().__init__(
            sensor_type="RGBDCamera",
            sensor_name=name,
            socket=socket,
            Hz=Hz,
            CaptureWidth=CaptureWidth,
            CaptureHeight=CaptureHeight,
            FovAngle=FovAngle,
            TargetGamma=TargetGamma,
            **kwargs
        )
