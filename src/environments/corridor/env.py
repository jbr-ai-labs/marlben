import nmmo


class Corridor(nmmo.Env):
    def __init__(self, config):
        super().__init__(config)
    
    def reward(self, agent):
        info = {"population": player.pop}

        if player.entID not in self.realm.players:
            return self.config.INDIVIDUAL_DEATH_PENALTY, info
        if self.realm.tick >= self.config.HORIZON:
            return self.config.INDIVIDUAL_SURVIVAL_REWARD, info
        return 0, info
    
    def common_reward(self):
        if len(self.realm.players) == 0:
            return self.config.COMMON_DEATH_PENALTY
        if len(self.realm.players) == 2 and self.realm.tick >= self.config.HORIZON:
            return self.config.COMMON_SURVIVAL_REWARD
        return 0
    
    def step(self, actions):
        obs, rewards, dones, infos = super().step(actions)
        # reward["common"] = self.common_reward() # TODO: put it somewhere so that nothing breaks
        return obs, rewards, dones, infos

