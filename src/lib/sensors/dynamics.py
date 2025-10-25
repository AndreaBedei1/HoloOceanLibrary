"""
dynamics.py
-----------

Defines the Dynamics Sensor for HoloOcean simulations.
This sensor provides linear and angular dynamics data of the vehicle
in the global reference frame, useful for logging, control, and diagnostics.
"""

from lib.sensors.base import BaseSensor


class DynamicsSensor(BaseSensor):
    """
    Linear and angular dynamics sensor configuration.

    This sensor reports the vehicle’s translational and rotational dynamics
    (e.g., linear acceleration, angular velocity) in the global coordinate frame.
    It is commonly used for motion estimation, dynamics logging, or control
    feedback within the simulation environment.

    Parameters
    ----------
    Hz : int, optional
        Update frequency in Hertz. Default is ``30``.
    socket : str, optional
        Data connection socket name. Default is ``"COM"``.
    UseCOM : bool, optional
        If True, dynamics are computed relative to the vehicle’s center of mass.
        Default is ``True``.
    UseRPY : bool, optional
        If True, rotation data is provided as roll–pitch–yaw (RPY) angles.
        Default is ``True``.
    **kwargs
        Additional configuration parameters forwarded to the base sensor.

    Examples
    --------
    >>> from lib.sensors.dynamics import DynamicsSensor
    >>> dyn = DynamicsSensor(Hz=60, UseRPY=False)
    >>> print(dyn.to_dict())
    {'sensor_type': 'DynamicsSensor', 'socket': 'COM', 'Hz': 60,
     'configuration': {'UseCOM': True, 'UseRPY': False}}
    """

    def __init__(
        self,
        Hz: int = 30,
        socket: str = "COM",
        UseCOM: bool = True,
        UseRPY: bool = True,
        **kwargs
    ):
        super().__init__(
            sensor_type="DynamicsSensor",
            socket=socket,
            Hz=Hz,
            UseCOM=UseCOM,
            UseRPY=UseRPY,
            **kwargs
        )
