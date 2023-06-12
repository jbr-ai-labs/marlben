from .utils import _test_helper


from marlben.envs import GatheringBuilding, BuildingGatheringConfigScripted

def test_gathering_building_scripted():
    cfg_args = {"n_groups": 2, "agents_per_group": 1}
    _test_helper(env_class=GatheringBuilding, cfg_class=BuildingGatheringConfigScripted, cfg_args=cfg_args)
