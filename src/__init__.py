from enum import Enum

from .environments import Corridor
from src.core.config import get_config



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


def make(env_name, config_path):
    config = get_config(config_path)
    return EnvFactory.get_env(env_name)(config)
