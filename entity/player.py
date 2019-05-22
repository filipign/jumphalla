from enum import Enum

import pygame

from jumphalla.entity.game_entity import GameEntity


class Direction(Enum):
    RIGHT = 1
    LEFT = -1


class PlayerState(Enum):
    FALLING = 0
    IDLE = 1
    RUNNING = 2
    POWERING = 3
    JUMPING = 4


class Player(GameEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = pygame.image.load('resources/hero/idle-right-0.png')

    def update(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        if self.x_velocity > 0:
            self.x_velocity -= 1
        elif self.x_velocity < 0:
            self.x_velocity += 1

    def move(self, direction):
        self.x_velocity += self.x_acceleration * direction.value
        if abs(self.x_velocity) > self.x_max_velocity:
            self.x_velocity = self.x_max_velocity * direction.value

    def draw(self):
        return (self.img, (self.x, self.y))
