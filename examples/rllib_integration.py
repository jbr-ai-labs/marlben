from marlben.rllib import rllib_wrapper
from marlben.rllib.rllib_base import run_tune_experiment
from marlben.rllib.config.get_config import get_config

"""
An example showing how to train your algorithm using RLLib.
"""

if __name__ == '__main__':
    EnvConfig = get_config("Corridor")

    run_tune_experiment(EnvConfig(), 'Corridor', rllib_wrapper.PPOCustom)
