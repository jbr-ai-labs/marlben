import nmmo
from scripted import move
from scripted.baselines import Scripted


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
        Entity = nmmo.Serialized.Entity

        r = nmmo.scripting.Observation.attribute(agent, Entity.R)
        c = nmmo.scripting.Observation.attribute(agent, Entity.C)
        self._manage_direction(r, c)
        direction = move.towards(self._direction)
        self.actions[nmmo.action.Move] = {nmmo.action.Direction: direction}
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
        Entity = nmmo.Serialized.Entity
        r = nmmo.scripting.Observation.attribute(agent, Entity.R)
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

        self.actions[nmmo.action.Move] = {nmmo.action.Direction: direction}
        self.actions[nmmo.action.Build] = {nmmo.action.BuildDecision: building}

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
        self.water_prev = None
        self.food_prev = None

    def __call__(self, obs):
        super().__call__(obs)
        if self.food < self.food_max / 2 and len(self.known_food_sources) > 0:
            # Go grab something to eat
            self._move_to_resource(self.known_food_sources)
        elif self.water < self.water_max / 2 and len(self.known_water_sources) > 0:
            # Go get some water
            self._move_to_resource(self.known_water_sources)
        else:
            # Explore for more resource sources
            self.explore()
        return self.actions

    def _update_resources_register(self):
        # If tile with resource is obscured
        if self.water_prev is not None and self.water_prev < self.water:
            self.known_water_sources.update((self.currR, self.currC))

        if self.food_prev is not None and self.food_prev < self.food:
            self.known_food_sources.update((self.currR, self.currC))

        # If tile with resource is appeared to be private
        Tile = nmmo.Serialized.Tile
        for rDelta in (-1, 0, 1):
            for cDelta in (-1, 0, 1):
                if rDelta != 0 and cDelta != 0:
                    continue
                tile = self.ob.tile(rDelta, cDelta)
                coords = (nmmo.scripting.Observation.attribute(tile, Tile.R),
                          nmmo.scripting.Observation.attribute(tile, Tile.C))
                if nmmo.scripting.Observation.attribute(tile, Tile.Index) in (4, 8) and self.food < self.food_max - 1:
                    if coords in self.known_food_sources:
                        self.known_food_sources.discard(coords)
                    self.forbidden_food_sources.update(coords)

                if nmmo.scripting.Observation.attribute(tile, Tile.Index) in (7, 1) and self.water < self.water_max - 1:
                    if coords in self.known_water_sources:
                        self.known_water_sources.discard(coords)
                    self.forbidden_water_sources.update(coords)

        # If see not obscured resource tile with unknown privacy
        for tile in self.ob.tiles:
            coords = (nmmo.scripting.Observation.attribute(tile, Tile.R),
                      nmmo.scripting.Observation.attribute(tile, Tile.C))
            if nmmo.scripting.Observation.attribute(tile, Tile.Index) in (4, 8) and coords not in self.forbidden_food_sources:
                self.known_food_sources.update(coords)
            if nmmo.scripting.Observation.attribute(tile, Tile.Index) in (7, 1) and coords not in self.forbidden_water_sources:
                self.known_water_sources.update(coords)

    def _move_to_resource(self, known_sources):
        target_source = None
        target_distance = None
        for source in known_sources:
            distance = abs(source[0] - self.currR) + abs(source[1] - self.currC)
            if target_source is None or distance < target_distance:
                target_source = source
                target_distance = distance
        move.pathfind(self.config, self.ob, self.actions, target_source[0], target_source[1])