from nmmo.core import agent
from scripted.baselines import Meander



def parse_agent_configuration(agent_cfg):
    parameters = {}

    nent = agent_cfg["count"]
    spawn_params = agent_cfg["spawn_params"]
    agents = [Meander for _ in range(nent)] # TODO: change to neural network agents
    base_health = agent_cfg["health"]
    regen_health = agent_cfg["regen"]

    parameters["NENT"] = nent
    parameters["SPAWN_PARAMS"] = spawn_params
    parameters["AGENTS"] = agents
    parameters["BASE_HEALTH"] = base_health
    parameters["REGEN_HEALTH"] = regen_health
    
    return parameters
