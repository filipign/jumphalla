from abc import ABC, abstractmethod
from enum import Enum

import pygame

from jumphalla.entity import player
from jumphalla.map import game_map


class GameComponent(ABC):
    @abstractmethod
    def update(self):
        '''In this method, object should update it's internal logic'''
        pass

    @abstractmethod
    def draw(self):
        '''Returns:
            tuple: image loaded with pygame.image module and coordinates
            indicating where to draw image.
        '''
        pass


class GameState(GameComponent):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def key_pressed(self, keys):
        pass


class GameStateName(Enum):
    MENU = 0
    RUNNING = 1
    PAUSE = 2


class MenuState(GameState):
    def update(self):
        pass

    def draw(self):
        pass

    @property
    def name(self):
        return GameStateName.MENU

    def key_pressed(self, keys):
        pass


class RunningState(GameState):
    def __init__(self):
        self.player = player.Player(100, 100)
        self.map = game_map.GameMap('resources/map/background-0.png')

    def update(self):
        self.player.update()

    def draw(self):
        to_draw = []
        to_draw += self.map.draw()
        to_draw.append(self.player.draw())
        return tuple(to_draw)

    @property
    def name(self):
        return GameStateName.RUNNING

    def key_pressed(self, keys):
        if keys[pygame.K_RIGHT]:
            self.player.move(player.Direction.RIGHT)
        if keys[pygame.K_LEFT]:
            self.player.move(player.Direction.LEFT)


class PauseState(GameState):
    def update(self):
        pass

    def draw(self):
        pass

    @property
    def name(self):
        return GameStateName.PAUSE

    def key_pressed(self, keys):
        pass