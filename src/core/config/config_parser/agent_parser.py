from nmmo import Agent
from nmmo.core import agent
from scripted.baselines import Meander, CorridorAgent, Random


def parse_agent_configuration(agent_cfg):
    parameters = {}

    parameters["NENT"] = agent_cfg["count"]
    parameters["SPAWN_PARAMS"] = agent_cfg["spawn_params"]
    parameters["AGENTS"] = [CorridorAgent]
    parameters["BASE_HEALTH"] = agent_cfg["health"]
    parameters["REGEN_HEALTH"] = agent_cfg["regen"]

    return parameters
