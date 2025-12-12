"""
worlds.py
---------

Defines the available HoloOcean environments ("worlds") that can be used
to compose simulation scenarios. Each world corresponds to a specific
3D environment provided by the selected HoloOcean package, typically "Ocean".

Examples
--------
>>> from lib.worlds import World
>>> print(World.PierHarbor)
'PierHarbor'
>>> print(World.list_worlds())
['PierHarbor', 'OpenWater', 'SimpleUnderwater', 'Dam', 'Rooms']
"""


class World:
    """
    Enumeration of available HoloOcean simulation worlds.

    This class provides simple string constants representing the names
    of valid world environments. Each world corresponds to a predefined
    3D scene available in the HoloOcean "Ocean" package.

    Attributes
    ----------
    PierHarbor : str
        Dock and harbor environment with shallow water.
    OpenWater : str
        Open sea environment without obstacles.
    SimpleUnderwater : str
        Minimalistic flat seabed environment for testing.
    Dam : str
        Underwater environment featuring a dam structure.
    Rooms : str
        Closed environment with multiple rooms and corridors.

    Examples
    --------
    >>> World.PierHarbor
    'PierHarbor'
    >>> World.list_worlds()
    ['PierHarbor', 'OpenWater', 'SimpleUnderwater', 'Dam', 'Rooms']
    """

    PierHarbor = "PierHarbor"
    OpenWater = "OpenWater"
    SimpleUnderwater = "SimpleUnderwater"
    Dam = "Dam"
    Rooms = "Rooms"

    @classmethod
    def list_worlds(cls):
        """
        Return all available world names.

        Returns
        -------
        list of str
            Names of all worlds defined in this enumeration.
        """
        return [v for k, v in cls.__dict__.items() if not k.startswith("_")]
