from .utils import create_env, random_interaction
from nmmo.envs.gathering.env import Gathering
from nmmo.envs.gathering.configs.base import GatheringConfig
from nmmo.envs.gathering.configs.obscured import ObscuredGatheringConfig
from nmmo.envs.gathering.configs.obscured_and_exclusive import ObscuredAndExclusiveGatheringConfig
from nmmo.envs.gathering.configs.exclusive import ExclusiveGatheringConfig
from nmmo.envs.gathering.configs.building import BuildingGatheringConfig


def _test_create_with_config_class(cfg_class):
    for num_groups in (2, 4, 8):
        for num_agents_per_group in (2, 4, 8):
            try:
                create_env(Gathering, cfg_class(num_groups, num_agents_per_group))
            except Exception as e:
                raise Exception(f"Params ({num_groups}, {num_agents_per_group})") from e


def _test_interact_with_config_class(cfg_class):
    for num_groups in (2, 4, 8):
        for num_agents_per_group in (2, 4, 8):
            try:
                env = create_env(Gathering, cfg_class(num_groups, num_agents_per_group))
                random_interaction(env, 100)
            except Exception as e:
                raise Exception(f"Params ({num_groups}, {num_agents_per_group})") from e

def test_gathering_env():
    _test_create_with_config_class(GatheringConfig)
    _test_interact_with_config_class(GatheringConfig)

def test_obscured_gathering_env():
    _test_create_with_config_class(ObscuredGatheringConfig)
    _test_interact_with_config_class(ObscuredGatheringConfig)

def test_exclusive_gathering_env():
    _test_create_with_config_class(ExclusiveGatheringConfig)
    _test_interact_with_config_class(ExclusiveGatheringConfig)

def test_exclusive_and_obscured_env():
    _test_create_with_config_class(ObscuredAndExclusiveGatheringConfig)
    _test_interact_with_config_class(ObscuredAndExclusiveGatheringConfig)

def test_building_gathering_env():
    _test_create_with_config_class(BuildingGatheringConfig)
    _test_interact_with_config_class(BuildingGatheringConfig)

