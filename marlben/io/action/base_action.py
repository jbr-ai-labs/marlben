import marlben
from marlben.io.action.common import NodeType, Node
from marlben.io.action.move import Move
from marlben.io.action.attack import Attack
from marlben.io.action.share import Share
from marlben.io.action.build import Build
from marlben.lib.utils import staticproperty


class Action(Node):
    nodeType = NodeType.SELECTION

    @staticproperty
    def edges():
        '''List of valid actions'''
        return [Move, Attack, Share, Build]

    @staticproperty
    def n():
        return len(Action.arguments)

    def args(stim, entity, config):
        return marlben.Serialized.edges

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
