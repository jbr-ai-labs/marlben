from .utils import _test_create_with_config_class, _test_interact_with_config_class
from marlben.envs import GatheringExclusive, ExclusiveGatheringConfig


def test_gathering_exclusive_env():
    _test_create_with_config_class(GatheringExclusive, ExclusiveGatheringConfig)
    _test_interact_with_config_class(GatheringExclusive, ExclusiveGatheringConfig)

    class TestConfig(ExclusiveGatheringConfig):
        def __init__(self, n_groups, agents_per_group):
            super().__init__(n_groups, agents_per_group, tiles_per_agent=128)

    _test_create_with_config_class(GatheringExclusive, TestConfig)
    _test_interact_with_config_class(GatheringExclusive, TestConfig)