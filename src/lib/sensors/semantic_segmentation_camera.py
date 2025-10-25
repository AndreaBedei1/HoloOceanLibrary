"""
semantic_segmentation_camera.py
-------------------------------

Defines the Semantic Segmentation Camera for HoloOcean simulations.
This sensor captures images where each pixel represents a semantic class
(e.g., vehicle, seafloor, rock, coral), allowing perception and scene
understanding tasks.

Note
----
This sensor is currently marked as *Work In Progress* in HoloOcean
and may not be fully supported in all environments.
"""

import warnings
from lib.sensors.base import BaseSensor


class SemanticSegmentationCamera(BaseSensor):
    """
    Semantic segmentation camera configuration.

    This camera provides class-labeled images, where each pixel corresponds
    to a semantic category. It is used for computer vision, dataset generation,
    and perception research, allowing agents to identify and classify objects
    in the scene.

    Parameters
    ----------
    name : str, optional
        Custom sensor name. Default is ``"SemanticSegmentationCamera"``.
    Hz : int, optional
        Frame capture frequency in Hertz. Default is ``10``.
    socket : str, optional
        Data connection socket name. Default is ``"CameraSocket"``.
    CaptureWidth : int, optional
        Image width in pixels. Default is ``640``.
    CaptureHeight : int, optional
        Image height in pixels. Default is ``480``.
    **kwargs
        Additional parameters forwarded to the base configuration.

    Warnings
    --------
    UserWarning
        Issued at initialization since this sensor is *Work In Progress*
        in HoloOcean and may not be fully supported.

    Examples
    --------
    >>> from lib.sensors.semantic_segmentation_camera import SemanticSegmentationCamera
    >>> seg_cam = SemanticSegmentationCamera(Hz=15, CaptureWidth=800, CaptureHeight=600)
    SemanticSegmentationCamera is *Work In Progress* in HoloOcean and may not be fully supported.
    >>> print(seg_cam.to_dict())
    {'sensor_type': 'SemanticSegmentationCamera', 'sensor_name': 'SemanticSegmentationCamera',
     'socket': 'CameraSocket', 'Hz': 15,
     'configuration': {'CaptureWidth': 800, 'CaptureHeight': 600}}
    """

    def __init__(
        self,
        name: str = "SemanticSegmentationCamera",
        Hz: int = 10,
        socket: str = "CameraSocket",
        CaptureWidth: int = 640,
        CaptureHeight: int = 480,
        **kwargs
    ):
        warnings.warn(
            "SemanticSegmentationCamera is *Work In Progress* in HoloOcean "
            "and may not be fully supported.",
            UserWarning,
        )

        super().__init__(
            sensor_type="SemanticSegmentationCamera",
            sensor_name=name,
            socket=socket,
            Hz=Hz,
            configuration={
                "CaptureWidth": CaptureWidth,
                "CaptureHeight": CaptureHeight,
            },
            **kwargs
        )
