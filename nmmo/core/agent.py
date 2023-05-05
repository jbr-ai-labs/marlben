import random

from nmmo.io.action import Move, Direction


class Agent:
    scripted = False
    name = 'Neural_'

    def __init__(self, config, idx):
        """Base class for agents

        Args:
           config: A Config object
           idx: Unique AgentID int
        """
        self.config = config
        self.iden = idx

    def __call__(self, obs):
        """Used by scripted agents to compute actions. Override in subclasses.

        Args:
            obs: Agent observation provided by the environment
        """
        pass


class Random(Agent):
    """Moves randomly, including bumping into things and falling into lava"""

    def __call__(self, obs):
        return {Move: {Direction: random.choice(Direction.edges)}}
