from enum import Enum
import ray

from .environments import Corridor
from .environments.rllib_wrapper import RLlibEnv
from .neural import rllib_policy

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


for key in env_factory.keys():
    class CustomEnv(env_factory[key], RLlibEnv):
        pass
    ray.tune.registry.register_env(key, lambda config: CustomEnv(config))

ray.tune.registry.register_env('base', lambda config: RLlibEnv(config))