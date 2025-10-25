"""
bst.py
------

Defines the Biomass–Salinity–Temperature (BST) sensor for HoloOcean simulations.
This sensor models vertical water column properties including biological
biomass distribution, salinity (PSU), and temperature gradients.
"""

from lib.sensors.base import BaseSensor


class BSTSensor(BaseSensor):
    """
    Biomass, Salinity, and Temperature (BST) sensor configuration.

    This sensor simulates vertical gradients of biological and physical
    properties in the water column. It can be used to study the effect
    of depth on biomass concentration, salinity variation (halocline),
    and temperature profiles (thermocline).

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``2``.
    socket : str, optional
        Data connection socket name. Default is ``"BSTSocket"``.
    max_biomass : float, optional
        Maximum biomass concentration (arbitrary units). Default is ``1.0``.
    surface_biomass : float, optional
        Biomass concentration at the surface. Default is ``0.2``.
    peak_depth : float, optional
        Depth (m) at which biomass concentration is maximal. Default is ``20.0``.
    biocline_sharpness : float, optional
        Controls steepness of the biomass gradient. Default is ``3.0``.
    photic_zone_depth : float, optional
        Depth of the photic zone (m). Default is ``40.0``.
    deep_biomass : float, optional
        Biomass concentration at depth (m). Default is ``0.05``.
    surface_psu : float, optional
        Salinity at the surface (Practical Salinity Units). Default is ``35.0``.
    deep_psu : float, optional
        Salinity at depth. Default is ``37.0``.
    halocline_depth : float, optional
        Depth (m) of the halocline midpoint. Default is ``50.0``.
    halocline_thickness : float, optional
        Thickness (m) of the halocline region. Default is ``15.0``.
    surface_temp : float, optional
        Temperature at the surface (°C). Default is ``20.0``.
    deep_temp : float, optional
        Temperature at depth (°C). Default is ``4.0``.
    thermocline_depth : float, optional
        Depth (m) of the thermocline midpoint. Default is ``40.0``.
    thermocline_thickness : float, optional
        Thickness (m) of the thermocline region. Default is ``10.0``.
    **kwargs
        Additional parameters forwarded to the base sensor configuration.

    Examples
    --------
    >>> from lib.sensors.bst import BSTSensor
    >>> bst = BSTSensor(surface_temp=22.0, deep_temp=5.0, peak_depth=25.0)
    >>> print(bst.to_dict())
    {'sensor_type': 'BSTSensor', 'socket': 'BSTSocket', 'Hz': 2,
     'configuration': {'max_biomass': 1.0, 'surface_biomass': 0.2,
                       'peak_depth': 25.0, 'biocline_sharpness': 3.0,
                       'photic_zone_depth': 40.0, 'deep_biomass': 0.05,
                       'surface_psu': 35.0, 'deep_psu': 37.0,
                       'halocline_depth': 50.0, 'halocline_thickness': 15.0,
                       'surface_temp': 22.0, 'deep_temp': 5.0,
                       'thermocline_depth': 40.0,
                       'thermocline_thickness': 10.0}}
    """

    def __init__(
        self,
        Hz: int = 2,
        socket: str = "BSTSocket",
        max_biomass: float = 1.0,
        surface_biomass: float = 0.2,
        peak_depth: float = 20.0,
        biocline_sharpness: float = 3.0,
        photic_zone_depth: float = 40.0,
        deep_biomass: float = 0.05,
        surface_psu: float = 35.0,
        deep_psu: float = 37.0,
        halocline_depth: float = 50.0,
        halocline_thickness: float = 15.0,
        surface_temp: float = 20.0,
        deep_temp: float = 4.0,
        thermocline_depth: float = 40.0,
        thermocline_thickness: float = 10.0,
        **kwargs
    ):
        super().__init__(
            sensor_type="BSTSensor",
            socket=socket,
            Hz=Hz,
            max_biomass=max_biomass,
            surface_biomass=surface_biomass,
            peak_depth=peak_depth,
            biocline_sharpness=biocline_sharpness,
            photic_zone_depth=photic_zone_depth,
            deep_biomass=deep_biomass,
            surface_psu=surface_psu,
            deep_psu=deep_psu,
            halocline_depth=halocline_depth,
            halocline_thickness=halocline_thickness,
            surface_temp=surface_temp,
            deep_temp=deep_temp,
            thermocline_depth=thermocline_depth,
            thermocline_thickness=thermocline_thickness,
            **kwargs
        )
