from .utils import create_env, run_env


from nmmo.envs.gathering.env import Gathering
from nmmo.envs.gathering.configs.base import GatheringConfigScripted
from nmmo.envs.gathering.configs.building import BuildingGatheringConfigScripted


def _test_helper(cfg_class):
    env = create_env(Gathering, cfg_class(n_groups=2, agents_per_group=1))
    run_env(env, 100)


def test_gathering_scripted():
    _test_helper(cfg_class=GatheringConfigScripted)


def test_gathering_building_scripted():
    _test_helper(cfg_class=BuildingGatheringConfigScripted)
