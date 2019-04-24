from population import *
from innovator import *

gen_sum = 0
hid_sum = 0
n = 50

for i in range(n):
    print("run", i)

    setup_innovations(2, 1)
    pop = Population(2, 1, 150)

    extinct = False
    for i in range(1000):
        if pop.natural_selection():
            extinct = True
            break
        if pop.best_entity.assess() == 0:
            break

    if extinct:
        continue
        
    e = pop.best_entity
    
    gen_sum += pop.gen

    hidden = len(e.brain.nodes) - 3
    hid_sum += hidden

    print(len(e.brain.nodes) - 3)
    #print(e.brain)
    print(pop.gen)

print("Avg. Gen:", gen_sum/n, "Avg. Hiddens:", hid_sum/n)
'''
for s in pop.species:
	print(s.entities[0].brain)
	s.entities[0].assess()
	s.entities[0].calculate_fitness()
	print(s.entities[0].fitness)
	print("num of creatures",len(s.entities))
'''	


