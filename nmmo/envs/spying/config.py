from nmmo.envs import GatheringConfig


class ObscuredGatheringConfig(GatheringConfig):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.RESOURCE_HARVEST_RESTORE_FRACTION = self.RESOURCE_COOLDOWN / self.RESOURCE_BASE_RESOURCE
        self.NUM_VISIBILITY_COLORS = n_groups
        for i, group in enumerate(self.PLAYER_GROUPS):
            group.VISIBLE_COLORS = [i+1]
        self.PATH_MAPS = f'maps/gathering_obscured_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'
