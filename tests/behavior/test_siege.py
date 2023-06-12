from marlben.envs import SiegeConfigScripted
from marlben.envs import Siege
from tests.behavior.utils import _test_helper


def test_siege_scripted():
    cfg_args = {"n_groups": 2, "agents_per_group": 1}
    _test_helper(env_class=Siege, cfg_class=SiegeConfigScripted, cfg_args=cfg_args)