from population import *
from innovator import *
from entity import *
from species import *
from network import *

class Neat:

    def __init__(self, io, entity, size, config=None, verbose=True):
        self.entity = entity
        self.check_entity()

        
        self.io = io

        self.config = config

        self.configure()
        
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
            #s += "| No. Entities : {} ".format(str(len(self.pop.population)).ljust(3))
            print(s)
        

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

    def configure(self):
        
        if self.config != None:
            config = self.config
            
            if 'weight_mut' in config: Network.W_MUT = config['weight_mut']
            if 'connection_mut' in config: Network.C_MUT = config['connection_mut']
            if 'node_mut' in config: Network.N_MUT = config['node_mut']
            if 'random_weight' in config: Connection.W_MUT = config['random_weight']
            if 'weight_step' in config: Connection.WEIGHT_STEP = config['weight_step']
            
            if 'threshold' in config: Species.THRESHOLD = config['threshold']
            if 'disjoint' in config: Species.ED_COEFF = config['disjoint']
            if 'weights' in config: Species.W_COEFF = config['weights']

            if 'dup_parent' in config: Species.DUP_PARENT = config['dup_parent']
            if 'weak-parent_weight' in config: Species.PARENT_WEIGHT = config['weak-parent_weight']
            if 'gene_enable' in config: Species.GENE_ENABLE = config['gene_enable']

            if 'elite' in config: Population.ELITE = config['elite']
            if 'stale' in config: Population.STALE = config['stale']

            if 'weight_upper_bound' in config: Connection.WEIGHT_UB = config['weight_upper_bound']
            if 'weight_lower_bound' in config: Connection.WEIGHT_LB = config['weight_lower_bound']
            if 'weight_distr' in config: Connection.WEIGHT_DIST = config['weight_distr']


            

            

        
        
