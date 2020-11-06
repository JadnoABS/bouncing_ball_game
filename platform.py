import pygame
from random import random, randrange

class Platform:
    def __init__(self, height, spawn_area):
        self.height = height
        self.width = randrange(100, 500)
        self.pos = [spawn_area[0] - 100, randrange(self.height, spawn_area[0] - self.height)]
        self.color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))

    def draw(self, display):
        rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        pygame.draw.rect(display, self.color, rect)