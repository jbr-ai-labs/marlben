from .utils import create_env, random_interaction
from marlben.envs.corridor.env import Corridor
from marlben.envs.corridor.config import CorridorConfig


def test_corridor_env_create():
    create_env(Corridor, CorridorConfig())


def test_corridor_interaction():
    env = create_env(Corridor, CorridorConfig())
    random_interaction(env, 100)