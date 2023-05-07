from nmmo.envs.gathering_obscured_and_exclusive import GatheringObscuredAndExclusive, ObscuredAndExclusiveGatheringConfig
from scripted.environments.gathering import ObscuredAndExclusiveGatheringAgent
import numpy as np

from .test_gatchering_exclusive import _get_lifetimes_and_survivors


class ObscuredAndExclusiveGatheringScriptedConfig(ObscuredAndExclusiveGatheringConfig):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        for pg in self.PLAYER_GROUPS:
            pg.AGENTS[0] = ObscuredAndExclusiveGatheringAgent


def test_obscured_and_exclusive_gathering_simple():
    env = GatheringObscuredAndExclusive(ObscuredAndExclusiveGatheringConfig(1, 2))
    lifetime, survived = _get_lifetimes_and_survivors(env)
    assert np.mean(lifetime) >= 250
    assert survived >= 1


def test_obscured_and_exclusive_gathering_tiny():
    env = GatheringObscuredAndExclusive(ObscuredAndExclusiveGatheringConfig(2, 1))
    lifetime, survived = _get_lifetimes_and_survivors(env)
    assert np.mean(lifetime) >= 150
    assert survived >= 1


def test_obscured_and_exclusive_gathering_medium():
    env = GatheringObscuredAndExclusive(ObscuredAndExclusiveGatheringConfig(4, 2))
    lifetime, survived = _get_lifetimes_and_survivors(env)
    assert np.mean(lifetime) >= 50
    assert survived >= 1


def test_obscured_and_exclusive_gathering_large():
    env = GatheringObscuredAndExclusive(ObscuredAndExclusiveGatheringConfig(6, 4))
    lifetime, survived = _get_lifetimes_and_survivors(env)
    assert survived == 0