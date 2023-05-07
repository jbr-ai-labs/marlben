from nmmo.envs.gathering_obscured import GatheringObscured, ObscuredGatheringConfig
from scripted.environments.gathering import ObscuredAndExclusiveGatheringAgent
import numpy as np

from .test_gatchering_exclusive import _get_lifetimes_and_survivors


class ObscuredGatheringScriptedConfig(ObscuredGatheringConfig):
    def __init__(self, n_groups, agents_per_group):
        super().__init__(n_groups, agents_per_group)
        for pg in self.PLAYER_GROUPS:
            pg.AGENTS[0] = ObscuredAndExclusiveGatheringAgent


def test_obscured_gathering_simple():
    env = GatheringObscured(ObscuredGatheringScriptedConfig(1, 2))
    lifetime, survived = _get_lifetimes_and_survivors(env)
    assert np.mean(lifetime) >= 250
    assert survived >= 1


def test_obscured_gathering_tiny():
    env = GatheringObscured(ObscuredGatheringScriptedConfig(2, 1))
    lifetime, survived = _get_lifetimes_and_survivors(env)
    assert np.mean(lifetime) >= 250
    assert survived >= 1


def test_obscured_gathering_medium():
    env = GatheringObscured(ObscuredGatheringScriptedConfig(4, 2))
    lifetime, survived = _get_lifetimes_and_survivors(env)
    assert np.mean(lifetime) >= 150
    assert survived >= 2


def test_obscured_gathering_large():
    env = GatheringObscured(ObscuredGatheringScriptedConfig(6, 4))
    lifetime, survived = _get_lifetimes_and_survivors(env)
    assert np.mean(lifetime) >= 100
    assert survived >= 4