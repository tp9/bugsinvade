#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing pygame modules
import random, sys, pygame, time
from pygame.locals import *
from sprite_strip_anim import SpriteStripAnim

WINDOWWIDTH     = 480
WINDOWHEIGHT    = 640
FPS             = 30
BUGMOVEH        = 20
BUGMOVEV        = 20
BUGWIDTH        = 62
FACTOR          = 4
MOVESIDEWAYSFREQ= .75
MOVERATE = 9
BGCOLOR         = (0, 0, 0)

def main():
    global DISPLAYSURF, FPSCLOCK
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Bugs Attack!")

    while True:
        runGame()
        
def runGame():
    ship = SpriteStripAnim('img\invader.png', (204,154,18,10), 1, 1)
    shipWidth = ship.getWidth() * FACTOR
    shipHeight = ship.getHeight() * FACTOR
    bug1 = SpriteStripAnim('img\invader.png', (0, 144, 18, 10), 2, 1, True, 23)
    bug1Width = bug1.getWidth() * FACTOR
    bug1Height = bug1.getHeight() * FACTOR
    block = SpriteStripAnim('img\invader.png', (0,166,32,20), 5, 1)
    blockWidth = block.getWidth() * 2
    blockHeight = block.getHeight() * 2
    bug1_x = 0
    bug1_y = 0
    ship_x = 0
    lastMoveSideways = time.time()
    bugMoveRight = True
    shipMoveLeft = False
    shipMoveRight = False
    
    while True:
        checkForQuit()
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(pygame.transform.scale(ship.images[0], (shipWidth,shipHeight)), (ship_x, WINDOWHEIGHT - (shipHeight + 1)))        
        DISPLAYSURF.blit(pygame.transform.scale(bug1.next(), (bug1Width,bug1Height)), (bug1_x, bug1_y))
        DISPLAYSURF.blit(pygame.transform.scale(block.images[0], (blockWidth, blockHeight)), (50, 550))
        DISPLAYSURF.blit(pygame.transform.scale(block.images[0], (blockWidth, blockHeight)), (150, 550))
        DISPLAYSURF.blit(pygame.transform.scale(block.images[0], (blockWidth, blockHeight)), (250, 550))
        DISPLAYSURF.blit(pygame.transform.scale(block.images[0], (blockWidth, blockHeight)), (350, 550))
        pygame.display.flip()
        #event handler
        for event in pygame.event.get():
            #keyboard handler
            if event.type == KEYDOWN:
                if (event.key == K_LEFT) and (ship_x > 0):
                    shipMoveLeft = True
                    shipMoveRight = False                    
                elif (event.key == K_RIGHT) and (ship_x < WINDOWWIDTH - shipWidth):
                    shipMoveRight = True
                    shipMoveLeft = False
                else:
                    shipMoveRight = False
                    shipMoveLeft = False
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    shipMoveLeft = False
                elif event.key == K_RIGHT:
                    shipMoveRight = False

        #move ship
        #check position of ship
        if ship_x <= 0:
            shipMoveLeft = False
        elif ship_x >= (WINDOWWIDTH - shipWidth):
            shipMoveRight = False
        if shipMoveLeft:
            ship_x -= MOVERATE
        elif shipMoveRight:
            ship_x += MOVERATE
                
        if (time.time() - lastMoveSideways) > MOVESIDEWAYSFREQ:
            if bug1_x + BUGMOVEH > WINDOWWIDTH - bug1Width:
                bugMoveRight = False
            elif bug1_x - BUGMOVEH < 0:
                bugMoveRight = True
            if bugMoveRight:
                bug1_x += BUGMOVEH
            else:
                bug1_x -= BUGMOVEH
                
            lastMoveSideways = time.time()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def checkForQuit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()


if __name__ == "__main__": #This calls the game loop
    main()