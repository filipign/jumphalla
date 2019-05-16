# TODO: cleanup imports
from game.game_state import GameStateName
from game.game_state import MenuState
from game.game_state import RunningState
from game.game_state import PauseState


class GameManager:
    '''State manager handle game states as menu, pause, actual running game and
    also window that draw graphics.
    '''
    def __init__(self):
        self.states = {
            GameStateName.MENU: MenuState(),
            GameStateName.PAUSE: PauseState(),
            GameStateName.RUNNING: RunningState(),
        }
        self.current_state = self.states[GameStateName.MENU]

    def update(self):
        self.current_state.update()

    def change_state(self, state):
        '''This function changes current state of the game, old state is still
        stored in memory.
        '''
        self.states[self.current_state.get_name()] = self.current_state
        self.current_state = self.states[state]
