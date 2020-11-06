import pygame

class Ball:
    def __init__(self, radius, vel, color, jump_vel, winSize):
        self.radius = radius
        self.vel = vel
        self.color = color
        self.pos = [50 + self.radius, winSize[1] - self.radius]
        self.jump_vel = jump_vel

    def draw(self, display):
        pygame.draw.circle(display, self.color, self.pos, self.radius)