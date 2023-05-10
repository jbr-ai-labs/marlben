from marlben.config.base.config import PlayerGroupConfig
from marlben.core.agent import Agent
from marlben.core.spawn.spawn_system.position_samplers import RangePositionSampler
from marlben.core.spawn.spawn_system.skill_samplers import CustomSkillSampler
from marlben.envs.boss_fight.config import BossFightConfig, TankGroupConfig, BossGroupConfig
from marlben.io.action.attack import Range, Heal, Mage, Melee


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
