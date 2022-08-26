import nmmo
from os import path as osp


class BossFight(nmmo.Env):
    def __init__(self, config):
        config.PATH_MAPS = osp.join(osp.abspath(osp.dirname(__file__)), "maps")
        super().__init__(config)

    def step(self, actions):
        obs, rewards, dones, infos = super().step(actions)
        if self._done():
            for k in dones:
                dones[k] = True
        return obs, rewards, dones, infos

    def _done(self):
        return len(self.realm.entity_group_manager.npc_groups[0].dead) > 0