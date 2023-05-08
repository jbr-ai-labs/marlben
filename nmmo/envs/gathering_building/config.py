from os import path as osp

from nmmo.config import Building
from nmmo.envs import GatheringConfig, GatheringConfigScripted
from scripted.environments.gathering import GatheringBuildingAgent

PATH_TO_CUSTOM_MAPS = osp.dirname(__file__)


class BuildingGatheringConfig(GatheringConfig, Building):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = f'maps/gathering_building_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'



class BuildingGatheringConfigScripted(GatheringConfigScripted, Building):
    AGENT_TYPE = GatheringBuildingAgent
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = osp.join(PATH_TO_CUSTOM_MAPS, "test_maps")
        
