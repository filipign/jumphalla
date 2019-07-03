import unittest

from jumphalla.map import game_map
from jumphalla.config import config


class GameMapTests(unittest.TestCase):
    '''Test cases for game map implementation.'''
    def setUp(self):
        self.game_map = game_map.GameMap(config['map']['background'])

    def tearDown(self):
        pass

    def test_get_tile_out_of_index(self):
        '''It should return None when provided wrong index.'''
        tile = self.game_map.map_handler.get_tile(-1, -1)
        self.assertIsNone(tile)
        tile = self.game_map.map_handler.get_tile(9999, 9999)
        self.assertIsNone(tile)

    def test_change_level(self):
        '''It should change level.'''
        current_index = self.game_map.map_handler.level_index
        self.game_map.map_handler.change_level(up=True)
        self.assertEqual(current_index + 1, self.game_map.map_handler.level_index)

    def test_change_level_fails(self):
        '''It should not change level and index, when player is at the end of
        map.
        '''
        current_index = self.game_map.map_handler.level_index
        current_level = self.game_map.map_handler.current_level
        self.game_map.map_handler.change_level(up=False)
        self.assertEqual(current_index, self.game_map.map_handler.level_index)
        self.assertEqual(current_level, self.game_map.map_handler.current_level)

    def test_set_level(self):
        '''It should change level.'''
        self.game_map.map_handler.set_level(1)
        self.assertEqual(1, self.game_map.map_handler.level_index)

    def test_set_level_fails(self):
        '''It should not change level, when provided index points out of map.'''
        current_level = self.game_map.map_handler.current_level
        self.game_map.map_handler.set_level(-2)
        self.assertEqual(current_level, self.game_map.map_handler.current_level)