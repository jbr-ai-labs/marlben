from .utils import _test_create_with_config_class, _test_interact_with_config_class
from nmmo.envs import GatheringExclusive, ExclusiveGatheringConfig


def test_gathering_exclusive_env():
    _test_create_with_config_class(GatheringExclusive, ExclusiveGatheringConfig)
    _test_interact_with_config_class(GatheringExclusive, ExclusiveGatheringConfig)
