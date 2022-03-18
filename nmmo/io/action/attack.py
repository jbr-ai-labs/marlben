import numpy as np

from nmmo.io.action.common import NodeType, Node, Fixed
from nmmo.lib.utils import staticproperty


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