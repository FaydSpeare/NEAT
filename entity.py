import random
from network import *

class Entity(object):

    def __init__(self, io, net=None):
        self.io = io

        if net == None:
            self.brain = Network(io[0], io[1])
        else:
            self.brain = net

        self.fitness = 0
        self.shared_fitness = 0
        self.solved = False

    def think(self, vision):
        return self.brain.feed_forward(vision)

    def mutate(self):
        self.brain.mutate()

    def replicate(self):
        return self.__class__(self.io, self.brain.replicate())

    def child(self, net):
        return self.__class__(self.io, net)

    def __repr__(self):
        return "Entity: {{ Fitness={:.2f} , Hidden_Nodes={} }}".format(float(self.fitness), len(self.brain.hiddens))

        
        
    
