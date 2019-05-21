import pygame

from game.game_manager import GameManager


class Game:
    def __init__(self):
        # TODO: Into config file
        self.fps = 60
        self.frame_time = int(10**3/self.fps)  # msec
        self.window = self.create_window()
        self.manager = GameManager(self.window)

    def run(self):
        '''Main loop of the game'''
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
        pygame.init()
        # TODO: read this from config file
        window = pygame.display.set_mode((1216, 800))
        pygame.display.set_caption("Jumphalla")
        return window
