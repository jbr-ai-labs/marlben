from typing import Callable
from os import path as osp

from nmmo.core.agent import Agent
from scripted.baselines import CorridorAgent
from nmmo.core.spawn.spawn_system.position_samplers import UniformPositionSampler
from nmmo.core.spawn.spawn_system.skill_samplers import CustomSkillSampler
from nmmo.systems.achievement import Task
from src.core.map_generator.custom_map_generator import CustomMapGenerator
from src.core.map_generator import PATH_TO_CUSTOM_MAPS


from ..base.config import PlayerGroupConfig, Config
from ..systems import Sharing


HORIZON = 70


class PlayerDiedTask(Callable):
    __name__ = "Die"

    def __call__(self, realm, entity):
        return 0 if entity.alive else 1


class PlayerSurvivedTask(Callable):
    __name__ = "Survive"

    def __init__(self, horizon):
        super().__init__()
        self.horizon = horizon

    def __call__(self, realm, entity):
        survived = entity.alive and realm.tick >= self.horizon
        return 1 if survived else 0


class TraderGroupConfig(PlayerGroupConfig):
    def __init__(self, agents, n_ent, coordinates_sampler, skill_sampler=CustomSkillSampler({})):
        super().__init__()
        self.NENT = n_ent
        self.SPAWN_COORDINATES_SAMPLER = coordinates_sampler
        self.SPAWN_SKILLS_SAMPLER = skill_sampler
        self.AGENTS = agents
    
    SPAWN_ATTEMPTS_PER_ENT = 1
    BASE_HEALTH = 5
    REGEN_HEALTH = False


class BaseCorridorConfig(Config, Sharing):       
    TASKS = [Task(PlayerDiedTask(), 1, -1.0),
             Task(PlayerSurvivedTask(horizon=HORIZON), 1, 1.0)]

    TERRAIN_CENTER = 14
    TERRAIN_BORDER = 9
    NSTIM = 10
    MAP_HEIGHT = 3
    MAP_WIDTH = 10
    TOP_LEFT_CORNER = [17, 12]

    MAP_PREVIEW_DOWNSCALE = 1
    TERRAIN_LOG_INTERPOLATE_MIN = 0
    PATH_MAPS = osp.join(PATH_TO_CUSTOM_MAPS, "corridor")
    MAP_GENERATOR = CustomMapGenerator

    RESOURCE_BASE_RESOURCE = 14
    RESOURCE_HARVEST_RESTORE_FRACTION = 1.0
    RESOURCE_COOLDOWN = 5

    TRAIN_HORIZON = HORIZON
    EVAL_HORIZON = HORIZON


def create_group_config(agents):
    return [
        TraderGroupConfig(
            agents=[agents[0]], 
            n_ent=1,
            coordinates_sampler=UniformPositionSampler(r_range=[1, 1], c_range=[4, 4])
        ),
        TraderGroupConfig(
            agents=[agents[1]], 
            n_ent=1,
            coordinates_sampler=UniformPositionSampler(r_range=[1, 1], c_range=[5, 5])
        )
    ]

def process_agents(player_groups):
    agents = []
    for group in player_groups:
        agents.extend(group.AGENTS)
    return agents

class ScriptedCorridorConfig(BaseCorridorConfig):
    PLAYER_GROUPS = create_group_config(agents=[CorridorAgent, CorridorAgent])
    AGENTS = process_agents(PLAYER_GROUPS)

class OneNeuralCorridorConfig(BaseCorridorConfig):
    PLAYER_GROUPS = create_group_config(agents=[Agent, CorridorAgent])
    AGENTS = process_agents(PLAYER_GROUPS)

class CorridorConfig(BaseCorridorConfig):
    PLAYER_GROUPS = create_group_config(agents=[Agent, Agent])
    AGENTS = process_agents(PLAYER_GROUPS)
