import random

from marlben.envs.colors import GatheringExclusive, ExclusiveGatheringConfig
from marlben.lib import material
from scripted.environments.gathering import ObscuredAndExclusiveGatheringAgent
import numpy as np

"""
A set of testcases for Colors environment.
Each test checks that outcome with scripted policies are within given boundaries.
It's expected that with increasing number of agents it becomes harder to find and collect resources.
"""


class ExclusiveGatheringScriptedConfig(ExclusiveGatheringConfig):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        for pg in self.PLAYER_GROUPS:
            pg.AGENTS[0] = ObscuredAndExclusiveGatheringAgent


def _get_lifetimes_and_survivors(env):
    _ = env.reset()
    water_num = np.sum([1 for row in env.realm.map.tiles for tile in row if int(tile.mat.index) in (material.Water.index, material.BalancedWater.index)])
    food_num = np.sum([1 for row in env.realm.map.tiles for tile in row if int(tile.mat.index) in (material.Forest.index, material.BalancedForest.index)])

    assert water_num == env.config.NENT
    assert food_num == 2 * env.config.NENT

    max_timesteps = 500
    timesteps = max_timesteps
    done = False
    prev_players_num = sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups)
    lifetime = []

    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        players_num = sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups)
        if players_num < prev_players_num:
            lifetime.extend([max_timesteps - timesteps]*(prev_players_num - players_num))

        prev_players_num = players_num
        done = done or players_num == 0
    survived = prev_players_num
    lifetime.extend([max_timesteps] * survived)
    return lifetime, survived


def test_exclusive_gathering_simple():
    random.seed(0)
    np.random.seed(0)
    env = GatheringExclusive(ExclusiveGatheringScriptedConfig(1, 2))
    survivors = []
    lifetimes = []

    for _ in range(10):
        lifetime, survived = _get_lifetimes_and_survivors(env)
        survivors.append(survived)
        lifetimes.extend(lifetime)
    assert np.mean(lifetimes) >= 250
    assert np.mean(survivors) >= 1.0


def test_exclusive_gathering_tiny():
    random.seed(0)
    np.random.seed(0)
    env = GatheringExclusive(ExclusiveGatheringScriptedConfig(2, 1))
    survivors = []
    lifetimes = []

    for _ in range(10):
        lifetime, survived = _get_lifetimes_and_survivors(env)
        survivors.append(survived)
        lifetimes.extend(lifetime)

    assert np.mean(lifetimes) >= 200
    assert np.mean(survivors) >= 0.5


def test_exclusive_gathering_medium():
    random.seed(0)
    np.random.seed(0)
    env = GatheringExclusive(ExclusiveGatheringScriptedConfig(3, 2))
    survivors = []
    lifetimes = []

    for _ in range(10):
        lifetime, survived = _get_lifetimes_and_survivors(env)
        survivors.append(survived)
        lifetimes.extend(lifetime)
    assert np.mean(lifetimes) >= 80
    assert np.mean(survivors) >= 0.2


def test_exclusive_gathering_large():
    random.seed(0)
    np.random.seed(0)
    env = GatheringExclusive(ExclusiveGatheringScriptedConfig(4, 4))
    survivors = []
    lifetimes = []

    for _ in range(10):
        lifetime, survived = _get_lifetimes_and_survivors(env)
        survivors.append(survived)
        lifetimes.extend(lifetime)
    assert 110 >= np.mean(lifetimes) >= 60
    assert 1 >= np.mean(survivors)
