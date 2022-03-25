from nmmo.core.realm import PlayerManager, NPCManager
from .spawn_system import SpawnFactory



class CustomPlayerManager(PlayerManager):
    def __init__(self, config, realm): 
        super().__init__(config, realm)
        spawn_type = config.SPAWN_PARAMS['type']
        self.spawn_func = SpawnFactory.get_spawn_system(spawn_type)

    def spawn(self):
        self.spawn_func(self, self.config, self.realm)

class CustomNPCManager(NPCManager):
    pass
