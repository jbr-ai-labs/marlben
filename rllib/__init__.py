import ray

from nmmo.envs import Corridor
from nmmo.envs.gathering.env import Gathering
from .rllib_wrapper import RLlibEnv
from .neural import rllib_policy

env_factory = {
    'Corridor': Corridor,
    'Gathering': Gathering
}


for key in env_factory.keys():
    class CustomEnv(env_factory[key], RLlibEnv):
        pass
    ray.tune.registry.register_env(key, lambda config: CustomEnv(config))

ray.tune.registry.register_env('base', lambda config: RLlibEnv(config))
