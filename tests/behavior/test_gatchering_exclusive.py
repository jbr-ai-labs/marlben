from nmmo.envs.gathering_exclusive import GatheringExclusive, ExclusiveGatheringConfig
from scripted.environments.gathering import ObscuredAndExclusiveGatheringAgent
import numpy as np


class ExclusiveGatheringScriptedConfig(ExclusiveGatheringConfig):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        for pg in self.PLAYER_GROUPS:
            pg.AGENTS[0] = ObscuredAndExclusiveGatheringAgent


def _get_lifetimes_and_survivors(env):
    _ = env.reset()
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
    env = GatheringExclusive(ExclusiveGatheringScriptedConfig(1, 2))
    lifetime, survived = _get_lifetimes_and_survivors(env)
    assert np.mean(lifetime) >= 250
    assert survived >= 1


def test_exclusive_gathering_tiny():
    env = GatheringExclusive(ExclusiveGatheringScriptedConfig(2, 1))
    lifetime, survived = _get_lifetimes_and_survivors(env)
    assert np.mean(lifetime) >= 250
    assert survived >= 1


def test_exclusive_gathering_medium():
    env = GatheringExclusive(ExclusiveGatheringScriptedConfig(4, 2))
    lifetime, survived = _get_lifetimes_and_survivors(env)
    assert np.mean(lifetime) >= 150
    assert survived >= 2


def test_exclusive_gathering_large():
    env = GatheringExclusive(ExclusiveGatheringScriptedConfig(6, 4))
    lifetime, survived = _get_lifetimes_and_survivors(env)
    assert np.mean(lifetime) >= 100
    assert survived >= 3
