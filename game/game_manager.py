# TODO: cleanup imports
import json

import pygame

from jumphalla.game import game_state
from jumphalla.config import config


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
        self.current_state = self.states[game_state.GameStateName.MENU]
        self.window = window

    def update(self):
        '''Calls update and key_pressed function on current state'''
        if self.current_state == self.states[game_state.GameStateName.MENU]:
            if self.current_state.choosen_state != game_state.GameStateName.MENU:
                self.change_state(self.current_state.choosen_state)
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
        if state == game_state.GameStateName.LOAD:
            self.states[self.current_state.name] = self.current_state
            self.current_state = self.states[game_state.GameStateName.RUNNING]
            self.load_state(config['save'])
            return

        self.states[self.current_state.name] = self.current_state
        self.current_state = self.states[state]

    def load_state(self, path):
        '''Loads state of the game

        Args:
            path (str): Path to save file.
        '''
        state = {}
        with open(path, 'r') as file_handler:
            state = json.load(file_handler)
        self.current_state.load_state(state['x'], state['y'], state['level'])
