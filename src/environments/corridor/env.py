import nmmo


class Corridor(nmmo.Env):
    def __init__(self, config):
        super().__init__(config)
    
    def step(self, actions):
        return super().step(actions)
