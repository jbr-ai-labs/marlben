from src.environments import rllib_wrapper
from src.rllib_base import run_tune_experiment
from src.config import get_config


if __name__ == '__main__':
    EnvConfig = get_config("Gathering")

    run_tune_experiment(EnvConfig(), 'Gathering', rllib_wrapper.PPO)
