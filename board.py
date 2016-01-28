'''
    File:           board.py
    Author:         Deep Aggarwal
    Description:    A class to represent Board
'''

import math
import random
import sys

import pygame
from pygame.locals import *


class Board():
    """This class represents the board of the game."""

    def __init__(self):
        """Board class constructor."""

        # Initialize a screen for display
        width, height = 768, 512
        self.screen = pygame.display.set_mode((width, height))

        # Load graphics
        self.backgroundImage = pygame.image.load("resources/images/backgroundImage.png")
#backgroundImage.png
#cannon.png
#cannonOrig.jpg
#chocolateDrop.png
#chocolateDropOrig.jpg
#peanutOrig.png
#peanutWithChocolate.png
#peanut_higherResolution.png
#peanut_lowerOrig.png
#peanut_lowerResolution.png

        # Set the name on the window
        pygame.display.set_caption("Shootin' Goobers")

        # Set board start: start or update
        self.state = "start"

    #def draw(self):

    def start(self):
        """This function displayes the game's start menu."""

        while(1):
            # Create font
            startFont = pygame.font.SysFont(None, 80)

            # Create text surface
            startLabel = startFont.render("Press spacebar to start!", 1, (255, 255, 255))

            # Draw surface
            self.screen.blit(startLabel, (60, 200))

            # Loop through the events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        self.state = "update"
                        return

            # Update the contents of the entire display
            pygame.display.flip()

    def update(self):
        """This function updates the board."""

        # Clear the screen
        self.screen.fill(0)

        if self.state == "start":
            self.start()

        self.screen.blit(self.backgroundImage, (0, 0))

        #Draw the board

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()
