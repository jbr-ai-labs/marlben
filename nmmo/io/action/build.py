from nmmo.io.action.common import Fixed, NodeType, Node  # , BoolDecision
from nmmo.lib.utils import staticproperty
from nmmo.lib.material import Stone


class Build(Node):
    priority = 3
    nodeType = NodeType.SELECTION

    @staticproperty
    def edges():
        return [BuildDecision]

    @staticproperty
    def leaf():
        return True

    def call(env, entity, build_decision):
        if not env.config.game_system_enabled('Building'):
            return

        r, c = entity.history.lastPos

        tile = env.map.tiles[r, c]
        if tile.occupied or tile.lava:
            return

        if entity.status.freeze > 0:
            return

        if build_decision:
            config = env.map.tiles[r, c].config
            env.map.tiles[r, c].reset(Stone, True, True, config)


class BuildDecision(Node):
    argType = Fixed

    @classmethod
    def N(cls, config):
        return 2

    def args(stim, entity, config):
        return [0, 1]

    @staticproperty
    def arg_name():
        return "build_decision"
