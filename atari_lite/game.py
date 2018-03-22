from abc import ABC, abstractmethod
from .actions import Action
import numpy as np


class Sprite(ABC):
    __slots__ = 'y_pos', 'y_vel', 'height', \
                'x_pos', 'x_vel', 'width', \
                'shape'

    def __init__(self, y_pos, y_vel, x_pos, x_vel):
        self.y_pos = y_pos
        self.y_vel = y_vel
        self.x_pos = x_pos
        self.x_vel = x_vel


class Game(ABC):
    SCREEN_HEIGHT = 50
    SCREEN_WIDTH = 50

    def __init__(self, seed=1):
        np.random.seed(seed)
        self._screen = np.ones((self.SCREEN_HEIGHT, self.SCREEN_WIDTH), dtype=np.uint8)
        self._game_over = False

    @abstractmethod
    def step(self, action=Action.NOOP):
        """"""

    def _draw(self, sprites):
        self._screen[:] = 1
        for sprite in sprites:
            self._screen[sprite.y_pos:sprite.y_pos+sprite.height, sprite.x_pos:sprite.x_pos+sprite.width] = sprite.shape

    @abstractmethod
    def reset(self):
        """"""

    def get_screen(self):
        return self._screen

    def game_over(self):
        return self._game_over
