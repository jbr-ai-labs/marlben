
from nmmo.envs.corridor import ScriptedCorridorConfig, OneNeuralCorridorConfig, CorridorConfig, Corridor
from nmmo.envs.boss_fight import BossFightConfig, BossFight
from nmmo.envs.gathering import GatheringConfig, GatheringConfigScripted, Gathering
from nmmo.envs.gathering_building import BuildingGatheringConfig, BuildingGatheringConfigScripted, GatheringBuilding
from nmmo.envs.gathering_obscured import ObscuredGatheringConfig, GatheringObscured
from nmmo.envs.gathering_exclusive import ExclusiveGatheringConfig, GatheringExclusive
from nmmo.envs.gathering_obscured_and_exclusive import ObscuredAndExclusiveGatheringConfig, GatheringObscuredAndExclusive


name2config = {
    "CorridorScripted": ScriptedCorridorConfig,
    "CorridorSinglePlayer": OneNeuralCorridorConfig,
    "Corridor": CorridorConfig,
    "Gathering": GatheringConfig,
    "GatheringScripted": GatheringConfigScripted,
    "GatheringBuilding": BuildingGatheringConfig,
    "GatheringBuildingScripted": BuildingGatheringConfigScripted,
    "GatheringObscured": ObscuredGatheringConfig,
    "GatheringExclusive": ExclusiveGatheringConfig,
    "GatheringObscuredAndExclusive": ObscuredAndExclusiveGatheringConfig
}
