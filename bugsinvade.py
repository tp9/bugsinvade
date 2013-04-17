#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing pygame modules
import random, sys, pygame, time, os
from pygame.locals import *
from sprite_strip_anim import SpriteStripAnim

WINDOWWIDTH     = 640
WINDOWHEIGHT    = 480
FPS             = 30
BUGMOVEH        = 20
BUGMOVEV        = 20
BUGSPACE        = 80
BUGROWHEIGHT    = 50
BUGBOUNDARY     = WINDOWHEIGHT - 100
BLOCKSPACE      = 200
FACTOR          = 3
MOVERATE        = 9
BULLETSPEED     = 9
BGCOLOR         = (0, 0, 0)
TEXTSHADOWCOLOR = (185,185,185)
TEXTCOLOR       = (255,255,255)


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
        showGameOverScreen()

        
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
    bugSprite = SpriteStripAnim('invader.png', (0, 144, 18, 10), 2, 1, True, 23)
    bugWidth = bugSprite.getWidth() * FACTOR
    bugHeight = bugSprite.getHeight() * FACTOR
    bugs = []
    for bugRow in range(5):
        bugs.append([])
        for bug in range(6):
            bugs[bugRow].append({'surface': pygame.transform.scale(bugSprite.images[0], (bugWidth,bugHeight)),
                        'image': 0,
                        'x': 0 + (bug * BUGSPACE),
                        'y': bugRow * BUGROWHEIGHT
            })
            
    # make blocks
    blockSprite = SpriteStripAnim('invader.png', (0,166,33,20), 5, 1)
    blockWidth = blockSprite.getWidth() * FACTOR
    blockHeight = blockSprite.getHeight() * FACTOR
    blocks = []
    for i in range(3):
        blocks.append({'surface':pygame.transform.scale(blockSprite.images[0], (blockWidth, blockHeight)),
                       'rect':pygame.Rect((75 + (i * BLOCKSPACE), WINDOWHEIGHT - 100, blockWidth, blockHeight)),
                       'image':0})
                       
    # set initial timers and movement directions
    lastMoveSideways = time.time()
    roundTimer = time.time()
    bugMoveFreq = .75
    bugMoveRight = True
    bugMoveDown = False
    shipMoveLeft = False
    shipMoveRight = False
    
    while True:
        checkForQuit()
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(pygame.transform.scale(ship.images[0], (shipWidth,shipHeight)), (ship_x, WINDOWHEIGHT - (shipHeight + 1)))
        for bugRow in bugs:
            for bug in bugRow:
                bug['rect'] = pygame.Rect((bug['x'],
                                bug['y'],
                                bugWidth,
                                bugHeight))
                DISPLAYSURF.blit(bug['surface'], bug['rect'])
        for block in blocks:
            DISPLAYSURF.blit(block['surface'], block['rect'])
            
        pygame.display.flip()
                
        # event handler
        for event in pygame.event.get():
            # keyboard handler
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
                            'x': ship_x + 22,
                            'y': WINDOWHEIGHT - (shipHeight + 1)})
            # releasing left and right keys
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    shipMoveLeft = False
                elif event.key == K_RIGHT:
                    shipMoveRight = False

        # move ship
        if ship_x <= 0:
            shipMoveLeft = False
        elif ship_x >= (WINDOWWIDTH - shipWidth):
            shipMoveRight = False
        if shipMoveLeft:
            ship_x -= MOVERATE
        elif shipMoveRight:
            ship_x += MOVERATE
            
        # move bullets
        if bullets != []:
            for bullet in bullets[:]:
                bullet['rect'] = pygame.Rect((bullet['x'],
                                bullet['y'],
                                bulletWidth,
                                bulletHeight))
                DISPLAYSURF.blit(bullet['surface'], bullet['rect'])
                if bullet['y'] < 0:
                    bullets.remove(bullet)
                else: # collision detection
                    bugHit = False
                    for bugsRow in range(len(bugs)-1, -1, -1):
                        if bugHit:
                            break
                        for bug in bugs[bugsRow][:]:
                            if bullet['rect'].colliderect(bug['rect']) and not bugHit:
                                bullets.remove(bullet)
                                bugs[bugsRow].remove(bug)
                                if bugs[bugsRow] == []:
                                    del bugs[bugsRow]
                                bugHit = True # break after hitting first bug
                            elif bugHit:
                                break
                    for block in blocks[:]:
                        if bullet['rect'].colliderect(block['rect']):
                            bullets.remove(bullet)
                            if block['image'] < 4:
                                block['image'] += 1
                                block['surface'] = pygame.transform.scale(blockSprite.images[block['image']], (blockWidth,blockHeight))
                            elif block['image'] == 4:
                                blocks.remove(block)
                    if bullets != []:
                        bullet['y'] -= BULLETSPEED
                
        # check roundTimer
        if time.time() - roundTimer > 10 and bugMoveFreq > .15:
            bugMoveFreq -= .15
            roundTimer = time.time()
            
        # move bugs
        if (time.time() - lastMoveSideways) > bugMoveFreq and bugs != []:
            if len(bugs[0]) > 0 or len(bugs[1]) > 0 or len(bugs[2]) > 0:
                # set bug direction
                max_X = 0
                min_X = WINDOWWIDTH
                for bugRow in range(len(bugs)):
                    max_X = max(bugs[bugRow][len(bugs[bugRow])-1]['x'], max_X)
                    min_X = min(bugs[bugRow][0]['x'], min_X)
                if max_X + BUGMOVEH > WINDOWWIDTH - bugWidth:
                    bugMoveRight = False
                    bugMoveDown = True
                elif min_X - BUGMOVEH < 0:
                    bugMoveRight = True
                    bugMoveDown = True
            for bugsRow in bugs:
                for bug in bugsRow:
                    if bugMoveDown:
                        bug['y'] += BUGMOVEV
                        if bug['y'] > BUGBOUNDARY:
                            return
                    if bugMoveRight:
                        bug['x'] += BUGMOVEH
                    else:
                        bug['x'] -= BUGMOVEH
                    # alternate animation
                    if bug['image'] == 0:
                        bug['image'] = 1
                    else:
                        bug['image'] = 0
                    bug['surface'] = pygame.transform.scale(bugSprite.images[bug['image']], (bugWidth,bugHeight))
            if bugMoveDown:
                bugMoveDown = False
            lastMoveSideways = time.time()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        
def showGameOverScreen():
    titleSurf = pygame.font.Font('freesansbold.ttf', 100).render('Game Over', True, TEXTSHADOWCOLOR)
    titleRect = titleSurf.get_rect()
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    titleSurf = pygame.font.Font('freesansbold.ttf', 100).render('Game Over', True, TEXTCOLOR)
    titleRect = titleSurf.get_rect()
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    pressKeySurf = pygame.font.Font('freesansbold.ttf', 18).render('Press a key to play.', True, TEXTCOLOR)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    
    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

        
def checkForKeyPress():
    checkForQuit()
    
    for event in pygame.event.get([KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]):
        if event.type in (KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION):
            continue
        return event.key
    return None
    
    
def checkForQuit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    

if __name__ == "__main__":
    main()