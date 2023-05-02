from .utils import create_env, random_interaction
from nmmo.envs.corridor.env import Corridor
from nmmo.envs.corridor.corridor import CorridorConfig


def test_bossfight_env_create():
    create_env(Corridor, CorridorConfig())


def test_bossfight_interaction():
    env = create_env(Corridor, CorridorConfig())
    random_interaction(env, 100)