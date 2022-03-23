from enum import Enum

from .base import spawn_concurrent, spawn_continuous, spawn_in_range


class SpawnFactory:
    class Type(Enum):
        CONCURRENT = 'concurrent'
        CONTINUOUS = 'continuous'
        IN_RANGE   = 'in_range'
    
    def get_spawn_system(spawn_system_name):
        mode = SpawnFactory.Type(spawn_system_name)
        if mode == SpawnFactory.Type.CONCURRENT:
            return spawn_concurrent
        if mode == SpawnFactory.Type.CONTINUOUS:
            return spawn_continuous
        if mode == SpawnFactory.Type.IN_RANGE:
            return spawn_in_range
