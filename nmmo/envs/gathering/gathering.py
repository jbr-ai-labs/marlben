from nmmo.config import Resource, Small, Building

HORIZON = 70


class GatheringConfig(Small, Resource):
    TRAIN_HORIZON = HORIZON
    EVAL_HORIZON = HORIZON


class GatheringBuildingConfig(Small, Resource, Building):
    TRAIN_HORIZON = HORIZON
    EVAL_HORIZON = HORIZON
