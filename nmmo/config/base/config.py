import os

import numpy as np

import nmmo
from nmmo.config.common import Template, SequentialLoader
from nmmo.core.spawn.spawn_system import position_samplers, skill_samplers


class NPCGroupConfig(Template):
    SPAWN_COORDINATES_SAMPLER = position_samplers.UniformPositionSampler()
    SPAWN_SKILLS_SAMPLER = skill_samplers.DefaultNPCSkillSampler(1, None, None)
    SPAWN_ATTEMPTS_PER_ENT = 5
    NENT = 16


class PlayerGroupConfig(Template):
    AGENT_LOADER = SequentialLoader
    SPAWN_COORDINATES_SAMPLER = position_samplers.ConcurrentPositionSampler()
    SPAWN_SKILLS_SAMPLER = skill_samplers.DefaultSkillSampler()
    SPAWN_ATTEMPTS_PER_ENT = 5
    BANNED_ATTACK_STYLES = []
    NENT = 16


class Config(Template):
    '''An environment configuration object

   Global constants are defined as static class variables. You can override
   any Config variable using standard CLI syntax (e.g. --NENT=128).

   The default config as of v1.5 uses 1024x1024 maps with up to 2048 agents
   and 1024 NPCs. It is suitable to time horizons of 8192+ steps. For smaller
   experiments, consider the SmallMaps config.

   Notes:
      We use Google Fire internally to replace standard manual argparse
      definitions for each Config property. This means you can subclass
      Config to add new static attributes -- CLI definitions will be
      generated automatically.
   '''

    def __init__(self):
        super().__init__()

        if __debug__:
            err = 'config.Config is a base class. Use config.{Small, Medium Large}'''
            assert type(self) != Config, err

    ############################################################################
    ### Meta-Parameters
    RENDER = False

    def game_system_enabled(self, name) -> bool:
        return hasattr(self, name)

    ############################################################################
    ### Population Parameters
    AGENT_LOADER = SequentialLoader
    '''Agent loader class specifying spawn sampling'''

    AGENTS = []
    '''Agent classes from which to spawn'''

    TASKS = []
    '''Tasks for which to compute rewards'''

    NPC_GROUPS = []
    PLAYER_GROUPS = []
    '''Groups of players and NPCs to spawn in the environment'''

    NMAPS = 1
    '''Number of maps to generate'''

    NTILE = 6
    # TODO: Find a way to auto-compute this
    '''Number of distinct terrain tile types'''

    NSTIM = 7
    '''Number of tiles an agent can see in any direction'''

    N_AGENT_OBS = 100
    '''Number of distinct agent observations'''

    @property
    def WINDOW(self):
        '''Size of the square tile crop visible to an agent'''
        return 2 * self.NSTIM + 1

    ############################################################################
    ### Agent Parameters
    BASE_HEALTH = 10
    '''Initial Constitution level and agent health'''

    ############################################################################
    ### Terrain Generation Parameters
    MAP_GENERATOR = None
    '''Specifies a user map generator. Uses default generator if unspecified.'''

    FORCE_MAP_GENERATION = False
    '''Whether to regenerate and overwrite existing maps'''

    GENERATE_MAP_PREVIEWS = False
    '''Whether map generation should also save .png previews (slow + large file size)'''

    MAP_PREVIEW_DOWNSCALE = 1
    '''Downscaling factor for png previews'''

    TERRAIN_CENTER = None
    '''Size of each map (number of tiles along each side)'''

    TERRAIN_BORDER = 16
    TOP_LEFT_CORNER = (16, 16)
    '''Number of lava border tiles surrounding each side of the map'''

    @property
    def TERRAIN_SIZE(self):
        return int(self.TERRAIN_CENTER + 2 * self.TERRAIN_BORDER)

    @property
    def NENT(self):
        return sum([cfg.NENT for cfg in self.PLAYER_GROUPS])

    @property
    def NPOP(self):
        return len(self.PLAYER_GROUPS)

    TERRAIN_FLIP_SEED = False
    '''Whether to negate the seed used for generation (useful for unique heldout maps)'''

    TERRAIN_FREQUENCY = -3
    '''Base noise frequency range (log2 space)'''

    TERRAIN_FREQUENCY_OFFSET = 7
    '''Noise frequency octave offset (log2 space)'''

    TERRAIN_LOG_INTERPOLATE_MIN = -2
    '''Minimum interpolation log-strength for noise frequencies'''

    TERRAIN_LOG_INTERPOLATE_MAX = 0
    '''Maximum interpolation log-strength for noise frequencies'''

    TERRAIN_TILES_PER_OCTAVE = 8
    '''Number of octaves sampled from log2 spaced TERRAIN_FREQUENCY range'''

    TERRAIN_LAVA = 0.0
    '''Noise threshold for lava generation'''

    TERRAIN_WATER = 0.30
    '''Noise threshold for water generation'''

    TERRAIN_GRASS = 0.70
    '''Noise threshold for grass'''

    TERRAIN_FOREST = 0.85
    '''Noise threshold for forest'''

    ############################################################################
    ### Path Parameters
    PATH_ROOT = os.path.dirname(nmmo.__file__)
    '''Global repository directory'''

    PATH_CWD = os.getcwd()
    '''Working directory'''

    PATH_RESOURCE = os.path.join(PATH_ROOT, 'resource')
    '''Resource directory'''

    PATH_TILE = os.path.join(PATH_RESOURCE, '{}.png')
    '''Tile path -- format me with tile name'''

    PATH_MAPS = None
    '''Generated map directory'''

    PATH_MAP_SUFFIX = 'map{}/map.npy'
    '''Map file name'''
