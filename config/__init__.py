from . import bases, baselines
from .bases import Small
from .scale import Debug
from nmmo.config import name2config


def get_config(env_name):
    EnvConfig = name2config[env_name]

    class Cfg(EnvConfig, Small, Debug):
        RENDER = True

    return Cfg
