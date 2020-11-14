import pygame
from random import random, choice
from ball import Ball
from coin import Coin
from spike import Spike

pygame.init()

# Game Settings
size_k = 1               # That's the proportion constant
screen_size = (1024 * size_k, 576 * size_k)
framerate = 30
gravity = 2
initial_jump_vel = 38
game_over = False


# Screen elements
display = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Bouncing Ball Game")

def main():
    # Game Elements Settings
    game_running = True
    char = Ball(50 * size_k, 10 * size_k, (200, 100, 50), initial_jump_vel * size_k, screen_size)
    floor = pygame.Rect(0, screen_size[1] - 100, screen_size[0], 100)
    coins = []
    spikes = []
    spike_count = framerate * 2
    points = 0
    game_over = False

    # Game Loop
    while game_running and not game_over:
        pygame.time.delay(1000 // framerate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()

        # Coin Spawning
        if random() >= 0.97:
            coins.append(Coin(30 * size_k, 50 * size_k, (232, 252, 3), screen_size))

        for coin in coins:
            coin.pos[0] -= 10
            if coin.rect.colliderect(char.rect):
                pygame.mixer.music.load('get_coin.mp3')
                pygame.mixer.music.play()
                points += 1
                coins.remove(coin)

        # Spikes Spawning
        if spike_count > 0:
            spike_count -= 1
        elif spike_count == 0:
            spikes.append(Spike(100, screen_size[0] + 100, screen_size[1] - 100))
            spike_count = framerate * 2

        for spike in spikes:
            spike.pos[0] -= 10
            if spike.rect.colliderect(char.rect):
                pygame.mixer.music.load('lost.wav')
                pygame.mixer.music.play()
                game_over = True

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
        display.fill((0,0,0))

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Score: {}".format(points), True, (100, 255, 10))
        display.blit(text, (screen_size[0] // 2 - 50, 50))
        pygame.draw.rect(display, (0, 0, 255), floor)
        char.draw(display)
        for spike in spikes:
            spike.draw(display)
        for coin in coins:
            coin.draw(display)
        pygame.display.update()
    showGameOver()

def showGameOver():
    font = pygame.font.Font('freesansbold.ttf', 50)
    text_gameover = font.render("Game Over", True, (200, 200, 0))
    display.blit(text_gameover, (screen_size[0] / 2.8, screen_size[1] / 3))
    font = pygame.font.Font('freesansbold.ttf', 30)
    text_gameover = font.render("Press space to try again", True, (200, 200, 0))
    display.blit(text_gameover, (screen_size[0] / 3, screen_size[1] / 2))
    pygame.display.flip()
    resume = False
    while not resume:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    resume = True
        
        pygame.time.delay(1000 // framerate)
    main()

main()
