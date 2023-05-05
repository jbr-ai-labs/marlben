from .utils import create_env, random_interaction
from nmmo.envs.boss_fight.env import BossFight, BossFightConfig


def test_bossfight_env_create():
    create_env(BossFight, BossFightConfig())


def test_bossfight_interaction():
    env = create_env(BossFight, BossFightConfig())
    random_interaction(env, 100)