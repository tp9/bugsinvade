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
BUGSPACE        = 50
BUGROWHEIGHT    = 50
BLOCKSPACE      = 140
FACTOR          = 3
MOVESIDEWAYSFREQ= .75
BULLETFIREDFREQ = .50
MOVERATE = 9
BGCOLOR         = (0, 0, 0)

def main():
    global DISPLAYSURF, FPSCLOCK
    # set initial position of the game window
    os.environ['SDL_VIDEO_WINDOW_POS'] = "5,40"
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Bugs Invade!")

    while True:
        runGame()
        
def runGame():
    ship = SpriteStripAnim('invader.png', (204,154,18,10), 1, 1)
    shipWidth = ship.getWidth() * FACTOR
    shipHeight = ship.getHeight() * FACTOR
    bulletImg = SpriteStripAnim('invader.png', (89, 188, 10, 10), 1, 1)
    bulletWidth = bulletImg.getWidth()
    bulletHeight = bulletImg.getHeight()
    ship_x = 0
    bullets = []
    # make bugs
    bug1Sprite = SpriteStripAnim('invader.png', (0, 144, 18, 10), 2, 1, True, 23)
    bugWidth = bug1Sprite.getWidth() * FACTOR
    bugHeight = bug1Sprite.getHeight() * FACTOR
    bugsRow1 = makeBugRow(bug1Sprite.images[0], 0, bugWidth, bugHeight)
    bug2Sprite = SpriteStripAnim('invader.png', (0, 144, 18, 10), 2, 1, True, 23)
    bugsRow2 = makeBugRow(bug1Sprite.images[0], 1, bugWidth, bugHeight)
    bug3Sprite = SpriteStripAnim('invader.png', (0, 144, 18, 10), 2, 1, True, 23)
    bugsRow3 = makeBugRow(bug1Sprite.images[0], 2, bugWidth, bugHeight)
    # make blocks
    blockSprite = SpriteStripAnim('invader.png', (0,166,33,20), 5, 1)
    blockWidth = blockSprite.getWidth() * 2
    blockHeight = blockSprite.getHeight() * 2
    blocks = []
    for i in range(3):
        blocks.append({'surface':pygame.transform.scale(blockSprite.images[0], (blockWidth, blockHeight)),
                       'rect':pygame.Rect((75 + (i * BLOCKSPACE), 550, blockWidth, blockHeight)),
                       'image':0,
                       'x':75 + (i * BLOCKSPACE),
                       'y':550})
    # set initial timers
    lastMoveSideways = time.time()
    lastBulletFired = time.time() - BULLETFIREDFREQ
    
    bugMoveRight = True
    shipMoveLeft = False
    shipMoveRight = False
    
    while True:
        checkForQuit()
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(pygame.transform.scale(ship.images[0], (shipWidth,shipHeight)), (ship_x, WINDOWHEIGHT - (shipHeight + 1)))
        for bug in bugsRow1:
            bug['rect'] = pygame.Rect((bug['x'],
                            bug['y'],
                            bugWidth,
                            bugHeight))
            DISPLAYSURF.blit(bug['surface'], bug['rect'])
        for bug in bugsRow2:
            bug['rect'] = pygame.Rect((bug['x'],
                            bug['y'],
                            bugWidth,
                            bugHeight))
            DISPLAYSURF.blit(bug['surface'], bug['rect'])
        for bug in bugsRow3:
            bug['rect'] = pygame.Rect((bug['x'],
                            bug['y'],
                            bugWidth,
                            bugHeight))
            DISPLAYSURF.blit(bug['surface'], bug['rect'])
        for block in blocks:
            DISPLAYSURF.blit(block['surface'], block['rect'])
            
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
                if event.key == K_SPACE and bullets == []:
                    bullets.append({'surface':pygame.transform.scale(bulletImg.images[0], (bulletWidth,bulletHeight)),
                            'x': ship_x + 25,
                            'y': WINDOWHEIGHT - (shipHeight + 1)})
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
        # assert(1==2)
        #removed cloning to test bug
        if bullets != []:
            for bullet in bullets[:]:
                bullet['rect'] = pygame.Rect((bullet['x'],
                                bullet['y'],
                                bulletWidth,
                                bulletHeight))
                DISPLAYSURF.blit(bullet['surface'], bullet['rect'])
                # bullet['y'] -= MOVERATE
                if bullet['y'] < 0:
                    bullets.remove(bullet)
                    print "Test"
                else:
                    for bug in bugsRow1[:]:
                        if bullet['rect'].colliderect(bug['rect']):
                            bullets.remove(bullet)
                            bugsRow1.remove(bug)
                            break # break after hitting first bug
                    for block in blocks[:]:
                        if bullet['rect'].colliderect(block['rect']):
                            bullets.remove(bullet)
                            if block['image'] < 4:
                                block['image'] += 1
                                block['surface'] = pygame.transform.scale(blockSprite.images[block['image']], (blockWidth,blockHeight))
                            elif block['image'] == 4:
                                blocks.remove(block)
                    if bullets != []:
                        bullet['y'] -= MOVERATE
                
        #move bug
        if (time.time() - lastMoveSideways) > MOVESIDEWAYSFREQ:
            if len(bugsRow1) > 0:
                # set bug direction
                if max(
                        bugsRow1[len(bugsRow1)-1]['x'],
                        bugsRow2[len(bugsRow2)-1]['x'],
                        bugsRow3[len(bugsRow3)-1]['x']
                        ) + BUGMOVEH > WINDOWWIDTH - bugWidth:
                    bugMoveRight = False
                elif min(
                        bugsRow1[0]['x'],
                        bugsRow2[0]['x'],
                        bugsRow3[0]['x']
                        ) - BUGMOVEH < 0:
                    bugMoveRight = True
            for bug in bugsRow1:
                if bugMoveRight:
                    bug['x'] += BUGMOVEH
                else:
                    bug['x'] -= BUGMOVEH
                # alternate animation
                if bug['image'] == 0:
                    bug['image'] = 1
                else:
                    bug['image'] = 0
                bug['surface'] = pygame.transform.scale(bug1Sprite.images[bug['image']], (bugWidth,bugHeight))
            for bug in bugsRow2:
                if bugMoveRight:
                    bug['x'] += BUGMOVEH
                else:
                    bug['x'] -= BUGMOVEH
                # alternate animation
                if bug['image'] == 0:
                    bug['image'] = 1
                else:
                    bug['image'] = 0
                bug['surface'] = pygame.transform.scale(bug1Sprite.images[bug['image']], (bugWidth,bugHeight))
            for bug in bugsRow3:
                if bugMoveRight:
                    bug['x'] += BUGMOVEH
                else:
                    bug['x'] -= BUGMOVEH
                # alternate animation
                if bug['image'] == 0:
                    bug['image'] = 1
                else:
                    bug['image'] = 0
                bug['surface'] = pygame.transform.scale(bug1Sprite.images[bug['image']], (bugWidth,bugHeight))
            lastMoveSideways = time.time()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeBugRow(bugSprite, row, bugWidth, bugHeight):
    bugs = []
    for i in range(6):
        bugs.append({'surface': pygame.transform.scale(bugSprite, (bugWidth,bugHeight)),
                    'image': 0,
                    'x': 0 + (i * BUGSPACE),
                    'y': row * BUGROWHEIGHT
        })
    return bugs
        
def checkForQuit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    

if __name__ == "__main__": #This calls the game loop
    main()