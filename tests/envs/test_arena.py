from marlben.envs import ArenaConfig
from marlben.envs import Arena
from tests.envs.utils import _test_create_with_config_class, _test_interact_with_config_class


def test_gathering_env():
    _test_create_with_config_class(Arena, ArenaConfig)
    _test_interact_with_config_class(Arena, ArenaConfig)