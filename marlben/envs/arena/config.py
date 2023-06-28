from os import path as osp
from marlben.config import Combat
from marlben.envs.gathering.config import GatheringConfig, GatheringConfigScripted

from marlben.scripted.environments.gathering import GatheringCombatAgent



PATH_TO_CUSTOM_MAPS = osp.dirname(__file__)


class ArenaConfig(GatheringConfig, Combat):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = f'maps/arena_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'

class ArenaConfigScripted(GatheringConfigScripted, Combat):
    AGENT_TYPE = GatheringCombatAgent
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = osp.join(PATH_TO_CUSTOM_MAPS, "test_maps")