from pettingzoo.test import parallel_api_test

import nmmo


def test_pettingzoo_api():
    env = nmmo.Env()
    parallel_api_test(env, num_cycles=2000)
