import unittest

from jumphalla.game import game_state
from jumphalla.config import config


class RunningStateTests(unittest.TestCase):
    '''Test cases for running state implementation.
    For test purposes test_config.json is used, that contains path to test map.
    '''
    def setUp(self):
        self.running_state = game_state.RunningState()

    def tearDown(self):
        pass

    def test_nearby_tiles_are_empty(self):
        '''0.map is empty, method should return that nearby tiles are empty,
        no matter where player is placed.
        '''
        proper_tiles = {
            'upper_left': False,
            'upper_right': False,
            'down_left': False,
            'down_right': False,
        }
        tiles = self.running_state.get_nearby_tiles()
        self.assertEqual(proper_tiles, tiles)

    def test_nearby_tiles_right_taken(self):
        '''Tiles next to player (on right) should be shown as taken.
        Test map 1 used in this test.
        '''
        proper_tiles = {
            'upper_left': False,
            'upper_right': True,
            'down_left': False,
            'down_right': True,
        }
        self.running_state.game_map.set_level(1)
        self.running_state.player.set_position(70, 70)
        tiles = self.running_state.get_nearby_tiles()
        self.assertEquals(proper_tiles, tiles)

    def test_nearby_tiles_left_taken(self):
        '''Tiles next to player (on left) should be shown as taken.
        Test map 1 used in this test.
        '''
        proper_tiles = {
            'upper_left': True,
            'upper_right': False,
            'down_left': True,
            'down_right': False,
        }
        self.running_state.game_map.set_level(1)
        self.running_state.player.set_position(192, 70)
        tiles = self.running_state.get_nearby_tiles()
        self.assertEquals(proper_tiles, tiles)

    def test_nearby_tiles_floor(self):
        '''Player should have ground under his feet.
        Test map 1 used in this test.
        '''
        proper_tiles = {
            'upper_left': False,
            'upper_right': False,
            'down_left': True,
            'down_right': True,
        }
        self.running_state.game_map.set_level(1)
        self.running_state.player.set_position(150, 260)
        tiles = self.running_state.get_nearby_tiles()
        self.assertEquals(proper_tiles, tiles)

    def test_nearby_tiles_roof(self):
        '''Player should have roof above his head.
        Test map 1 used in this test.
        '''
        proper_tiles = {
            'upper_left': True,
            'upper_right': True,
            'down_left': False,
            'down_right': False,
        }
        self.running_state.game_map.set_level(1)
        self.running_state.player.set_position(150, 360)
        tiles = self.running_state.get_nearby_tiles()
        self.assertEquals(proper_tiles, tiles)
