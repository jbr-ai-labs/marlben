from enum import Enum

from .environments import Corridor



env_factory = {
    'Corridor': Corridor
}


class EnvFactory:
    class Type(Enum):
        CORRIDOR = 'Corridor'
    
    @staticmethod
    def get_env(env_name):
        env_type = EnvFactory.Type(env_name)
        if env_type == EnvFactory.Type.CORRIDOR:
            return Corridor


def make(env_name, config):
    return EnvFactory.get_env(env_name)(config)
