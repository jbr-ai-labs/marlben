from enum import Enum, auto

import numpy as np

import nmmo
from nmmo.lib import utils
from nmmo.lib.utils import staticproperty


class NodeType(Enum):
    # Tree edges
    STATIC = auto()  # Traverses all edges without decisions
    SELECTION = auto()  # Picks an edge to follow

    # Executable actions
    ACTION = auto()  # No arguments
    CONSTANT = auto()  # Constant argument
    VARIABLE = auto()  # Variable argument


class Node(metaclass=utils.IterableNameComparable):
    @staticproperty
    def edges():
        return []

    # Fill these in
    @staticproperty
    def priority():
        return None

    @staticproperty
    def type():
        return None

    @staticproperty
    def leaf():
        return False

    @classmethod
    def N(cls, config):
        return len(cls.edges)

    def args(stim, entity, config):
        return []


class Fixed:
    pass


# ActionRoot
class Action(Node):
    nodeType = NodeType.SELECTION

    @staticproperty
    def edges():
        '''List of valid actions'''
        return [Move, Attack, Share]

    @staticproperty
    def n():
        return len(Action.arguments)

    def args(stim, entity, config):
        return nmmo.Serialized.edges

        # Called upon module import (see bottom of file)

    # Sets up serialization domain
    def hook():
        idx = 0
        arguments = []
        for action in Action.edges:
            for args in action.edges:
                if not 'edges' in args.__dict__:
                    continue
                for arg in args.edges:
                    arguments.append(arg)
                    arg.serial = tuple([idx])
                    arg.idx = idx
                    idx += 1
        Action.arguments = arguments


class Move(Node):
    priority = 2
    nodeType = NodeType.SELECTION

    def call(env, entity, direction):
        r, c = entity.pos
        entID = entity.entID
        entity.history.lastPos = (r, c)
        rDelta, cDelta = direction.delta
        rNew, cNew = r + rDelta, c + cDelta

        # One agent per cell
        tile = env.map.tiles[rNew, cNew]
        if tile.occupied and not tile.lava:
            return

        if entity.status.freeze > 0:
            return

        env.dataframe.move(nmmo.Serialized.Entity, entID, (r, c), (rNew, cNew))
        entity.base.r.update(rNew)
        entity.base.c.update(cNew)

        env.map.tiles[r, c].delEnt(entID)
        env.map.tiles[rNew, cNew].addEnt(entity)

        if env.map.tiles[rNew, cNew].lava:
            entity.receiveDamage(None, entity.resources.health.val)

    @staticproperty
    def edges():
        return [Direction]

    @staticproperty
    def leaf():
        return True


class Direction(Node):
    argType = Fixed

    @staticproperty
    def edges():
        return [North, South, East, West]

    def args(stim, entity, config):
        return Direction.edges


class North(Node):
    delta = (-1, 0)


class South(Node):
    delta = (1, 0)


class East(Node):
    delta = (0, 1)


class West(Node):
    delta = (0, -1)


class Attack(Node):
    priority = 1
    nodeType = NodeType.SELECTION

    @staticproperty
    def n():
        return 4

    @staticproperty
    def edges():
        return [Style, Target]

    @staticproperty
    def leaf():
        return True

    def inRange(entity, stim, config, N):
        R, C = stim.shape
        R, C = R // 2, C // 2

        rets = set([entity])
        for r in range(R - N, R + N + 1):
            for c in range(C - N, C + N + 1):
                for e in stim[r, c].ents.values():
                    rets.add(e)

        rets = list(rets)
        return rets

    def l1(pos, cent):
        r, c = pos
        rCent, cCent = cent
        return abs(r - rCent) + abs(c - cCent)

    def call(env, entity, style, targ):
        if entity.isPlayer and not env.config.game_system_enabled('Combat'):
            return

            # Check if self targeted
        if entity.entID == targ.entID:
            return

        # ADDED: POPULATION IMMUNITY
        # if entity.population == targ.population:
        #   return

        # Check attack range
        rng = style.attackRange(env.config)
        start = np.array(entity.base.pos)
        end = np.array(targ.base.pos)
        dif = np.max(np.abs(start - end))

        # Can't attack same cell or out of range
        if dif == 0 or dif > rng:
            return

            # Execute attack
        entity.history.attack = {}
        entity.history.attack['target'] = targ.entID
        entity.history.attack['style'] = style.__name__
        targ.attacker = entity
        targ.attackerID.update(entity.entID)

        from nmmo.systems import combat
        dmg = combat.attack(entity, targ, style.skill)

        if style.freeze and dmg > 0:
            targ.status.freeze.update(env.config.COMBAT_FREEZE_TIME)

        return dmg


class Style(Node):
    argType = Fixed

    @staticproperty
    def edges():
        return [Melee, Range, Mage, Heal]

    def args(stim, entity, config):
        return Style.edges


class Target(Node):
    argType = None

    # argType = int

    @classmethod
    def N(cls, config):
        # return config.WINDOW ** 2
        return config.N_AGENT_OBS

    def args(stim, entity, config):
      #Should pass max range?
        return Attack.inRange(entity, stim, config, None)


class Melee(Node):
    nodeType = NodeType.ACTION
    index = 0
    freeze = False

    def attackRange(config):
        return config.COMBAT_MELEE_REACH

    def skill(entity):
        return entity.skills.melee


class Range(Node):
    nodeType = NodeType.ACTION
    index = 1
    freeze = False

    def attackRange(config):
        return config.COMBAT_RANGE_REACH

    def skill(entity):
        return entity.skills.range


class Mage(Node):
    nodeType = NodeType.ACTION
    index = 2
    freeze = True

    def attackRange(config):
        return config.COMBAT_MAGE_REACH

    def skill(entity):
        return entity.skills.mage


class Heal(Node):
    nodeType = NodeType.ACTION
    index = 3
    freeze = False

    def attackRange(config):
        return config.COMBAT_HEAL_REACH

    def skill(entity):
        return entity.skills.heal


class Share(Node):
    priority = 0
    nodeType = NodeType.SELECTION

    @staticproperty
    def edges():
        return [Resource, Target, ResourceAmount]

    @staticproperty
    def leaf():
        return True

    def inRange(entity, stim, config, N):
        R, C = stim.shape
        R, C = R // 2, C // 2

        rets = set([entity])
        for r in range(R - N, R + N + 1):
            for c in range(C - N, C + N + 1):
                for e in stim[r, c].ents.values():
                    rets.add(e)

        rets = list(rets)
        return rets

    def call(env, entity, resource, targ, amount):
        if not env.config.game_system_enabled('Sharing') or not env.config.game_system_enabled('Resource'):
            return

        # Check if self targeted
        if entity.entID == targ.entID:
            return

        # Check sharing range
        rng = env.config.SHARING_DISTANCE
        start = np.array(entity.base.pos)
        end = np.array(targ.base.pos)
        dif = np.max(np.abs(start - end))

        # Can't attack same cell or out of range
        if dif == 0 or dif > rng:
            return

        # Execute attack
        entity.history.share = {}
        entity.history.share['target'] = targ.entID
        entity.history.share['resource'] = resource.__name__
        entity.history.share['amount'] = amount

        from nmmo.systems import sharing
        true_amount = sharing.share(entity, targ, resource.resource, amount)

        return true_amount


class ResourceAmount(Node):
    argType = None

    # argType = Player

    @classmethod
    def N(cls, config):
        # return config.WINDOW ** 2
        return config.N_AGENT_OBS

    def args(stim, entity, config):
        # Should pass max range?
        return list(range(max(entity.food.max, entity.water.max)))


class Resource(Node):
    argType = Fixed

    @staticproperty
    def edges():
        return [Water, Food]

    def args(stim, entity, config):
        return Style.edges


class Water(Node):
    nodeType = NodeType.ACTION
    index = 0

    def resource(entity):
        return entity.resources.water


class Food(Node):
    nodeType = NodeType.ACTION
    index = 1

    def resource(entity):
        return entity.resources.food


# TODO: Add communication
class Message:
    pass


# TODO: Add trade
class Exchange:
    pass


# TODO: Solve AGI
class BecomeSkynet:
    pass


Action.hook()