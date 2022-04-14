from src.environments import rllib_wrapper
from src.rllib_base import run_tune_experiment
from src.environments.corridor.config import corridor_config

if __name__ == '__main__':
    corridor_config.RENDER = True
    run_tune_experiment(corridor_config, 'Corridor', rllib_wrapper.PPO)
