import nmmo
from scripted import baselines
from .map_generator import CorridorMapGenerator
from src.core.custom_managers import CustomNPCManager, CustomPlayerManager



class Config(nmmo.config.Small, nmmo.config.AllGameSystems):
    """Config objects subclass a nmmo.config.{Small, Medium, Large} template

    Can also specify config game systems to enable various features"""

    # Agents will be instantiated using templates included with the baselines
    # Meander: randomly wanders around
    # Forage: explicitly searches for food and water
    # Combat: forages and actively fights other agents
    AGENTS = [baselines.Meander, baselines.Meander]

    TERRAIN_CENTER = 5
    NENT = 2
    NMOB = 0
    NSTIM = 1
    TERRAIN_BORDER = 2

    # Set a unique path for demo maps
    PATH_MAPS = 'src/environments/corridor/maps'
    SPAWN_PARAMS = {
        'type': 'in_range',
        'r_ranges': [(3, 5), (3, 5)],
        'c_ranges': [(3, 3), (5, 5)]
    }
    PLAYER_MANAGER = None
    NPC_MANAGER = None

    # Force terrain generation -- avoids unexpected behavior from caching
    FORCE_MAP_GENERATION = False
    MAP_GENERATOR = CorridorMapGenerator
    PLAYER_MANAGER = CustomPlayerManager
    NPC_MANAGER = CustomNPCManager

    # def SPAWN(self):
    #     return [(3, 3)]
