import math
import random
from entity import *

class Species:

    THRESHOLD = 4.0
    ED_COEFF = 1
    W_COEFF = 3.0

    DUP_PARENT = 0.25
    PARENT_WEIGHT = 0.5
    GENE_ENABLE = 0.75

    def __init__(self, first, innov):
        self.entities = []
        
        self.standard = first.brain.replicate()
        self.champion = first.replicate()

        self.innov = innov

        self.best_fitness = 0
        self.stale = 0

        self.gen_fitness = 0
        self.entities.append(first)

    def add(self, entity):
        self.entities.append(entity)

    def sort(self):
        self.entities.sort(key=lambda x: x.fitness, reverse = True)

        self.gen_fitness = self.entities[0].fitness
        if self.entities[0].fitness > self.best_fitness:
            self.best_fitness = self.entities[0].fitness
            self.champion = self.entities[0].replicate()
            self.stale = 0
        else:
            self.stale += 1

        self.standard = self.entities[0].brain.replicate()

    def calculate_fitness(self):
        for e in self.entities:
            e.calc_fitness()

    def cull(self):
        if len(self.entities) > 2:
            for i in range(math.floor(len(self.entities)/2)):
                del self.entities[-1]

    def share_fitness(self):
        for e in self.entities:
            e.fitness /= len(self.entities)

    def get_average_fitness(self):
        total = 0
        for e in self.entities:
            total += e.fitness
        return total / len(self.entities)

    def select_parent(self):

        fitness_sum = 0
        for e in self.entities:
            fitness_sum += e.fitness

        rand = random.randint(0, math.floor(fitness_sum))
        running_sum = 0

        for e in self.entities:
            running_sum += e.fitness
            if running_sum > rand:
                return e

        return self.entities[0]

    def progeny(self):
        progeny = None
        if random.random() < Species.DUP_PARENT:
            progeny = self.select_parent().replicate()
        else:
            parent1 = self.select_parent()
            parent2 = self.select_parent()

            if parent1.fitness < parent2.fitness:
                brain = crossover(parent2.brain, parent1.brain)
                progeny = parent2.child(brain)
            else:
                brain = crossover(parent1.brain, parent2.brain)
                progeny = parent1.child(brain)
        progeny.mutate()
        return progeny

def are_compatible(net1, net2):
    e_and_d = excess_and_disjoint(net1, net2)
    w_diff = weight_diff(net1, net2)

    length = len(net1.connections)+len(net1.bias_connections) + len(net2.connections)+len(net2.bias_connections)
    
    N = 1
    '''
    if length > 40:
        N = length
    '''

    comp = ((Species.ED_COEFF * e_and_d) / N) + (Species.W_COEFF * w_diff)
    return comp < Species.THRESHOLD
    
def crossover(strong_parent, weak_parent):
    child = strong_parent.replicate()

    for conn in child.connections:
        for weak_conn in weak_parent.connections:
            if conn.num == weak_conn.num:
                if random.random() < Species.PARENT_WEIGHT:
                    conn.weight = weak_conn.weight

                if not conn.enabled or not weak_conn.enabled:
                    if random.random() < Species.GENE_ENABLE:
                        conn.enabled = False
                    else:
                        conn.enabled = True 
                break

    for conn in child.bias_connections:
        for weak_conn in weak_parent.bias_connections:
            if conn.num == weak_conn.num:
                if random.random() < Species.PARENT_WEIGHT:
                    conn.weight = weak_conn.weight
                break
    return child    

def excess_and_disjoint(net1, net2):
    matched = 0
    for conn in net1.connections:
        for other in net2.connections:
            if other.num == conn.num:
                matched += 1
                break
    return len(net1.connections) + len(net2.connections) - 2*matched  

def weight_diff(net1, net2):
    matched = 0
    total = 0
    for conn in net1.connections:
        for other in net2.connections:
            if other.num == conn.num:
                matched += 1
                total += abs(conn.weight - other.weight)
                break
    if matched == 0:
        return 100
    return total/matched
    
