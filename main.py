from population import *
from innovator import *

setup_innovations(2, 1)
pop = Population(2, 1, 150)

for i in range(800):
    if pop.natural_selection():
        break
    if pop.best_fitness > 780:
        break
    

for s in pop.species:
	print(s.entities[0].brain)
	s.entities[0].assess()
	s.entities[0].calculate_fitness()
	print(s.entities[0].fitness)
	print("num of creatures",len(s.entities))
	


