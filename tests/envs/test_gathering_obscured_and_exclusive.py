from .utils import _test_create_with_config_class, _test_interact_with_config_class
from nmmo.envs import GatheringObscuredAndExclusive, ObscuredAndExclusiveGatheringConfig


def test_gathering_obscure_and_exclusive_env():
    _test_create_with_config_class(GatheringObscuredAndExclusive, ObscuredAndExclusiveGatheringConfig)
    _test_interact_with_config_class(GatheringObscuredAndExclusive, ObscuredAndExclusiveGatheringConfig)

    class TestConfig(ObscuredAndExclusiveGatheringConfig):
        def __init__(self, n_groups, agents_per_group):
            super().__init__(n_groups, agents_per_group, tiles_per_agent=128)

    _test_create_with_config_class(GatheringObscuredAndExclusive, TestConfig)
    _test_interact_with_config_class(GatheringObscuredAndExclusive, TestConfig)
