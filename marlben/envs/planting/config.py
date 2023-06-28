from os import path as osp

from marlben.config import Planting
from marlben.envs import GatheringConfig, GatheringConfigScripted
from marlben.scripted.environments.gathering import GatheringPlantingAgent



PATH_TO_CUSTOM_MAPS = osp.dirname(__file__)


class PlantingGatheringConfig(GatheringConfig, Planting):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = f'maps/planting_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'



class PlantingGatheringConfigScripted(GatheringConfigScripted, Planting):
    AGENT_TYPE = GatheringPlantingAgent
    PLANTING_COST = 1 #
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = osp.join(PATH_TO_CUSTOM_MAPS, "test_maps")
        
