from os import path as osp


from nmmo import Agent
from nmmo.config import Resource
from nmmo.config.base.config import PlayerGroupConfig, Config
from nmmo.core.map_generation.pregen_map_generator import PregeneratedMapGenerator
from nmmo.envs.gathering.utils.map_generator import GatheringMapGenerator
from nmmo.core.spawn.spawn_system.position_samplers import UniformPositionSampler
from scripted.baselines import GatheringAgent
import math


HORIZON = 20
PATH_TO_CUSTOM_MAPS = osp.dirname(osp.dirname(__file__))




class GatheringPlayerGroup(PlayerGroupConfig):

    def __init__(self, n_agents, visible_colors=(), accessible_colors=(), agents=None, coord_sampler=None):
        super().__init__()
        self.NENT = n_agents
        self.VISIBLE_COLORS = visible_colors
        self.ACCESSIBLE_COLORS = accessible_colors
        self.AGENTS = agents if agents is not None else [Agent]
        if coord_sampler is not None:
            self.SPAWN_COORDINATES_SAMPLER = coord_sampler


def create_group_config(agents, agents_per_group, coord_samplers=None):
    cfgs = []
    if coord_samplers is None:
        coord_samplers = [None] * len(agents)
    for i, agent in enumerate(agents):
        cfg = GatheringPlayerGroup(
            agents=[agent],
            n_agents=agents_per_group,
            coord_sampler=coord_samplers[i]
        )
        cfgs.append(cfg)
    return cfgs


def process_agents(player_groups):
    agents = []
    for group in player_groups:
        agents.extend(group.AGENTS)
    return agents

class BaseGatheringConfig(Resource, Config):
    TRAIN_HORIZON = HORIZON
    EVAL_HORIZON = HORIZON
    MAP_GENERATOR = GatheringMapGenerator
    RESOURCE_COOLDOWN = 8
    RESOURCE_BASE_RESOURCE = 32
    RESOURCE_HARVEST_RESTORE_FRACTION = 1 / RESOURCE_COOLDOWN
    
    def __init__(self, n_groups, agents_per_group):
        super().__init__()
        assert n_groups > 0 and agents_per_group > 0
        total_agents = n_groups * agents_per_group
        map_size = math.ceil((total_agents * 32)**0.5 / 4) * 4  # Round up. Should be divisible by 4
        self.MAP_WIDTH = map_size
        self.MAP_HEIGHT = map_size
        self.TERRAIN_CENTER = map_size
        self.PATH_MAPS = f'maps/gathering_{map_size}x{map_size}'


class GatheringConfig(BaseGatheringConfig):
    AGENT_TYPE = Agent
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PLAYER_GROUPS = create_group_config([self.AGENT_TYPE for _ in range(n_groups)], agents_per_group)
        self.AGENTS = process_agents(self.PLAYER_GROUPS)

class GatheringConfigScripted(BaseGatheringConfig):
    MAP_GENERATOR = PregeneratedMapGenerator
    RESOURCE_HARVEST_RESTORE_FRACTION = 1.0
    AGENT_TYPE = GatheringAgent
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        self.PATH_MAPS = osp.join(PATH_TO_CUSTOM_MAPS, "test_maps", "base")
        coord_samplers = []
        for group in range(n_groups):
            column = (1 + group // 2) * (1 - group % 2) + (7 - group // 2 - 1) * (group % 2)
            coord_samplers.append(
                UniformPositionSampler(r_range=[4, 4], c_range=[column, column])
            )
        self.PLAYER_GROUPS = create_group_config([self.AGENT_TYPE for _ in range(n_groups)], agents_per_group, coord_samplers=coord_samplers)
        self.AGENTS = process_agents(self.PLAYER_GROUPS)
