from rllib import rllib_wrapper
from rllib.rllib_base import run_tune_experiment
from config import get_config


if __name__ == '__main__':
    EnvConfig = get_config("CorridorScripted")

    run_tune_experiment(EnvConfig(), 'Corridor', rllib_wrapper.PPO)
