from src.environments import rllib_wrapper
from src.rllib_base import run_tune_experiment
from nmmo import Agent
from nmmo.config import get_config

from config.bases import Small
from config.scale import Debug


if __name__ == '__main__':
    EnvConfig = get_config("CorridorScripted")
    class Cfg(EnvConfig, Small, Debug):
        RENDER = True

    run_tune_experiment(Cfg(), 'Corridor', rllib_wrapper.PPO)
