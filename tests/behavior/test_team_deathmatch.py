from marlben.envs import TeamDeathmatchConfigScripted
from marlben.envs import TeamDeathmatch
from tests.behavior.utils import _test_helper_combat


def test_teamdeathmatch_scripted():
    cfg_args = {"n_groups": 2, "agents_per_group": 1}
    _test_helper_combat(env_class=TeamDeathmatch, cfg_class=TeamDeathmatchConfigScripted, cfg_args=cfg_args)
