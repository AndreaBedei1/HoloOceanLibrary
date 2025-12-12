"""
collision.py
------------

Defines the Collision Sensor for HoloOcean simulations.
This sensor detects physical impacts between the agent and the environment,
providing information useful for navigation safety, obstacle avoidance,
and control feedback.
"""

from lib.sensors.base import BaseSensor


class CollisionSensor(BaseSensor):
    """
    Collision detection sensor configuration.

    This sensor detects and reports collisions between the ROV/AUV and
    objects in the simulated environment. It can be used to trigger
    control reactions, evaluate contact forces, or log impact events
    during autonomous navigation experiments.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``30``.
    socket : str, optional
        Data connection socket name. Default is ``"CollisionSocket"``.
    **kwargs
        Additional configuration parameters (e.g., sensitivity thresholds)
        forwarded to the base configuration.

    Examples
    --------
    >>> from lib.sensors.collision import CollisionSensor
    >>> collision = CollisionSensor(Hz=60)
    >>> print(collision.to_dict())
    {'sensor_type': 'CollisionSensor', 'socket': 'CollisionSocket', 'Hz': 60}
    """

    def __init__(
        self,
        Hz: int = 30,
        socket: str = "CollisionSocket",
        **kwargs
    ):
        super().__init__(
            sensor_type="CollisionSensor",
            socket=socket,
            Hz=Hz,
            **kwargs
        )
