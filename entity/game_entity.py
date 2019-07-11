class GameEntity:
    '''GameEntity is base of how objects in game, like player, will behave.
    This includes physics attributes and basics properties. Values in pixels.
    '''
    def __init__(self, x, y):
        super().__init__()

        # constants
        # x and y of upper left corner
        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = 0

        self.x_acceleration = 1
        self.y_acceleration = 1

        self.x_max_velocity = 8
        self.y_max_velocity = 15

        self.width_hitbox = 64
        self.height_hitbox = 64

        self.slowing_speed = 0.3
        self.stopping_limit = 0.5

    def get_coords(self):
        return (self.x, self.y)

    def set_position(self, x=None, y=None):
        self.x = x or self.x
        self.y = y or self.y
