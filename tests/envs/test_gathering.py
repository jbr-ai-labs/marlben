from .utils import _test_create_with_config_class, _test_interact_with_config_class
from marlben.envs import Gathering, GatheringConfig


def test_gathering_env():
    _test_create_with_config_class(Gathering, GatheringConfig)
    _test_interact_with_config_class(Gathering, GatheringConfig)
