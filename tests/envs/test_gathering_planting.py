from .utils import _test_create_with_config_class, _test_interact_with_config_class
from nmmo.envs import GatheringPlanting, PlantingGatheringConfig


def test_gathering_planting_env():
    _test_create_with_config_class(GatheringPlanting, PlantingGatheringConfig)
    _test_interact_with_config_class(GatheringPlanting, PlantingGatheringConfig)
