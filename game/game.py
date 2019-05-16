import pygame

from game.game_manager import GameManager


class Game:
    def __init__(self):
        self.manager = GameManager()
        # TODO: Into config file
        self.fps = 60
        self.frame_time = int(10**3/self.fps)  # msec
        self.create_window()

    def run(self):
        '''Main loop of the game'''
        run = True
        print(self.frame_time)
        while run:
            pygame.time.delay(self.frame_time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit()

    def create_window(self):
        pygame.init()
        # TODO: read this from config file
        window = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Jumphalla")
        return window

