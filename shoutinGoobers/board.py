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

# Global variables
peanutTimer = 100
peanutTimerFaster = 0


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

        # Set initial position of cannon
        self.cannonPosition = [344, 393]

        # Set initial state of keys (K_a and K_d): [K_a: False, K_d: False]
        self.keysState = [False, False]

        # Set the initial position of the first evil peanut
        self.peanuts = [[40, 0]]

        # Peanuts hit by chocolate drop
        self.peanutsGotHit = []

        # Chocolate drops
        self.chocolateDrops = []

        # Set the name on the window
        pygame.display.set_caption("Shootin' Goobers")

        # Set board start: start or update
        self.state = "start"

        # Load graphics
        self.backgroundImage = pygame.image.load("resources/images/backgroundImage.png")
        self.cannonImage = pygame.image.load("resources/images/cannon.png")
        self.chocolateDropImage = pygame.image.load("resources/images/chocolateDrop.png")
        self.peanutOrigImage = pygame.image.load("resources/images/peanutOrig.png")
        self.peanutWithChocolateImage = pygame.image.load("resources/images/peanutWithChocolateSmall.png")
        self.scorePanelImage = pygame.image.load("resources/images/scorePanel.png")

        # Load audio files
        self.hit = pygame.mixer.Sound("resources/audio/hit.wav")
        self.hit.set_volume(0.05)

    def start(self):
        """This function displays the game's start menu."""

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
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        self.state = "update"
                        return

            # Update the contents of the entire display
            pygame.display.flip()

    def end(self):
        """This function displays the gameover message."""

        while(1):
            # Create font
            startFont = pygame.font.SysFont(None, 80)

            # Create text surface
            startLabel = startFont.render("Game Over!", 1, (255, 255, 255))

            # Draw surface
            self.screen.blit(startLabel, (210, 200))

            # Loop through the events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_q:
                        pygame.quit()
                        sys.exit()

            # Update the contents of the entire display
            pygame.display.flip()

    def update(self):
        """This function updates the board."""

        # Make global variables accessible
        global peanutTimer
        global peanutTimerFaster
        peanutTimer -= 1

        # Clear the screen
        self.screen.fill(0)

        # If board state is start, show the start menu
        if self.state == "start":
            self.start()

        # Set the background image
        self.screen.blit(self.backgroundImage, (0, 0))

        # Set the cannon
        self.screen.blit(self.cannonImage, (self.cannonPosition[0], self.cannonPosition[1]))

        # 6.2 - Draw chocolateDrops
        for cdrop in self.chocolateDrops:
            index = 0
            cdrop[1] -= 7
            for projectile in self.chocolateDrops:
                self.screen.blit(self.chocolateDropImage, (projectile[0], projectile[1]))

        # Let the evil peanuts fall on kind-hearted cannon
        if peanutTimer == 0:
            self.peanuts.append([random.randint(0, self.backgroundImage.get_width()-40), 0])
            peanutTimer = 100 - (peanutTimerFaster*2)
            if peanutTimerFaster >= 36:
                peanutTimerFaster = 36
            else:
                peanutTimerFaster += 3
        index = 0
        for peanut in self.peanuts:
            if peanut[1] > self.backgroundImage.get_height():
                self.peanuts.pop(index)
            peanut[1] += 2

            # Attack the nice cannon
            peanutRect = pygame.Rect(self.peanutOrigImage.get_rect())
            peanutRect.top = peanut[1]
            peanutRect.left = peanut[0]
            if peanutRect.top > self.backgroundImage.get_height():
                self.peanuts.pop(index)

            # Check for collisions of chocolateDrop and peanut
            index1 = 0
            for cdrop in self.chocolateDrops:
                bullrect = pygame.Rect(self.chocolateDropImage.get_rect())
                bullrect.left = cdrop[0]
                bullrect.top = cdrop[1]
                if peanutRect.colliderect(bullrect):
                    self.hit.play()
                    self.peanuts.pop(index)
                    self.peanutsGotHit.append(self.peanutWithChocolateImage)
                    self.chocolateDrops.pop(index1)
                    self.score += 1
                index1 += 1

            # Next evil peanut
            index += 1

        for peanut in self.peanuts:
            self.screen.blit(self.peanutOrigImage, peanut)

        # Set the score panel
        for i in range(int(math.ceil(self.height/float(self.scorePanelImage.get_height())))):
            self.screen.blit(self.scorePanelImage, (self.backgroundImage.get_width(), self.scorePanelImage.get_height()*i))
            self.screen.blit(self.scorePanelImage, (self.backgroundImage.get_width() + self.scorePanelImage.get_width(), self.scorePanelImage.get_height()*i))

        # Draw clock
        clockFont = pygame.font.Font(None, 44)
        clockText = clockFont.render(str((180000-pygame.time.get_ticks())/60000)+":"+str((180000-pygame.time.get_ticks())/1000 % 60).zfill(2), True, (255, 255, 255))
        textRect = clockText.get_rect()
        textRect.topright = [875, 55]
        self.screen.blit(clockText, textRect)

        # Show player score
        scoreFont = pygame.font.SysFont(None, 44)
        scoreIntegerFont = pygame.font.SysFont(None, 35)
        scoreText = scoreFont.render("Score", 1, (255, 255, 255))
        myScore = scoreIntegerFont.render(str(self.score), 1, (255, 255, 255))
        self.screen.blit(scoreText, (805, 425))
        self.screen.blit(myScore, (840, 465))

        # When a peanut gets hit by chocolateDrop, add it to the side panel
        hIndex = 771
        vIndex = 280
        if self.peanutsGotHit:
            for p in self.peanutsGotHit:
                if(hIndex > 900):
                    hIndex = 771
                    vIndex += 35
                if(vIndex > 400):
                    self.end()
                self.screen.blit(self.peanutWithChocolateImage, (hIndex, vIndex))
                hIndex += 17

        # Display game name on sidebar
        gameNameFont = pygame.font.Font("resources/fonts/xCelsion.ttf", 20)
        gameNameText1 = gameNameFont.render("Shootin'", 1, (125, 255, 155))
        gameNameText2 = gameNameFont.render("Goobers", 1, (125, 255, 155))
        self.screen.blit(gameNameText1, (780, 225))
        self.screen.blit(gameNameText2, (778, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == K_a:
                    self.keysState[0] = True
                if event.key == K_d:
                    self.keysState[1] = True
                if event.key == K_RSHIFT:
                    position = pygame.mouse.get_pos()
                    self.chocolateDrops.append([self.cannonPosition[0]+22, self.cannonPosition[1]])
            if event.type == pygame.KEYUP:
                if event.key == K_a:
                    self.keysState[0] = False
                if event.key == K_d:
                    self.keysState[1] = False

        # Move the cannon if the keys A or D are pressed
        if self.keysState[0]:
            if self.cannonPosition[0] >= -10:
                self.cannonPosition[0] -= 5
        if self.keysState[1]:
            if self.cannonPosition[0] <= (self.backgroundImage.get_width()-70):
                self.cannonPosition[0] += 5

        # Update the full display Surface to the screen
        pygame.display.flip()
