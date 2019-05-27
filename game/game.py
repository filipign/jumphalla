import pygame

from jumphalla.config import config
from game.game_manager import GameManager


class Game:
    def __init__(self):
        '''Game module is top level class, handles game loop.'''
        self.frame_time = int(10**3 / config['game']['fps'])  # in msec
        self.window = self.create_window()
        self.manager = GameManager(self.window)

    def run(self):
        '''Main loop of the game, loops as long as window not receive quit
        signal.
        '''
        running = True

        while running:
            self.manager.update()
            self.manager.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.time.delay(self.frame_time)
        pygame.quit()

    def create_window(self):
        '''Initializes pygame window with parameters from config file

        Returns:
            Surface: initialized pygame window
        '''
        pygame.init()
        window = pygame.display.set_mode((config['window']['width'],
                                          config['window']['height']))
        pygame.display.set_caption(config['game']['name'])
        return window
