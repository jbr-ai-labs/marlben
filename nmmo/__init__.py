from .core.map_generation.base import MapGenerator, Terrain
from .systems.achievement import Task
from .core.env import Env
from .core.agent import Agent
from .core import agent
from .io.action import Action
from .io.stimulus import Serialized
from .io import action
from .overlay import Overlay, OverlayRegistry
from .lib.rating import OpenSkillRating
from .lib import material
from . import scripting
from .version import __version__

import os

motd = open(os.path.dirname(__file__) + '/resource/ascii.txt').read().format(__version__)


__all__ = ['Env', 'scripting', 'agent', 'Agent', 'Serialized', 'action', 'Action', 'material',
           'Task', 'Overlay', 'OverlayRegistry']
