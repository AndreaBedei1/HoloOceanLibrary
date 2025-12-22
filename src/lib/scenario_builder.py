from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from lib.worlds import World


@dataclass
class ScenarioConfig:
    """
    Represents the complete configuration of a HoloOcean scenario.
    """

    # =========================
    # CORE SCENARIO FIELDS
    # =========================
    name: str
    package_name: str = "Ocean"
    world: str = World.PierHarbor
    main_agent: str = "rov0"
    agents: List[Dict[str, Any]] = field(default_factory=list)

    # =========================
    # OPTIONAL ENV / OCTREE
    # (None => use HoloOcean defaults)
    # =========================
    env_min: Optional[List[float]] = None
    env_max: Optional[List[float]] = None
    octree_min: Optional[float] = None
    octree_max: Optional[float] = None

    # =========================
    # FLUENT API
    # =========================
    def set_package(self, package: str) -> "ScenarioConfig":
        self.package_name = package
        return self

    def set_world(self, world: str) -> "ScenarioConfig":
        if world not in World.list_worlds():
            raise ValueError(f"Unknown world: {world}")
        self.world = world
        return self

    def set_main_agent(self, agent_name: str) -> "ScenarioConfig":
        self.main_agent = agent_name
        return self

    def add_agent(self, agent: Any) -> "ScenarioConfig":
        if not hasattr(agent, "to_dict"):
            raise TypeError("Agent must implement to_dict() method.")
        self.agents.append(agent.to_dict())
        return self

    def clear_agents(self) -> "ScenarioConfig":
        self.agents.clear()
        return self

    # =========================
    # ENV / OCTREE SETTERS
    # =========================
    def set_env_bounds(
        self,
        env_min: List[float],
        env_max: List[float],
    ) -> "ScenarioConfig":
        """
        Override environment bounds.
        If not called, HoloOcean world defaults are used.
        """
        self.env_min = env_min
        self.env_max = env_max
        return self

    def set_octree(
        self,
        octree_min: float,
        octree_max: float,
    ) -> "ScenarioConfig":
        """
        Override octree resolution parameters.
        If not called, HoloOcean world defaults are used.
        """
        self.octree_min = octree_min
        self.octree_max = octree_max
        return self

    # =========================
    # EXPORT
    # =========================
    def to_dict(self) -> Dict[str, Any]:
        """
        Export the scenario configuration as a dictionary
        compatible with holoocean.make().
        """
        cfg = {
            "name": self.name,
            "package_name": self.package_name,
            "world": self.world,
            "main_agent": self.main_agent,
            "agents": self.agents,
        }

        # Only override if explicitly set
        if self.env_min is not None:
            cfg["env_min"] = self.env_min
        if self.env_max is not None:
            cfg["env_max"] = self.env_max
        if self.octree_min is not None:
            cfg["octree_min"] = self.octree_min
        if self.octree_max is not None:
            cfg["octree_max"] = self.octree_max

        return cfg
