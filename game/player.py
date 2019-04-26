import pygame
import random

import sys
sys.path.append("..")

from network import *

class Player:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.colour = (0, 0, 255)

        self.jumping = False
        self.velocity = 0

        self.gravity = 1

        self.score = 0

        self.t = 0

        self.brain = Network(2,1)

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.w, self.h))


    def tick(self, ob):
        self.t += 1
        if self.t == 60:
            self.score += 1
            self.t = 0

        if not self.jumping:
            dist = (ob.x - self.x)/800
            height = (self.h - ob.h)/self.h
            print(dist, height)
            output = self.brain.feed_forward([dist, height])[0]
            print(output)
            if  output > 0.5:
                self.velocity = 15
                self.jumping = True

        self.y = min(450, self.y - self.velocity )

        if self.y < 450:
            self.velocity -= self.gravity

        if self.y == 450:
            self.velocity = max(0, self.velocity)
            self.jumping = False

        

            
            
            
        
        
