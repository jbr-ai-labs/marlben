import nmmo
from config import scale
from config.bases import Small
from nmmo.config import build_from_dict
from nmmo.core.spawn.custom_managers import CustomNPCManager, CustomPlayerManager
from .map_generator import CorridorMapGenerator

config_dict = {"presets_list": [nmmo.config.AllGameSystems, Small, scale.Debug],
               "parameters": {"AGENTS": [nmmo.Agent, nmmo.Agent],
                              "TERRAIN_CENTER": 5,
                              "NENT": 2,
                              "NMOB": 0,
                              "NSTIM": 1,
                              "TERRAIN_BORDER": 2,
                              "PATH_MAPS": 'src/environments/corridor/maps',
                              "SPAWN_PARAMS": {'type': 'in_range',
                                               'r_ranges': [(3, 5), (3, 5)],
                                               'c_ranges': [(3, 3), (5, 5)]},
                              "PLAYER_MANAGER": CustomPlayerManager,
                              "NPC_MANAGER": CustomNPCManager,
                              "MAP_GENERATOR": CorridorMapGenerator,
                              "FORCE_MAP_GENERATION": False}}

corridor_config = build_from_dict(config_dict)
