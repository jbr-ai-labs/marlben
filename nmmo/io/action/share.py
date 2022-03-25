import numpy as np

from nmmo.io.action.attack import Target, Style
from nmmo.io.action.common import NodeType, Node, Fixed
from nmmo.lib.utils import staticproperty


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