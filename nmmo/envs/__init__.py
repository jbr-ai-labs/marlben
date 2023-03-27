from .corridor import Corridor

from .corridor.corridor import ScriptedCorridorConfig, OneNeuralCorridorConfig, CorridorConfig
from nmmo.envs.gathering.configs.base import GatheringConfig
from nmmo.envs.gathering.configs.building import BuildingGatheringConfig
from nmmo.envs.gathering.configs.obscured import ObscuredGatheringConfig
from nmmo.envs.gathering.configs.exclusive import ExclusiveGatheringConfig
from nmmo.envs.gathering.configs.obscured_and_exclusive import ObscuredAndExclusiveGatheringConfig

name2config = {
    "CorridorScripted": ScriptedCorridorConfig,
    "CorridorSinglePlayer": OneNeuralCorridorConfig,
    "Corridor": CorridorConfig,
    "Gathering": GatheringConfig,
    "GatheringBuilding": BuildingGatheringConfig,
    "GatheringObscured": ObscuredGatheringConfig,
    "GatheringExclusive": ExclusiveGatheringConfig,
    "GatheringObscuredAndExclusive": ObscuredAndExclusiveGatheringConfig
}