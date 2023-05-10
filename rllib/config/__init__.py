from marlben.envs import name2config
from . import bases, baselines
from .bases import Small
from .scale import Debug


def get_config(env_name):
    EnvConfig = name2config[env_name]

    class Cfg(EnvConfig, Small, Debug):
        RENDER = False

    return Cfg
