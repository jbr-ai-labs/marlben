from os import path as osp

from marlben import Task, Agent
from marlben.config import Combat
from marlben.config.base.config import PlayerGroupConfig
from marlben.envs.gathering.config import GatheringConfig, GatheringConfigScripted
from marlben.io.action import Range, Mage, Melee

from marlben.scripted.environments.gathering import GatheringCombatAgent



PATH_TO_CUSTOM_MAPS = osp.dirname(__file__)

class PreyKilledTask:
    __name__ = 'hunt'
    def __call__(self, realm, entity):
        if not entity.alive or realm.entity_group_manager.player_groups[entity.population].banned_attack_styles is not None:
            return 0

        # Amount of Prey died at this turn
        return sum(
            [len(group.dead) for group in realm.entity_group_manager.player_groups if group.group_id != entity.population]
        )

class PreyGroupConfig(PlayerGroupConfig):
    def __init__(self, agents, n_ent):
        super().__init__()
        self.NENT = n_ent
        self.AGENTS = agents

    BASE_HEALTH = 5
    BANNED_ATTACK_STYLES = [Range, Mage, Melee]


class PredatorGroupConfig(PlayerGroupConfig):
    def __init__(self, agents, n_ent):
        super().__init__()
        self.NENT = n_ent
        self.AGENTS = agents

    BASE_HEALTH = 10

class PredatorPreyConfig(GatheringConfig, Combat):
    TASKS = [Task(PreyKilledTask(), 1, 10.)]
    PLAYER_GROUPS = [PreyGroupConfig([Agent], 10), PredatorGroupConfig([Agent], 3)]
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = f'maps/predator_prey_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'

class PredatorPreyConfigScripted(GatheringConfigScripted, Combat):
    AGENT_TYPE = GatheringCombatAgent
    TASKS = [Task(PreyKilledTask(), 1, 10.)]
    PLAYER_GROUPS = [PreyGroupConfig([Agent], 10), PredatorGroupConfig([Agent], 3)]
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = osp.join(PATH_TO_CUSTOM_MAPS, "test_maps")
