import pygame
import random  # For getting random co-ordinates for enemy pic
import math
from pygame import mixer # This is for all soundtracts and music etc

# Initialize the pygame
pygame.init()

# Create a screen to display the game.(width,height) of the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon of the game window.
pygame.display.set_caption("Space Invader")  # FOR TITLE
icon = pygame.image.load('Spaceshipicon.png')
pygame.display.set_icon(icon)

# Background
BackgroundImg = pygame.image.load('Backgroundimage.jpg')
pygame.display.set_icon(BackgroundImg)

# Background soundtrack
mixer.music.load('background.wav') # For a long track like a background track we use music.load.
mixer.music.play(-1)  # The -1 keeps the soundtrack playing continuously.
# But for a shorter sound like a bullet sound, we use Sound instead of music.load

# Player image
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
# The above two lines are the player co-ordinates.
player_change = 0

# Enemy image
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies =6
"""enemyImg = pygame.image.load('enemypic.png')
    enemyX = random.randint(0, 735)  # gets a random co-ordinate for enemypic
    enemyY = random.randint(50, 150)  # In the paranthesis we give a start value and an end value
    enemyX_change = 0.3
    enemyY_change = 40 # This is for a single enemy image"""
# For multiple enemy image
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('enemypic.png'))
    enemyX.append(random.randint(0, 735))  # gets a random co-ordinate for enemypic
    enemyY.append(random.randint(50, 150))  # In the paranthesis we give a start value and an end value
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_state = "ready"

# Score(displaying on the game window)
score_value=0
font = pygame.font.Font('freesansbold.ttf',32)

# Game Over Text:
over_font = pygame.font.Font('freesansbold.ttf',64)

textX = 10
textY = 10
# While showing the score, first we render the score and then we blit it on the screen
def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255,255,255)) # In render, the first value in the parameters is the text that we are putting in, then True, Then the colour.
    screen.blit(score, (x , y))

def game_over_text():
    over_text= over_font.render("GAME OVER", True, (255, 255,
                                                             255))  # In render, the first value in the parameters is the text that we are putting in, then True, Then the colour.
    screen.blit(over_text, (200,250))

def player(x, y):
    screen.blit(playerImg, (
        x, y))  # blit means to draw and with this function we are basically drawing the player icon on the screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state  # Since we are accessing an already created variable, we are  using global
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Checking whether the bullet and the enemy have collided or not
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# The two lines of code below are basically making the screen continue showing the result of the program.

running = True
# GAME LOOP
while running:

    # To change the background of our display screen we use :
    # Notice that this is put in an infinite while loop.
    # Also in the parameters values are RGB- Red, Green, Blue. The values go from 0-255
    screen.fill(((0, 0, 0)))
    # playerX+=0.5  This is increasing the co-ordinates due to which the playership is moving

    # Background Image
    screen.blit(BackgroundImg, (0,
                                0))  # When a background Image is added to the display screen, the players start moving slower than before. This is so because every time in the loop, the code has to load a heavy file.

    for event in pygame.event.get():  # The .event.get() function returns what event is taking place in the game.
        if event.type == pygame.QUIT:  # If the user has clicked the X icon, then we need to quit the display screen
            running = False
        # If keystroke is pressed then check whether it is right or left.
        if event.type == pygame.KEYDOWN:  # This just checks if a key is being pressed or not.
            # Checking which button is pressed.
            if event.key == pygame.K_LEFT:
                player_change = - 0.3  # Changing the co-ordinates of the icon
            if event.key == pygame.K_RIGHT:
                player_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play() # No -1 here because we don't want it to play in a loop
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0
    playerX += player_change  # Adding the co-ordinate change to player position
    # Checking for the boundary conditions.
    if playerX >= 736:  # 736 is used instead of 800 since we are considering the 64 px width of the spaceship
        playerX = 0
    elif playerX <= 0:
        playerX = 736

    """enemyX += enemyX_change
    if enemyX >= 736:  # For enemy
        enemyX_change = -0.3
        enemyY += enemyY_change
    elif enemyX <= 0:
        enemyX_change = 0.3
        enemyY += enemyY_change # If we were considering one enemy"""

    #For multiple enemy movement
    for i in range(no_of_enemies):

        # Game over condition
        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()  # This helps us write a game over text directly
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 736:  # For enemy
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision == True:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i] , enemyY[i] , i)
    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # Calling the player function so that we can see the player icon.
    # After the screen fill, it wont update and work unless we type in the code below
    show_score(textX , textY)
    pygame.display.update()  # This updates the display( Game window ) from time to time.
