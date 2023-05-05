import nmmo
from nmmo.io.action.common import NodeType, Node, Fixed
from nmmo.lib.utils import staticproperty


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

        if tile.accessibility_color not in entity.accessible_colors:
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

    @staticproperty
    def arg_name():
        return "direction"


class North(Node):
    index = 0
    delta = (-1, 0)


class South(Node):
    index = 1
    delta = (1, 0)


class East(Node):
    index = 2
    delta = (0, 1)


class West(Node):
    index = 3
    delta = (0, -1)
