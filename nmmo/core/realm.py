from collections import defaultdict
from typing import Dict
from nmmo.core.spawn.base_manager import NPCManager, PlayerManager
from nmmo import core, infrastructure


def prioritized(entities: Dict, merged: Dict):
    """Sort actions into merged according to priority"""
    for idx, actions in entities.items():
        for atn, args in actions.items():
            merged[atn.priority].append((idx, (atn, dict([(k.arg_name, v) for k, v in args.items()]))))
    return merged


class Realm:
    """Top-level world object"""

    def __init__(self, config):
        self.config = config

        # Generate maps if they do not exist
        config.MAP_GENERATOR(config).generate_all_maps()

        # Load the world file
        self.dataframe = infrastructure.Dataframe(config)
        self.map = core.Map(config, self)

        # Entity handlers
        self.players = PlayerManager(config, self)
        self.npcs = NPCManager(config, self)

    def reset(self, idx):
        '''Reset the environment and load the specified map
      Args:
         idx: Map index to load
      '''
        print('----reset----')
        self.map.reset(self, idx)
        self.players.reset()
        self.npcs.reset()
        self.tick = 0

    def packet(self):
        '''Client packet'''
        return {'environment': self.map.repr,
                'resource': self.map.packet,
                'player': self.players.packet,
                'npc': self.npcs.packet}

    @property
    def population(self):
        '''Number of player agents'''
        return len(self.players.entities)

    def entity(self, entID):
        '''Get entity by ID'''
        if entID < 0:
            return self.npcs[entID]
        else:
            return self.players[entID]

    def step(self, actions):
        '''Run game logic for one tick
      
        Args:
            actions: Dict of agent actions
        '''
        # Prioritize actions
        npcActions = self.npcs.actions(self)
        merged = defaultdict(list)
        prioritized(actions, merged)
        prioritized(npcActions, merged)
        # Update entities and perform actions
        self.players.update(actions)
        self.npcs.update(npcActions)

        # Execute actions
        for priority in sorted(merged):
            for entID, (atn, args) in merged[priority]:
                ent = self.entity(entID)
                atn.call(self, ent, **args)

        # Spawn new agent and cull dead ones
        # TODO: Place cull before spawn once PettingZoo API fixes respawn on same tick as death bug
        self.players.spawn()
        self.npcs.spawn()

        dead = self.players.cull()
        self.npcs.cull()

        # Update map
        self.map.step()
        self.tick += 1

        return dead
