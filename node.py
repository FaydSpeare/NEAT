import random
import math

class Node(object):

    def __init__(self):
        self.node = True

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

    def __init__(self):
        super().__init__()

    def activate(self):
        super().activate()

class Output(Node):

    def __init__(self):
        super().__init__()

    def activate(self):
        self.out_val = 1 / (1 + math.exp(-self.in_val))

class Hidden(Node):

    def __init__(self):
        super().__init__()

    def activate(self):
        self.out_val = 1 / (1 + math.exp(-self.in_val))

class Bias(Node):

    def __init__(self):
        super().__init__()
        self.in_val = 1

    def activate(self):
        super().activate()




class Connection(object):

    def __init__(self, input, output, innovation):
        self.input = input
        self.output = output

        self.weight = random.gauss(0, 1)

        self.enabled = True
        self.innovation = innovation

    def feed(self):
        self.output.in_val += self.input.out_val * self.weight

class Network(object):

    def __init__(self, inputs, outputs):

        self.inputs = []
        self.hiddens = {}
        self.outputs = []

        self.bias = Bias()
        
        self.nodes = []
        self.node_conns = {}
        self.connections = []

        self.bias_connections = []

        for i in range(inputs):
            node = Input()
            self.inputs.append(node)
            self.nodes.append(node)

        for i in range(outputs):
            node = Output()
            self.outputs.append(node)
            self.nodes.append(node)

        for node in self.inputs:
            self.node_conns[node] = []

        for i in range(inputs):
            for j in range(outputs):
                connection = Connection(self.inputs[i], self.outputs[j], 1)
                self.node_conns[self.inputs[i]].append(connection)
                self.connections.append(connection)

        for i in range(outputs):
            connection = Connection(self.bias, self.outputs[i], 1)
            self.bias_connections.append(connection)

    def feed_forward(self, inputs):
        results = []

        self.bias.in_val = 1
        self.bias.activate()
        for conn in self.bias_connections:
            conn.feed()

        for i in range(len(self.inputs)):
            node = self.inputs[i]
            node.in_val = inputs[i]
            node.activate()
            for conn in self.node_conns[node]:
                conn.feed()
            node.in_val = 0

        for i in range(len(self.hiddens)):

            for node in self.hiddens[i]:
                node.activate()
                for conn in self.node_conns[node]:
                    conn.feed()
                node.in_val = 0

        for node in self.outputs:
            node.activate()
            results.append(node.out_val)
            node.in_val = 0

        return results

    #def add_node(self):

    def randomise_weights(self):
        for conn in self.connections:
            conn.weight = random.gauss(0, 1)
        for conn in self.bias_connections:
            conn.weight = random.gauss(0, 1)
        
        

        

        

        

