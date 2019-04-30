import random
import math

class Node(object):

    def __init__(self, layer, num):
        self.layer = layer

        self.num = num
        
        self.in_val = 0
        self.out_val = 0

        self.recurrent_in_val = 0

    def is_input(self):
        return isinstance(self, Input)

    def is_hidden(self):
        return isinstance(self, Hidden)

    def is_output(self):
        return isinstance(self, Output)

    def activate(self):
        self.out_val = self.in_val

class Input(Node):

    def __init__(self, num):
        super().__init__(0, num)

    def activate(self):
        super().activate()

    def replicate(self):
        node = Input(self.num)
        return node

class Output(Node):

    def __init__(self, num):
        super().__init__(1, num)

    def activate(self):
        self.in_val += self.recurrent_in_val
        try:
            ans = math.exp(-4.9*self.in_val)
        except OverflowError:
            ans = float('inf')
        self.out_val = 1 / (1 + ans)
        self.recurrent_in_val = 0

    def replicate(self):
        node = Output(self.num)
        node.layer = self.layer
        return node

class Hidden(Node):

    def __init__(self, num):
        super().__init__(None, num)

    def activate(self):
        self.in_val += self.recurrent_in_val
        try:
            ans = math.exp(-4.9*self.in_val)
        except OverflowError:
            ans = float('inf')
        self.out_val = 1 / (1 + ans)
        self.recurrent_in_val = 0
    
    def replicate(self):
        node = Hidden(self.num)
        node.layer = self.layer
        return node

class Bias(Node):

    def __init__(self, num):
        super().__init__(0, num)
        self.in_val = 1

    def activate(self):
        super().activate()

    def replicate(self):
        node = Bias(self.num)
        return node


class Connection(object):

    WEIGHT_UB = 3
    WEIGHT_LB = -3
    WEIGHT_STEP = 0.01
    WEIGHT_DIST = ('uniform', 0, 1)
    RANDOM_WEIGHT = 0.1

    def __init__(self, input, output, num):
        self.input = input
        self.output = output

        
        self.recurrent = False
        if self.input == self.output:
            self.recurrent = True

        self.weight = self.rand()
        self.enabled = True
        self.num = num

    def feed(self):
        if self.enabled:
            if self.recurrent:
                self.output.recurrent_in_val += self.input.out_val * self.weight
            else:
                self.output.in_val += self.input.out_val * self.weight

    def mutate_weight(self):
        if random.random() < Connection.RANDOM_WEIGHT:
            self.weight = self.rand()
        else:
            self.weight += self.rand() * Connection.WEIGHT_STEP
        
        if self.weight > Connection.WEIGHT_UB: self.weight = Connection.WEIGHT_UB
        elif self.weight < Connection.WEIGHT_LB: self.weight = Connection.WEIGHT_LB

    def rand(self):
        if Connection.WEIGHT_DIST[0] == 'uniform':
            width = (Connection.WEIGHT_DIST[2] - Connection.WEIGHT_DIST[1])
            return (random.random() * width) + Connection.WEIGHT_DIST[1]
        elif Connection.WEIGHT_DIST[0] == 'gaussian':
            return random.gauss(Connection.WEIGHT_DIST[1], Connection.WEIGHT_DIST[2])




        
        
        

        

        

        

