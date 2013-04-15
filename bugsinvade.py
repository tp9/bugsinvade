#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing pygame modules
import random, sys, pygame, time, os
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
BULLETFIREDFREQ = .50
MOVERATE = 9
BGCOLOR         = (0, 0, 0)

def main():
    global DISPLAYSURF, FPSCLOCK
    
    os.environ['SDL_VIDEO_WINDOW_POS'] = "5,25"
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Bugs Attack!")

    while True:
        runGame()
        
def runGame():
    ship = SpriteStripAnim('invader.png', (204,154,18,10), 1, 1)
    shipWidth = ship.getWidth() * FACTOR
    shipHeight = ship.getHeight() * FACTOR
    bug1 = SpriteStripAnim('invader.png', (0, 144, 18, 10), 2, 1, True, 23)
    bug1Width = bug1.getWidth() * FACTOR
    bug1Height = bug1.getHeight() * FACTOR
    block = SpriteStripAnim('invader.png', (0,166,32,20), 5, 1)
    blockWidth = block.getWidth() * 2
    blockHeight = block.getHeight() * 2
    bulletImg = SpriteStripAnim('invader.png', (89, 188, 10, 10), 1, 1)
    bulletWidth = bulletImg.getWidth() * 2
    bulletHeight = bulletImg.getHeight() * 2
    bug1_x = 0
    bug1_y = 0
    ship_x = 0
    bullets = []
    lastMoveSideways = time.time()
    lastBulletFired = time.time() - BULLETFIREDFREQ
    
    bugMoveRight = True
    shipMoveLeft = False
    shipMoveRight = False
    
    while True:
        checkForQuit()
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(pygame.transform.scale(ship.images[0], (shipWidth,shipHeight)), (ship_x, WINDOWHEIGHT - (shipHeight + 1)))        
        DISPLAYSURF.blit(pygame.transform.scale(bug1.next(), (bug1Width,bug1Height)), (bug1_x, bug1_y))
        DISPLAYSURF.blit(pygame.transform.scale(block.images[0], (blockWidth, blockHeight)), (75, 550))
        DISPLAYSURF.blit(pygame.transform.scale(block.images[0], (blockWidth, blockHeight)), (215, 550))
        DISPLAYSURF.blit(pygame.transform.scale(block.images[0], (blockWidth, blockHeight)), (350, 550))
        pygame.display.flip()
        
        #event handler
        for event in pygame.event.get():
            #keyboard handler
            if event.type == KEYDOWN:
                # left and right keys
                if (event.key == K_LEFT) and (ship_x > 0):
                    shipMoveLeft = True
                    shipMoveRight = False                    
                elif (event.key == K_RIGHT) and (ship_x < WINDOWWIDTH - shipWidth):
                    shipMoveRight = True
                    shipMoveLeft = False
                # space bar
                if event.key == K_SPACE and time.time() - lastBulletFired > BULLETFIREDFREQ:
                    newBullet = {'surface':pygame.transform.scale(bulletImg.images[0], (bulletWidth,bulletHeight)),
                            'x': ship_x + 25,
                            'y': WINDOWHEIGHT - (shipHeight + 1)}                
                    bullets.append(newBullet)
                    # bullets.append([ship_x + 25, WINDOWHEIGHT - (shipHeight + 1)])
                    lastBulletFired = time.time()
            # releasing left and right keys
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    shipMoveLeft = False
                elif event.key == K_RIGHT:
                    shipMoveRight = False

        #move ship
        if ship_x <= 0:
            shipMoveLeft = False
        elif ship_x >= (WINDOWWIDTH - shipWidth):
            shipMoveRight = False
        if shipMoveLeft:
            ship_x -= MOVERATE
        elif shipMoveRight:
            ship_x += MOVERATE
            
        #move bullets
        if bullets != []:
            for i, bullet in enumerate(bullets[:]):
                DISPLAYSURF.blit(bullet['surface'], (bullet['x'], bullet['y']))
                # DISPLAYSURF.blit(pygame.transform.scale(bulletImg.images[0], (bulletWidth,bulletHeight)), (bullet[0], bullet[1]))        
                bullet['y'] -= MOVERATE
                if bullet['y'] < 0:
                    bullets.remove(bullet)
                # elif bulletImg.colliderect(bug1.rect):
                    # bullets.remove(bullet)
                    # del bug1
                
        #move bug
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