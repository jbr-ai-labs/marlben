from marlben.envs import name2config
from .presets.bases import Small
from .presets.scale import Debug
def get_config(env_name):
    EnvConfig = name2config[env_name]

    class Cfg(EnvConfig, Small, Debug):
        RENDER = False

    return Cfg