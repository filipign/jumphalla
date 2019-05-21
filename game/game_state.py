from abc import ABC, abstractmethod
from enum import Enum

import pygame

from jumphalla.entity import player


class GameComponent(ABC):
    @abstractmethod
    def update(self):
        '''In this method, object should update it's internal logic'''
        pass

    @abstractmethod
    def draw(self):
        '''In this method, object should return it's image to draw on screen,
        with x,y coordinates
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

    def update(self):
        self.player.update()

    def draw(self):
        return self.player.draw()

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