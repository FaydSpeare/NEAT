import random

class Entity:

    def __init__(self, inputs, outputs):
        
        self.brain = Network(inputs, outputs)

        self.fitness = 0
        self.score = 0
        self.best_score = 0
        self.alive = True

    def think(self, vision):
        return self.brain.feed_forward(vision)

    def mutate(self):
        self.brain.mutate()

    def calculate_fitness(self):
        self.fitness = random.randint(0, 100) 
        
        
    
