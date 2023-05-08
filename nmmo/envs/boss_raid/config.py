from typing import Callable

from nmmo.core.spawn.spawn_system.position_samplers import RangePositionSampler
from nmmo.core.spawn.spawn_system.skill_samplers import CustomSkillSampler
from nmmo.io.action.attack import Range, Heal, Mage, Melee
from nmmo.systems.achievement import Task
from nmmo.core.map_generation.pregen_map_generator import PregeneratedMapGenerator
from nmmo.config.base.config import NPCGroupConfig, PlayerGroupConfig, Config
from nmmo.config.systems import NPC
from nmmo.core.agent import Agent

from nmmo.envs.boss_fight.config import BossFightConfig, TankGroupConfig, BossGroupConfig


class FighterGroupConfig(PlayerGroupConfig):
    def __init__(self, n_ent=2, coordinates_sampler=RangePositionSampler(list(range(1, 4)), list(range(3, 7))),
                 skill_sampler=CustomSkillSampler({"constitution": {"name": "const", "level": 50},
                                                   "melee": {"name": "const", "level": 15},
                                                   "range": {"name": "const", "level": 20}})):
        super().__init__()
        self.NENT = n_ent
        self.SPAWN_COORDINATES_SAMPLER = coordinates_sampler
        self.SPAWN_SKILLS_SAMPLER = skill_sampler

    SPAWN_ATTEMPTS_PER_ENT = 10
    BANNED_ATTACK_STYLES = [Heal, Mage]
    AGENTS = [Agent]


class HealerGroupConfig(PlayerGroupConfig):
    def __init__(self, n_ent=2, coordinates_sampler=RangePositionSampler(list(range(1, 4)), list(range(3, 7))),
                 skill_sampler=CustomSkillSampler({"constitution": {"name": "const", "level": 50},
                                                   "heal": {"name": "const", "level": 20}})):
        super().__init__()
        self.NENT = n_ent
        self.SPAWN_COORDINATES_SAMPLER = coordinates_sampler
        self.SPAWN_SKILLS_SAMPLER = skill_sampler

    SPAWN_ATTEMPTS_PER_ENT = 10
    BANNED_ATTACK_STYLES = [Range, Melee, Mage]
    AGENTS = [Agent]


class BossRaidConfig(BossFightConfig):
    def __init__(self, n_tanks=2, n_fighters=2, n_healers=2):
        super().__init__()
        self.NPC_GROUPS = [BossGroupConfig(n_tanks, n_fighters, n_healers)]
        self.PLAYER_GROUPS = [TankGroupConfig(n_tanks), FighterGroupConfig(n_fighters), HealerGroupConfig(n_healers)]
