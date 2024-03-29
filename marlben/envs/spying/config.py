from marlben.envs import GatheringConfig


class ObscuredGatheringConfig(GatheringConfig):
    def __init__(self, n_groups, agents_per_group, tiles_per_agent=32, adjust_resource_amount=False):
        super().__init__(n_groups, agents_per_group, tiles_per_agent, adjust_resource_amount)
        self.RESOURCE_HARVEST_RESTORE_FRACTION = self.RESOURCE_COOLDOWN / self.RESOURCE_BASE_RESOURCE
        self.NUM_VISIBILITY_COLORS = n_groups
        for i, group in enumerate(self.PLAYER_GROUPS):
            group.VISIBLE_COLORS = [i+1]
        self.PATH_MAPS = f'maps/spying_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'
