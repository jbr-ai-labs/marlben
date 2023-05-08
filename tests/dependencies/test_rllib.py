from rllib import rllib_wrapper
from rllib.config import get_config
from rllib.rllib_base import run_tune_experiment


def test_rllib_api():
    config = get_config("Corridor")()
    config.TRAINING_ITERATIONS = 1
    config.EVALUATE = False
    config.TRAIN_BATCH_SIZE = 10
    config.SGD_MINIBATCH_SIZE = 1
    config.ROLLOUT_FRAGMENT_LENGTH = 1
    config.TRAIN_HORIZON = 10
    config.EVALUATION_HORIZON = 10
    run_tune_experiment(config, 'Corridor', rllib_wrapper.PPO)
