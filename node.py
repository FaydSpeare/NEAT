import random
import math

node_count = 0
conn_count = 0

class Node(object):

    def __init__(self, layer):
        self.layer = layer

        global node_count
        self.num = node_count
        node_count += 1

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
        super().__init__(0)

    def activate(self):
        super().activate()

class Output(Node):

    def __init__(self):
        super().__init__(1)

    def activate(self):
        self.out_val = 1 / (1 + math.exp(-self.in_val))

class Hidden(Node):

    def __init__(self):
        super().__init__(None)

    def activate(self):
        self.out_val = 1 / (1 + math.exp(-self.in_val))

class Bias(Node):

    def __init__(self):
        super().__init__(0)
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

        global conn_count
        self.num = conn_count
        conn_count += 1

    def feed(self):
        if self.enabled:
            self.output.in_val += self.input.out_val * self.weight

class Network(object):

    def __init__(self, inputs, outputs):

        self.hidden_layers = 0

        # list of input nodes
        self.inputs = []

        # dict key = layer, value = list of nodes in layer
        self.hiddens = {}

        # list of output nodes
        self.outputs = []

        # bias node
        self.bias = Bias()

        # list of all nodes w/o bias
        self.nodes = []

        # dict key = input node, value = list of connections
        self.node_conns = {}

        # list of connections w/o bias conns
        self.connections = []

        # list of bias connections
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

        for i in range(self.hidden_layers):
            for node in self.hiddens[i+1]:
                node.activate()
                for conn in self.node_conns[node]:
                    conn.feed()
                node.in_val = 0

        for node in self.outputs:
            node.activate()
            results.append(node.out_val)
            node.in_val = 0

        return results

    def add_node(self):

        # choose a random connection (not bias connection)
        conn = random.choice(self.connections)

        # disable connection
        conn.enabled = False

        # create new node
        node = Hidden()
        self.nodes.append(node)

        # give new node bias connection
        b = Connection(self.bias, node, 1)
        self.bias_connections.append(b)

        # create two new connections
        c1 = Connection(conn.input, node, 1)
        c2 = Connection(node, conn.output, 1)

        self.connections.append(c1)
        self.connections.append(c2)

        self.node_conns[conn.input].append(c1)
        self.node_conns[node] = [c2]

        # fix weights
        c1.weight = 1
        c2.weight = conn.weight

        node.layer = conn.input.layer + 1
        if node.layer == conn.output.layer: # create new layer
            
            if node.layer not in self.hiddens: # create if layer n'existe pas
                self.hiddens[node.layer] = [node]
                
            else:
                print("entered at ", node.layer)
                for i in range(node.layer, self.hidden_layers + 1)[::-1]:
                    self.hiddens[i+1] = self.hiddens.pop(i)

                    # increment layers
                    for n in self.hiddens[i+1]:
                        n.layer += 1

                # add new layer
                self.hiddens[node.layer] = [node]

            # increment output layer
            for n in self.outputs:
                n.layer += 1
                
            self.hidden_layers += 1  
                
        else:
            self.hiddens[node.layer].append(node)

        return


    def add_connection(self):
        return

    def randomise_weights(self):
        for conn in self.connections:
            conn.weight = random.gauss(0, 1)
        for conn in self.bias_connections:
            conn.weight = random.gauss(0, 1)

    def __repr__(self):
        s = "bias:\n"
        s += "  node " + str(self.bias.num) + "\n"
        for c in self.bias_connections:
            s += "    conn " + str(c.num) + ": " + str(c.input.num) + " -> " + str(c.output.num) + "\n"
    
            
        s += "inputs:\n"
        for n in self.inputs:
            s += "  node " + str(n.num) + "\n"
            for c in self.node_conns[n]:
                s += "    conn " + str(c.num) + ": " + str(c.input.num) + " -> " + str(c.output.num) + "\n"

        for layer in range(1, self.hidden_layers+1):
            s += "layer " + str(layer) + ":\n"
            for n in self.hiddens[layer]:
                s += "  node " + str(n.num) + "\n"
                for c in self.node_conns[n]:
                    s += "    conn " + str(c.num) + ": " + str(c.input.num) + " -> " + str(c.output.num) + "\n"

        s += "outputs:\n"
        for n in self.outputs:
            s += "  node " + str(n.num) + "\n"
        s += str(self.hidden_layers)

        return s
            
        

        
        
        

        

        

        

