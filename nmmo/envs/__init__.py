from .corridor import Corridor

from .corridor.corridor import ScriptedCorridorConfig, OneNeuralCorridorConfig, CorridorConfig
from .gathering.gathering import GatheringConfig, GatheringBuildingConfig

name2config = {
    "CorridorScripted": ScriptedCorridorConfig,
    "CorridorSinglePlayer": OneNeuralCorridorConfig,
    "Corridor": CorridorConfig,
    "Gathering": GatheringConfig,
    "GatheringBuilding": GatheringBuildingConfig
}