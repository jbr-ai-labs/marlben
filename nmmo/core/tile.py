import numpy as np

import nmmo
from nmmo.lib import material


class Tile:
    def __init__(self, config, realm, r, c):
        self.config = config
        self.realm = realm
        self.ents = {}

        self.serialized = 'R{}-C{}'.format(r, c)

        self.r = nmmo.Serialized.Tile.R(realm.dataframe, self.serial, r)
        self.c = nmmo.Serialized.Tile.C(realm.dataframe, self.serial, c)
        self.nEnts = nmmo.Serialized.Tile.NEnts(realm.dataframe, self.serial)
        self.index = nmmo.Serialized.Tile.Index(
            realm.dataframe, self.serial, 0)
        self._visibility_color = nmmo.Serialized.Tile.VisibilityColor(
            realm.dataframe, self.serial)
        self._accessibility_color = nmmo.Serialized.Tile.AccessibilityColor(
            realm.dataframe, self.serial)

        realm.dataframe.init(nmmo.Serialized.Tile, self.serial, (r, c))

    @property
    def serial(self):
        return self.serialized

    @property
    def repr(self):
        return ((self.r, self.c))

    @property
    def pos(self):
        return self.r.val, self.c.val

    @property
    def habitable(self):
        return self.mat in material.Habitable

    @property
    def vacant(self):
        return len(self.ents) == 0 and self.habitable

    @property
    def occupied(self):
        return not self.vacant

    @property
    def impassible(self):
        return self.mat in material.Impassible

    @property
    def lava(self):
        return self.mat == material.Lava

    @property
    def static(self):
        """No updates needed"""
        assert self.capacity <= self.mat.capacity
        return self.capacity == self.mat.capacity

    @property
    def visibility_color(self):
        return self._visibility_color.val

    @property
    def accessibility_color(self):
        return self._accessibility_color.val

    def reset(self, mat, vc, ac, config):
        self.state = mat(config)
        self.mat = mat(config)

        self.capacity = self.mat.capacity
        self.current_cooldown = 0
        self.tex = mat.tex
        self.ents = {}
        self._accessibility_color.update(ac)
        self._visibility_color.update(vc)

        self.nEnts.update(0)
        self.index.update(self.state.index)

    def addEnt(self, ent):
        assert ent.entID not in self.ents
        self.nEnts.update(1)
        self.ents[ent.entID] = ent

    def delEnt(self, entID):
        assert entID in self.ents
        self.nEnts.update(0)
        del self.ents[entID]

    def step(self):
        if not self.static:
            if self.config.RESOURCE_COOLDOWN > -1:  # if cooldown system is enabled
                if self.current_cooldown == 0:  # if enough time passed capacity must be restored
                    self.capacity = 1
                else:
                    self.current_cooldown -= 1
            elif np.random.rand() < self.mat.respawn:
                self.capacity += 1

        if self.static:
            self.state = self.mat
            self.index.update(self.state.index)

    def harvest(self):
        if self.capacity == 0:
            return False
        elif self.capacity <= 1:
            # if harvesting, cooldown must be set to max
            self.current_cooldown = self.config.RESOURCE_COOLDOWN
            self.state = self.mat.degen(self.config)
            self.index.update(self.state.index)
        self.capacity -= 1
        return True
