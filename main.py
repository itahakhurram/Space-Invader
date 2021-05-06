import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('.vscode/icon_image/background.png')

#background music
mixer.music.load('.vscode/sound_effect/background_music.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('.vscode/icon_image/icon.png')
pygame.display.set_icon(icon)

# spaceship: player
playerimage = pygame.image.load('.vscode/icon_image/space_ship.png')
player_x = 370
player_y = 480
player_x_change = 0

def player(x,y):
    screen.blit(playerimage,(x,y))

# Enemy
enemyimage = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_count = 6

for i in range(enemy_count):
    enemyimage.append(pygame.image.load('.vscode/icon_image/enemy.png'))
    enemyimage.append(pygame.image.load('.vscode/icon_image/enemy_1.png'))
    enemyimage.append(pygame.image.load('.vscode/icon_image/enemy_2.png'))
    enemyimage.append(pygame.image.load('.vscode/icon_image/enemy_3.png'))
    enemyimage.append(pygame.image.load('.vscode/icon_image/enemy_4.png'))
    enemyimage.append(pygame.image.load('.vscode/icon_image/enemy_5.png'))
    enemy_x.append(random.randint(0,735))
    enemy_y.append(random.randint(50,150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyimage[i], (x,y))

# bullet
bulletimage = pygame.image.load('.vscode/icon_image/bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimage, (x + 16, y + 10))

def bullet_collision(enemy_x,enemy_y,bullet_x,bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x,2) + math.pow(enemy_y - bullet_y,2))
    if distance < 27:
        return True
    else:
        return False

#score
score = 0
font = pygame.font.Font('.vscode/font/leaf_font.ttf',32)
text_x = 10
text_y = 10

def show_score(x,y):
    score_display = font.render("Score: " + str(score),True,(255,255,255))
    screen.blit(score_display,(x,y))

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_message():
    game_over_display = game_over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(game_over_display,(200,250))

# Game loop
running = True
while running:
    
    # RGB: screen background
    screen.fill((102,178,255))
    screen.blit(background,(0,0))

    
    for event in pygame.event.get():

        # Exit
        if event.type == pygame.QUIT:
            running = False

        # Keystroke check
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5  
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('.vscode/sound_effect/laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x,bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Boundary check

    # Player     
    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy
    for i in range(enemy_count):

        # Game Over
        if enemy_y[i] > 440:
            for j in range(enemy_count):
                enemy_y[j] = 2000
            game_over_message()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

        # Collision
        collision = bullet_collision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        if collision:
            explosion_sound = mixer.Sound('.vscode/sound_effect/explosion.wav')
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            enemy_x[i] = random.randint(0,735)
            enemy_y[i] = random.randint(50,150)
        enemy(enemy_x[i],enemy_y[i],i)
    
    # Bullet movement
    if bullet_y <=0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bullet_x,bullet_y)
        bullet_y -= bullet_y_change

    player(player_x,player_y)
    show_score(text_x,text_y)

    pygame.display.update()