import marlben
from os import path as osp
from .config import BossRaidConfig

"""
A variant of the Boss Fight environment with more agents and more resilient NPCs, requiring a greater degree of coordination as a result.
Besides Tank class, there are also Healer and Fighter classes for agent, which makes the coordination much more difficult since each agent has it's own role and set of actions.

Implementation details are located in config file
"""
class Raid(marlben.Env):
    def __init__(self, config=None):
        if config is None:
            config = BossRaidConfig()
        config.PATH_MAPS = osp.join(osp.abspath(osp.dirname(__file__)), "../../envs/raid/maps")
        super().__init__(config)

    def step(self, actions):
        obs, rewards, dones, infos = super().step(actions)
        if self._done():
            for k in dones:
                dones[k] = True
        return obs, rewards, dones, infos

    def _done(self):
        return len(self.realm.entity_group_manager.npc_groups[0].dead) > 0
