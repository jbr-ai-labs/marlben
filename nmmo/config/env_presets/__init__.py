from .corridor import ScriptedCorridorConfig, OneNeuralCorridorConfig, CorridorConfig


name2config = {
    "CorridorScripted": ScriptedCorridorConfig,
    "CorridorSinglePlayer": OneNeuralCorridorConfig,
    "Corridor": CorridorConfig
}