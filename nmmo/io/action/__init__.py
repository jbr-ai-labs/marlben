from .base_action import Action
from .attack import Attack, Target, Style, Melee, Range, Mage, Heal
from .share import Share, Target, ResourceAmount, Resource, Food, Water
from .move import Move, Direction, West, North, South, East
from .message import Message
from .common import Fixed

Action.hook()