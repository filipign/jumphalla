import unittest

from jumphalla.entity import player
from jumphalla.config import config


class PlayerCollisionTests(unittest.TestCase):
    '''Test cases for player implementation'''
    def setUp(self):
        self.player = player.Player(100, 100)
        self.tile_width = config['map']['tile']['width']
        self.tile_height = config['map']['tile']['height']

    def tearDown(self):
        pass

    def test_player_falling(self):
        '''Player start one tile above the blocked tile falling, should stop
        falling.
        '''
        nearby_tiles = {
            'upper_left': False,
            'upper_right': False,
            'down_left': True,
            'down_right': True,
        }
        self.player.collision_check(nearby_tiles,
                                    self.tile_width,
                                    self.tile_height)
        # TODO: when states gonna be well defined, check if player is in
        # certain state, for now just if he stopped falling
        self.assertEqual(self.player.current_state, player.PlayerState.FALLING)
        self.assertEqual(self.player.y_velocity, 0)

    def test_player_hit_wall_right(self):
        '''Player walk into wall on his right side, wall should stop him.'''
        nearby_tiles = {
            'upper_left': False,
            'upper_right': True,
            'down_left': True,
            'down_right': True,
        }
        # Player is close to third tile in a row
        self.player.set_position(x=60, y=64)
        self.player.x_velocity=10
        self.player.update(nearby_tiles, self.tile_width, self.tile_height)
        # Assert that, when he is running right, he should be put as close as
        # possible to the tile he is running into.
        self.assertEqual(self.player.x, 64)
        self.assertEqual(self.player.x_velocity, 0)

    def test_player_hit_wall_left(self):
        '''Player walk into wall on his left side, wall should stop him.'''
        nearby_tiles = {
            'upper_left': True,
            'upper_right': False,
            'down_left': True,
            'down_right': True,
        }
        # Player is close to first tile in a row
        self.player.set_position(x=68, y=64)
        self.player.x_velocity=-10
        self.player.update(nearby_tiles, self.tile_width, self.tile_height)
        # Assert that, when he is running left, he should be put as close as
        # possible to the tile he is running into.
        self.assertEqual(self.player.x, 64)
        self.assertEqual(self.player.x_velocity, 0)

    def test_player_hit_roof(self):
        '''When player is jumping and hit the roof, he should be stopped'''
        nearby_tiles = {
            'upper_left': True,
            'upper_right': True,
            'down_left': False,
            'down_right': False,
        }
        # Player is close 1 tile in column
        self.player.set_position(x=68, y=68)
        self.player.y_velocity=-10
        self.player.update(nearby_tiles, self.tile_width, self.tile_height)
        # Assert that, when he is jumping and hit roof, he is put as close as
        # possible to the roof
        self.assertEqual(self.player.y, 64)

if __name__ == '__main__':
    unittest.main()