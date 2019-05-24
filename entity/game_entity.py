class GameEntity():
    '''GameEntity is base of how objects in game like player will behave.
    This includes physics attributes and basics properties. Values in pixels.
    '''
    def __init__(self, x, y):
        super().__init__()

        # x and y of upper left corner
        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = 0

        self.x_acceleration = 3
        self.y_acceleration = 3

        self.x_max_velocity = 15
        self.y_max_velocity = 15

        self.width_hitbox = 64
        self.height_hitbox = 64

    def get_coords(self):
        return (self.x, self.y)

    def set_position(self, x=None, y=None):
        self.x = x or self.x
        self.y = y or self.y
