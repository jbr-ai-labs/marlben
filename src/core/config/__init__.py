from nmmo.config.common import Template
from .config_parser import parse_configuration
from src.core.managers import CustomNPCManager, CustomPlayerManager
from src.core.map_generator import CustomMapGenerator
from nmmo.config.builders import build_from_dict


def get_config(cfg_path):
    cfg_dict = {}
    cfg_dict["presets_list"] = ["Config", "Sharing"]
    cfg_dict["parameters"] = parse_configuration(cfg_path)
    cfg_dict["parameters"]["PLAYER_MANAGER"] = CustomPlayerManager
    cfg_dict["parameters"]["NPC_MANAGER"] = CustomNPCManager
    cfg_dict["parameters"]["MAP_GENERATOR"] = CustomMapGenerator
    cfg_dict["parameters"]["GENERATE_MAP_PREVIEWS"] = False
    Composed = build_from_dict(cfg_dict)
    return Composed