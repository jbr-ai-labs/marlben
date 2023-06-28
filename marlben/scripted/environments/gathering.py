import copy
import random

import numpy as np

import marlben
from marlben.lib import material
from marlben.scripted import move, attack
from marlben.scripted.baselines import Scripted
from marlben.io.action import Move, Direction, East, West, South, North
from marlben import scripting

class GatheringAgent(Scripted):
    name = 'GatheringAgent_'
    '''Collects Resourses in a simple Gathering Env'''

    def __init__(self, config, idx):
        super().__init__(config, idx)

        self._current_target = "Water"
        self._forest_pos = 13
        self._water_pos = 10
        self._direction = (-1, 0)


    def _switch_direction(self, direction):
        return tuple([-1 * d for d in direction])

    def _manage_direction(self, r, c):
        if self._current_target == "Forest" and r == self._forest_pos:
            self._direction = self._switch_direction(self._direction)
            self._current_target = "Water"
        elif self._current_target == "Water" and r == self._water_pos:
            self._direction = self._switch_direction(self._direction)
            self._current_target = "Forest"

    def gather_actions(self):
        agent = self.ob.agent
        Entity = marlben.Serialized.Entity

        r = marlben.scripting.Observation.attribute(agent, Entity.R)
        c = marlben.scripting.Observation.attribute(agent, Entity.C)
        self._manage_direction(r, c)
        direction = move.towards(self._direction)
        self.actions[marlben.action.Move] = {marlben.action.Direction: direction}
        return self.actions

    def attack_actions(self, npc_only=True):
        self.scan_agents(npc_only=npc_only)
        if self.closest is not None:
            self.target = self.closest
            self.targetID = self.closestID
            self.targetDist = self.closestDist
        self.style = marlben.action.Melee
        self.attack()
        return self.actions

    def __call__(self, obs):
        super().__call__(obs)
        return self.gather_actions()


class GatheringBuildingAgent(GatheringAgent):
    def __init__(self, config, idx):
        super().__init__(config, idx)

        self._building_finished = False
        self._building_target_num = 0
        self._building_targets = [13, 10]
        self._need_building = False
        self._sidestep = -(self.iden % 2 * 2 - 1)

    def build_actions(self):
        agent = self.ob.agent
        Entity = marlben.Serialized.Entity
        r = marlben.scripting.Observation.attribute(agent, Entity.R)
        building = self._need_building

        if self._building_target_num < len(self._building_targets):
            target = self._building_targets[self._building_target_num]
            direction = target - r
            if direction == 0:
                self._building_target_num += 1
                direction = (0, -self._sidestep)
                direction = move.towards(direction)
                self._sidestep *= -1
            else:
                direction = int(direction / abs(direction))
                direction = move.towards((direction, 0))

        self._need_building = self._building_target_num > 0

        self.actions[marlben.action.Move] = {marlben.action.Direction: direction}
        self.actions[marlben.action.Build] = {marlben.action.BuildDecision: building}

        self._building_finished = self._building_target_num > 1

        return self.actions

    def __call__(self, obs):
        super().__call__(obs)
        if not self._building_finished:
            return self.build_actions()
        return self.gather_actions()


class ObscuredAndExclusiveGatheringAgent(Scripted):
    def __init__(self, config, idx):
        super().__init__(config, idx)
        self.known_water_sources = set()
        self.known_food_sources = set()
        self.forbidden_water_sources = set()
        self.forbidden_food_sources = set()
        self.doubtful_food_sources = set()
        self.doubtful_water_sources = set()

        self.unexplored = set([
            (r + self.config.TERRAIN_BORDER, c + self.config.TERRAIN_BORDER)
            for r in range(self.config.MAP_HEIGHT)
            for c in range(self.config.MAP_WIDTH)
        ])
        self.unvisited = set([
            (r + self.config.TERRAIN_BORDER, c + self.config.TERRAIN_BORDER)
            for r in range(self.config.MAP_HEIGHT)
            for c in range(self.config.MAP_WIDTH)
        ])
        self.resource_cooldowns = {}

        self.exploration_target = None
        self.prev_adjacent_tiles = None
        self.water_prev = None
        self.food_prev = None

    def explore(self):
        if (self.exploration_target is None or
            random.random() < ((len(self.unexplored) / (self.config.MAP_WIDTH * self.config.MAP_HEIGHT))**2) / 2 or
            abs(self.exploration_target[0] - self.currR) + abs(self.exploration_target[1] - self.currC) < self.config.NSTIM
        ):
            if len(self.unexplored) > 0:
                self.exploration_target = random.sample(self.unexplored, 1)[0]
            elif len(self.unvisited) > 0:
                self.exploration_target = random.sample(self.unvisited, 1)[0]

        move.pathfind(self.config, self.ob, self.actions,
                      self.exploration_target[0] - self.currR,
                      self.exploration_target[1] - self.currC)

    def __call__(self, obs):
        super().__call__(obs)

        for key in copy.deepcopy(set(self.resource_cooldowns.keys())):
            self.resource_cooldowns[key] -= 1
            if self.resource_cooldowns[key] <= 0:
                self.resource_cooldowns.pop(key)

        Tile = marlben.Serialized.Tile
        for tile in self.ob.tiles:
            coords = (round(marlben.scripting.Observation.attribute(tile, Tile.R)),
                      round(marlben.scripting.Observation.attribute(tile, Tile.C)))
            if coords in self.unexplored:
                self.unexplored.discard(coords)

            if marlben.scripting.Observation.attribute(tile, Tile.Index) != material.Grass.index:
                self.unvisited.discard(coords)

        coords = (self.currR, self.currC)
        self.unvisited.discard(coords)

        self._update_resources_register()
        resources_to_check = []

        if self.food < 3 * self.food_max / 4 and len(self.known_food_sources) > 0:
            # Go grab something to eat
            resources_to_check.append((self.food / self.food_max, self.known_food_sources))

        if self.water < 3 * self.water_max / 4 and len(self.known_water_sources) > 0:
            # Go get some water
            resources_to_check.append((self.water / self.water_max, self.known_water_sources))

        if len(resources_to_check) > 0:
            if len(resources_to_check) == 1 or resources_to_check[0][0] > resources_to_check[1][0]:
                self._move_to_resource(resources_to_check[0][1])
            else:
                self._move_to_resource(resources_to_check[1][1])
        else:
            # Explore for more resource sources
            self.explore()
        _steps = 0
        while not self._validate_movement_action() and _steps < 5:
            self.actions[Move][Direction] = np.random.choice([East, West, South, North])
            _steps += 1
        if not self._validate_movement_action():
            self.actions = {}
        return self.actions

    def _validate_movement_action(self):
        Tile = marlben.Serialized.Tile
        Observation = marlben.scripting.Observation
        if self.actions[Move][Direction] == North and Observation.attribute(self.ob.tile(-1, 0), Tile.Index) == material.Lava.index:
            return False
        if self.actions[Move][Direction] == South and Observation.attribute(self.ob.tile(+1, 0), Tile.Index) == material.Lava.index:
            return False
        if self.actions[Move][Direction] == East and Observation.attribute(self.ob.tile(0, +1), Tile.Index) == material.Lava.index:
            return False
        if self.actions[Move][Direction] == West and Observation.attribute(self.ob.tile(0, -1), Tile.Index) == material.Lava.index:
            return False
        return True

    def _update_resources_register(self):
        adjacent_tiles = [(self.currR+1, self.currC), (self.currR, self.currC+1),
                            (self.currR-1, self.currC), (self.currR, self.currC-1)]

        # If tile with resource is obscured
        if self.water_prev is not None and self.water_prev < self.water:
            near_source = False
            for t in self.prev_adjacent_tiles[0]:
                near_source = near_source or t in self.known_water_sources
            if not near_source:
                self.known_water_sources.add((self.prev_adjacent_tiles[1][0], self.prev_adjacent_tiles[1][1]))

        if self.food_prev is not None and self.food_prev < self.food:
            near_source = False
            for t in self.prev_adjacent_tiles[0]:
                near_source = near_source or t in self.known_food_sources
            if not near_source:
                self.known_food_sources.add((self.prev_adjacent_tiles[1][0], self.prev_adjacent_tiles[1][1]))

        self.prev_adjacent_tiles = (adjacent_tiles, (self.currR, self.currC))

        # If tile with resource is appeared to be private
        Tile = marlben.Serialized.Tile
        if self.food_prev is not None and self.water_prev is not None:
            for tile_pos in self.doubtful_food_sources:
                tile = self.ob.tile(tile_pos[0] - self.currR, tile_pos[1] - self.currC)
                dst = abs(tile_pos[0] - self.currR) + abs(tile_pos[1] - self.currC)
                tile_type = round(marlben.scripting.Observation.attribute(tile, Tile.Index))
                if tile_type in (material.Forest.index, material.BalancedForest.index) and self.food < self.food_prev and dst <= 1:
                    if tile_pos in self.known_food_sources:
                        self.known_food_sources.discard(tile_pos)
                    self.forbidden_food_sources.add(tile_pos)

            for tile_pos in self.doubtful_water_sources:
                tile = self.ob.tile(tile_pos[0] - self.currR, tile_pos[1] - self.currC)
                dst = abs(tile_pos[0] - self.currR) + abs(tile_pos[1] - self.currC)
                tile_type = round(marlben.scripting.Observation.attribute(tile, Tile.Index))
                if tile_type in (material.Water.index, material.BalancedWater.index) and self.water < self.water_prev and dst <= 1:
                    if tile_pos in self.known_water_sources:
                        self.known_water_sources.discard(tile_pos)
                    self.forbidden_water_sources.add(tile_pos)

            self.doubtful_food_sources.clear()
            self.doubtful_water_sources.clear()

            for tile_pos in adjacent_tiles:
                tile = self.ob.tile(tile_pos[0] - self.currR, tile_pos[1] - self.currC)
                tile_type = round(marlben.scripting.Observation.attribute(tile, Tile.Index))

                if tile_type in (material.Water.index, material.BalancedWater.index) and self.water < self.water_prev:
                    self.doubtful_water_sources.add(tile_pos)

                if tile_type in (material.Forest.index, material.BalancedForest.index) and self.food < self.food_prev:
                    self.doubtful_food_sources.add(tile_pos)

        # If see not obscured resource tile with unknown privacy
        for tile in self.ob.tiles:
            coords = (round(marlben.scripting.Observation.attribute(tile, Tile.R)),
                      round(marlben.scripting.Observation.attribute(tile, Tile.C)))
            tile_type = round(marlben.scripting.Observation.attribute(tile, Tile.Index))
            if tile_type in (material.Forest.index, material.BalancedForest.index) and coords not in self.forbidden_food_sources:
                self.known_food_sources.add(coords)
            if tile_type in (material.Water.index, material.BalancedWater.index) and coords not in self.forbidden_water_sources:
                self.known_water_sources.add(coords)

            if tile_type in (material.ScrubImpassible.index, material.Scrub.index):
                if coords not in self.resource_cooldowns:
                    self.resource_cooldowns[coords] = self.config.RESOURCE_COOLDOWN
                if coords not in self.known_water_sources and coords not in self.forbidden_water_sources and coords not in self.known_food_sources and coords not in self.forbidden_food_sources:
                    self.known_food_sources.add(coords)
                    self.known_water_sources.add(coords)

        self.water_prev = self.water
        self.food_prev = self.food

    def _move_to_resource(self, known_sources):
        any_target_source = None
        target_source = None
        target_distance = None
        for source in known_sources:
            if any_target_source is None:
                any_target_source = source
            if source in self.resource_cooldowns:
                continue
            distance = abs(source[0] - self.currR) + abs(source[1] - self.currC)
            if target_source is None or distance < target_distance:
                target_source = source
                target_distance = distance
        if target_source is None:
            target_source = any_target_source
        move.pathfind(self.config, self.ob, self.actions,
                      target_source[0] - self.currR, target_source[1] - self.currC)


class GatheringPlantingAgent(GatheringAgent):
    def __init__(self, config, idx):
        super().__init__(config, idx)

        self._planted = False
        self._forest_pos += 1

    def plant_actions(self):
        if self._planted:
            return self.actions
        agent = self.ob.agent
        Entity = marlben.Serialized.Entity
        r = marlben.scripting.Observation.attribute(agent, Entity.R)
        plant_decision = self._current_target == "Water" and r == self._forest_pos
        self._planted = plant_decision
        if self._planted:
            self._forest_pos -= 1
        self.actions[marlben.action.Plant] = {marlben.action.PlantDecision: plant_decision}
        return self.actions
    
    def __call__(self, obs):
        super().__call__(obs)
        self.gather_actions()
        return self.plant_actions()


class SiegeAgent(GatheringBuildingAgent):
    def __init__(self, config, idx):
        super().__init__(config, idx)

    def __call__(self, obs):
        super().__call__(obs)
        self.actions = self.attack_actions()
        return self.actions


class PveAgent(GatheringAgent):
    def __init__(self, config, idx):
        super().__init__(config, idx)

    def __call__(self, obs):
        super().__call__(obs)
        self.actions = self.attack_actions()
        return self.actions
        

class GatheringCombatAgent(GatheringAgent):
    def __init__(self, config, idx):
        super().__init__(config, idx)
        self._attacks = (self.iden + 1) % 2 == 0
        self._mid_col = 11 + int(not self._attacks)
    
    def fight_started(self):
        agent = self.ob.agent
        Entity = marlben.Serialized.Entity
        c = marlben.scripting.Observation.attribute(agent, Entity.C)
        return c == self._mid_col

    def go_to_fight_actions(self):
        agent = self.ob.agent
        Entity = marlben.Serialized.Entity
        c = marlben.scripting.Observation.attribute(agent, Entity.C)

        if c != self._mid_col:
            move_action = {Direction: East if self._attacks else West}
            self.actions[Move] = move_action
        return self.actions

    def __call__(self, obs):
        super().__call__(obs)
        if not self.fight_started():
            self.go_to_fight_actions()
        else:
            self.gather_actions()
        if self._attacks:
            self.attack_actions(npc_only=False)
        return self.actions
