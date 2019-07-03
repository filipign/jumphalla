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


class StateImageHandler:
    '''Handles images and animations for a Player entity'''
    def __init__(self):
        # TODO: paths to config file
        self.running_img = pygame.image.load('resources/hero/idle-right-0.png')
        self.powering_img = pygame.image.load('resources/hero/powering.png')


class Player(GameEntity):
    def __init__(self, x, y):
        '''Main class representing hero that player will take control of in
        the game.

        Args:
            x (int): Starting x coordinate.
            y (int): Starting y coordinate.
        '''
        super().__init__(x, y)
        self.img = StateImageHandler()
        self.current_state = PlayerState.FALLING

        # Values in pixels
        self.powering_jump = 0
        self.powering_speed = 1
        self.max_powering = 14
        self.jump_direction = Direction.UP

        self.jump_time = 14  # frames
        self.jump_timer = 0

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

        # slowing down if moving on the ground
        if self.y_velocity > -1:
            if self.x_velocity > 0.5:
                self.x_velocity -= 0.3
            elif self.x_velocity < 0.5:
                self.x_velocity += 0.3

            if self.x_velocity < 0.5 and self.x_velocity > -0.5:
                self.x_velocity = 0

        if self.current_state == PlayerState.FALLING:
            if self.jump_timer != 0:
                self.jump_timer -= 1
                return
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

    def move(self, directions):
        '''Changes player velocity, based on given direction.

        Args:
            direction (dict): dict of direction 0's and 1's, indicating where
                should player move.

        Example:
            directions = {
                'UP': 0,
                'LEFT': 1,
                'RIGHT': 1
            }
        '''
        if self.current_state == PlayerState.POWERING:
            if not directions['UP']:
                self.y_velocity = (-self.powering_jump if
                                   self.powering_jump < self.max_powering
                                   else -self.max_powering)
                if self.jump_direction != Direction.UP:
                    if self.powering_jump < self.max_powering:
                        self.x_velocity = int((self.powering_jump
                                               * self.jump_direction.value
                                               * 0.5))
                    else:
                        self.x_velocity = int((self.max_powering
                                               * self.jump_direction.value
                                               * 0.5))
                self.x_velocity = int(self.x_velocity)
                self.jump_timer = self.jump_time
                self.powering_jump = 0
                self.jump_direction = Direction.UP
                return

            if directions['UP']:
                self.powering_jump += self.powering_speed

            if directions['LEFT']:
                self.jump_direction = Direction.LEFT

            if directions['RIGHT']:
                self.jump_direction = Direction.RIGHT

        if self.current_state == PlayerState.RUNNING:
            if directions['UP']:
                self.current_state = PlayerState.POWERING
                return

            if directions['RIGHT'] or directions['LEFT']:
                direction = (Direction.RIGHT if directions['RIGHT'] else
                             Direction.LEFT)
                self.x_velocity += self.x_acceleration * direction.value
                if abs(self.x_velocity) > self.x_max_velocity:
                    self.x_velocity = self.x_max_velocity * direction.value

    def draw(self):
        if self.current_state == PlayerState.POWERING:
            return (self.img.powering_img, (self.x, self.y))

        return (self.img.running_img, (int(self.x), int(self.y)))