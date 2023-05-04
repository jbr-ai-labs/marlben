from .utils import _test_helper


from nmmo.envs import Gathering, GatheringConfigScripted

def test_gathering_scripted():
    cfg_args = {"n_groups": 2, "agents_per_group": 1}
    _test_helper(env_class=Gathering, cfg_class=GatheringConfigScripted, cfg_args=cfg_args)
