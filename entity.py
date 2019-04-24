import random
from network import *

class Entity:

    def __init__(self, inputs, outputs, net=None):
        self.inputs = inputs
        self.outputs = outputs

        if net == None:
            self.brain = Network(inputs, outputs)
        else:
            self.brain = net

        self.fitness = 0
        self.score = 0
        self.best_score = 0
        self.alive = True

    def think(self, vision):
        return self.brain.feed_forward(vision)

    def mutate(self):
        self.brain.mutate()

    def calculate_fitness(self):
        res = (self.think([0, 0])[0])**3
        res += (1 - self.think([0, 1])[0])**3
        res += (1 - self.think([1, 0])[0])**3
        res += (self.think([1, 1])[0])**3

        #if(res < 0.5):
            #print("\n\nGOT ONE\n")
        
        self.fitness = (4-res)*(4-res)#random.randint(0, 100)

    def replicate(self):
        clone = Entity(self.inputs, self.outputs)
        clone.brain = self.brain.replicate()
        clone.best_score = self.best_score
        return clone

    def assess(self):
        err = 0
        if self.think([0, 0])[0] > 0.5:
            err += 1
        if self.think([1, 0])[0] < 0.5:
            err += 1
        if self.think([0, 1])[0] < 0.5:
            err += 1
        if self.think([1, 1])[0] > 0.5:
            err += 1
        
        '''
        res = (self.think([0, 0])[0])
        res += (self.think([0, 1])[0])
        res += (1 - self.think([1, 0])[0])
        res += (1 - self.think([1, 1])[0])
        '''
        return err
        
        
    
