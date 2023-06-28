from marlben.envs.raid.config import BossRaidConfig
from marlben.envs.raid.env import Raid
from scripted.environments.bossfight import BossFightTankAgent, BossRaidHealerAgent

"""
A simple way to modify your environment config by inheriting from the base config.
This method is highly recommended as such inherited configs are supported by third-party libraries such as RLLib.

You may use config override functional if you are not satisfied with set of built-in environments.

For example, if you want to evaluate performance with different number of agents for a specific task, 
you may need to change some of the parameters in the environment configuration.

For an instance, it can be useful if an amount of an agents in the real environment is not known, i.e. 
different number of agents in each working space.

Even more, if you want to complicate a task for an agent or make it easier, you may do so by changing some of the config parameters.
"""


class CustomConfig(BossRaidConfig):
    def __init__(self, n_tanks=2, n_fighters=2):
        super().__init__(2*n_tanks, n_fighters, n_healers=2)

        # This changes is similar to ones in config_env.py
        self.NPC_GROUPS[0].NENT = 2
        self.TASKS[0].reward = 100
        self.PLAYER_GROUPS[0].AGENTS.append(BossFightTankAgent)
        self.PLAYER_GROUPS[2].AGENTS[0] = BossRaidHealerAgent


if __name__ == "__main__":
    config = CustomConfig()
    # Create an environment
    env = Raid(config)