import pygame

class Ball:
    def __init__(self, radius, vel, color, jump_vel, winSize):
        self.radius = radius
        self.vel = vel
        self.color = color
        self.pos = [50 + self.radius, winSize[1] - self.radius - 100]
        self.jump_vel = jump_vel
        self.rect = None
        self.isOnSurface = True
        self.isJumping = False
        self.isGoingUp = False

    def draw(self, display):
        self.rect = pygame.draw.circle(display, self.color, self.pos, self.radius)
        return self.rect