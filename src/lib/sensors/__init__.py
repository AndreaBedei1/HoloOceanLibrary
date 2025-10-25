"""
sensors/__init__.py
-------------------

Unified entry point for all HoloOcean sensor definitions.

This module provides a single factory-style class `Sensor` that aggregates
all available sensor types. Each sensor class is fully configurable and
inherits from BaseSensor, allowing you to override or extend any parameter
defined in the official HoloOcean documentation.

Usage example:
    from lib.sensors import Sensor

    sensors = [
        Sensor.Pose(),
        Sensor.Depth(Sigma=0.2),
        Sensor.IMU(),
        Sensor.RGBCamera(name="FrontCamera", width=800, height=600),
        Sensor.SinglebeamSonar(RangeMax=30.0),
        Sensor.DVL(MaxRange=50),
    ]
"""

# --- Base class ---
from lib.sensors.base import BaseSensor

# --- Core sensors ---
from lib.sensors.pose import PoseSensor
from lib.sensors.depth import DepthSensor
from lib.sensors.imu import IMUSensor
from lib.sensors.camera import RGBCamera
from lib.sensors.stereo_camera import StereoCamera
from lib.sensors.rgbd_camera import RGBDCamera
from lib.sensors.semantic_segmentation_camera import SemanticSegmentationCamera

# --- Acoustic & navigation sensors ---
from lib.sensors.sonar import SinglebeamSonar, SidescanSonar, ImagingSonar, ProfilingSonar
from lib.sensors.dvl import DVL
from lib.sensors.magnetometer import MagnetometerSensor
from lib.sensors.gps import GPSSensor
from lib.sensors.beacon import AcousticBeaconSensor
from lib.sensors.optical_modem import OpticalModemSensor

# --- Environmental & physical sensors ---
from lib.sensors.bst import BSTSensor
from lib.sensors.dynamics import DynamicsSensor

# --- Proximity and motion sensors ---
from lib.sensors.rangefinder import RangeFinderSensor
from lib.sensors.collision import CollisionSensor
from lib.sensors.velocity import VelocitySensor

# --- Lidar sensors ---
from lib.sensors.raycast_lidar import RaycastLidar
from lib.sensors.raycast_semantic_lidar import RaycastSemanticLidar


class Sensor:
    """
    Centralized registry of all HoloOcean sensor classes.
    """

    # --- Core sensors ---
    Pose = PoseSensor
    Depth = DepthSensor
    IMU = IMUSensor
    RGBCamera = RGBCamera
    StereoCamera = StereoCamera
    RGBD = RGBDCamera
    SemanticSegmentation = SemanticSegmentationCamera

    # --- Acoustic & navigation sensors ---
    SinglebeamSonar = SinglebeamSonar
    SidescanSonar = SidescanSonar
    ImagingSonar = ImagingSonar
    ProfilingSonar = ProfilingSonar
    DVL = DVL
    Magnetometer = MagnetometerSensor
    GPS = GPSSensor
    Beacon = AcousticBeaconSensor
    OpticalModem = OpticalModemSensor

    # --- Environmental & physical sensors ---
    BST = BSTSensor
    Dynamics = DynamicsSensor

    # --- Proximity and motion sensors ---
    RangeFinder = RangeFinderSensor
    Collision = CollisionSensor
    Velocity = VelocitySensor

    # --- Lidar sensors ---
    RaycastLidar = RaycastLidar
    RaycastSemanticLidar = RaycastSemanticLidar
