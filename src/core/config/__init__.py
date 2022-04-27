from nmmo.config import Config, Sharing
from .config_parser import parse_configuration
from nmmo.config.builders import build_from_dict
from config.bases import Small
from config.scale import Debug


def get_config(cfg_path):
    cfg_dict = {}
    cfg_dict["presets_list"] = [Sharing, Small, Debug]
    cfg_dict["parameters"] = parse_configuration(cfg_path)
    Composed = build_from_dict(cfg_dict)
    
    return Composed