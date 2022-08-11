from .base import *
from .systems import *
from .presets import Default
from .builders import build_from_dict
from .env_presets import name2config



def get_config(env_name):
    return name2config[env_name]
