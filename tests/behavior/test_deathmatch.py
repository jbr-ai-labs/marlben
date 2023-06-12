from marlben.envs import DeathmatchConfigScripted
from marlben.envs import Deathmatch
from tests.behavior.utils import _test_helper_combat


def test_deathmatch_scripted():
    cfg_args = {"n_groups": 2, "agents_per_group": 1}
    _test_helper_combat(env_class=Deathmatch, cfg_class=DeathmatchConfigScripted, cfg_args=cfg_args)
