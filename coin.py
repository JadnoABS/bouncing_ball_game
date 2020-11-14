import pygame
from random import randrange

class Coin:
    def __init__(self, width, height, color, winSize):
        self.size = [width, height]
        self.pos = [winSize[0] + 100, randrange(100, winSize[1] - 200)]
        self.color = color
        self.rect = pygame.Rect(self.pos, self.size)

    def draw(self, display):
        self.rect = pygame.Rect(self.pos, self.size)
        return pygame.draw.ellipse(display, self.color, self.rect)