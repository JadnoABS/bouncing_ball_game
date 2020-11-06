import pygame
from random import random
from ball import Ball
from platform import Platform

pygame.init()

# Game Settings
game_running = True 
size_k = 1            # That's the proportion constant
screen_size = (1024 * size_k, 576 * size_k)
framerate = 30
gravity = 35
initial_jump_vel = 30
jumping = False
jump_state = 0
isOnSurface = True

# Screen elements
display = pygame.display.set_mode(screen_size)
char = Ball(50 * size_k, 10 * size_k, (200, 100, 50), initial_jump_vel * size_k, screen_size)
platforms = []

# Game Loop
while game_running:
    pygame.time.delay(1000 // framerate)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    keys = pygame.key.get_pressed()

    if random() >= 0.99:
        platforms.append(Platform(100, screen_size))

    for plat in platforms:
        plat.pos[0] -= 10

    # Char movement
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
            char.jump_vel -= gravity / framerate
            isOnSurface = False
        elif char.jump_vel <= 0 or not up and char.pos[1] < screen_size[1] - char.radius:
            char.pos[1] += char.jump_vel
            char.jump_vel += gravity / framerate
            up = False
        else:
            isOnSurface = True
            char.jump_vel = initial_jump_vel
            jumping = False

    # Draw char and screen refresh
    display.fill((0,0,0))
    char.draw(display)
    for plat in platforms:
        plat.draw(display)
    pygame.display.update()

pygame.quit()
