from jumphalla.game.game_state import GameComponent


class GameEntity(GameComponent):
    '''GameEntity is base of how objects in game like player will behave.
    This includes physics attributes and basics properties.
    '''
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = 0

        self.x_acceleration = 2
        self.y_acceleration = 3

        self.x_max_velocity = 15
        self.y_max_velocity = 30

