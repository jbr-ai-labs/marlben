from nmmo.envs import Corridor, CorridorConfig
from tests.envs.utils import create_env


def test_pettingzoo_api():
    env = create_env(Corridor, CorridorConfig())
    # TODO fix infinite import time
    # from pettingzoo.test import parallel_api_test
    #parallel_api_test(env, num_cycles=1)
