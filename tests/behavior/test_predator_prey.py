from marlben.envs import PredatorPreyConfigScripted
from marlben.envs import PredatorPrey
from tests.behavior.utils import _test_helper_combat


def test_predator_prey_scripted():
    cfg_args = {"n_groups": 2, "agents_per_group": 1}
    _test_helper_combat(env_class=PredatorPrey, cfg_class=PredatorPreyConfigScripted, cfg_args=cfg_args)
