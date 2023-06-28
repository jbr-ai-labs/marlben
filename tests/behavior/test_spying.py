import random

from marlben.envs.spying import GatheringObscured, ObscuredGatheringConfig
from marlben.scripted.environments.gathering import ObscuredAndExclusiveGatheringAgent
import numpy as np

from .test_colors import _get_lifetimes_and_survivors

"""
A set of testcases for Spying environment.
Each test checks that outcome with scripted policies are within given boundaries.
It's expected that with increasing number of agents it becomes harder to find and collect resources.
"""

class ObscuredGatheringScriptedConfig(ObscuredGatheringConfig):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        for pg in self.PLAYER_GROUPS:
            pg.AGENTS[0] = ObscuredAndExclusiveGatheringAgent


def test_obscured_gathering_simple():
    random.seed(0)
    np.random.seed(0)
    env = GatheringObscured(ObscuredGatheringScriptedConfig(1, 2))
    survivors = []
    lifetimes = []

    for _ in range(10):
        lifetime, survived = _get_lifetimes_and_survivors(env)
        survivors.append(survived)
        lifetimes.extend(lifetime)
    assert np.mean(lifetimes) >= 200
    assert np.mean(survivors) >= 0.5


def test_obscured_gathering_tiny():
    random.seed(0)
    np.random.seed(0)
    env = GatheringObscured(ObscuredGatheringScriptedConfig(2, 1))
    survivors = []
    lifetimes = []

    for _ in range(10):
        lifetime, survived = _get_lifetimes_and_survivors(env)
        survivors.append(survived)
        lifetimes.extend(lifetime)
    assert 200 >= np.mean(lifetimes) >= 80


def test_obscured_gathering_medium():
    random.seed(0)
    np.random.seed(0)
    env = GatheringObscured(ObscuredGatheringScriptedConfig(3, 2))
    survivors = []
    lifetimes = []

    for _ in range(10):
        lifetime, survived = _get_lifetimes_and_survivors(env)
        survivors.append(survived)
        lifetimes.extend(lifetime)
    assert 100 >= np.mean(lifetimes) >= 55


def test_obscured_gathering_large():
    random.seed(0)
    np.random.seed(0)
    env = GatheringObscured(ObscuredGatheringScriptedConfig(4, 4))
    survivors = []
    lifetimes = []

    for _ in range(10):
        lifetime, survived = _get_lifetimes_and_survivors(env)
        survivors.append(survived)
        lifetimes.extend(lifetime)
    assert 85 >= np.mean(lifetimes) >= 40
