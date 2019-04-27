# IMPORT NEAT
from neat import *
from examples import *


# MUTATION RATES
weight = 0.8
conn = 0.05
node = 0.01
mut_rates = (weight, conn, node)

# SPECIES DIFFERENTIATION
thresh = 3.0
disjoint = 1.0
weights = 0.5
spec_diff = (thresh, disjoint, weights)

# COMBINED PARAMS
params = [mut_rates, spec_diff]

# Input/Output for Networks
io = (2, 1)

# Population Size
size = 500

# PLAYER SUBCLASS OF ENTITY
Player = XOR

# NEAT
neat = Neat(io, Player, size, params=params)

## ADD ASSESSMENT FUNCTION TO NEAT
neat.stop_condition = xor_assessment

neat.run()




    


