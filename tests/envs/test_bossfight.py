from .utils import create_env, random_interaction
from marlben.envs.boss_fight.env import BossFight, BossFightConfig

"""
A load testcase. Checks creating an environment with different parameters and random interactions.
Helps to find raising exceptions and check computational resources load.
"""

def test_bossfight_env_create():
    create_env(BossFight, BossFightConfig())


def test_bossfight_interaction():
    env = create_env(BossFight, BossFightConfig())
    random_interaction(env, 100)