import random
from collections.abc import Mapping

import numpy as np

from nmmo import Serialized
from nmmo.core.spawn.spawn_system import SpawnFactory
from nmmo.entity import Player
from nmmo.entity.npc import NPC
from nmmo.lib import colors
from nmmo.io.action import Attack, Style, Melee, Range, Mage, Heal
import copy


class _IdCounter:
    def __init__(self):
        self.reset()

    def reset(self):
        self.npc_id = 0
        self.player_id = 0

    def next_npc_id(self):
        self.npc_id -= 1
        return self.npc_id

    def next_player_id(self):
        self.player_id += 1
        return self.player_id


class GroupsManager:
    def __init__(self, config, realm):
        self.realm = realm
        self.config = config
        self.id_counter = _IdCounter()

        self.npc_groups = [
            NPCGroup(config, realm, npc_group_config, self.id_counter)
            for npc_group_config in self.config.NPC_GROUPS
        ]
        self.player_groups = [
            PlayerGroup(config, realm, player_group_config, self.id_counter, i)
            for i, player_group_config in enumerate(self.config.PLAYER_GROUPS)
        ]

    def spawn(self):
        for npc_group in self.npc_groups:
            npc_group.spawn()
        for player_group in self.player_groups:
            player_group.spawn()

    def reset(self):
        self.id_counter.reset()
        for npc_group in self.npc_groups:
            npc_group.reset()
        for player_group in self.player_groups:
            player_group.reset()

    def get_npc_actions(self):
        actions = {}
        for npc_group in self.npc_groups:
            actions.update(npc_group.actions())
        return actions

    def get_entity_by_id(self, id):
        if id < 0:
            for npc_group in self.npc_groups:
                if id in npc_group.entities:
                    return npc_group[id]
        else:
            for player_group in self.player_groups:
                if id in player_group.entities:
                    return player_group[id]
        return None

    @property
    def packet(self):
        npc_packet = [npc_group.packet for npc_group in self.npc_groups]
        player_packet = [player_group.packet for player_group in self.player_groups]
        return self.merge_packets(npc_packet), self.merge_packets(player_packet)
    
    def merge_packets(self, packets):
        result = {}
        for packet in packets:
            result.update(packet)
        return result

    def update(self, actions):
        for npc_group in self.npc_groups:
            npc_group.update(actions)
        for player_group in self.player_groups:
            player_group.update(actions)

    def update_diary(self):
        for player_group in self.player_groups:
            player_group.update_diary()

    def players_count(self):
        count = 0
        for player_group in self.player_groups:
            count += len(player_group.entities)
        return count

    def mask_player_actions(self, actions: dict):
        result = {}
        for i, action in actions.items():
            for player_group in self.player_groups:
                if i in player_group.entities:
                    result[i] = player_group.mask_action(action)
                    break
        return result

    def cull(self):
        dead = {}
        for npc_group in self.npc_groups:
            npc_group.cull()
        for player_group in self.player_groups:
            dead.update(player_group.cull())
        return dead


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


class NPCGroup(EntityGroup):
    def __init__(self, config, realm, group_config, id_counter):
        super().__init__(config, realm)
        self.realm = realm
        self.group_config = group_config
        self.coordinate_sampler = self.group_config.SPAWN_COORDINATES_SAMPLER
        self.skills_sampler = self.group_config.SPAWN_SKILLS_SAMPLER
        self.id_counter = id_counter
        self.available_styles = list({Melee, Range, Mage}.difference(
            set(group_config.BANNED_ATTACK_STYLES)))

    def spawn(self):
        if not self.config.game_system_enabled('NPC'):
            return  # TODO: Move to global manager

        for _ in range(self.group_config.NENT - len(self.entities)):
            for _ in range(self.group_config.SPAWN_ATTEMPTS_PER_ENT):
                r, c = self.coordinate_sampler.get_next()
                if self.realm.map.tiles[r, c].occupied:
                    continue

                skills = self.skills_sampler.get_next((r, c))
                # TODO: Check & change
                npc = NPC.spawn(self.realm, (r, c),
                                self.id_counter.next_npc_id(), skills)
                npc.skills.style = random.choice(self.available_styles)
                if npc:
                    super().spawn(npc)
                    break

    def reset(self):
        super().reset()
        self.coordinate_sampler.reset(self.config)
        self.skills_sampler.reset(self.config)

    def actions(self):
        actions = {}
        for idx, entity in self.entities.items():
            actions[idx] = entity.decide(self.realm)
        return actions


class PlayerGroup(EntityGroup):
    def __init__(self, config, realm, group_config, id_counter, group_id):
        super().__init__(config, realm)
        print("AGENTS", config.AGENTS)
        self.group_config = group_config
        self.loader = group_config.AGENT_LOADER
        self.palette = colors.Palette()
        self.coordinate_sampler = self.group_config.SPAWN_COORDINATES_SAMPLER
        self.skills_sampler = self.group_config.SPAWN_SKILLS_SAMPLER
        self.banned_attack_styles = self.group_config.BANNED_ATTACK_STYLES
        self.realm = realm
        self.id_counter = id_counter
        self.group_id = group_id

    def spawn(self):
        if self.spawned:
            return
        self.spawned = True
        for _ in range(self.group_config.NENT - len(self.entities)):
            r_f, c_f = None, None
            for _ in range(self.group_config.SPAWN_ATTEMPTS_PER_ENT):
                r, c = self.coordinate_sampler.get_next()
                if not self.realm.map.tiles[r, c].occupied:
                    r_f, c_f = r, c
                    break

            if r_f is not None:
                pop_id, agent = next(self.agents)
                agent = agent(self.config, self.id_counter.next_player_id())
                skills = self.skills_sampler.get_next((r_f, c_f))
                player = Player(self.realm, (r_f, c_f), agent, self.palette.color(
                    self.group_id), self.group_id, skills)
                super().spawn(player)

    def update_diary(self):
        for entID, entity in self.entities.items():
            entity.update_diary(self.realm)

    def reset(self):
        super().reset()
        self.agents = self.loader(self.group_config)
        self.coordinate_sampler.reset(self.config)
        self.skills_sampler.reset(self.config)

    def mask_action(self, action: dict):
        # action = copy.deepcopy(action)
        if Attack in action:
            if action[Attack][Style] in self.banned_attack_styles:
                action.pop(Attack)
        return action