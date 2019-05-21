# TODO: cleanup imports
import pygame

from game.game_state import GameStateName
from game.game_state import MenuState
from game.game_state import RunningState
from game.game_state import PauseState

class GameManager:
    '''State manager handle game states as menu, pause, actual running game and
    also window that draw graphics.
    '''
    def __init__(self, window):
        self.states = {
            GameStateName.MENU: MenuState(),
            GameStateName.PAUSE: PauseState(),
            GameStateName.RUNNING: RunningState(),
        }
        self.current_state = self.states[GameStateName.RUNNING]
        self.window = window

    def update(self):
        self.current_state.key_pressed(pygame.key.get_pressed())
        self.current_state.update()

    def draw(self):
        self.window.fill((0, 0, 0))
        to_draw = self.current_state.draw()
        self.window.blit(to_draw[0], to_draw[1])
        pygame.display.flip()

    def change_state(self, state):
        '''This function changes current state of the game, old state is still
        still stored in memory.
        '''
        self.states[self.current_state.get_name()] = self.current_state
        self.current_state = self.states[state]
