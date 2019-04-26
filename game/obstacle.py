import pygame

class Obstacle:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.colour = (255, 0, 0)

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.w, self.h))

    def tick(self):
        self.x -= 6
        if self.x < -self.w:
            self.x = 800

    
