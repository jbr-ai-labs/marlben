from marlben.envs.raid.config import BossRaidConfig
from marlben.envs.raid.env import Raid
from marlben.scripted.environments.bossfight import BossFightTankAgent, BossRaidHealerAgent

"""
A simple way to modify your environment config by inheriting from the base config.
This method is highly recommended as such inherited configs are supported by third-party libraries such as RLLib.
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