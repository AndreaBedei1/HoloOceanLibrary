"""
scenario_builder.py
-------------------

Provides an object-oriented interface for constructing HoloOcean scenarios.
A scenario defines the simulation environment, the agents involved, and
the package/world to be loaded by HoloOcean.

Typical usage combines this class with `World`, `Rover`, and `AgentConfig`
to create complete simulation setups.

Examples
--------
>>> from lib.scenario_builder import ScenarioConfig
>>> from lib.worlds import World
>>> from lib.rover import Rover
>>> rov = Rover.BlueROV2(name="rov0")
>>> scenario = (
...     ScenarioConfig(name="BlueROV_Keyboard")
...     .set_world(World.PierHarbor)
...     .add_agent(rov)
... )
>>> print(scenario.to_dict())
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from lib.worlds import World


@dataclass
class ScenarioConfig:
    """
    Represents the complete configuration of a HoloOcean scenario.

    This class manages high-level parameters such as the simulation package,
    world environment, main agent, and all agents participating in the scene.
    It provides a fluent interface for building scenarios programmatically.

    Attributes
    ----------
    name : str
        Name of the scenario (used by HoloOcean).
    package_name : str, optional
        HoloOcean package name (default: "Ocean").
    world : str, optional
        Environment or world to load (default: `World.PierHarbor`).
    main_agent : str, optional
        Identifier of the main controllable agent (default: "rov0").
    agents : list of dict, optional
        List of agent configurations, each provided as a dictionary.

    Examples
    --------
    >>> scenario = ScenarioConfig(name="Demo").set_world(World.OpenWater)
    >>> scenario.add_agent(Rover.BlueROV2("rov0"))
    >>> cfg = scenario.to_dict()
    """

    name: str
    package_name: str = "Ocean"
    world: str = World.PierHarbor
    main_agent: str = "rov0"
    agents: List[Dict[str, Any]] = field(default_factory=list)

    def set_package(self, package: str) -> "ScenarioConfig":
        """
        Define the HoloOcean package to use.

        Parameters
        ----------
        package : str
            Name of the HoloOcean package (e.g., "Ocean").

        Returns
        -------
        ScenarioConfig
            The updated instance, allowing for method chaining.
        """
        self.package_name = package
        return self

    def set_world(self, world: str) -> "ScenarioConfig":
        """
        Select the simulation world environment.

        Parameters
        ----------
        world : str
            World name (must exist in `World.list_worlds()`).

        Raises
        ------
        ValueError
            If the provided world name is not recognized.

        Returns
        -------
        ScenarioConfig
            The updated instance.
        """
        if world not in World.list_worlds():
            raise ValueError(f"Unknown world: {world}")
        self.world = world
        return self

    def set_main_agent(self, agent_name: str) -> "ScenarioConfig":
        """
        Set which agent will be the primary controllable one.

        Parameters
        ----------
        agent_name : str
            Name of the main agent.

        Returns
        -------
        ScenarioConfig
            The updated instance.
        """
        self.main_agent = agent_name
        return self

    def add_agent(self, agent: Any) -> "ScenarioConfig":
        """
        Add a configured agent to the scenario.

        Parameters
        ----------
        agent : Any
            Agent object that implements a `to_dict()` method.

        Raises
        ------
        TypeError
            If the provided object does not implement `to_dict()`.

        Returns
        -------
        ScenarioConfig
            The updated instance.
        """
        if not hasattr(agent, "to_dict"):
            raise TypeError("Agent must implement to_dict() method.")
        self.agents.append(agent.to_dict())
        return self

    def clear_agents(self) -> "ScenarioConfig":
        """
        Remove all agents from the scenario.

        Returns
        -------
        ScenarioConfig
            The updated instance.
        """
        self.agents.clear()
        return self

    def to_dict(self) -> Dict[str, Any]:
        """
        Export the scenario configuration as a dictionary.

        Returns
        -------
        dict
            A structure compatible with `holoocean.make()`, ready for simulation.
        """
        return {
            "name": self.name,
            "package_name": self.package_name,
            "world": self.world,
            "main_agent": self.main_agent,
            "agents": self.agents,
        }
