from nmmo.config.base.config import Config


class Small(Config):
    '''A small config for debugging and experiments with an expensive outer loop'''

    PATH_MAPS = 'maps/small'
    MAP_PREVIEW_DOWNSCALE = 4

    TERRAIN_LOG_INTERPOLATE_MIN = 0

    TERRAIN_CENTER = 32
    NENT = 64
    NMOB = 32

    PLAYER_SPAWN_ATTEMPTS = 1

    NPC_LEVEL_MAX = 10
    NPC_LEVEL_SPREAD = 1


class Medium(Config):
    '''A medium config suitable for most academic-scale research'''

    PATH_MAPS = 'maps/medium'
    MAP_PREVIEW_DOWNSCALE = 16

    TERRAIN_CENTER = 128
    NENT = 256
    NMOB = 128

    PLAYER_SPAWN_ATTEMPTS = 2

    NPC_LEVEL_MAX = 30
    NPC_LEVEL_SPREAD = 5


class Large(Config):
    '''A large config suitable for large-scale research or fast models'''

    PATH_MAPS = 'maps/large'
    MAP_PREVIEW_DOWNSCALE = 64

    TERRAIN_CENTER = 1024
    NENT = 2048
    NMOB = 1024

    PLAYER_SPAWN_ATTEMPTS = 16

    NPC_LEVEL_MAX = 99
    NPC_LEVEL_SPREAD = 10