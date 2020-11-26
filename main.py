#--- Bouncing Ball Game [Version 1.0] (I am working on a better name hahah) ---#
#--- Programed by Jadno Barbosa - November 2020 (During quarantine and last year of high school) ---#

import pygame
from random import random

from settings import Settings
from ball import Ball
from coin import Coin
from bomb import Bomb
from spike import Spike

pygame.init()

# Game Settings
gameSettings = Settings()
screen_size = (int(gameSettings.get('screenSettings', 'width')), int(gameSettings.get('screenSettings', 'height')))
framerate = 60
game_over = False
clock = pygame.time.Clock()

# Custom settings
ball_color = tuple(map(int, gameSettings.get('playerSettings', 'ballcolor').split(',')))

# Screen elements
display = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Bouncing Ball Game")
background_image = pygame.image.load('assets/images/backgrounds/{}.png'.format(gameSettings.get('screenSettings', 'Background')))
background_image = pygame.transform.scale(background_image.convert_alpha(), screen_size)

def runGame():
    # Screen Elements Settings
    screen_size = (int(gameSettings.get('screenSettings', 'Width')), int(gameSettings.get('screenSettings', 'Height')))
    background_image = pygame.image.load('assets/images/backgrounds/{}.png'.format(gameSettings.get('screenSettings', 'Background')))
    background_image = pygame.transform.scale(background_image.convert_alpha(), screen_size)
    ball_color = tuple(map(int, gameSettings.get('playerSettings', 'ballColor').split(',')))
    display = pygame.display.set_mode(screen_size)
    frame = 0

    # Game Elements Settings
    gravity = screen_size[1] / 720
    initial_jump_vel = screen_size[1] / 24
    elements_vel = screen_size[0] / 216
    game_running = True
    char = Ball(screen_size[0] / 25, screen_size[0] / 144, ball_color, screen_size, jump_vel=initial_jump_vel)
    floor = pygame.Rect(0, screen_size[1] - 100, screen_size[0], 100)
    coins = []
    bombs = []
    spikes = []
    score = 0
    game_over = False
    display.blit(background_image, (0,0))

    # Game Loop
    while game_running and not game_over:
        clock.tick(framerate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        if frame % (framerate * 20) == 0:
            elements_vel += 3

        # Coin Spawning
        if random() >= 0.99:
            coins.append(Coin(screen_size[0] / 42, screen_size[1] / 14, (232, 252, 3), screen_size))

        for coin in coins:
            coin.pos[0] -= elements_vel
            if char.rect:
                if coin.rect.colliderect(char.rect):
                    pygame.mixer.music.load('assets/sounds/get_coin.mp3')
                    pygame.mixer.music.play()
                    score += 1
                    coins.remove(coin)
            if coin.pos[0] < -coin.rect.width:
                coins.remove(coin)

        # Bombs spawning
        if random() >= 0.99 and len(bombs) < 5: 
            bombs.append(Bomb(screen_size[1] / 14, screen_size))

        for bomb in bombs:
            bomb.pos[0] -= elements_vel
            if char.rect:
                if bomb.rect.colliderect(char.rect):
                    bomb.explode(display)
                    pygame.mixer.music.load('assets/sounds/explosion.wav')
                    pygame.mixer.music.play()
                    game_over = True
            if bomb.pos[0] < -bomb.rect.width:
                bombs.remove(bomb)

        # Spikes Spawning
        if frame % 120 == 0:
            spikes.append(Spike(100, screen_size[0] + 100, screen_size[1] - 100))

        for spike in spikes:
            spike.pos[0] -= elements_vel
            if char.rect:
                if spike.rect.colliderect(char.rect):
                    pygame.mixer.music.load('assets/sounds/lost.wav')
                    pygame.mixer.music.play()
                    game_over = True
            if spike.pos[0] < -spike.width:
                spikes.remove(spike)

        # Char movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            char.pos[0] += char.vel
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            char.pos[0] -= char.vel
        if keys[pygame.K_SPACE]:
            char.isJumping = True
            if char.isOnSurface:
                char.isGoingUp = True
        if char.isJumping:
            if char.jump_vel > 0 and char.isGoingUp:
                char.pos[1] -= char.jump_vel
                char.jump_vel -= gravity
                char.isOnSurface = False
            elif char.jump_vel <= 0 or not char.isGoingUp and char.pos[1] < screen_size[1] - char.radius - 100:
                char.pos[1] += char.jump_vel
                char.jump_vel += gravity
                char.isGoingUp = False
            else:
                char.isOnSurface = True
                char.jump_vel = initial_jump_vel
                char.isJumping = False

        # Char, coin and score drawing and screen refresh
        display.fill((255, 255, 255))
        display.blit(background_image, (0, 0))

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Score: {}".format(score), True, (100, 255, 10))
        display.blit(text, (screen_size[0] // 2 - 50, 50))
        pygame.draw.rect(display, (0, 0, 255), floor)
        char.draw(display)
        for coin in coins:
            coin.draw(display)
        for bomb in bombs:
            bomb.draw(display)
        for spike in spikes:
            spike.draw(display)
        frame += 1
        pygame.display.update()
    if game_over:
        if score > int(gameSettings.get('playerSettings', 'bestscore')):
            gameSettings.set('playerSettings', 'bestscore', score)
        showGameOver()
    elif not game_running:
        pygame.quit()

def showGameOver():
    # Draw Game Over message
    font = pygame.font.Font('freesansbold.ttf', 50)
    text_gameover = font.render("Game Over", True, (200, 200, 0))
    display.blit(text_gameover, (screen_size[0] / 2 - text_gameover.get_rect().width / 2, screen_size[1] / 3))

    font = pygame.font.Font('freesansbold.ttf', 30)
    text_play = font.render("Press space to try again", True, (200, 200, 0))
    display.blit(text_play, (screen_size[0] / 2 - text_play.get_rect().width/2, screen_size[1] / 2))

    sttngs_img = pygame.image.load('assets/images/Settings.png')
    display.blit(sttngs_img, (10, 10))

    pygame.display.flip()
    resume = False
    quit = False

    while not resume and not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    resume = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                sttngs_rect = sttngs_img.get_rect()
                if 10 <= mouse[0] <= sttngs_rect.width + 10 and 10 <= mouse[1] <= sttngs_rect.height + 10:
                    gameSettings.openScreen(screen_size, display)
                    showStartScreen()
        
        clock.tick(framerate)
    if resume:
        runGame()
    elif quit: 
        pygame.quit()

def showStartScreen():
    # Screen Elements Settings
    screen_size = (int(gameSettings.get('screenSettings', 'Width')), int(gameSettings.get('screenSettings', 'Height')))
    background_image = pygame.image.load('assets/images/backgrounds/{}.png'.format(gameSettings.get('screenSettings', 'Background'))).convert_alpha()
    ball_color = tuple(map(int, gameSettings.get('playerSettings', 'ballColor').split(',')))
    background_image = pygame.transform.scale(background_image, screen_size)
    display = pygame.display.set_mode(screen_size)

    game_running = False
    
    # Draw Start Screen Ball and Floor
    display.fill((255,255,255))
    display.blit(background_image, (0,0))
    char = Ball(screen_size[0] / 25, screen_size[0] / 144, ball_color, screen_size)
    floor = pygame.Rect(0, screen_size[1] - 100, screen_size[0], 100)
    pygame.draw.rect(display, (0, 0, 255), floor)
    char.draw(display)

    # Draw Logo and Settings Button
    ball_logo = pygame.image.load('assets/images/BallLogo.png')
    ball_logo_pos = (screen_size[0] / 2 - (ball_logo.get_rect().width / 2), -100)
    sttngs_img = pygame.image.load('assets/images/Settings.png')
    display.blit(ball_logo, ball_logo_pos)
    display.blit(sttngs_img, (10, 10))

    # Draw play text
    font = pygame.font.Font('freesansbold.ttf', 30)
    best_score = gameSettings.get('playerSettings', 'bestscore')
    text_score = font.render('Best Score: ' + best_score, True, (200, 200, 0))
    display.blit(text_score, (screen_size[0]/2 - text_score.get_width()/2, 100))
    text_play = font.render("Press SPACE to play", True, (200, 200, 0))
    display.blit(text_play, (screen_size[0]/2 - text_play.get_width()/2, screen_size[1] - 150))
    pygame.display.flip()

    quit = False
    while not game_running and not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_running = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                sttngs_rect = sttngs_img.get_rect()
                if 10 <= mouse[0] <= sttngs_rect.width + 10 and 10 <= mouse[1] <= sttngs_rect.height + 10:
                    sttngs = gameSettings.openScreen(screen_size, display)
                    if sttngs == 'Quit':
                        quit = True
                    else:
                        showStartScreen()

        clock.tick(framerate)
    if game_running:
        runGame()
    elif quit:
        pygame.quit()

# Game Start Point
showStartScreen()
