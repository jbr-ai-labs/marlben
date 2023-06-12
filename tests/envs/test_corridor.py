from .utils import create_env, random_interaction
from marlben.envs.corridor.env import Corridor
from marlben.envs.corridor.config import CorridorConfig

"""
A load testcase. Checks creating an environment with different parameters and random interactions.
Helps to find raising exceptions and check computational resources load.
"""

def test_corridor_env_create():
    create_env(Corridor, CorridorConfig())


def test_corridor_interaction():
    env = create_env(Corridor, CorridorConfig())
    random_interaction(env, 100)