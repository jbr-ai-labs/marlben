from nmmo.core.spawn.base_manager import PlayerManager, NPCManager
from nmmo.core.spawn.spawn_system import SpawnFactory


class CustomPlayerManager(PlayerManager):
    def __init__(self, config, realm):
        super().__init__(config, realm)
        self.spawn_type = config.SPAWN_PARAMS['type']
        self.spawn_func = SpawnFactory.get_spawn_system(self.spawn_type)

    def spawn(self):
        self.spawn_func(self, self.config, self.realm)


class CustomNPCManager(NPCManager):
    pass
