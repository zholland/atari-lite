from enum import Enum


class Action(Enum):
    NOOP = 'NOOP'
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    FIRE = 'FIRE'
