from marlben.envs.corridor import ScriptedCorridorConfig, OneNeuralCorridorConfig, CorridorConfig, Corridor
from marlben.envs.boss_fight import BossFightConfig, BossFight
from marlben.envs.gathering import GatheringConfig, GatheringConfigScripted, Gathering
from marlben.envs.building import BuildingGatheringConfig, BuildingGatheringConfigScripted, GatheringBuilding
from marlben.envs.planting import PlantingGatheringConfig, PlantingGatheringConfigScripted, GatheringPlanting
from marlben.envs.spying import ObscuredGatheringConfig, GatheringObscured
from marlben.envs.colors import ExclusiveGatheringConfig, GatheringExclusive
from marlben.envs.exploring import ObscuredAndExclusiveGatheringConfig, GatheringObscuredAndExclusive
from marlben.envs.siege import SiegeConfig, SiegeConfigScripted, Siege


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
    "GatheringObscuredAndExclusive": ObscuredAndExclusiveGatheringConfig,
    "Siege": SiegeConfig,
    "SiegeScripted": SiegeConfigScripted
}
