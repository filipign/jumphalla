#!/usr/bin/env python3
'''It's main file that starts game application'''
import sys
sys.path.append('..')
from jumphalla.game.game import Game


def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
