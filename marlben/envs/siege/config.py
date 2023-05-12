from os import path as osp
from marlben.config import NPC
from marlben.envs import BuildingGatheringConfig, BuildingGatheringConfigScripted
from marlben.envs.gathering.config import GatheringPlayerGroup

from marlben.core.spawn.spawn_system.position_samplers import UniformPositionSampler
from marlben.core.spawn.spawn_system.skill_samplers import CustomSkillSampler
from marlben.config.base.config import NPCGroupConfig, Config
from marlben.io.action.attack import Range, Heal, Mage, Melee

from scripted.environments.gathering import SiegeAgent



PATH_TO_CUSTOM_MAPS = osp.dirname(__file__)

class MobsGroupConfig(NPCGroupConfig):
    BANNED_ATTACK_STYLES = {Heal, Range, Mage}
    DANGER = 1.0 
    SPAWN_ATTEMPTS_PER_ENT = 10

    def __init__(self, n_groups, agents_per_group, coord_sampler=None):
        super().__init__()
        if coord_sampler is not None:
            self.SPAWN_COORDINATES_SAMPLER = coord_sampler
        self.NENT = n_groups * agents_per_group
        self.SPAWN_SKILLS_SAMPLER = CustomSkillSampler(
            {"constitution": {"name": "const", "level": 2},
             "melee": {"name": "const", "level": 2}})

class SiegePlayerGroupConfig(GatheringPlayerGroup):
    BANNED_ATTACK_STYLES = [Range, Heal, Mage]

class SiegeConfig(BuildingGatheringConfig, NPC):
    PLAYER_GROUP_CONFIG = SiegePlayerGroupConfig
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.NPC_GROUPS = [MobsGroupConfig(n_groups, agents_per_group)]
        self.PATH_MAPS = f'maps/siege_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'


class SiegeConfigScripted(BuildingGatheringConfigScripted, NPC):
    PLAYER_GROUP_CONFIG = SiegePlayerGroupConfig
    AGENT_TYPE = SiegeAgent
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.NPC_GROUPS = [MobsGroupConfig(n_groups, agents_per_group,
            coord_sampler=UniformPositionSampler(r_range=[4, 4], c_range=[3, 5]))]
        self.PATH_MAPS = osp.join(PATH_TO_CUSTOM_MAPS, "test_maps")