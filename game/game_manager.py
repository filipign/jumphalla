# TODO: cleanup imports
import pygame

from jumphalla.game import game_state


class GameManager:
    '''State manager handle game states as menu, pause, actual running game and
    also window that draw graphics.
    '''
    def __init__(self, window):
        self.states = {
            game_state.GameStateName.MENU: game_state.MenuState(),
            game_state.GameStateName.PAUSE: game_state.PauseState(),
            game_state.GameStateName.RUNNING: game_state.RunningState(),
        }
        self.current_state = self.states[game_state.GameStateName.RUNNING]
        self.window = window

    def update(self):
        self.current_state.key_pressed(pygame.key.get_pressed())
        self.current_state.update()

    def draw(self):
        self.window.fill((0, 0, 0))
        # to_draw = self.current_state.draw()
        self.window.blits(self.current_state.draw())
        pygame.display.flip()

    def change_state(self, state):
        '''This function changes current state of the game, old state is still
        still stored in memory.
        '''
        self.states[self.current_state.get_name()] = self.current_state
        self.current_state = self.states[state]
