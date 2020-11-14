# I had an idea to this class but it didn went well
# Ill leave it here just in case I need it sometime

import pygame
from random import randrange

class Platform:
    def __init__(self, height, x, y):
        self.height = height
        self.width = randrange(100, 500)
        self.pos = [x - 100, y]
        self.color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.vertices = {
            "TL": [self.rect.x, self.rect.y],
            "TR": [self.rect.x + self.width, self.rect.y],
            "BL": [self.rect.x, self.rect.y + self.height],
            "BR": [self.rect.x + self.width, self.rect.y + self.height]
        }

    def draw(self, display):
        self.rect.left = self.pos[0]
        pygame.draw.rect(display, self.color, self.rect)

    def checkCollision(self, rect):
        return self.rect.colliderect(rect)