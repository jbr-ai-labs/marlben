from marlben.envs import PveConfigScripted
from marlben.envs import Pve
from tests.behavior.utils import _test_helper


def test_pve_scripted():
    cfg_args = {"n_groups": 2, "agents_per_group": 1}
    _test_helper(env_class=Pve, cfg_class=PveConfigScripted, cfg_args=cfg_args)