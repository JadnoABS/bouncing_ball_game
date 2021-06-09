import pygame
from random import randrange

class Spike:
    def __init__(self, height, x, y):
        self.height = height
        self.width = randrange(100, 250)
        self.pos = [x, y]
        self.color = (255,0,0)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def draw(self, display):
        self.vertices = [
            [self.pos[0], self.pos[1]], 
            [self.pos[0]+self.width/8, self.pos[1]-30], 
            [self.pos[0]+self.width/4, self.pos[1]], 
            [self.pos[0]+3*self.width/8, self.pos[1]-30],
            [self.pos[0]+self.width/2, self.pos[1]],
            [self.pos[0]+5*self.width/8, self.pos[1]-30],
            [self.pos[0]+3*self.width/4, self.pos[1]],
            [self.pos[0]+7*self.width/8, self.pos[1]-30],
            [self.pos[0]+self.width, self.pos[1]],
            [self.pos[0]+self.width, self.pos[1]+self.height],
            [self.pos[0], self.pos[1]+self.height]
            ]
        self.rect = pygame.draw.polygon(display, self.color, self.vertices)
        return self.rect
