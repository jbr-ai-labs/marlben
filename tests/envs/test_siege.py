from .utils import _test_create_with_config_class, _test_interact_with_config_class
from marlben.envs import Siege, SiegeConfig


def test_siege_env():
    _test_create_with_config_class(Siege, SiegeConfig)
    _test_interact_with_config_class(Siege, SiegeConfig)
