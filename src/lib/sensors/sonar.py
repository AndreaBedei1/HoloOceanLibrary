"""
sonar.py
--------

Defines the main sonar sensors available in HoloOcean (v2.1 and later).

Implements:
- SinglebeamSonar
- SidescanSonar
- ImagingSonar
- ProfilingSonar

Each sonar type simulates a different acoustic sensing configuration
used for underwater mapping, navigation, and perception.
"""

from lib.sensors.base import BaseSensor


# =====================================================================
# 1. Singlebeam Sonar
# =====================================================================

class SinglebeamSonar(BaseSensor):
    """
    Single-beam sonar configuration.

    Simulates a single conical acoustic beam returning echo intensity
    as a function of range. Useful for depth measurement or profiling
    along a single direction.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``10``.
    socket : str, optional
        Data connection socket name. Default is ``"SonarSocket"``.
    OpeningAngle : float, optional
        Cone opening angle (degrees). Default is ``30.0``.
    RangeMin, RangeMax : float, optional
        Minimum and maximum measurable ranges in meters.
        Defaults are ``0.5`` and ``30.0``.
    RangeBins : int, optional
        Number of bins used to discretize the return signal. Default is ``200``.
    AddSigma, MultSigma, RangeSigma : float, optional
        Additive, multiplicative, and range noise parameters. Defaults are small.
    ShowWarning : bool, optional
        Whether to display warning messages. Default is ``True``.
    ViewRegion, ViewOctree : bool or float, optional
        Debug visualization options for sonar rays. Defaults are ``False`` and ``-10.0``.
    WaterDensity, WaterSpeedSound : float, optional
        Physical parameters of the medium. Defaults are ``997.0`` kg/m³ and ``1480.0`` m/s.
    UseApprox : bool, optional
        Use approximate ray–collision model. Default is ``True``.
    **kwargs
        Additional configuration parameters.

    Examples
    --------
    >>> from lib.sensors.sonar import SinglebeamSonar
    >>> sonar = SinglebeamSonar(Hz=5, RangeMax=20.0)
    >>> print(sonar.to_dict()["sensor_type"])
    SinglebeamSonar
    """

    def __init__(
        self,
        Hz: int = 10,
        socket: str = "SonarSocket",
        OpeningAngle: float = 30.0,
        RangeMin: float = 0.5,
        RangeMax: float = 30.0,
        RangeBins: int = 200,
        AddSigma: float = 0.0,
        MultSigma: float = 0.0,
        RangeSigma: float = 0.1,
        ShowWarning: bool = True,
        InitOctreeRange: float = 40.0,
        ViewRegion: bool = False,
        ViewOctree: float = -10.0,
        WaterDensity: float = 997.0,
        WaterSpeedSound: float = 1480.0,
        UseApprox: bool = True,
        **kwargs
    ):
        super().__init__(
            sensor_type="SinglebeamSonar",
            socket=socket,
            Hz=Hz,
            OpeningAngle=OpeningAngle,
            RangeMin=RangeMin,
            RangeMax=RangeMax,
            RangeBins=RangeBins,
            AddSigma=AddSigma,
            MultSigma=MultSigma,
            RangeSigma=RangeSigma,
            ShowWarning=ShowWarning,
            InitOctreeRange=InitOctreeRange,
            ViewRegion=ViewRegion,
            ViewOctree=ViewOctree,
            WaterDensity=WaterDensity,
            WaterSpeedSound=WaterSpeedSound,
            UseApprox=UseApprox,
            **kwargs
        )


# =====================================================================
# 2. Sidescan Sonar
# =====================================================================

class SidescanSonar(BaseSensor):
    """
    Side-scan sonar configuration.

    Simulates a narrow-elevation, wide-azimuth sonar used to image the
    seafloor laterally. Produces high-resolution acoustic maps for
    terrain or object detection.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``10``.
    Azimuth : float, optional
        Azimuthal field of view in degrees. Default is ``170.0``.
    Elevation : float, optional
        Elevation angle of the sonar beam (degrees). Default is ``0.25``.
    RangeMin, RangeMax : float, optional
        Minimum and maximum ranges in meters. Defaults are ``0.5`` and ``40.0``.
    RangeBins : int, optional
        Number of range samples. Default is ``2000``.
    AddSigma, MultSigma : float, optional
        Additive and multiplicative noise. Defaults are ``0.05`` each.
    Other parameters
        See :class:`SinglebeamSonar` for shared configuration options.
    """

    def __init__(
        self,
        Hz: int = 10,
        socket: str = "SonarSocket",
        Azimuth: float = 170.0,
        Elevation: float = 0.25,
        RangeMin: float = 0.5,
        RangeMax: float = 40.0,
        RangeBins: int = 2000,
        AddSigma: float = 0.05,
        MultSigma: float = 0.05,
        ShowWarning: bool = True,
        InitOctreeRange: float = 50.0,
        ViewRegion: bool = False,
        ViewOctree: float = -10.0,
        WaterDensity: float = 997.0,
        WaterSpeedSound: float = 1480.0,
        UseApprox: bool = True,
        **kwargs
    ):
        super().__init__(
            sensor_type="SidescanSonar",
            socket=socket,
            Hz=Hz,
            Azimuth=Azimuth,
            Elevation=Elevation,
            RangeMin=RangeMin,
            RangeMax=RangeMax,
            RangeBins=RangeBins,
            AddSigma=AddSigma,
            MultSigma=MultSigma,
            ShowWarning=ShowWarning,
            InitOctreeRange=InitOctreeRange,
            ViewRegion=ViewRegion,
            ViewOctree=ViewOctree,
            WaterDensity=WaterDensity,
            WaterSpeedSound=WaterSpeedSound,
            UseApprox=UseApprox,
            **kwargs
        )


# =====================================================================
# 3. Imaging Sonar
# =====================================================================

class ImagingSonar(BaseSensor):
    """
    Imaging sonar configuration.

    Simulates a forward-looking multi-beam sonar producing 2D acoustic
    intensity images, often used for navigation and obstacle detection.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``2``.
    Azimuth, Elevation : float, optional
        Horizontal and vertical field-of-view angles (degrees).
        Defaults are ``120.0`` and ``20.0``.
    RangeMin, RangeMax : float, optional
        Detection range limits in meters. Defaults are ``1.0`` and ``40.0``.
    RangeBins, AzimuthBins : int, optional
        Sampling resolution along range and azimuth. Defaults are ``512``.
    MultiPath, ClusterSize, ScaleNoise : bool or int, optional
        Simulation controls for acoustic reflection modeling.
    Other parameters
        See :class:`SinglebeamSonar` for shared options.
    """

    def __init__(
        self,
        Hz: int = 2,
        socket: str = "SonarSocket",
        Azimuth: float = 120.0,
        Elevation: float = 20.0,
        RangeMin: float = 1.0,
        RangeMax: float = 40.0,
        RangeBins: int = 512,
        AzimuthBins: int = 512,
        AddSigma: float = 0.15,
        MultSigma: float = 0.2,
        MultiPath: bool = True,
        ClusterSize: int = 5,
        ScaleNoise: bool = True,
        AzimuthStreaks: int = -1,
        RangeSigma: float = 0.1,
        ShowWarning: bool = True,
        InitOctreeRange: float = 50.0,
        ViewRegion: bool = False,
        ViewOctree: float = -10.0,
        WaterDensity: float = 997.0,
        WaterSoundSpeed: float = 1480.0,
        UseApprox: bool = True,
        **kwargs
    ):
        super().__init__(
            sensor_type="ImagingSonar",
            socket=socket,
            Hz=Hz,
            Azimuth=Azimuth,
            Elevation=Elevation,
            RangeMin=RangeMin,
            RangeMax=RangeMax,
            RangeBins=RangeBins,
            AzimuthBins=AzimuthBins,
            AddSigma=AddSigma,
            MultSigma=MultSigma,
            MultiPath=MultiPath,
            ClusterSize=ClusterSize,
            ScaleNoise=ScaleNoise,
            AzimuthStreaks=AzimuthStreaks,
            RangeSigma=RangeSigma,
            ShowWarning=ShowWarning,
            InitOctreeRange=InitOctreeRange,
            ViewRegion=ViewRegion,
            ViewOctree=ViewOctree,
            WaterDensity=WaterDensity,
            WaterSoundSpeed=WaterSoundSpeed,
            UseApprox=UseApprox,
            **kwargs
        )


# =====================================================================
# 4. Profiling Sonar
# =====================================================================

class ProfilingSonar(BaseSensor):
    """
    Profiling sonar configuration.

    Simulates a narrow, scanning sonar that builds range profiles of the
    environment using vertical or horizontal sweeps. Often used for mapping
    and structural inspection tasks.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``2``.
    Azimuth, Elevation : float, optional
        Field-of-view parameters for scanning. Defaults are ``120.0`` and ``1.0``.
    RangeMin, RangeMax : float, optional
        Detection range limits in meters. Defaults are ``1.0`` and ``60.0``.
    Other parameters
        See :class:`SinglebeamSonar` for shared configuration options.
    """

    def __init__(
        self,
        Hz: int = 2,
        socket: str = "SonarSocket",
        Azimuth: float = 120.0,
        Elevation: float = 1.0,
        RangeMin: float = 1.0,
        RangeMax: float = 60.0,
        RangeBins: int = 512,
        AzimuthBins: int = 512,
        AddSigma: float = 0.15,
        MultSigma: float = 0.2,
        MultiPath: bool = True,
        ClusterSize: int = 5,
        ScaleNoise: bool = True,
        AzimuthStreaks: int = -1,
        RangeSigma: float = 0.1,
        ShowWarning: bool = True,
        InitOctreeRange: float = 70.0,
        ViewRegion: bool = False,
        ViewOctree: float = -10.0,
        **kwargs
    ):
        super().__init__(
            sensor_type="ProfilingSonar",
            socket=socket,
            Hz=Hz,
            Azimuth=Azimuth,
            Elevation=Elevation,
            RangeMin=RangeMin,
            RangeMax=RangeMax,
            RangeBins=RangeBins,
            AzimuthBins=AzimuthBins,
            AddSigma=AddSigma,
            MultSigma=MultSigma,
            MultiPath=MultiPath,
            ClusterSize=ClusterSize,
            ScaleNoise=ScaleNoise,
            AzimuthStreaks=AzimuthStreaks,
            RangeSigma=RangeSigma,
            ShowWarning=ShowWarning,
            InitOctreeRange=InitOctreeRange,
            ViewRegion=ViewRegion,
            ViewOctree=ViewOctree,
            **kwargs
        )
