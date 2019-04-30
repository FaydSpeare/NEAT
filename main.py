# IMPORT NEAT
from neat import *
from examples import *

config = {
    
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
    'stale' : 15,

    # WEIGHTS
    'weight_upper_bound' : 3,
    'weight_lower_bound' : -3,
    'weight_step' : 0.01,
    'weight_distr' : ('gaussian', 0, 1),

    'recurrent' : False    

}

# Input/Output for Networks
io = (2, 1)

# Population Size
size = 100

# PLAYER SUBCLASS OF ENTITY
Player = XOR

# NEAT
neat = Neat(io, Player, size, config)

## ADD ASSESSMENT FUNCTION TO NEAT
neat.stop_condition = xor_assessment

neat.run()





    


