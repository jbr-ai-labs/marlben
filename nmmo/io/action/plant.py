from nmmo.io.action.common import Fixed, NodeType, Node
from nmmo.lib import material
from nmmo.lib.utils import staticproperty
from nmmo.lib.material import BalancedForest


class Plant(Node):
    priority = 4
    nodeType = NodeType.SELECTION

    @staticproperty
    def edges():
        return [PlantDecision]

    @staticproperty
    def leaf():
        return True

    def call(env, entity, plant_decision):
        if not env.config.game_system_enabled('Planting'):
            return

        if plant_decision == 0:
            return

        r, c = entity.history.lastPos

        tile = env.map.tiles[r, c]
        if tile.occupied or tile.lava or tile.mat == material.Water or tile.mat == material.Forest or tile.impassible:
            return

        if entity.status.freeze > 0:
            return

        if entity.resources.food.val >= env.config.PLANTING_COST:
            config = env.map.tiles[r, c].config
            tile = env.map.tiles[r, c]
            tile.reset(BalancedForest, True, True, config)
            env.map.harvest(r, c)
            entity.resources.food.decrement(env.config.PLANTING_COST)


class PlantDecision(Node):
    argType = Fixed

    @classmethod
    def N(cls, config):
        return 2

    def args(stim, entity, config):
        return [0, 1]

    @staticproperty
    def arg_name():
        return "plant_decision"
