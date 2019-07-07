import unittest

from jumphalla.entity import player
from jumphalla.config import config


class PlayerCollisionTests(unittest.TestCase):
    '''Test cases for player collision implementation

    Collision algorithm makes for player one pixel buffor when determines his
    position - it's still refered as 'as close as possible to the wall'.
    '''
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
        self.player.set_position(x=60, y=63)
        self.player.x_velocity=10
        self.player.update(nearby_tiles, self.tile_width, self.tile_height)
        # Assert that, when he is running right, he should be put as close as
        # possible to the tile he is running into.
        self.assertEqual(self.player.x, 63)
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
        self.player.set_position(x=68, y=65)
        self.player.x_velocity=-10
        self.player.update(nearby_tiles, self.tile_width, self.tile_height)
        # Assert that, when he is running left, he should be put as close as
        # possible to the tile he is running into.
        self.assertEqual(self.player.x, 65)
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

class PlayerMoveTests(unittest.TestCase):
    '''Test cases for player move metod implementation.'''
    def setUp(self):
        self.player = player.Player(100, 100)
        self.player.current_state = player.PlayerState.RUNNING
        self.floor_tiles = {
            'upper_left': False,
            'upper_right': False,
            'down_left': True,
            'down_right': True,
        }
        self.tile_width = config['map']['tile']['width']
        self.tile_height = config['map']['tile']['height']

    def tearDown(self):
        pass

    def test_player_move_right(self):
        '''If player stays on the ground and there is no walls, he should be
        able to run to the right
        '''
        directions = {
            'UP': 0,
            'LEFT': 0,
            'RIGHT': 1
        }
        self.player.move(directions)
        self.player.update(self.floor_tiles, self.tile_width, self.tile_height)
        self.assertTrue(self.player.x_velocity > 0)

    def test_player_move_left(self):
        '''If player stays on the ground and there is no walls, he should be
        able to run to the left
        '''
        directions = {
            'UP': 0,
            'LEFT': 1,
            'RIGHT': 0
        }
        self.player.move(directions)
        self.player.update(self.floor_tiles, self.tile_width, self.tile_height)
        self.assertTrue(self.player.x_velocity < 0)

    def test_player_move_both_direction(self):
        '''If player stays on the ground and there is no walls, and player
        choose both right and left direction, player will still run right
        '''
        directions = {
            'UP': 0,
            'LEFT': 1,
            'RIGHT': 1
        }
        self.player.move(directions)
        self.player.update(self.floor_tiles, self.tile_width, self.tile_height)
        self.assertTrue(self.player.x_velocity > 0)

    def test_player_should_start_powering(self):
        '''If player is not falling he could be able to start powering jump.'''
        directions = {
            'UP': 1,
            'LEFT': 0,
            'RIGHT': 0
        }
        self.player.move(directions)
        self.player.update(self.floor_tiles, self.tile_width, self.tile_height)
        self.assertTrue(self.player.current_state == player.PlayerState.POWERING)

    def test_player_should_start_falling(self):
        '''If player starts jump, he should be in falling state'''
        directions = {
            'UP': 0,
            'LEFT': 0,
            'RIGHT': 0
        }
        tiles = {
            'upper_left': False,
            'upper_right': False,
            'down_left': False,
            'down_right': False,
        }
        self.player.current_state = player.PlayerState.POWERING
        self.player.powering_jump = 10
        self.player.move(directions)
        self.player.update(tiles, self.tile_width, self.tile_height)
        self.assertTrue(self.player.current_state == player.PlayerState.FALLING)

    def test_player_cant_move_falling(self):
        '''Player should not move while falling.'''
        directions = {
            'UP': 0,
            'LEFT': 0,
            'RIGHT': 1
        }
        temp_speed = self.player.x_velocity
        self.player.current_state = player.PlayerState.FALLING
        self.player.move(directions)
        self.player.update(self.floor_tiles, self.tile_width, self.tile_height)
        self.assertTrue(self.player.x_velocity == temp_speed)

if __name__ == '__main__':
    unittest.main()
