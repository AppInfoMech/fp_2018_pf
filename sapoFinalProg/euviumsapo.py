import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 255, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
TruckSIZE = 25
TruckMINSPEED = 3
ADDNEWElementRATE = 80
PLAYERMOVERATE = 5

# Set up pygame and the window.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Eu vi um sapo')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('death.wav')
music = pygame.mixer.music.load('music.mp3')
WingameOverSound = pygame.mixer.Sound('victory.wav')


# Set up images and hitboxes.
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
TruckImage = pygame.image.load('truck.png')
LogImage = pygame.image.load('logs.png')
bg = pygame.image.load('bg.jpg')
lake = pygame.image.load('lake2.jpg')
lakeRect = lake.get_rect()
goal = pygame.image.load('goal.jpg')
goalRect = goal.get_rect()



def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

# Function for collision with trucks
def playerHasHitTruck(playerRect, Trucks):
    for b in Trucks:
        if playerRect.colliderect(b['rect']):
            return True
        if playerRect.colliderect(b['rect4']):
            return True
        
    return False


# Function for drowning detection
def checkDrown(playerRect, Logs, lakeRect):
    if playerRect.colliderect(lakeRect):
        for l in Logs:
            if playerRect.colliderect(l['rect1']):
                return False
            if playerRect.colliderect(l['rect2']):
                return False
            if playerRect.colliderect(l['rect3']):
                return False 
            else:
                return True 
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)




# Show the "Start" screen.
windowSurface.blit(bg, (0,0))
drawText('Eu vi um sapo', font, windowSurface, (WINDOWWIDTH / 3 + 5), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


while True:
    # Set up the start of the game.
    pygame.mixer.music.play(-1)
    Win = False
    Trucks = []
    Logs = []
    timer = 1000
    playerRect.topleft = (300,  WINDOWHEIGHT - 60)
    lakeRect.topleft = (0, 200)
    goalRect.topleft = (0, -30)
    moveLeft = moveRight = moveUp = moveDown = False
    ElementAddCounter = 79

    while True: # The game loop runs while the game part is playing.
        timer -= 1 # Decrease timer.

        windowSurface.blit(bg, (0,0))

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = True
                    moveRight = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False


        for l in Logs:
            if playerRect.colliderect(l['rect1']) and playerRect.right < WINDOWWIDTH:
                playerRect.move_ip(l['speed1'], 0)
            if playerRect.colliderect(l['rect2']) and playerRect.left > 0:
                playerRect.move_ip(l['speed2'], 0)
            if playerRect.colliderect(l['rect3']) and playerRect.left > 0:
                playerRect.move_ip(l['speed3'], 0)

        # Add new elements at the top of the screen, if needed.
        ElementAddCounter += 1
        if ElementAddCounter == ADDNEWElementRATE:
            ElementAddCounter = 0
            newTruck = {'rect': pygame.Rect(600, 475 - TruckSIZE, 120, 60),
                        'rect4': pygame.Rect(600, 115 - TruckSIZE, 120, 60),
                        'speed': -3,
                        'speed4': -7,
                        'surface': pygame.transform.scale(TruckImage, (120, 60)),
                        }

            Trucks.append(newTruck)


            newLog = {'rect1': pygame.Rect(-120, 295 - TruckSIZE, 120, 60),
                      'rect2': pygame.Rect(600, 370 - TruckSIZE, 120, 60),
                      'rect3': pygame.Rect(600, 220 - TruckSIZE, 120, 40),
                      'speed1': 6,
                      'speed2': -5,
                      'speed3': -4,
                      'surface': pygame.transform.scale(LogImage, (120, 60))
                    }
            Logs.append(newLog)

        # Move the player around.
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)

        # Move the Trucks.
        for b in Trucks:
            b['rect'].move_ip(b['speed'], 0)
            b['rect4'].move_ip(b['speed4'], 0)

        for l in Logs:
            l['rect1'].move_ip(l['speed1'], 0)
            l['rect2'].move_ip(l['speed2'], 0)
            l['rect3'].move_ip(l['speed3'], 0)
                
            

        # Delete Trucks that have fallen past the bottom.
        for b in Trucks[:]:
            if b['rect'].top > WINDOWWIDTH:
                Trucks.remove(b)

        # Draw the game world on the window.
        windowSurface.blit(bg, (0,0))


        # Draw lake 
        windowSurface.blit(lake, (0, 200))
        

        # Draw finish line/goal
        windowSurface.blit(goal, goalRect)
        
            
        # Draw each Truck.
        for b in Trucks:
            windowSurface.blit(b['surface'], b['rect'])
            windowSurface.blit(b['surface'], b['rect4'])


        # Draw logs
        for l in Logs:
            windowSurface.blit(l['surface'], l['rect1'])
            windowSurface.blit(l['surface'], l['rect2'])
            windowSurface.blit(l['surface'], l['rect3'])

        
        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect) 

        # Draw timer
        drawText('Timer: %s' % (timer), font, windowSurface, 10, 0)
        

        pygame.display.update()

        # Checking for collisions. 
        # Trucks 
        if playerHasHitTruck(playerRect, Trucks):
            break      

        # Drowning
        if checkDrown(playerRect, Logs, lakeRect):
            break
    
        # Goal
        if playerRect.colliderect(goalRect):
            Win = True
            break

        # Checks if timer has ran out   
        if timer == 0:
                    break

        mainClock.tick(FPS)

        

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    if Win == True:
        WingameOverSound.play()

        drawText('YOU WIN', font, windowSurface, (WINDOWWIDTH / 3 + 25), (WINDOWHEIGHT / 3) + 50)
        drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 100)
        pygame.display.update()
        waitForPlayerToPressKey()
        
        WingameOverSound.stop()
    else:    
        
        gameOverSound.play()

        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3 - 10), (WINDOWHEIGHT / 3) + 50)
        drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 100)
        pygame.display.update()
        waitForPlayerToPressKey()
        gameOverSound.stop()
    


