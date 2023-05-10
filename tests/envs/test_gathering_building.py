from .utils import _test_create_with_config_class, _test_interact_with_config_class
from marlben.envs import GatheringBuilding, BuildingGatheringConfig


def test_gathering_building_env():
    _test_create_with_config_class(GatheringBuilding, BuildingGatheringConfig)
    _test_interact_with_config_class(GatheringBuilding, BuildingGatheringConfig)
