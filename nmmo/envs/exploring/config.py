from nmmo.envs import GatheringConfig


class ObscuredAndExclusiveGatheringConfig(GatheringConfig):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.NUM_ACCESSIBILITY_COLORS = n_groups
        self.NUM_VISIBILITY_COLORS = n_groups
        self.RESOURCE_HARVEST_RESTORE_FRACTION = 1. - 1 / self.RESOURCE_COOLDOWN

        for i, group in enumerate(self.PLAYER_GROUPS):
            group.ACCESSIBLE_COLORS = [i+1]
            group.VISIBLE_COLORS = [i+1]

        self.PATH_MAPS = f'maps/exploring_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'
