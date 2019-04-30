from population import Population
from innovator import setup_innovations
from entity import Entity
from species import Species
from network import Network
from node import Connection

class Neat(object):

    __isfrozen = False


    def __init__(self, io, entity, size, config=None, verbose=True):

        setup_innovations(io)
        
        self.__entity = entity
        self.__io = io
        self.__config = config
        self.__stop_condition = None
        self.__solved = False
        self.__solvers = []
        self.__verbose = verbose
        self.__pop = Population(io, self.__entity, size)

        self.__setup()
        self.__check_entity()

        self.__isfrozen = True

        
        
    # Properties

    @property
    def population(self):
        return self.__pop

    @property
    def solvers(self):
        return self.__solvers

    @property
    def stop_condition(self):
        return self.__stop_condition

    @stop_condition.setter
    def stop_condition(self, function):
        self.__stop_condition = function


    # Publics

    def is_solved(self):
        if self.__stop_condition == None:
            if self.__verbose:
                print("Warning: NEAT Object without stop condition cannot be solved")
        return self.__solved

    def next(self):
        '''
        Runs the next iteration of natural selection.
        If verbose was set to True, information about the generation is displayed
        '''
        
        self.__pop.natural_selection()
        if self.__verbose:
            s  = "| Gen : {} ".format(str(self.__pop.gen).ljust(3))
            s += "| No. Species : {} ".format(str(len(self.__pop.species)).ljust(3))
            s += "| Score : {} ".format("{:.2f}".format(self.__pop.gen_fitness).ljust(8))
            s += "| HighScore : {} ".format("{:.2f}".format(self.__pop.best_fitness).ljust(8))
            print(s)
        

    def run(self, iterations = 'inf'):
        '''
        Runs the specified number of iterations of natural selections through next().

        Parameters:
                    iterations (int): number of iterations (default = inf)

        '''
        if iterations == 'inf':
            if self.__stop_condition == None:
                raise Exception("stop condition required for run")
            while not self.__solved:
                self.next()
                if self.__stop_condition != None:
                    for spec in self.__pop.species:
                        e = spec.entities[0]
                        result = self.__stop_condition(e)
                        if result:
                            self.__solvers.append(e)
                        self.__solved = self.__solved or result
            print("SOLVED...")
        else:
            for i in range(iterations):
                self.next()
                


    # Privates
        
    def __check_entity(self):
        if not issubclass(self.__entity, Entity):
            raise Exception("entity must be a subclass of Entity")

        fitness_func = getattr(self.__entity, "calc_fitness", None)
        if not callable(fitness_func):
            raise Exception("entity must implement 'calc_fitness' function")
        
    
    def __setup(self):
        self.default_config = {
    
                # MUTATION RATES
                'weight_mut' : 0.95,
                'connection_mut' : 0.1,
                'node_mut' : 0.05,
                'random_weight' : 0.1,
                
                # SPECIES DIFFERENTIATION
                'threshold' : 3.0,
                'disjoint' : 1.0,
                'weights' : 0.5,

                # CROSSOVER
                'dup-parent' : 0.25,
                'weak-parent-weight' : 0.5,
                'gene-enable' : 0.75,

                # NATURAL SELECTION
                'elite' : 2,
                'stale_species' : 15,
                'stale__pop' : 20,

                # WEIGHTS
                'weight_upper_bound' : 3,
                'weight_lower_bound' : -3,
                'weight_step' : 0.01,
                'weight_distr' : ('gaussian', 0, 1),

                # RECURRENT NETWORK
                'recurrent': False
        }
        self.__configure(self.default_config)
        if self.__config != None: self.__configure(self.__config)
        
    def __configure(self, config):
       
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
        if 'stale_species' in config: Population.STALE_SPEC = config['stale_species']
        if 'stale__pop' in config: Population.STALE__pop = config['stale__pop']

        if 'weight_upper_bound' in config: Connection.WEIGHT_UB = config['weight_upper_bound']
        if 'weight_lower_bound' in config: Connection.WEIGHT_LB = config['weight_lower_bound']
        if 'weight_distr' in config: Connection.WEIGHT_DIST = config['weight_distr']

        if 'recurrent' in config: Network.RECURRENT = config['recurrent']

    # Magics
    
    def __repr__(self):
        return repr(self.__pop)

    def __call__(self):
        self.run()

    def __getattr__(self, name):
        print("Atrribute {} does not exist".format(name))

    def __setattr__(self, name, val):
        if self.__isfrozen and not hasattr(self, name):
            print("Atrribute {} does not exist".format(name))
        object.__setattr__(self, name, val)
        
        


            

            

        
        
