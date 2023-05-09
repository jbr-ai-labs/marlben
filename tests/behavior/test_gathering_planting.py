from .utils import _test_helper


from nmmo.envs import GatheringPlanting, PlantingGatheringConfigScripted

def test_gathering_planting_scripted():
    cfg_args = {"n_groups": 2, "agents_per_group": 1}
    _test_helper(env_class=GatheringPlanting, cfg_class=PlantingGatheringConfigScripted, cfg_args=cfg_args)
