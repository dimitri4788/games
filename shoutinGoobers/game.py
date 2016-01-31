'''
    File:           game.py
    Author:         Deep Aggarwal
    Description:    The main file where the game starts
'''

import pygame
from pygame.locals import *
import board


def main(argc=None, argv=None):
    """The main module where the game starts."""

    # Initialize all imported Pygame modules
    pygame.init()

    # Create a board object
    boardObj = board.Board()

    # Start the game and keep it running
    while(1):
        boardObj.update()

if __name__ == "__main__":
    main()
