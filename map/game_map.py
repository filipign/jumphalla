import pygame
import numpy as np


class Tile():
    def __init__(self, solid=False, path=None):
        '''Args:
            path (string): path to image file
            solid (boolean): boolean that indicates if tile is solid
        '''
        self.img = path and pygame.image.load(path)
        self.solid = solid


class GameMap:
    def __init__(self, background_path):
        # constants
        self.width = 19
        self.heigth = 13

        self.tile_width = 64
        self.tile_height = 64

        self.background = pygame.image.load(background_path)
        self.level = self.load_level()
        self.tiles = self.generate_tiles_dict()
        self.level_graphics = self.generate_level_graphics()

    def draw(self):
        return [(self.background, (0, 0))] + self.level_graphics

    def load_level(self):
        return np.loadtxt('resources/map/levels/1.map', dtype=int)

    def generate_level_graphics(self):
        tiles_map = []
        for i in range(self.heigth):
            for j in range(self.width):
                if self.level[i][j] > 0:
                    tiles_map.append((self.tiles[self.level[i][j]].img,
                                     (j * self.tile_height, i * self.tile_width)))
        return tiles_map

    def generate_tiles_dict(self):
        return {
            0: Tile(),
            1: Tile(solid=True, path='resources/map/floor-0.png')
        }
