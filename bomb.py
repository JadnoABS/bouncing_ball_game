import pygame
from random import randrange

class Bomb:
    def __init__(self, width, winSize):
        self.size = [int(width), int(width)]
        self.pos = [winSize[0] + 100, randrange(100, winSize[1] - 200)]
        self.img = pygame.image.load('assets/images/Bomb.png')
        self.img = pygame.transform.scale(self.img.convert_alpha(), self.size)
        self.explosion_img = pygame.image.load('assets/images/Explosion.png')
        self.explosion_img = pygame.transform.scale(self.explosion_img.convert_alpha(), [i*2 for i in self.size])
        self.rect = pygame.Rect(self.pos, self.size)

    def draw(self, display):
        self.rect = pygame.Rect(self.pos, self.size)
        display.blit(self.img, self.pos)
    
    def explode(self, display):
        self.img = self.explosion_img
