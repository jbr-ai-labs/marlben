from marlben.envs import ArenaConfig
from marlben.envs import Arena
from tests.envs.utils import _test_create_with_config_class, _test_interact_with_config_class

"""
A load testcase. Checks creating an environment with different parameters and random interactions.
Helps to find raising exceptions and check computational resources load.
"""

def test_gathering_env():
    _test_create_with_config_class(Arena, ArenaConfig)
    _test_interact_with_config_class(Arena, ArenaConfig)