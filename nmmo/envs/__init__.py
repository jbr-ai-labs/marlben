from nmmo.envs.corridor import ScriptedCorridorConfig, OneNeuralCorridorConfig, CorridorConfig, Corridor
from nmmo.envs.boss_fight import BossFightConfig, BossFight
from nmmo.envs.gathering import GatheringConfig, GatheringConfigScripted, Gathering
from nmmo.envs.building import BuildingGatheringConfig, BuildingGatheringConfigScripted, GatheringBuilding
from nmmo.envs.planting import PlantingGatheringConfig, PlantingGatheringConfigScripted, GatheringPlanting
from nmmo.envs.spying import ObscuredGatheringConfig, GatheringObscured
from nmmo.envs.colors import ExclusiveGatheringConfig, GatheringExclusive
from nmmo.envs.exploring import ObscuredAndExclusiveGatheringConfig, GatheringObscuredAndExclusive


name2config = {
    "CorridorScripted": ScriptedCorridorConfig,
    "CorridorSinglePlayer": OneNeuralCorridorConfig,
    "Corridor": CorridorConfig,
    "Gathering": GatheringConfig,
    "GatheringScripted": GatheringConfigScripted,
    "GatheringBuilding": BuildingGatheringConfig,
    "GatheringBuildingScripted": BuildingGatheringConfigScripted,
    "GatheringPlanting": PlantingGatheringConfig,
    "GatheringPlantingScripted": PlantingGatheringConfigScripted,
    "GatheringObscured": ObscuredGatheringConfig,
    "GatheringExclusive": ExclusiveGatheringConfig,
    "GatheringObscuredAndExclusive": ObscuredAndExclusiveGatheringConfig
}
