from src.environments import rllib_wrapper
from src.rllib_base import run_tune_experiment
from src.core.config import get_config



if __name__ == '__main__':
    corridor_config = get_config("./src/environments/corridor/config.json")
    corridor_config.RENDER = True
    run_tune_experiment(corridor_config, 'Corridor', rllib_wrapper.PPO)
