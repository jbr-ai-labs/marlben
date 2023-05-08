from nmmo.envs.predator_prey import PredatorPrey
from nmmo.envs.predator_prey.config import PredatorPreyConfig
from tests.envs.utils import _test_create_with_config_class, _test_interact_with_config_class


def test_predator_prey_env():
    _test_create_with_config_class(PredatorPrey, PredatorPreyConfig)
    _test_interact_with_config_class(PredatorPrey, PredatorPreyConfig)
