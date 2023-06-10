import marlben
from os import path as osp
from .config import BossFightConfig

"""
A two-agent environment where the goal is to eliminate one strong NPC. 
Alone, no single agent can deal with NPCs, so achieving the goal requires coordination from the agents. 
A separate difficulty lies in the fact that the agents need to take damage in turn for mutual survival. 
Otherwise, the agent who takes all the damage will run out of health points earlier than the NPC.

Implementation details are located in config file
"""
class BossFight(marlben.Env):
    def __init__(self, config=None):
        if config is None:
            config = BossFightConfig()
        config.PATH_MAPS = osp.join(osp.abspath(osp.dirname(__file__)), "../../envs/boss_fight/maps")
        super().__init__(config)

    def step(self, actions):
        obs, rewards, dones, infos = super().step(actions)
        if self._done():
            for k in dones:
                dones[k] = True
        return obs, rewards, dones, infos

    def _done(self):
        return len(self.realm.entity_group_manager.npc_groups[0].dead) > 0
