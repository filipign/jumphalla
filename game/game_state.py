from abc import ABC, abstractmethod
from enum import Enum


class GameState(ABC):
    def __init__(self):
        self.name = 'abstract'
        self.current_background = 'current_background'

    @abstractmethod
    def update(self):
        pass

    def get_background(self):
        return self.current_background

    def get_name(self):
        return self.name


class GameStateName(Enum):
    MENU = 0
    RUNNING = 1
    PAUSE = 2

class MenuState(GameState):
    def __init__(self):
        self.name = GameStateName.MENU

    def update(self):
        pass


class RunningState(GameState):
    def __init__(self):
        self.name = GameStateName.RUNNING

    def update(self):
        pass


class PauseState(GameState):
    def __init__(self):
        self.name = GameStateName.PAUSE

    def update(self):
        pass
