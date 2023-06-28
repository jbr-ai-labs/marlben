from marlben.envs.raid.config import BossRaidConfig
from marlben.envs.raid.env import Raid
from scripted.environments.bossfight import BossFightTankAgent, BossRaidHealerAgent

"""
A simple example of manually overriding some of config parameters.
This way of modifying config may be useful if you want to change an environment configuration during training.
However, such way of modifying configuration is not supported by many libs such as RLLib.

Note: It's recommended to use another way to customize environment. See override_config.py for example.
"""


if __name__ == "__main__":
    config = BossRaidConfig()

    # Change reward for killing the raid boss
    config.TASKS[0].reward = 100

    # Add second raid boss
    config.NPC_GROUPS[0].NENT = 2

    # Override amount of tank agents
    config.PLAYER_GROUPS[0].NENT = 4

    # Make some of the tank agents scripted
    config.PLAYER_GROUPS[0].AGENTS.append(BossFightTankAgent)

    # Make all of the healer agents scripted
    config.PLAYER_GROUPS[2].AGENTS[0] = BossRaidHealerAgent

    # Create an environment
    env = Raid(config)