from .utils import _test_create_with_config_class, _test_interact_with_config_class
from nmmo.envs import GatheringObscured, ObscuredGatheringConfig


def test_gathering_obscured_env():
    _test_create_with_config_class(GatheringObscured, ObscuredGatheringConfig)
    _test_interact_with_config_class(GatheringObscured, ObscuredGatheringConfig)

    class TestConfig(ObscuredGatheringConfig):
        def __init__(self, n_groups, agents_per_group):
            super().__init__(n_groups, agents_per_group, tiles_per_agent=128)

    _test_create_with_config_class(GatheringObscured, TestConfig)
    _test_interact_with_config_class(GatheringObscured, TestConfig)
