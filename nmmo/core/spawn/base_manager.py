from collections.abc import Mapping

import numpy as np

import nmmo
from nmmo.core.spawn.spawn_system import SpawnFactory
from nmmo.entity import Player
from nmmo.entity.npc import NPC
from nmmo.lib import colors


class EntityGroup(Mapping):
    def __init__(self, config, realm):
        self.dataframe = realm.dataframe
        self.config = config

        self.entities = {}
        self.dead = {}

    def __len__(self):
        return len(self.entities)

    def __contains__(self, e):
        return e in self.entities

    def __getitem__(self, key):
        return self.entities[key]

    def __iter__(self):
        yield from self.entities

    def items(self):
        return self.entities.items()

    @property
    def corporeal(self):
        return {**self.entities, **self.dead}

    @property
    def packet(self):
        return {k: v.packet() for k, v in self.corporeal.items()}

    def reset(self):
        for entID, ent in self.entities.items():
            self.dataframe.remove(Serialized.Entity, entID, ent.pos)

        self.spawned = False
        self.entities = {}
        self.dead = {}

    def add(iden, entity):
        assert iden not in self.entities
        self.entities[iden] = entity

    def remove(iden):
        assert iden in self.entities
        del self.entities[iden]

    def spawn(self, entity):
        pos, entID = entity.pos, entity.entID
        self.realm.map.tiles[pos].addEnt(entity)
        self.entities[entID] = entity

    def cull(self):
        self.dead = {}
        for entID in list(self.entities):
            player = self.entities[entID]
            if not player.alive:
                r, c = player.base.pos
                entID = player.entID
                self.dead[entID] = player

                self.realm.map.tiles[r, c].delEnt(entID)
                del self.entities[entID]
                self.realm.dataframe.remove(
                    Serialized.Entity, entID, player.pos)

        return self.dead

    def update(self, actions):
        for entID, entity in self.entities.items():
            entity.update(self.realm, actions)


class NPCManager(EntityGroup):
    def __init__(self, config, realm):
        super().__init__(config, realm)
        self.realm = realm

    def reset(self):
        super().reset()
        self.idx = -1

    def spawn(self):
        if not self.config.game_system_enabled('NPC'):
            return

        for _ in range(self.config.NPC_SPAWN_ATTEMPTS):
            if len(self.entities) >= self.config.NMOB:
                break

            center = self.config.TERRAIN_CENTER
            border = self.config.TERRAIN_BORDER
            r, c = np.random.randint(border, center+border, 2).tolist()
            if self.realm.map.tiles[r, c].occupied:
                continue

            npc = NPC.spawn(self.realm, (r, c), self.idx)
            if npc:
                super().spawn(npc)
                self.idx -= 1

    def actions(self, realm):
        actions = {}
        for idx, entity in self.entities.items():
            actions[idx] = entity.decide(realm)
        return actions


class PlayerManager(EntityGroup):
    def __init__(self, config, realm):
        super().__init__(config, realm)

        self.loader = config.AGENT_LOADER
        self.palette = colors.Palette()
        self.realm = realm
        spawn_type = config.SPAWN_PARAMS['type']
        self.spawn_func = SpawnFactory.get_spawn_system(spawn_type)

    def spawn(self):
        self.spawn_func(self, self.config, self.realm)

    def reset(self):
        super().reset()
        self.agents = self.loader(self.config)
        self.idx = 1

    def spawnIndividual(self, r, c):
        pop, agent = next(self.agents)
        agent = agent(self.config, self.idx)
        player = Player(self.realm, (r, c), agent,
                        self.palette.color(pop), pop)
        super().spawn(player)
        self.idx += 1
