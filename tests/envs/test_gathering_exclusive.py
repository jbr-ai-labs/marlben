from .utils import _test_create_with_config_class, _test_interact_with_config_class
from marlben.envs import GatheringExclusive, ExclusiveGatheringConfig

"""
A load testcase. Checks creating an environment with different parameters and random interactions.
Helps to find raising exceptions and check computational resources load.
"""

def test_gathering_exclusive_env():
    _test_create_with_config_class(GatheringExclusive, ExclusiveGatheringConfig)
    _test_interact_with_config_class(GatheringExclusive, ExclusiveGatheringConfig)