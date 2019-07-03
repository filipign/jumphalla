import pygame
import numpy as np

import os
import os.path

from jumphalla.config import config

class Tile:
    def __init__(self, solid=False, path=None):
        '''Args:
            path (string): path to image file
            solid (boolean): boolean that indicates if tile is solid
        '''
        self.img = path and pygame.image.load(path)
        self.solid = solid


class MapHandler:
    '''Loads levels and handle their state management.'''
    def __init__(self):
        self.width = config['map']['width']
        self.heigth = config['map']['height']

        self.tile_width = config['map']['tile']['width']
        self.tile_height = config['map']['tile']['height']

        self.tiles = self.generate_tiles_dict()
        self.levels = []
        self.init_levels()
        self.generate_level_graphics()
        self.current_level = self.levels[0]
        self.level_index = 0

    def init_levels(self):
        '''Loads levels into memory.

        Function counts number of files in map directory, every map file is
        named with integer indicating which level is this.
        '''
        path = config['map']['maps_path']
        self.no_maps = len(os.listdir(path))
        for m in range(self.no_maps):
            self.levels.append({
                'matrix': self.load_level('{}{}.map'.format(path, m)),
                'tiles': None
            })

    def load_level(self, path):
        '''Loads map file.

        Map file is matrix of numbers separated with whitespace, each number
        represents tile.

        Example:
        0 0 0 0
        0 0 2 0
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
        for level in self.levels:
            tiles_map = []
            for i in range(self.heigth):
                for j in range(self.width):
                    if level['matrix'][i][j] > 0:
                        tiles_map.append((self.tiles[level['matrix'][i][j]].img,
                                            (j * self.tile_height, i * self.tile_width)))
            level['tiles'] = tiles_map

    def generate_tiles_dict(self):
        '''Generate dictionary of all tiles.

        (not the neatest way to handle it, but it's convinient)

        Returns:
            dict: Keys of integers mapped on Tiles objects
        '''
        path = config['map']['tiles_path']
        return {
            0: Tile(),
            1: Tile(solid=True, path='{}floor-0.png'.format(path))
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
        return self.tiles[self.current_level['matrix'][y][x]]

    def change_level(self, up):
        '''Changes map, based on player direction (up/down)

        Args:
            up (bool): player direction, True if heading up, False otherwise.
        '''
        index = 1 if up else -1
        self.level_index += index
        if self.level_index < 0 or self.level_index >= self.no_maps:
            self.level_index -= index
            return

        self.current_level = self.levels[self.level_index]

    def set_level(self, level):
        '''Changes map, based on provided level id.

        Args:
            level (int): Level id that state will change to.
        '''
        if self.level_index < 0 or self.level_index >= self.no_maps:
            return
        self.level_index = level
        self.current_level = self.levels[level]

# This will require refactor
class GameMap:
    def __init__(self, background_path):
        '''Handles map logic and graphics.'''
        self.width = config['map']['width']
        self.heigth = config['map']['height']

        self.tile_width = config['map']['tile']['width']
        self.tile_height = config['map']['tile']['height']

        self.background = pygame.image.load(background_path)
        self.map_handler = MapHandler()

    def draw(self):
        return [(self.background, (0, 0))] + self.map_handler.current_level['tiles']

    def get_tile(self, x, y):
        return self.map_handler.get_tile(x, y)

    def change_level(self, up):
        self.map_handler.change_level(up)

    def set_level(self, level):
        self.map_handler.set_level(level)
