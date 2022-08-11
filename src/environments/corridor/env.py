import nmmo


class Corridor(nmmo.Env):
    def __init__(self, config):
        super().__init__(config)

    def step(self, actions):
        obs, rewards, dones, infos = super().step(actions)
        # reward["common"] = self.common_reward() # TODO: put it somewhere so that nothing breaks
        return obs, rewards, dones, infos
