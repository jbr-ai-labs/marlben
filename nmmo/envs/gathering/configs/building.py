from nmmo.config import Building
from nmmo.envs import GatheringConfig


class BuildingGatheringConfig(GatheringConfig, Building):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = f'maps/gathering_obscured_and_exclusive_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'
