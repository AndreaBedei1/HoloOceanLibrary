"""
camera.py
---------

Defines the RGB camera sensor for HoloOcean simulations.
This sensor captures visual frames from the simulated environment,
providing standard RGB image data for perception and computer vision tasks.
"""

from lib.sensors.base import BaseSensor


class RGBCamera(BaseSensor):
    """
    RGB camera sensor configuration.

    This sensor simulates a visual RGB camera that captures image frames
    from the underwater environment. It supports configurable frame rate,
    resolution, and optional field-of-view or optical parameters.

    Parameters
    ----------
    name : str, optional
        Custom sensor name (e.g., "FrontCamera"). Default is ``"FrontCamera"``.
    Hz : int, optional
        Frame capture frequency in Hertz. Default is ``10``.
    socket : str, optional
        Data connection socket name. Default is ``"CameraSocket"``.
    CaptureWidth : int, optional
        Frame width in pixels. Default is ``640``.
    CaptureHeight : int, optional
        Frame height in pixels. Default is ``480``.
    **kwargs
        Additional camera parameters (e.g., ``FOV``, ``Gamma``, ``Gain``)
        forwarded to the base configuration.

    Examples
    --------
    >>> from lib.sensors.camera import RGBCamera
    >>> cam = RGBCamera(name="FrontCamera", Hz=30, CaptureWidth=800, CaptureHeight=600, FOV=90.0)
    >>> print(cam.to_dict())
    {'sensor_type': 'RGBCamera', 'sensor_name': 'FrontCamera', 'socket': 'CameraSocket', 'Hz': 30,
     'configuration': {'CaptureWidth': 800, 'CaptureHeight': 600, 'FOV': 90.0}}
    """

    def __init__(
        self,
        name: str = "FrontCamera",
        Hz: int = 10,
        socket: str = "CameraSocket",
        CaptureWidth: int = 640,
        CaptureHeight: int = 480,
        **kwargs
    ):
        super().__init__(
            sensor_type="RGBCamera",
            sensor_name=name,
            socket=socket,
            Hz=Hz,
            CaptureWidth=CaptureWidth,
            CaptureHeight=CaptureHeight,
            **kwargs
        )
