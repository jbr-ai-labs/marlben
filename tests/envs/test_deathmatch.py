from nmmo.envs.deathmatch.config import DeathmatchConfig
from nmmo.envs.deathmatch.env import Deathmatch
from tests.envs.utils import _test_create_with_config_class, _test_interact_with_config_class


def test_deathmatch_env():
    _test_create_with_config_class(Deathmatch, DeathmatchConfig)
    _test_interact_with_config_class(Deathmatch, DeathmatchConfig)