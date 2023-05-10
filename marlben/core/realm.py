from collections import defaultdict
from typing import Dict
from marlben.core.spawn.base_manager import GroupsManager
from marlben import core, infrastructure


def prioritized(entities: Dict, merged: Dict):
    """Sort actions into merged according to priority"""
    for idx, actions in entities.items():
        for atn, args in actions.items():
            merged[atn.priority].append(
                (idx, (atn, dict([(k.arg_name, v) for k, v in args.items()]))))
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
        self.entity_group_manager = GroupsManager(config, self)

    def reset(self, idx):
        '''Reset the environment and load the specified map
      Args:
         idx: Map index to load
      '''
        print('----reset----')
        self.map.reset(self, idx)
        self.entity_group_manager.reset()
        self.tick = 0

    def packet(self):
        '''Client packet'''
        npc, player = self.entity_group_manager.packet
        return {'environment': self.map.repr,
                'resource': self.map.packet,
                'player': player,
                'npc': npc}

    @property
    def population(self):
        '''Number of player agents'''
        return self.entity_group_manager.players_count()

    def entity(self, entID):
        '''Get entity by ID'''
        return self.entity_group_manager.get_entity_by_id(entID)

    def players(self):
        players = []
        for player_group in self.entity_group_manager.player_groups:
            players.extend(player_group.entities.items())
        return players

    def agents(self):
        agents = []
        for player_group in self.entity_group_manager.player_groups:
            agents.extend(player_group.entities.keys())
        return agents

    def step(self, actions):
        '''Run game logic for one tick

        Args:
            actions: Dict of agent actions
        '''

        actions = self.entity_group_manager.mask_player_actions(actions)
        # Prioritize actions
        npcActions = self.entity_group_manager.get_npc_actions()
        merged = defaultdict(list)
        prioritized(actions, merged)
        prioritized(npcActions, merged)
        # Update entities and perform actions

        total_actions = dict()
        total_actions.update(actions)
        total_actions.update(npcActions)
        self.entity_group_manager.update(total_actions)

        # Execute actions
        for priority in sorted(merged):
            for entID, (atn, args) in merged[priority]:
                ent = self.entity(entID)
                atn.call(self, ent, **args)

        # Spawn new agent and cull dead ones
        # TODO: Place cull before spawn once PettingZoo API fixes respawn on same tick as death bug
        self.entity_group_manager.spawn()

        dead = self.entity_group_manager.cull()
        self.entity_group_manager.update_diary()

        # Update map
        self.map.step()
        self.tick += 1

        return dead
