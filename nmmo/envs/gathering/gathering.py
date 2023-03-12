from nmmo import Agent
from nmmo.config import Resource, Building
from nmmo.config.base.config import PlayerGroupConfig, Config
from .utils.map_generator import GatheringMapGenerator
import math

HORIZON = 500


class GatheringPlayerGroup(PlayerGroupConfig):
    AGENTS = [Agent]

    def __init__(self, n_agents, visible_colors=(), accessible_colors=()):
        super().__init__()
        self.NENT = n_agents
        self.VISIBLE_COLORS = visible_colors
        self.ACCESSIBLE_COLORS = accessible_colors


class GatheringConfig(Resource, Config):
    TRAIN_HORIZON = HORIZON
    EVAL_HORIZON = HORIZON
    MAP_GENERATOR = GatheringMapGenerator
    RESOURCE_COOLDOWN = 8
    RESOURCE_BASE_RESOURCE = 32
    RESOURCE_HARVEST_RESTORE_FRACTION = 1 / RESOURCE_COOLDOWN

    def __init__(self, n_groups, agents_per_group):
        super().__init__()
        assert n_groups > 0 and agents_per_group > 0
        self.PLAYER_GROUPS = [GatheringPlayerGroup(agents_per_group) for _ in range(n_groups)]
        total_agents = n_groups * agents_per_group
        map_size = math.ceil((total_agents * 32)**0.5 / 4) * 4  # Round up. Should be divisible by 4
        self.MAP_WIDTH = map_size
        self.MAP_HEIGHT = map_size
        self.TERRAIN_CENTER = map_size
        self.PATH_MAPS = f'maps/gathering_{map_size}x{map_size}'


class ObscuredGatheringConfig(GatheringConfig):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.NUM_VISIBILITY_COLORS = n_groups
        for i, group in enumerate(self.PLAYER_GROUPS):
            group.VISIBLE_COLORS = [i+1]
        self.PATH_MAPS = f'maps/gathering_obscured_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'


class ExclusiveGatheringConfig(GatheringConfig):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.NUM_ACCESSIBILITY_COLORS = n_groups
        for i, group in enumerate(self.PLAYER_GROUPS):
            group.ACCESSIBLE_COLORS = [i+1]
        self.PATH_MAPS = f'maps/gathering_exclusive_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'


class ObscuredAndExclusiveGatheringConfig(GatheringConfig):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.NUM_ACCESSIBILITY_COLORS = n_groups
        self.NUM_VISIBILITY_COLORS = n_groups

        for i, group in enumerate(self.PLAYER_GROUPS):
            group.ACCESSIBLE_COLORS = [i+1]
            group.VISIBLE_COLORS = [i+1]

        self.PATH_MAPS = f'maps/gathering_obscured_and_exclusive_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'


class BuildingGatheringConfig(GatheringConfig, Building):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = f'maps/gathering_obscured_and_exclusive_{self.MAP_WIDTH}x{self.MAP_HEIGHT}'
