from nmmo.envs import GatheringConfig


class ExclusiveGatheringConfig(GatheringConfig):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.NUM_ACCESSIBILITY_COLORS = n_groups
        for i, group in enumerate(self.PLAYER_GROUPS):
            group.ACCESSIBLE_COLORS = [i+1]
        self.PATH_MAPS = f'maps/gathering_exclusive_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'
