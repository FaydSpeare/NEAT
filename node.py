import random
import math

class Node(object):

    def __init__(self, layer, num):
        self.layer = layer

        self.num = num
        
        self.in_val = 0
        self.out_val = 0

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
        self.out_val = 1 / (1 + math.exp(-4.9*self.in_val))

    def replicate(self):
        node = Output(self.num)
        node.layer = self.layer
        return node

class Hidden(Node):

    def __init__(self, num):
        super().__init__(None, num)

    def activate(self):
        self.out_val = 1 / (1 + math.exp(-4.9*self.in_val))
    
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

    def __init__(self, input, output, num):
        self.input = input
        self.output = output

        self.weight = random.random()*2 - 1

        self.enabled = True

        self.num = num

    def feed(self):
        if self.enabled:
            self.output.in_val += self.input.out_val * self.weight

    def mutate_weight(self):
        if random.random() < 0.1:
            self.weight = random.random()*2 - 1
        else:
            self.weight += random.gauss(0, 1) / 50
        
        if self.weight > 1:
            self.weight = 1
        elif self.weight < -1:
            self.weight = -1
            




        
        
        

        

        

        

