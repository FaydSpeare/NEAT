# IMPORT NEAT
from neat import *
from examples import *


# MUTATION RATES
weight = 0.9
conn = 0.2
node = 0.05
mut_rates = (weight, conn, node)

# SPECIES DIFFERENTIATION
thresh = 4.0
disjoint = 1.0
weights = 3.0
spec_diff = (thresh, disjoint, weights)

# COMBINED PARAMS
params = [mut_rates, spec_diff]

# Input/Output for Networks
io = (7, 10)

# Population Size
size = 200

# PLAYER SUBCLASS OF ENTITY
Player = DIGITS

# NEAT
neat = Neat(io, Player, size, params=params)

## ADD ASSESSMENT FUNCTION TO NEAT
neat.stop_condition = digits_assessment

neat.run()






    


