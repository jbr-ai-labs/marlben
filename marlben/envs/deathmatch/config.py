from os import path as osp
from typing import Callable

from marlben import Task
from marlben.config import Combat
from marlben.envs.gathering.config import GatheringConfig, GatheringConfigScripted

from marlben.scripted.environments.gathering import GatheringCombatAgent



PATH_TO_CUSTOM_MAPS = osp.dirname(__file__)

class AgentKilledTask(Callable):
    __name__ = "AgentKilled"
    def __call__(self, realm, entity):
        if entity.dead:
            return 0

        # Amount of Players died at this turn
        return sum([len(group.dead) for group in realm.entity_group_manager.player_groups])

class DeathmatchConfig(GatheringConfig, Combat):
    TASKS = [Task(AgentKilledTask(), 1, 10.)]
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = f'maps/deathmatch_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'

class DeathmatchConfigScripted(GatheringConfigScripted, Combat):
    AGENT_TYPE = GatheringCombatAgent
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = osp.join(PATH_TO_CUSTOM_MAPS, "test_maps")