import os
from dataclasses import field

import marlben
from marlben.config.common import Template, SequentialLoader
from marlben.core.spawn.spawn_system import position_samplers, skill_samplers
from marlben.io.action import Heal


class NPCGroupConfig(Template):
    SPAWN_COORDINATES_SAMPLER = position_samplers.UniformPositionSampler()
    SPAWN_SKILLS_SAMPLER = skill_samplers.DefaultNPCSkillSampler(1, None, None)
    SPAWN_ATTEMPTS_PER_ENT = 5
    BANNED_ATTACK_STYLES = [Heal]  # By default, monsters can't heal someone
    NENT = 16
    DANGER = None  # Compute vanilla NMMO danger by default


class PlayerGroupConfig(Template):
    AGENT_LOADER = SequentialLoader
    SPAWN_COORDINATES_SAMPLER = position_samplers.ConcurrentPositionSampler()
    SPAWN_SKILLS_SAMPLER = skill_samplers.DefaultSkillSampler()
    SPAWN_ATTEMPTS_PER_ENT = 10
    BANNED_ATTACK_STYLES = []
    VISIBLE_COLORS = []
    ACCESSIBLE_COLORS = []
    AGENTS = []
    NENT = 2


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

    def __init__(self, dictionary=None):
        super().__init__()

        if dictionary is not None:
            self._populate_config(dictionary)

    def _populate_config(self, dictionary):
        for k, v in dictionary.items():
            print(k, v)
            if isinstance(v, dict):
                self._populate_config(v)
            else:
                setattr(self, k, v)
    ############################################################################
    # Meta-Parameters
    RENDER: bool = False

    def items(self):
        class_vars = {}
        for cls in self.__class__.mro()[:-1]:
            class_vars.update({
                k: v for k, v in cls.__dict__.items()
                if k not in object.__dict__ and not k.startswith('_')
                and not callable(v)
                and not isinstance(v, property)
            })
        return class_vars.items()

    def game_system_enabled(self, name) -> bool:
        return hasattr(self, name)

    ############################################################################
    # Visibility and Accessibility settings
    NUM_VISIBILITY_COLORS: int = 0
    NUM_ACCESSIBILITY_COLORS: int = 0

    # Population Parameters
    AGENT_LOADER = SequentialLoader
    '''Agent loader class specifying spawn sampling'''

    TASKS = []
    '''Tasks for which to compute rewards'''

    NPC_GROUPS = []
    PLAYER_GROUPS = []
    '''Groups of players and NPCs to spawn in the environment'''

    NMAPS = 1
    '''Number of maps to generate'''

    NTILE = 16
    # TODO: Find a way to auto-compute this
    '''Number of distinct terrain tile types'''

    NSTIM = 7
    '''Number of tiles an agent can see in any direction'''

    N_AGENT_OBS = 100
    '''Number of distinct agent observations'''

    def WINDOW(self):
        '''Size of the square tile crop visible to an agent'''
        return 2 * self.NSTIM + 1

    ############################################################################
    # Agent Parameters
    BASE_HEALTH = 10
    '''Initial Constitution level and agent health'''

    ############################################################################
    # Terrain Generation Parameters
    MAP_GENERATOR = None
    '''Specifies a user map generator. Uses default generator if unspecified.'''

    FORCE_MAP_GENERATION = True
    '''Whether to regenerate and overwrite existing maps'''

    GENERATE_MAP_PREVIEWS = False
    '''Whether map generation should also save .png previews (slow + large file size)'''

    MAP_PREVIEW_DOWNSCALE = 1
    '''Downscaling factor for png previews'''

    TERRAIN_CENTER = None  # TODO: Remove as we support HEIGHT and WIDTH parameters
    '''Size of each map (number of tiles along each side)'''

    TERRAIN_BORDER = 8
    TOP_LEFT_CORNER = (8, 8)  # TODO: Should implement as a property instead
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

    TERRAIN_TILES_PER_OCTAVE = 4
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
    # Path Parameters
    PATH_ROOT = os.path.dirname(marlben.__file__)
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
