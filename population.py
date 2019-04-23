from species import *
from entity import *

class Population(object):

    def __init__(self, inputs, outputs, pop_size):
        self.inputs = inputs
        self.outputs = outputs
        self.pop_size = pop_size

        self.population = []
        self.species = []

        for i in range(pop_size):
            entity = Entity(inputs, outputs)
            entity.mutate()
            self.population.append(entity)

    def natural_selection(self):

        self.speciate()
        

    def speciate(self):

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
        
        
                    

    
