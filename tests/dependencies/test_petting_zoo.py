from marlben.envs import Corridor, CorridorConfig
from pettingzoo.test import parallel_api_test
from tests.envs.utils import create_env


def test_pettingzoo_api():
    env = create_env(Corridor, CorridorConfig())
    parallel_api_test(env, num_cycles=1000)
