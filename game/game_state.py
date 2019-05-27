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
            tuple: images loaded with pygame.image module and coordinates
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
        '''
        Handling pressed keys.

        Args:
            keys (list): list of boolean values, indicating what key is pressed.
        '''
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
        self.game_map = game_map.GameMap('resources/map/background-0.png')

    def update(self):
        self.player.update(self.get_nearby_tiles(),
                           self.game_map.tile_width,
                           self.game_map.tile_width)

    def draw(self):
        to_draw = []
        to_draw += self.game_map.draw()
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
        if keys[pygame.K_UP]:
            self.player.move(player.Direction.UP)

    def get_nearby_tiles(self):
        '''Get 4 nearby tiles, for player object to check if he collides with them.

        Returns:
            dict: Dictionary of 4 closest tiles, with bools values indicating
                that tiles is solid or not.

        Example:
            `{
                'upper_left': False,
                'upper_right': False,
                'down_left': True,
                'down_right': True,
            }`
        '''
        left = int((self.player.x + self.player.x_velocity) / self.game_map.tile_width)
        right = left + 1
        up = int((self.player.y + self.player.y_velocity) / self.game_map.tile_height)
        down = up + 1

        upper_left = self.game_map.get_tile(left, up)
        upper_right = self.game_map.get_tile(right, up)
        down_left = self.game_map.get_tile(left, down)
        down_right = self.game_map.get_tile(right, down)
        return {
            'upper_left': (upper_left is not None
                           and self.game_map.tiles[upper_left].is_solid),
            'upper_right': (upper_right is not None
                            and self.game_map.tiles[upper_right].is_solid),
            'down_left': (down_left is not None
                          and self.game_map.tiles[down_left].is_solid),
            'down_right': (down_right is not None
                           and self.game_map.tiles[down_right].is_solid),
        }


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
