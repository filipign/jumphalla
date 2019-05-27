# TODO: cleanup imports
import pygame

from jumphalla.game import game_state


class GameManager:
    def __init__(self, window):
        '''GameManager handles game states as menu, pause, actual running game
        and also window that draw graphics.

        When GameManager object is initialized, it creates all game states and
        set current state to `Running`.

        Args:
            window (:obj:`Surface`): Initialized pygame window
        '''
        self.states = {
            game_state.GameStateName.MENU: game_state.MenuState(),
            game_state.GameStateName.PAUSE: game_state.PauseState(),
            game_state.GameStateName.RUNNING: game_state.RunningState(),
        }
        self.current_state = self.states[game_state.GameStateName.RUNNING]
        self.window = window

    def update(self):
        '''Calls update and key_pressed function on current state'''
        self.current_state.key_pressed(pygame.key.get_pressed())
        self.current_state.update()

    def draw(self):
        '''Fills window with sprites.

        First, whole window is painted with black color, then current state
        gather all necessery pairs of (image, coordinates) to draw images.
        '''
        self.window.fill((0, 0, 0))
        self.window.blits(self.current_state.draw())
        pygame.display.flip()

    def change_state(self, state):
        '''Changes current state of the game, old state is still
        stored in memory.

        Args:
            state (:obj:`GameState`): Game state that will be set as current
                state.
        '''
        self.states[self.current_state.get_name()] = self.current_state
        self.current_state = self.states[state]
