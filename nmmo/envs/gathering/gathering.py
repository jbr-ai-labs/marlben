from nmmo.config import Resource, Small

HORIZON = 70


class GatheringConfig(Small, Resource):
    TRAIN_HORIZON = HORIZON
    EVAL_HORIZON = HORIZON
