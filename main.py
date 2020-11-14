import pygame
from random import random, choice
from ball import Ball
from coin import Coin
from platform import Platform

pygame.init()

# Game Settings
game_running = True 
size_k = 1            # That's the proportion constant
screen_size = (1024 * size_k, 576 * size_k)
framerate = 30
gravity = 2
initial_jump_vel = 40
jumping = False
jump_state = 0
isOnSurface = True
jumping = False
up = False

# Screen elements
display = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Bouncing Ball Game")
char = Ball(50 * size_k, 10 * size_k, (200, 100, 50), initial_jump_vel * size_k, screen_size)
coins = []
points = 0
font = pygame.font.Font('freesansbold.ttf', 30)

# Game Loop
while game_running:
    pygame.time.delay(1000 // framerate)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Coin Spawning
    if random() >= 0.99:
        coins.append(Coin(50, 100, (232, 252, 3), screen_size))

    for coin in coins:
        coin.pos[0] -= 10
        if coin.rect.colliderect(char.rect):
            points += 1
            coins.remove(coin)

    # Char movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        char.pos[0] += char.vel
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        char.pos[0] -= char.vel
    if keys[pygame.K_SPACE]:
        jumping = True
        if isOnSurface:
            up = True
    if jumping:
        if char.jump_vel > 0 and up:
            char.pos[1] -= char.jump_vel
            char.jump_vel -= gravity
            isOnSurface = False
        elif char.jump_vel <= 0 or not up and char.pos[1] < screen_size[1] - char.radius:
            char.pos[1] += char.jump_vel
            char.jump_vel += gravity
            up = False
        else:
            isOnSurface = True
            char.jump_vel = initial_jump_vel
            jumping = False

    # Char, coin and score drawing and screen refresh
    display.fill((0,0,0))

    text = font.render("Score: {}".format(points), True, (100, 255, 10))
    display.blit(text, (screen_size[0] // 2 - 50, 50))

    char.draw(display)
    for coin in coins:
        coin.draw(display)
    pygame.display.update()

pygame.quit()
