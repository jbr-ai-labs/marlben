from .utils import _test_create_with_config_class, _test_interact_with_config_class
from marlben.envs import Pve, PveConfig


def test_siege_env():
    _test_create_with_config_class(Pve, PveConfig)
    _test_interact_with_config_class(Pve, PveConfig)
