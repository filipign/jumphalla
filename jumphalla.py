#!/usr/bin/env python3
'''It's main file that starts game application'''
from game.game import Game


def main():
    game = Game()
    game.run()
    input("Press any key to exit")

if __name__ == '__main__':
    main()
