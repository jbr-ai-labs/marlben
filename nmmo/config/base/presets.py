from nmmo.config.base.config import Config
from nmmo.core.spawn.spawn_system import skill_samplers
from .config import NPCGroupConfig, PlayerGroupConfig
from ... import Agent


class SmallNPCGroupConfig(NPCGroupConfig):
    NENT = 32
    SPAWN_SKILLS_SAMPLER = skill_samplers.DefaultNPCSkillSampler(1, 10, 1)


class SmallPlayerGroupConfig(PlayerGroupConfig):
    NENT = 1
    AGENTS = [Agent]


class Small(Config):
    '''A small config for debugging and experiments with an expensive outer loop'''

    PATH_MAPS = 'maps/small'
    MAP_PREVIEW_DOWNSCALE = 4

    TERRAIN_LOG_INTERPOLATE_MIN = 0

    TERRAIN_CENTER = 4
    MAP_HEIGHT = 4
    MAP_WIDTH = 4
    PLAYER_GROUPS = [SmallPlayerGroupConfig(), SmallPlayerGroupConfig()]


class MediumNPCGroupConfig(NPCGroupConfig):
    NENT = 128
    SPAWN_SKILLS_SAMPLER = skill_samplers.DefaultNPCSkillSampler(1, 30, 5)


class MediumPlayerGroupConfig(PlayerGroupConfig):
    NENT = 256


class Medium(Config):
    '''A medium config suitable for most academic-scale research'''

    PATH_MAPS = 'maps/medium'
    MAP_PREVIEW_DOWNSCALE = 16

    TERRAIN_CENTER = 128
    MAP_HEIGHT = 128
    MAP_WIDTH = 128

    PLAYER_GROUPS = [MediumPlayerGroupConfig()]
    NPC_GROUPS = [MediumNPCGroupConfig()]


class LargeNPCGroupConfig(NPCGroupConfig):
    NENT = 1024
    SPAWN_SKILLS_SAMPLER = skill_samplers.DefaultNPCSkillSampler(1, 99, 10)


class LargePlayerGroupConfig(PlayerGroupConfig):
    NENT = 2048


class Large(Config):
    '''A large config suitable for large-scale research or fast models'''

    PATH_MAPS = 'maps/large'
    MAP_PREVIEW_DOWNSCALE = 64

    TERRAIN_CENTER = 1024
    MAP_HEIGHT = 1024
    MAP_WIDTH = 1024
    PLAYER_GROUPS = [LargePlayerGroupConfig()]
    NPC_GROUPS = [LargeNPCGroupConfig()]