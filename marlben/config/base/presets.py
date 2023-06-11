from dataclasses import dataclass, field

from marlben.config.base.config import Config
from marlben.core.spawn.spawn_system import skill_samplers
from .config import NPCGroupConfig, PlayerGroupConfig
from ... import Agent
from ...core.spawn.spawn_system.skill_samplers import SkillsSampler


class SmallNPCGroupConfig(NPCGroupConfig):
    NENT = 32
    SPAWN_SKILLS_SAMPLER = skill_samplers.DefaultNPCSkillSampler(1, 10, 1)


class SmallPlayerGroupConfig(PlayerGroupConfig):
    NENT = 1
    AGENTS = [Agent]


@dataclass
class Small(Config):
    '''A small config for debugging and experiments with an expensive outer loop'''

    PATH_MAPS: str = 'maps/small'
    MAP_PREVIEW_DOWNSCALE: int = 4

    TERRAIN_LOG_INTERPOLATE_MIN: int = 0

    TERRAIN_CENTER: int = 8  # 4
    MAP_HEIGHT: int = 4
    MAP_WIDTH: int = 4
    PLAYER_GROUPS: list = field(default_factory=lambda: [SmallPlayerGroupConfig(), SmallPlayerGroupConfig()])


@dataclass
class MediumNPCGroupConfig(NPCGroupConfig):
    NENT: int = 128
    SPAWN_SKILLS_SAMPLER: SkillsSampler = skill_samplers.DefaultNPCSkillSampler(1, 30, 5)


@dataclass
class MediumPlayerGroupConfig(PlayerGroupConfig):
    NENT: int = 256


@dataclass
class Medium(Config):
    '''A medium config suitable for most academic-scale research'''

    PATH_MAPS = 'maps/medium'
    MAP_PREVIEW_DOWNSCALE = 16

    TERRAIN_CENTER = 128
    MAP_HEIGHT = 128
    MAP_WIDTH = 128

    PLAYER_GROUPS = [MediumPlayerGroupConfig()]
    NPC_GROUPS = [MediumNPCGroupConfig()]


@dataclass
class LargeNPCGroupConfig(NPCGroupConfig):
    NENT = 1024
    SPAWN_SKILLS_SAMPLER = skill_samplers.DefaultNPCSkillSampler(1, 99, 10)


@dataclass
class LargePlayerGroupConfig(PlayerGroupConfig):
    NENT = 2048


@dataclass
class Large(Config):
    '''A large config suitable for large-scale research or fast models'''

    PATH_MAPS = 'maps/large'
    MAP_PREVIEW_DOWNSCALE = 64

    TERRAIN_CENTER = 1024
    MAP_HEIGHT = 1024
    MAP_WIDTH = 1024
    PLAYER_GROUPS = [LargePlayerGroupConfig()]
    NPC_GROUPS = [LargeNPCGroupConfig()]
