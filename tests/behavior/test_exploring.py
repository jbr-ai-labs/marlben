import random

from marlben.envs.exploring import GatheringObscuredAndExclusive, ObscuredAndExclusiveGatheringConfig
from scripted.environments.gathering import ObscuredAndExclusiveGatheringAgent
import numpy as np

from .test_colors import _get_lifetimes_and_survivors

"""
A set of testcases for Exploring environment.
Each test checks that outcome with scripted policies are within given boundaries.
It's expected that with increasing number of agents it becomes harder to find and collect resources.
"""

class ObscuredAndExclusiveGatheringScriptedConfig(ObscuredAndExclusiveGatheringConfig):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        for pg in self.PLAYER_GROUPS:
            pg.AGENTS[0] = ObscuredAndExclusiveGatheringAgent


def test_obscured_and_exclusive_gathering_simple():
    random.seed(0)
    np.random.seed(0)
    env = GatheringObscuredAndExclusive(ObscuredAndExclusiveGatheringScriptedConfig(1, 2))
    survivors = []
    lifetimes = []

    for _ in range(10):
        lifetime, survived = _get_lifetimes_and_survivors(env)
        survivors.append(survived)
        lifetimes.extend(lifetime)
    assert np.mean(lifetimes) >= 200
    assert np.mean(survivors) >= 0.7


def test_obscured_and_exclusive_gathering_tiny():
    random.seed(0)
    np.random.seed(0)
    env = GatheringObscuredAndExclusive(ObscuredAndExclusiveGatheringScriptedConfig(2, 1))
    survivors = []
    lifetimes = []

    for _ in range(10):
        lifetime, survived = _get_lifetimes_and_survivors(env)
        survivors.append(survived)
        lifetimes.extend(lifetime)
    assert np.mean(lifetimes) >= 200
    assert np.mean(survivors) >= 0.75


def test_obscured_and_exclusive_gathering_medium():
    random.seed(0)
    np.random.seed(0)
    env = GatheringObscuredAndExclusive(ObscuredAndExclusiveGatheringScriptedConfig(3, 2))
    survivors = []
    lifetimes = []

    for _ in range(10):
        lifetime, survived = _get_lifetimes_and_survivors(env)
        survivors.append(survived)
        lifetimes.extend(lifetime)
    assert 200 >= np.mean(lifetimes) >= 100
    assert np.mean(survivors) >= 0.6


def test_obscured_and_exclusive_gathering_large():
    random.seed(0)
    np.random.seed(0)
    env = GatheringObscuredAndExclusive(ObscuredAndExclusiveGatheringScriptedConfig(4, 4))
    survivors = []
    lifetimes = []

    for _ in range(10):
        lifetime, survived = _get_lifetimes_and_survivors(env)
        survivors.append(survived)
        lifetimes.extend(lifetime)
    assert 90 >= np.mean(lifetimes) >= 37
    assert 1.5 >= np.mean(survivors)