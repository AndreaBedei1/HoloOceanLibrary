"""
stereo_camera.py
----------------

Defines the Stereo RGB Camera sensor for HoloOcean simulations.
This sensor captures synchronized left and right RGB frames used to compute
stereo disparity and depth estimation.

It emulates a binocular vision setup similar to stereo vision systems
in robotics, such as ZED or RealSense cameras.
"""

from lib.sensors.base import BaseSensor


class StereoCamera(BaseSensor):
    """
    Stereo RGB camera configuration.

    This sensor simulates a stereo vision pair composed of left and right
    RGB cameras. It outputs paired images and can generate disparity or
    depth maps for 3D reconstruction, SLAM, or obstacle detection.
    The stereo baseline, field of view, and image resolution are fully
    configurable.

    Parameters
    ----------
    name : str, optional
        Custom sensor name. Default is ``"StereoCamera"``.
    Hz : int, optional
        Frame capture frequency in Hertz. Default is ``10``.
    socket : str, optional
        Data connection socket name. Default is ``"CameraSocket"``.
    width : int, optional
        Image width in pixels. Default is ``640``.
    height : int, optional
        Image height in pixels. Default is ``480``.
    FOV : float, optional
        Horizontal field of view in degrees. Default is ``90.0``.
    Baseline : float, optional
        Distance between the two virtual cameras (meters). Default is ``0.3``.
    DisparityScale : float, optional
        Scale factor for disparity-to-depth conversion. Default is ``1.0``.
    Gain : float, optional
        Gain factor applied to captured frames. Default is ``1.0``.
    Exposure : float, optional
        Exposure time in seconds. Default is ``0.01``.
    Gamma : float, optional
        Gamma correction value. Default is ``1.0``.
    UseNoise : bool, optional
        If True, adds photometric noise to the output images. Default is ``False``.
    **kwargs
        Additional configuration parameters forwarded to the base configuration.

    Examples
    --------
    >>> from lib.sensors.stereo_camera import StereoCamera
    >>> stereo = StereoCamera(Hz=15, Baseline=0.25, FOV=100.0)
    >>> print(stereo.to_dict())
    {'sensor_type': 'StereoCamera', 'sensor_name': 'StereoCamera',
     'socket': 'CameraSocket', 'Hz': 15,
     'configuration': {'CaptureWidth': 640, 'CaptureHeight': 480,
                       'FOV': 100.0, 'Baseline': 0.25,
                       'DisparityScale': 1.0, 'Gain': 1.0,
                       'Exposure': 0.01, 'Gamma': 1.0,
                       'UseNoise': False}}
    """

    def __init__(
        self,
        name: str = "StereoCamera",
        Hz: int = 10,
        socket: str = "CameraSocket",
        width: int = 640,
        height: int = 480,
        FOV: float = 90.0,
        Baseline: float = 0.3,
        DisparityScale: float = 1.0,
        Gain: float = 1.0,
        Exposure: float = 0.01,
        Gamma: float = 1.0,
        UseNoise: bool = False,
        **kwargs,
    ):
        super().__init__(
            sensor_type="StereoCamera",
            sensor_name=name,
            socket=socket,
            Hz=Hz,
            CaptureWidth=width,
            CaptureHeight=height,
            FOV=FOV,
            Baseline=Baseline,
            DisparityScale=DisparityScale,
            Gain=Gain,
            Exposure=Exposure,
            Gamma=Gamma,
            UseNoise=UseNoise,
            **kwargs,
        )
