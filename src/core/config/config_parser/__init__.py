import json

from os import path as osp

from .agent_parser import parse_agent_configuration
from .map_parser import parse_map_configuration
from .resources_parser import parse_resources_configuration
from .environment_parser import parse_env_configuration



def parse_configuration(cfg_path):
    with open(cfg_path, "rb") as f:
        cfg = json.load(f)
    path_to_maps = osp.join(osp.dirname(cfg_path), "maps")
    parameters = {}
    parameters["PATH_MAPS"] = path_to_maps

    parameters.update(parse_agent_configuration(cfg["agents"]))
    parameters.update(parse_map_configuration(cfg["map"]))
    parameters.update(parse_resources_configuration(cfg["resources"]))
    parameters.update(parse_env_configuration(cfg["environment"]))
    # TODO: parse other parts of config
    return parameters
