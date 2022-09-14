from .corridor import Corridor

from src.environments.corridor.corridor import ScriptedCorridorConfig, OneNeuralCorridorConfig, CorridorConfig
from src.environments.gathering.gathering import GatheringConfig

name2config = {
    "CorridorScripted": ScriptedCorridorConfig,
    "CorridorSinglePlayer": OneNeuralCorridorConfig,
    "Corridor": CorridorConfig,
    "Gathering": GatheringConfig
}