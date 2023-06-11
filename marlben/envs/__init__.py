from marlben.config import Planting
from marlben.envs.corridor import ScriptedCorridorConfig, OneNeuralCorridorConfig, CorridorConfig, Corridor
from marlben.envs.boss_fight import BossFightConfig, BossFight
from marlben.envs.gathering import GatheringConfig, GatheringConfigScripted, Gathering
from marlben.envs.building import BuildingGatheringConfig, BuildingGatheringConfigScripted, GatheringBuilding
from marlben.envs.planting import PlantingGatheringConfig, PlantingGatheringConfigScripted, GatheringPlanting
from marlben.envs.raid import Raid
from marlben.envs.spying import ObscuredGatheringConfig, GatheringObscured
from marlben.envs.colors import ExclusiveGatheringConfig, GatheringExclusive
from marlben.envs.exploring import ObscuredAndExclusiveGatheringConfig, GatheringObscuredAndExclusive
from marlben.envs.siege import SiegeConfig, SiegeConfigScripted, Siege
from marlben.envs.pve import PveConfig, PveConfigScripted, Pve
from marlben.envs.deathmatch import DeathmatchConfig, DeathmatchConfigScripted, Deathmatch
from marlben.envs.team_deathmatch import TeamDeathmatchConfig, TeamDeathmatchConfigScripted, TeamDeathmatch
from marlben.envs.arena import ArenaConfig, ArenaConfigScripted, Arena
from marlben.envs.predator_prey import PredatorPreyConfig, PredatorPreyConfigScripted, PredatorPrey
from gymnasium.envs.registration import register


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
    "SiegeScripted": SiegeConfigScripted,
    "Pve": PveConfig,
    "PveScripted": PveConfigScripted,
    "Deathmatch": Deathmatch,
    "DeathmatchScripted": DeathmatchConfigScripted,
    "TeamDeathmatch": TeamDeathmatch,
    "TeamDeathmatchConfigScripted": TeamDeathmatchConfigScripted,
    "Arena": ArenaConfig,
    "ArenaScripted": ArenaConfigScripted,
    "PredatorPrey": PredatorPreyConfig,
    "PredatorPreyScripted": PredatorPreyConfigScripted
}

name2env = {
    'Corridor': Corridor,
    'Gathering': Gathering,
    'Arena': Arena,
    'Pve': Pve,
    'Deathmatch': Deathmatch,
    'TeamDeathmatch': TeamDeathmatch,
    'BossFight': BossFight,
    'Building': GatheringBuilding,
    'Colors': GatheringExclusive,
    'Exploring': GatheringObscuredAndExclusive,
    'Spying': GatheringObscured,
    'Raid': Raid,
    'Siege': Siege,
    'Planting': Planting,
    'PredatorPrey': PredatorPrey
}

for key in name2env.keys():
    register(
        id='MARLBEN-' + key + '-v1',
        entry_point=name2env[key]
    )


