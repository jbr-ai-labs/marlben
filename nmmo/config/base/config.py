import os

import numpy as np

import nmmo
from nmmo.config.common import Template, SequentialLoader


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
    '''Flag used by render mode'''

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

    NMAPS = 1
    '''Number of maps to generate'''

    NTILE = 6
    # TODO: Find a way to auto-compute this
    '''Number of distinct terrain tile types'''

    NSTIM = 7
    '''Number of tiles an agent can see in any direction'''

    NMOB = None
    '''Maximum number of NPCs spawnable in the environment'''

    NENT = None
    '''Maximum number of agents spawnable in the environment'''

    NPOP = 1
    '''Number of distinct populations spawnable in the environment'''

    N_AGENT_OBS = 100
    '''Number of distinct agent observations'''

    @property
    def TEAM_SIZE(self):
        assert not self.NENT % self.NPOP
        return self.NENT // self.NPOP

    @property
    def WINDOW(self):
        '''Size of the square tile crop visible to an agent'''
        return 2 * self.NSTIM + 1

    ############################################################################
    ### Agent Parameters
    BASE_HEALTH = 10
    '''Initial Constitution level and agent health'''

    PLAYER_SPAWN_ATTEMPTS = None
    '''Number of player spawn attempts per tick

   Note that the env will attempt to spawn agents until success
   if the current population size is zero.'''

    def SPAWN_CONTINUOUS(self):
        '''Generates spawn positions for new agents

      Default behavior randomly selects a tile position
      along the borders of the square game map

      Returns:
         tuple(int, int):

         position:
            The position (row, col) to spawn the given agent
      '''
        # Spawn at edges
        mmax = self.TERRAIN_CENTER + self.TERRAIN_BORDER
        mmin = self.TERRAIN_BORDER

        var = np.random.randint(mmin, mmax)
        fixed = np.random.choice([mmin, mmax])
        r, c = int(var), int(fixed)
        if np.random.rand() > 0.5:
            r, c = c, r
        return (r, c)

    def SPAWN_CONCURRENT(self):
        left = self.TERRAIN_BORDER
        right = self.TERRAIN_CENTER + self.TERRAIN_BORDER
        rrange = np.arange(left + 2, right, 4).tolist()

        assert not self.TERRAIN_CENTER % 4
        per_side = self.TERRAIN_CENTER // 4

        lows = (left + np.zeros(per_side, dtype=np.int)).tolist()
        highs = (right + np.zeros(per_side, dtype=np.int)).tolist()

        s1 = list(zip(rrange, lows))
        s2 = list(zip(lows, rrange))
        s3 = list(zip(rrange, highs))
        s4 = list(zip(highs, rrange))

        return s1 + s2 + s3 + s4

    @property
    def SPAWN(self):
        return self.SPAWN_CONTINUOUS

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
    '''Number of lava border tiles surrounding each side of the map'''

    @property
    def TERRAIN_SIZE(self):
        return int(self.TERRAIN_CENTER + 2 * self.TERRAIN_BORDER)

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