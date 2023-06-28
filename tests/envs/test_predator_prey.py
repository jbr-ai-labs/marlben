from marlben.envs.predator_prey import PredatorPrey
from marlben.envs.predator_prey.config import PredatorPreyConfig
from tests.envs.utils import _test_create_with_config_class, _test_interact_with_config_class

"""
A load testcase. Checks creating an environment with different parameters and random interactions.
Helps to find raising exceptions and check computational resources load.
"""

def test_predator_prey_env():
    _test_create_with_config_class(PredatorPrey, PredatorPreyConfig)
    _test_interact_with_config_class(PredatorPrey, PredatorPreyConfig)
