from enum import Enum, auto

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
