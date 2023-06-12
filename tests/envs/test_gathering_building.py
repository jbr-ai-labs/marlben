from .utils import _test_create_with_config_class, _test_interact_with_config_class
from marlben.envs import GatheringBuilding, BuildingGatheringConfig


def test_gathering_building_env():
    _test_create_with_config_class(GatheringBuilding, BuildingGatheringConfig)
    _test_interact_with_config_class(GatheringBuilding, BuildingGatheringConfig)

    class TestConfig(BuildingGatheringConfig):
        def __init__(self, n_groups, agents_per_group):
            super().__init__(n_groups, agents_per_group, tiles_per_agent=128)

    _test_create_with_config_class(GatheringBuilding, TestConfig)
    _test_interact_with_config_class(GatheringBuilding, TestConfig)
