from typing import Callable

from nmmo.core.spawn.spawn_system.position_samplers import RangePositionSampler
from nmmo.core.spawn.spawn_system.skill_samplers import CustomSkillSampler
from nmmo.io.action.attack import Melee, Range, Heal, Mage
from src.core.map_generator.custom_map_generator import CustomMapGenerator


from ..base.config import NPCGroupConfig, PlayerGroupConfig, Config
from ..systems import Combat, NPC, Progression


class BossGroupConfig(NPCGroupConfig):
    NENT = 1
    SPAWN_ATTEMPTS_PER_ENT = 10
    SPAWN_COORDINATES_SAMPLER = RangePositionSampler([8], [3])
    SPAWN_SKILLS_SAMPLER = CustomSkillSampler({"constitution": 250, "melee": 20})


class TankGroupConfig(PlayerGroupConfig):
    NENT = 2
    SPAWN_ATTEMPTS_PER_ENT = 10
    SPAWN_COORDINATES_SAMPLER = RangePositionSampler([1, 1], [2, 4])
    SPAWN_SKILLS_SAMPLER = CustomSkillSampler({"constitution": 200, "melee": 5})
    BANNED_ATTACK_STYLES = [Range, Heal, Mage]


class BossFightConfig(Config, Combat, NPC, Progression):
    NPC_GROUPS = [BossGroupConfig()]
    PLAYER_GROUPS = [TankGroupConfig()]
    TERRAIN_CENTER = 10
    MAP_HEIGHT = 7
    MAP_WIDTH = 10

    PATH_MAPS = 'maps/boss_fight'
    MAP_PREVIEW_DOWNSCALE = 1
    TERRAIN_LOG_INTERPOLATE_MIN = 0
    MAP_GENERATOR = CustomMapGenerator


class NpcKilledTask(Callable):
    def __init__(self, npc_group_id=0):
        self.dead_counter = 0
        self.npc_group_id = npc_group_id

    def __call__(self, realm, env):
        # Amount of NPCs died at this turn
        self.dead_counter += len(realm.entity_group_manager.npc_groups[self.npc_group_id].dead)
        return self.dead_counter