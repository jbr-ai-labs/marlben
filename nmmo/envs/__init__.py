from .corridor import Corridor

from .corridor.corridor import ScriptedCorridorConfig, OneNeuralCorridorConfig, CorridorConfig
from .gathering.gathering import GatheringConfig

name2config = {
    "CorridorScripted": ScriptedCorridorConfig,
    "CorridorSinglePlayer": OneNeuralCorridorConfig,
    "Corridor": CorridorConfig,
    "Gathering": GatheringConfig
}