from enum import Enum

import pygame

from jumphalla.entity.game_entity import GameEntity


class Direction(Enum):
    RIGHT = 1
    LEFT = -1
    UP = 0


class PlayerState(Enum):
    FALLING = 0
    IDLE = 1
    RUNNING = 2
    POWERING = 3
    JUMPING = 4


class Player(GameEntity):
    def __init__(self, x, y):
        '''Main class representing hero that player will take control of in
        the game.

        Args:
            x (int): Starting x coordinate.
            y (int): Starting y coordinate.
        '''
        super().__init__(x, y)
        self.img = pygame.image.load('resources/hero/idle-right-0.png')
        self.current_state = PlayerState.FALLING

    def update(self, nearby_tiles, tile_width, tile_height):
        '''Updates internal logic of player - change in his position on map
        (accounting object collision) and velocity.

        For object collision, player checks if his hitbox would cut with any
        nearby solid tile on map, if so then set player position as close to
        tile as possible.

        Args:
            nearby_tiles (dict): Dictionary of 4 closest tiles, with bools values indicating
                that tiles is solid or not.
            tile_width (int): Map tile width.
            tile_heigth (int): Map tile heigth.
        '''
        self.collision_check(nearby_tiles, tile_width, tile_height)

        self.x += self.x_velocity
        self.y += self.y_velocity

        # slowing down if not moving
        if self.x_velocity > 0:
            self.x_velocity -= 1
        elif self.x_velocity < 0:
            self.x_velocity += 1

        if self.current_state == PlayerState.FALLING:
            self.y_velocity += self.y_acceleration
            if abs(self.y_velocity) > self.y_max_velocity:
                self.y_velocity = self.y_max_velocity

    def collision_check(self, nearby_tiles, tile_width, tile_height):
        '''For object collision, player checks if his hitbox would cut with any
        nearby solid tile on map, if so then set player position as close to
        tile as possible.

        Args:
            nearby_tiles (dict): Dictionary of 4 closest tiles, with bools values indicating
                that tiles is solid or not.
            tile_width (int): Map tile width.
            tile_heigth (int): Map tile heigth.
        '''
        left = int((self.x + self.x_velocity) / tile_width)
        right = left + 1
        up = int((self.y + self.y_velocity) / tile_height)
        down = up + 1

        if self.x_velocity > 0:
            if nearby_tiles['upper_right'] and nearby_tiles['down_right']:
                self.x = tile_width * (right - 1)
                self.x_velocity = 0

        if self.x_velocity < 0:
            if nearby_tiles['upper_left'] and nearby_tiles['down_left']:
                self.x = tile_width * (left + 1)
                self.x_velocity = 0

        if self.y_velocity > 0:
            if nearby_tiles['down_left'] or nearby_tiles['down_right']:
                self.y = tile_height * (down - 1)
                self.y_velocity = 0
                self.current_state = PlayerState.RUNNING

        if self.y_velocity < 0:
            if nearby_tiles['upper_left'] or nearby_tiles['upper_right']:
                self.y = tile_height * (up + 1)
                self.y_velocity = 0
                self.current_state = PlayerState.FALLING

        if not nearby_tiles['down_left'] and not nearby_tiles['down_right']:
            self.current_state = PlayerState.FALLING

    def move(self, direction):
        '''Changes player velocity, based on given direction

        Args:
            direction (enum): Direction enum member, indicating where should
                player move.
        '''
        if direction == Direction.UP:
            self.y_velocity = -15
            return

        self.x_velocity += self.x_acceleration * direction.value
        if abs(self.x_velocity) > self.x_max_velocity:
            self.x_velocity = self.x_max_velocity * direction.value

    def draw(self):
        return (self.img, (self.x, self.y))
