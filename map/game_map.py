import pygame
import numpy as np

from jumphalla.config import config

class Tile():
    def __init__(self, solid=False, path=None):
        '''Args:
            path (string): path to image file
            solid (boolean): boolean that indicates if tile is solid
        '''
        self.img = path and pygame.image.load(path)
        self.is_solid = solid


class GameMap:
    def __init__(self, background_path):
        '''Handles map logic and graphics.'''
        self.width = config['map']['width']
        self.heigth = config['map']['height']

        self.tile_width = config['map']['tile']['width']
        self.tile_height = config['map']['tile']['height']

        self.background = pygame.image.load(background_path)
        self.level = self.load_level('resources/map/levels/1.map')
        self.tiles = self.generate_tiles_dict()
        self.level_graphics = self.generate_level_graphics()

    def draw(self):
        return [(self.background, (0, 0))] + self.level_graphics

    def load_level(self, path):
        '''Loads map file.

        Map file is matrix of numbers separated with whitespace, each number
        represents tile.

        Example:
        0 0 0 0
        0 0 0 0
        1 1 1 1

        Args:
            path (str): Path to map file.

        Returns:
            list of lists: Matrix filled with numbers that identify tiles.
        '''
        return np.loadtxt(path, dtype=int)

    def generate_level_graphics(self):
        '''Generate map pair of image, coords to be drawn in pygame window.

        Returns:
            list: Pairs of image and tuple with coordinates.
        '''
        tiles_map = []
        for i in range(self.heigth):
            for j in range(self.width):
                if self.level[i][j] > 0:
                    tiles_map.append((self.tiles[self.level[i][j]].img,
                                     (j * self.tile_height, i * self.tile_width)))
        return tiles_map

    def generate_tiles_dict(self):
        '''Generate dictionary of all tiles.

        (not the neatest way to handle it, but it's convinient)

        Returns:
            dict: Keys of integers mapped on Tiles objects
        '''
        return {
            0: Tile(),
            1: Tile(solid=True, path='resources/map/floor-0.png')
        }

    def get_tile(self, x, y):
        '''Check if tile is on map and return it if it is.

        Args:
            x (int): X coordinate of tile.
            y (int): Y coordinate of tile.

        Returns:
            Tile: Tile object placed in x, y.
        '''
        if x < 0 or x >= self.width:
            return None

        if y < 0 or y >= self.heigth:
            return None
        return self.level[y][x]
