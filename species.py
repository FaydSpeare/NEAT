import math

class Species:

    def __init__(self, first):
        self.entities = []
        
        self.standard = first.brain.replicate()
        self.best_entity = first.brain.replicate()

    def add(self, entity):
        self.entities.append(entity)

    def sort(self):
        return

    
THRESHOLD = 3
ED_COEFF = 1
W_COEFF = 0.5

def are_compatible(net1, net2):
    e_and_d = excess_and_disjoint(net1, net2)
    w_diff = weight_diff(net1, net2)

    length = len(net1.connections)+len(net1.bias_connections)
    N = 1 if length <= 20 else length

    comp = ((ED_COEFF * e_and_d) / N) + (W_COEFF * w_diff)
    print(comp)
    return comp < THRESHOLD
    
def crossover(strong_parent, weak_parent):
    child = strong_parent.replicate()

    for conn in child.connections:
        for weak_conn in weak_parent.connections:
            if conn.num == weak_conn.num:
                if random.random() < 0.5:
                    conn.weight = weak_conn.weight

                if not conn.enabled or not weak_conn.enabled:
                    if random.random() < 0.75:
                        conn.enabled = False
                    else:
                        conn.enabled = True 
                break

    for conn in child.bias_connections:
        for weak_conn in weak_parent.bias_connections:
            if conn.num == weak_conn.num:
                if random.random() < 0.5:
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
    
