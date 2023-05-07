from typing import Callable

from nmmo.core.spawn.spawn_system.position_samplers import RangePositionSampler
from nmmo.core.spawn.spawn_system.skill_samplers import CustomSkillSampler
from nmmo.io.action.attack import Range, Heal, Mage, Melee
from nmmo.systems.achievement import Task
from nmmo.core.map_generation.pregen_map_generator import PregeneratedMapGenerator
from nmmo.config.base.config import NPCGroupConfig, PlayerGroupConfig, Config
from nmmo.config.systems import NPC
from nmmo.core.agent import Agent


class NpcKilledTask(Callable):
    __name__ = "Kill boss"

    def __init__(self, npc_group_id=0):
        self.dead_counter = 0
        self.npc_group_id = npc_group_id

    def __call__(self, realm, entity):
        # Amount of NPCs died at this turn
        self.dead_counter += len(
            realm.entity_group_manager.npc_groups[self.npc_group_id].dead)
        return self.dead_counter


class PlayerDiedTask(Callable):
    __name__ = "Die"

    def __call__(self, realm, entity):
        return 0 if entity.alive else 1


class BossGroupConfig(NPCGroupConfig):
    def __init__(self, n_tanks, n_fighters, n_healers, coordinates_sampler=RangePositionSampler([8], [3])):
        super().__init__()
        self.SPAWN_COORDINATES_SAMPLER = coordinates_sampler
        self.SPAWN_SKILLS_SAMPLER = CustomSkillSampler(
            {"constitution": {"name": "const", "level": 125 * n_tanks + 250 * n_fighters},
             "melee": {"name": "const", "level": 20 + 10 * n_healers}})

    NENT = 1
    SPAWN_ATTEMPTS_PER_ENT = 10


class TankGroupConfig(PlayerGroupConfig):
    def __init__(self, n_ent=2, coordinates_sampler=RangePositionSampler([1, 1], [2, 4]),
                 skill_sampler=CustomSkillSampler({"constitution": {"name": "const", "level": 200},
                                                   "melee": {"name": "const", "level": 5}})):
        super().__init__()
        self.NENT = n_ent
        self.SPAWN_COORDINATES_SAMPLER = coordinates_sampler
        self.SPAWN_SKILLS_SAMPLER = skill_sampler

    SPAWN_ATTEMPTS_PER_ENT = 10
    BANNED_ATTACK_STYLES = [Range, Heal, Mage]
    AGENTS = [Agent]


class BossFightConfig(Config, NPC):
    NPC_GROUPS = [BossGroupConfig(2, 0, 0)]
    PLAYER_GROUPS = [TankGroupConfig(2)]
    TASKS = [Task(NpcKilledTask(0), 1, 10.), Task(PlayerDiedTask(), 1, -10.)]

    TOP_LEFT_CORNER = (16, 17)
    TERRAIN_CENTER = 12
    MAP_HEIGHT = 10
    MAP_WIDTH = 12

    MAP_PREVIEW_DOWNSCALE = 1
    TERRAIN_LOG_INTERPOLATE_MIN = 0
    MAP_GENERATOR = PregeneratedMapGenerator