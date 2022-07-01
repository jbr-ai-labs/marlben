import nmmo
from nmmo.lib import utils
from nmmo.systems import combat, equipment
import copy


class Resources:
    def __init__(self, ent):
        self.health = nmmo.Serialized.Entity.Health(ent.dataframe, ent.entID)
        self.water = nmmo.Serialized.Entity.Water(ent.dataframe, ent.entID)
        self.food = nmmo.Serialized.Entity.Food(ent.dataframe, ent.entID)

    def update(self, realm, entity, actions):
        self.health.max = entity.skills.constitution.level
        self.water.max = entity.skills.fishing.level
        self.food.max = entity.skills.hunting.level

    def packet(self):
        data = {}
        data['health'] = self.health.packet()
        data['food'] = self.food.packet()
        data['water'] = self.water.packet()
        return data


class Status:
    def __init__(self, ent):
        self.config = ent.config
        self.freeze = nmmo.Serialized.Entity.Freeze(ent.dataframe, ent.entID)

    def update(self, realm, entity, actions):
        self.freeze.decrement()

    def packet(self):
        data = {}
        data['freeze'] = self.freeze.val
        return data


class History:
    def __init__(self, ent):
        self.actions = None
        self.attack = None

        self.origPos = ent.pos
        self.exploration = 0
        self.playerKills = 0

        self.damage = nmmo.Serialized.Entity.Damage(ent.dataframe, ent.entID)
        self.timeAlive = nmmo.Serialized.Entity.TimeAlive(ent.dataframe, ent.entID)

        self.lastPos = None

    def update(self, realm, entity, actions):
        self.attack = None
        self.actions = actions
        self.damage.update(0)

        exploration = utils.linf(entity.pos, self.origPos)
        self.exploration = max(exploration, self.exploration)

        self.timeAlive.increment()

    def packet(self):
        data = {'damage': self.damage.val, 'timeAlive': self.timeAlive.val}

        if self.attack is not None:
            data['attack'] = self.attack

        return data


class Base:
    def __init__(self, ent, pos, iden, name, color, pop):
        self.name = name + str(iden)
        self.color = color
        r, c = pos

        self.r = nmmo.Serialized.Entity.R(ent.dataframe, ent.entID, r)
        self.c = nmmo.Serialized.Entity.C(ent.dataframe, ent.entID, c)

        self.population = nmmo.Serialized.Entity.Population(ent.dataframe, ent.entID, pop)
        self.self = nmmo.Serialized.Entity.Self(ent.dataframe, ent.entID, 1)
        self.identity = nmmo.Serialized.Entity.ID(ent.dataframe, ent.entID, ent.entID)
        self.level = nmmo.Serialized.Entity.Level(ent.dataframe, ent.entID, 3)

        ent.dataframe.init(nmmo.Serialized.Entity, ent.entID, (r, c))

    def update(self, realm, entity, actions):
        self.level.update(combat.level(entity.skills))

    @property
    def pos(self):
        return self.r.val, self.c.val

    def packet(self):
        data = {'r': self.r.val, 'c': self.c.val, 'name': self.name, 'color': self.color.packet(),
                'population': self.population.val, 'self': self.self.val}

        return data


class Entity:
    def __init__(self, realm, pos, iden, name, color, pop, skills):
        self.dataframe = realm.dataframe
        self.config = realm.config
        self.entID = iden
        self.skills = copy.deepcopy(skills)

        self.repr = None
        self.vision = 5

        self.attacker = None
        self.target = None
        self.closest = None
        self.spawnPos = pos

        self.attackerID = nmmo.Serialized.Entity.AttackerID(self.dataframe, self.entID, 0)

        # Submodules
        self.base = Base(self, pos, iden, name, color, pop)
        self.status = Status(self)
        self.history = History(self)
        self.resources = Resources(self)
        self.loadout = equipment.Loadout()

    def packet(self):
        data = {'status': self.status.packet(), 'history': self.history.packet(), 'loadout': self.loadout.packet(),
                'alive': self.alive}

        return data

    def update(self, realm, actions):
        '''Update occurs after actions, e.g. does not include history'''
        if self.history.damage == 0:
            self.attacker = None
            self.attackerID.update(0)

        self.base.update(realm, self, actions)
        self.status.update(realm, self, actions)
        self.history.update(realm, self, actions)

    def receiveDamage(self, source, dmg, stealing_enabled):
        self.history.damage.update(dmg)
        self.resources.health.decrement(dmg)

        if not self.alive and source:
            source.receiveLoot(self.loadout)
            return False

        return True

    def receiveLoot(self, loadout):
        pass

    def applyDamage(self, dmg, style, stealing_enabled):
        pass

    @property
    def pos(self):
        return self.base.pos

    @property
    def alive(self):
        if self.resources.health.empty:
            return False

        return True

    @property
    def isPlayer(self) -> bool:
        return False

    @property
    def isNPC(self) -> bool:
        return False
