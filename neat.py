from population import *
from innovator import *
from entity import *
from species import *
from network import *
import random



class Neat:

    def __init__(self, io, entity, size, params=None, verbose=True):
        self.entity = entity
        self.check_entity()
        
        self.io = io

        if params != None:
            mut_rates = params[0]
            Network.W_MUT = mut_rates[0]
            Network.C_MUT = mut_rates[1]
            Network.N_MUT = mut_rates[2]
            
            diff_specs = params[1]
            Species.THRESHOLD = diff_specs[0]
            Species.ED_COEFF = diff_specs[1]
            Species.W_COEFF = diff_specs[2]

        self.stop_condition = None
        self.solved = False
        self.solvers = []

        self.verbose = verbose
        
        setup_innovations(io[0], io[1])

        self.pop = Population(io, entity, size)
        
    def check_entity(self):
        if not issubclass(self.entity, Entity):
            raise Exception("entity must be a subclass of Entity")

        fitness_func = getattr(self.entity, "calc_fitness", None)
        if not callable(fitness_func):
            raise Exception("entity must implement 'calc_fitness' function")
        
    def next(self):
        self.pop.natural_selection()
        if self.verbose:
            
            s  = "| Gen : {} ".format(str(self.pop.gen).ljust(3))
            s += "| No. Species : {} ".format(str(len(self.pop.species)).ljust(3))
            s += "| Score : {} ".format("{:.2f}".format(self.pop.gen_fitness).ljust(8))
            s += "| HighScore : {} ".format("{:.2f}".format(self.pop.best_fitness).ljust(8))
            print(s)
            
#print("Gen: {} ~ Spec Count: {} ~ Current: {:.2f} ~ Best: {:.2f}".format(self.gen, len(self.species), self.gen_fitness, self.best_fitness))
            

    def run(self):
        if self.stop_condition == None:
            raise Exception("stop condition required for run")
        while not self.solved:
            self.next()
            if self.stop_condition != None:
                for spec in self.pop.species:
                    e = spec.entities[0]
                    result = self.stop_condition(e)
                    if result:
                        self.solvers.append(e)
                    self.solved = self.solved or result
        print("SOLVED...")
            

        
        
