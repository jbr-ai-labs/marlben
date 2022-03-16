from nmmo.core import Realm
from nmmo import core, infrastructure
from nmmo.core.realm import PlayerManager, NPCManager
from .spawn_system import spawn_factory



class CustomPlayerManager(PlayerManager):
    def __init__(self, config, realm): 
        super().__init__(config, realm)
        self.spawn_func = spawn_factory(config.SPAWN_PARAMS['type'])

    def spawn(self):
        self.spawn_func(self, self.config, self.realm)

class CustomNPCManager(NPCManager):
    pass
