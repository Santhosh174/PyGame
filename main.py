import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("space shooter")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
bg = pygame.image.load("bg.jpg")

mixer.music.load("background.wav")
mixer.music.play(-1)

#player
player_img = pygame.image.load("player.png")
playerx = 370
playery = 480
playerx_change = 0

#alien
alien_img = []
alienx = []
alieny = []
alienx_change = []
alieny_change = []
no_of_alien = 6

for i in range(no_of_alien):
    alien_img.append(pygame.image.load("alien.png"))
    alienx.append(random.randint(0,735))
    alieny.append(random.randint(50,150))
    alienx_change.append(1)
    alieny_change.append(40)

#bullet
bullet_img = pygame.image.load("bullet.png")
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 2
bullet_state = "ready"

#scoe
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textx = 10
texty = 10

over_font = pygame.font.Font("freesansbold.ttf",64)

def show_score(x,y):
    score = font.render("SCORE : "+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(player_img,(x,y))

def alien(x,y,i):
    screen.blit(alien_img[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img,(x + 16,y + 10))

def collision(alienx,alieny,bulletx,bullety):
    distance = math.sqrt((math.pow(alienx-bulletx,2))+(math.pow(alieny-bullety,2)))
    if distance<27:
        return True
    else:
        return False

def game_over():
    over = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over,(200,250))

running = True
while running:
    pass
    screen.fill((243,143,234))
    screen.blit(bg,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change -= 1
            if event.key == pygame.K_RIGHT:
                playerx_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(playerx,bullety)
            if event.key == pygame.K_q:
                running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
                
    #player movement                
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    #alien movement
    for i in range(no_of_alien):

        if alieny[i] > 465:
            for j in range(no_of_alien):
                alieny[j] = 2000
            game_over()
            break
        alienx[i] += alienx_change[i]
        if alienx[i] <= 0:
            alienx_change[i] = 1
            alieny[i] += alieny_change[i]
        elif alienx[i] >= 736:
            alienx_change[i] -= 1   
            alieny[i] += alieny_change[i]

        #collison
        collisions = collision(alienx[i],alieny[i],bulletx,bullety)
        if collisions:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            alienx[i] = random.randint(0,735)
            alieny[i] = random.randint(50,150)
            
        alien(alienx[i],alieny[i],i)
    #bullet movement    
    if bullet_state is "fire":
        fire_bullet(bulletx,bullety)
        bullety -= bullety_change
    if bullety <= 0:
        bullet_state = "ready"
        bullety = 480

        
    player(playerx,playery)
    show_score(textx,texty)
    pygame.display.update()
