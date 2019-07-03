#!/usr/bin/env python3
'''It's main file that starts game application'''
import sys
sys.path.append('..')
from jumphalla.game.game import Game


def main():
    # Writes 0 to load proper config file
    with open('testing', 'w') as file_handler:
        file_handler.write('0')
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
