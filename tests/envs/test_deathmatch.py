from marlben.envs import DeathmatchConfig
from marlben.envs import Deathmatch
from .utils import _test_create_with_config_class, _test_interact_with_config_class


"""
A load testcase. Checks creating an environment with different parameters and random interactions.
Helps to find raising exceptions and check computational resources load.
"""

def test_deathmatch_env():
    _test_create_with_config_class(Deathmatch, DeathmatchConfig)
    _test_interact_with_config_class(Deathmatch, DeathmatchConfig)