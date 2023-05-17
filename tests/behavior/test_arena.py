from marlben.envs import ArenaConfigScripted
from marlben.envs import Arena
from tests.behavior.utils import _test_helper_combat


def test_arena_scripted():
    cfg_args = {"n_groups": 2, "agents_per_group": 1}
    _test_helper_combat(env_class=Arena, cfg_class=ArenaConfigScripted, cfg_args=cfg_args)
