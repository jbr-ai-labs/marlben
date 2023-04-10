from .version import __version__

import os

motd = open(os.path.dirname(__file__) + '/resource/ascii.txt').read().format(__version__)

from . import scripting
from .lib import material
from .lib.rating import OpenSkillRating
from .overlay import Overlay, OverlayRegistry
from .io import action
from .io.stimulus import Serialized
from .io.action import Action
from .core import agent
from .core.agent import Agent
from .core.env import Env
from .systems.achievement import Task
from .core.map_generation.base import MapGenerator, Terrain

__all__ = ['Env', 'scripting', 'agent', 'Agent', 'Serialized', 'action', 'Action', 'material',
           'Task', 'Overlay', 'OverlayRegistry']
