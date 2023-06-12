from .utils import _test_create_with_config_class, _test_interact_with_config_class
from marlben.envs import Gathering, GatheringConfig

"""
A load testcase. Checks creating an environment with different parameters and random interactions.
Helps to find raising exceptions and check computational resources load.
"""

def test_gathering_env():
    _test_create_with_config_class(Gathering, GatheringConfig)
    _test_interact_with_config_class(Gathering, GatheringConfig)

    class TestConfig(GatheringConfig):
        def __init__(self, n_groups, agents_per_group):
            super().__init__(n_groups, agents_per_group, tiles_per_agent=128)

    _test_create_with_config_class(Gathering, TestConfig)
    _test_interact_with_config_class(Gathering, TestConfig)
