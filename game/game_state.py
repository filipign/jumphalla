from abc import ABC, abstractmethod
from enum import Enum

import pygame

from jumphalla.config import config
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
    LOAD = 3


class MenuState(GameState):
    def __init__(self):
        self.background = pygame.image.load(config['menu']['background'])
        self.pointer = pygame.image.load(config['menu']['pointer'])

        self.pointer_index = 0
        self.pointer_x = 400
        self.pointer_base_y = 240
        self.last_index = 2

        self.last_pressed = []
        self.choosen_state = GameStateName.MENU

    def update(self):
        pass

    def draw(self):
        return ((self.background, (0, 0)), (self.pointer,
                (self.pointer_x, self.pointer_base_y + 60 * self.pointer_index)))

    @property
    def name(self):
        return GameStateName.MENU

    def key_pressed(self, keys):
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            if self.pointer_index == 0:
                self.choosen_state = GameStateName.LOAD

            elif self.pointer_index == 1:
                self.choosen_state = GameStateName.RUNNING

            elif self.pointer_index == 2:
                pygame.quit()

        if keys[pygame.K_UP] and pygame.K_UP not in self.last_pressed:
            self.last_pressed.append(pygame.K_UP)
            self.pointer_index -= 1
            if self.pointer_index < 0:
                self.pointer_index = self.last_index
        elif not keys[pygame.K_UP] and pygame.K_UP in self.last_pressed:
            self.last_pressed.remove(pygame.K_UP)

        if keys[pygame.K_DOWN] and pygame.K_DOWN not in self.last_pressed:
            self.last_pressed.append(pygame.K_DOWN)
            self.pointer_index += 1
            if self.pointer_index > self.last_index:
                self.pointer_index = 0
        elif not keys[pygame.K_DOWN] and pygame.K_DOWN in self.last_pressed:
            self.last_pressed.remove(pygame.K_DOWN)


class RunningState(GameState):
    def __init__(self):
        self.player = player.Player(100, 100)
        self.game_map = game_map.GameMap(config['map']['background'])
        self.window_height = config['window']['height']

    def update(self):
        self.player.update(self.get_nearby_tiles(),
                           self.game_map.tile_width,
                           self.game_map.tile_height)

        if self.player.y < 0 or self.player.y > self.window_height:
            direction = True if self.player.y < 0 else False
            self.game_map.change_level(up=direction)
            self.player.set_position(y=self.window_height-abs(self.player.y))

    def draw(self):
        to_draw = []
        to_draw += self.game_map.draw()
        to_draw.append(self.player.draw())
        return tuple(to_draw)

    @property
    def name(self):
        return GameStateName.RUNNING

    def key_pressed(self, keys):
        '''Pass dict of direction 0's and 1's, indicating where should player
        move.
        '''
        directional_keys = {
            'UP': keys[pygame.K_UP],
            'LEFT': keys[pygame.K_LEFT],
            'RIGHT': keys[pygame.K_RIGHT]
        }
        self.player.move(directional_keys)

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
            'upper_left': upper_left.solid if upper_left is not None else None,
            'upper_right': (upper_right.solid if upper_right is not None
                            else None),
            'down_left': down_left.solid if down_left is not None else None,
            'down_right': down_right.solid if down_right is not None else None,
        }

    def load_state(self, x, y, level):
        '''Loads state of the game.

        Save should only remember player coordinates and his level.
        Args:
            x (int): Player x coordinate
            y (int): Player y coordinate
            level (int): Level to load
        '''
        self.player.set_position(x, y)
        self.game_map.set_level(level)


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
