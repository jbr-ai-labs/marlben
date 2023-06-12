from pdb import set_trace as T
import abc

import numpy as np

from marlben.systems import experience, combat, ai

from marlben.lib import material

### Infrastructure ###


class SkillGroup:
    def __init__(self, config):
        self.expCalc = experience.ExperienceCalculator()
        self.config = config
        self.skills = set()

    def update(self, realm, entity, actions):
        for skill in self.skills:
            skill.update(realm, entity)

    def packet(self):
        data = {}
        for skill in self.skills:
            data[skill.name] = skill.packet()
        return data


class Skill:
    skillItems = abc.ABCMeta

    def __init__(self, skillGroup):
        self.config = skillGroup.config
        self.expCalc = skillGroup.expCalc
        self.exp = 0

        skillGroup.skills.add(self)

    @property
    def name(self):
        return self.__class__.__name__.lower()

    def packet(self):
        data = {}

        data['exp'] = self.exp
        data['level'] = self.level

        return data

    def update(self, realm, entity):
        pass

    def setExpByLevel(self, level):
        self.exp = self.expCalc.expAtLevel(level)

    @property
    def level(self):
        lvl = self.expCalc.levelAtExp(self.exp)
        assert lvl == int(lvl)
        return int(lvl)

### Skill Subsets ###


class Harvesting(SkillGroup):
    def __init__(self, config):
        super().__init__(config)

        self.fishing = Fishing(self)
        self.hunting = Hunting(self)


class HarvestingBalanced(SkillGroup):
    def __init__(self, config):
        super().__init__(config)

        self.fishing = CollectResource(self, "water")
        self.hunting = CollectResource(self, "food")


class Combat(SkillGroup):
    def __init__(self, config):
        super().__init__(config)

        self.constitution = Constitution(self)
        self.defense = Defense(self)
        self.melee = Melee(self)
        self.range = Range(self)
        self.mage = Mage(self)
        self.heal = Heal(self)

    def packet(self):
        data = super().packet()
        data['level'] = combat.level(self)

        return data

    def applyDamage(self, dmg, style):
        if not self.config.game_system_enabled('Progression'):
            return

        config = self.config
        baseScale = config.PROGRESSION_BASE_XP_SCALE
        combScale = config.PROGRESSION_COMBAT_XP_SCALE
        conScale = config.PROGRESSION_CONSTITUTION_XP_SCALE

        if dmg > 0.:
            self.constitution.exp += dmg * baseScale * conScale

        skill = self.__dict__[style]
        skill.exp += abs(dmg) * baseScale * combScale

    def receiveDamage(self, dmg, stealing_enabled=True):
        if not self.config.game_system_enabled('Progression') or dmg < 0.:
            return

        config = self.config
        baseScale = config.PROGRESSION_BASE_XP_SCALE
        combScale = config.PROGRESSION_COMBAT_XP_SCALE
        conScale = config.PROGRESSION_CONSTITUTION_XP_SCALE

        self.constitution.exp += dmg * baseScale * conScale
        self.defense.exp += dmg * baseScale * combScale


class Skills(Harvesting, Combat):
    pass


class SkillsBalanced(HarvestingBalanced, Combat):
    pass


### Individual Skills ###
class CombatSkill(Skill):
    pass


class Constitution(CombatSkill):
    def __init__(self, skillGroup):
        super().__init__(skillGroup)
        self.setExpByLevel(self.config.BASE_HEALTH)

    def update(self, realm, entity):
        health = entity.resources.health
        food = entity.resources.food
        water = entity.resources.water
        config = self.config

        if not config.game_system_enabled('Resource'):
            health.increment(1)
            return

        # Heal if above fractional resource threshold
        regen = config.RESOURCE_HEALTH_REGEN_THRESHOLD
        foodThresh = food > regen * entity.skills.hunting.level
        waterThresh = water > regen * entity.skills.fishing.level

        if foodThresh and waterThresh and config.REGEN_HEALTH:
            restore = config.RESOURCE_HEALTH_RESTORE_FRACTION
            restore = np.floor(restore * self.level)
            health.increment(restore)

        if food.empty:
            health.decrement(1)

        if water.empty:
            health.decrement(1)


class Melee(CombatSkill):
    pass


class Range(CombatSkill):
    pass


class Mage(CombatSkill):
    pass


class Heal(CombatSkill):
    pass


class Defense(CombatSkill):
    pass


class Fishing(Skill):
    def __init__(self, skillGroup):
        super().__init__(skillGroup)
        config, level = self.config, 1
        if config.game_system_enabled('Progression'):
            level = config.PROGRESSION_BASE_RESOURCE
        elif config.game_system_enabled('Resource'):
            level = config.RESOURCE_BASE_RESOURCE

        self.setExpByLevel(level)

    def update(self, realm, entity):
        if not self.config.game_system_enabled('Resource'):
            return

        water = entity.resources.water
        water.decrement(1)

        adj_tiles = ai.utils.adjacentTiles(realm.map.tiles, entity.pos)
        water_nearby = False
        for tile in adj_tiles:
            water_in_tile = (type(tile.state) in [material.Water] and
                             tile.accessibility_color in entity.accessible_colors)
            water_nearby = water_nearby or water_in_tile
        if not water_in_tile:
            return

        restore = self.config.RESOURCE_HARVEST_RESTORE_FRACTION
        restore = np.floor(restore * self.level)
        water.increment(restore)

        if self.config.game_system_enabled('Progression'):
            self.exp += self.config.PROGRESSION_BASE_XP_SCALE * restore


class Hunting(Skill):
    def __init__(self, skillGroup):
        super().__init__(skillGroup)
        config, level = self.config, 1
        if config.game_system_enabled('Progression'):
            level = config.PROGRESSION_BASE_RESOURCE
        elif config.game_system_enabled('Resource'):
            level = config.RESOURCE_BASE_RESOURCE

        self.setExpByLevel(level)

    def update(self, realm, entity):
        if not self.config.game_system_enabled('Resource'):
            return

        food = entity.resources.food
        food.decrement(1)

        r, c = entity.pos
        tile = realm.map.tiles[r, c]
        if (type(tile.mat) not in [material.Forest] or
                tile.accessibility_color not in entity.accessible_colors or
                not realm.map.harvest(r, c)):
            return

        restore = self.config.RESOURCE_HARVEST_RESTORE_FRACTION
        restore = np.floor(restore * self.level)
        food.increment(restore)

        if self.config.game_system_enabled('Progression'):
            self.exp += self.config.PROGRESSION_BASE_XP_SCALE * restore


class CollectResource(Skill):

    TYPE2MAT = {
        'food': material.BalancedForest,
        'water': material.BalancedWater
    }
    TYPE2NAME = {
        'food': 'hunting',
        'water': 'fishing'
    }

    def __init__(self, skillGroup, resource_type):
        super().__init__(skillGroup)
        config, level = self.config, 1
        if config.game_system_enabled('Progression'):
            level = config.PROGRESSION_BASE_RESOURCE
        elif config.game_system_enabled('Resource'):
            level = config.RESOURCE_BASE_RESOURCE

        self.setExpByLevel(level)
        self.resource_type = resource_type
        self.material_type = self.TYPE2MAT[resource_type]

    @property
    def name(self):
        return self.TYPE2NAME[self.resource_type]

    def update(self, realm, entity):
        if not self.config.game_system_enabled('Resource'):
            return
        resource = getattr(entity.resources, self.resource_type)
        resource.decrement(1)

        resource_positions = ai.utils.adjacentPosWithMat(
            realm.map.tiles, entity.pos, self.material_type
        )
        resource_positions = [(r, c) for r, c in resource_positions
                              if realm.map.tiles[r, c].accessibility_color in entity.accessible_colors]

        if not len(resource_positions):
            return

        r, c = resource_positions[0]
        realm.map.harvest(r, c)

        restore = self.config.RESOURCE_HARVEST_RESTORE_FRACTION
        restore = np.floor(restore * self.level)
        resource.increment(restore)

        if self.config.game_system_enabled('Progression'):
            self.exp += self.config.PROGRESSION_BASE_XP_SCALE * restore
