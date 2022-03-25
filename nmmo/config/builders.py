from .base import *
from .systems import *
from .presets import *
import sys


def build_from_dict(config_dict):
    presets_list = config_dict["presets_list"]
    classes = []
    for preset in presets_list:
        classes.append(eval(preset))

    class CustomClass(*classes):
        pass

    config = CustomClass()
    for key, value in config_dict["parameters"]:
        setattr(config, key, value)

    return config