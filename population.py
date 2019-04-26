from species import *
from entity import *
import math

class Population(object):

    def __init__(self, io, entity, size):
        self.io = io
        self.size = size
        self.entity = entity

        self.population = []
        self.species = []

        self.gen = 0
        self.best_fitness = 0
        self.gen_fitness = 0

        self.best_entity = None

        self.stale = 0

        for i in range(size):
            entity = self.entity(io)
            entity.mutate()
            self.population.append(entity)

    def natural_selection(self):
        random.seed(a=None)
                    
        self.speciate()
        self.calculate_fitness()
        self.sort_species()
        
        self.cull_species()
        self.share_fitness()

        # kill stale and bad species

        for spec in self.species:
            if spec.stale > 15:
                self.species.remove(spec)

        fitness_sum = self.get_average_sum()

        for spec in self.species:
            if math.floor((spec.get_average_fitness() / fitness_sum) * self.size) < 1:
                self.species.remove(spec)

        if len(self.species) == 0:
            print("everyone died")
            return True

        children = []
        if self.stale > 20 and len(self.species) > 1:
            no_of_children = math.floor(self.size/2)-1
            for i in range(no_of_children):
                    children.append(self.species[0].progeny())
                    children.append(self.species[1].progeny())
            children.append(self.species[0].champion.replicate())
            children.append(self.species[1].champion.replicate())
            
        else:
            for spec in self.species:
                
                no_of_children = math.floor((spec.get_average_fitness() / fitness_sum) * self.size)
                
                if no_of_children >= 5:
                    children.append(spec.champion.replicate())
                    no_of_children -= 1
                for i in range(no_of_children):
                    children.append(spec.progeny())

        self.population = children
        self.gen += 1
        return False
        
    def speciate(self):
        for spec in self.population:
            spec.entities = []
        for entity in self.population:

            suitable_species = False
            
            for spec in self.species:
                if are_compatible(spec.standard, entity.brain):
                    spec.add(entity)
                    suitable_species = True
                    break

            if not suitable_species:
                self.species.append(Species(entity))

    def sort_species(self):
        for spec in self.species:
            spec.sort()

        self.species.sort(key=lambda x: x.gen_fitness, reverse = True)

        self.gen_fitness = 0
        self.stale += 1
        for spec in self.species:
            if spec.gen_fitness > self.best_fitness:
                self.best_fitness = spec.gen_fitness
                self.stale = 0
                self.best_entity = spec.entities[0].replicate()
            if spec.gen_fitness > self.gen_fitness:
                self.gen_fitness = spec.gen_fitness


    def calculate_fitness(self):
        for spec in self.species:
            spec.calculate_fitness()

    def cull_species(self):
        for spec in self.species:
            spec.cull()

    def share_fitness(self):
        for spec in self.species:
            spec.share_fitness()

    def get_average_sum(self):
        total = 0
        for spec in self.species:
            total += spec.get_average_fitness()
        return total
        
        
                    

    
