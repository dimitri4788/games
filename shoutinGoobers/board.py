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
        self.width = 924
        self.height = 512
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Set initial score to zero
        self.score = 0

        # Load graphics
        self.backgroundImage = pygame.image.load("resources/images/backgroundImage.png")
        self.cannon = pygame.image.load("resources/images/cannon.png")
        self.chocolateDrop = pygame.image.load("resources/images/chocolateDrop.png")
        self.peanutOrig = pygame.image.load("resources/images/peanutOrig.png")
        self.peanutWithChocolate = pygame.image.load("resources/images/peanutWithChocolate.png")
        self.scorePanel = pygame.image.load("resources/images/scorePanel.png")

        # Set the name on the window
        pygame.display.set_caption("Shootin' Goobers")

        # Set board start: start or update
        self.state = "start"

    def start(self):
        """This function displayes the game's start menu."""

        while(1):
            # Create font
            startFont = pygame.font.SysFont(None, 80)

            # Create text surface
            startLabel = startFont.render("Press spacebar to start!", 1, (255, 255, 255))

            # Draw surface
            self.screen.blit(startLabel, (140, 200))

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

        # If board state is start, show the start menu
        if self.state == "start":
            self.start()

        # Set the background image
        self.screen.blit(self.backgroundImage, (0, 0))

        # Set the score panel
        for i in range(int(math.ceil(self.height/float(self.scorePanel.get_height())))):
            self.screen.blit(self.scorePanel, (self.backgroundImage.get_width(), self.scorePanel.get_height()*i))
            self.screen.blit(self.scorePanel, (self.backgroundImage.get_width() + self.scorePanel.get_width(), self.scorePanel.get_height()*i))

        # Draw clock
        clockFont = pygame.font.Font(None, 44)
        clockText = clockFont.render(str((180000-pygame.time.get_ticks())/60000)+":"+str((180000-pygame.time.get_ticks())/1000%60).zfill(2), True, (255, 255, 255))
        textRect = clockText.get_rect()
        textRect.topright = [870, 35]
        self.screen.blit(clockText, textRect)

        #TODO show score too

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()
