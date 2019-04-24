from node import *
from innovator import *
from species import *

class Network(object):

    def next_node_innov(self):
        self.node_innov += 1
        return self.node_innov-1

    def next_conn_innov(self):
        self.conn_innov += 1
        return self.conn_innov-1

    def __init__(self, inputs, outputs, fill=True):

        self.node_innov = 0
        self.conn_innov = 0

        self.hidden_layers = 0

        self.node_innovations = set()

        # list of input nodes
        self.inputs = []

        # dict key = layer, value = list of nodes in layer
        self.hiddens = {}

        # list of output nodes
        self.outputs = []

        # bias node
        self.bias = Bias(self.next_node_innov())

        # list of all nodes w/o bias
        self.nodes = []

        # dict key = input node, value = list of connections
        self.node_conns = {}

        # list of connections w/o bias conns
        self.connections = []

        # list of bias connections
        self.bias_connections = []

        if fill:
            for i in range(inputs):
                node = Input(self.next_node_innov())
                self.inputs.append(node)
                self.nodes.append(node)

            for i in range(outputs):
                node = Output(self.next_node_innov())
                self.outputs.append(node)
                self.nodes.append(node)

            for node in self.inputs:
                self.node_conns[node] = []

            for i in range(outputs):
                connection = Connection(self.bias, self.outputs[i], self.next_conn_innov())
                self.bias_connections.append(connection)

            for i in range(inputs):
                for j in range(outputs):
                    connection = Connection(self.inputs[i], self.outputs[j], self.next_conn_innov())
                    self.node_conns[self.inputs[i]].append(connection)
                    self.connections.append(connection)

            for n in self.nodes:
                self.node_innovations.add(n.num)

            
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
            #node.in_val = 0
            #node.out_val = 0

        for i in range(self.hidden_layers):
            for node in self.hiddens[i+1]:
                node.activate()
                for conn in self.node_conns[node]:
                    conn.feed()
                #node.in_val = 0
                #node.out_val = 0

        for node in self.outputs:
            node.activate()
            results.append(node.out_val)
            #node.in_val = 0
            #node.out_val = 0

        for node in self.nodes:
            node.out_val = 0
            node.in_val = 0
        return results

    def add_node(self):

        # choose a random connection (not bias connection)
        conn = random.choice(self.connections)

        while node_innovation(conn.input.num, conn.output.num) in self.node_innovations:
            conn = random.choice(self.connections)

        # disable connection
        conn.enabled = False

        # create new node
        node = Hidden(node_innovation(conn.input.num, conn.output.num))
        self.nodes.append(node)
        self.node_innovations.add(node.num)

        # give new node bias connection
        b = Connection(self.bias, node, conn_innovation(self.bias.num, node.num))
        b.weight = 0
        self.bias_connections.append(b)

        # create two new connections
        c1 = Connection(conn.input, node, conn_innovation(conn.input.num, node.num))
        c2 = Connection(node, conn.output, conn_innovation(node.num, conn.output.num))

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
                #print("entered at ", node.layer)
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
            if self.hiddens.get(node.layer) == None:
                self.hiddens[node.layer] = [node]
            self.hiddens[node.layer].append(node)

        return


    def add_connection(self):

        attempts = 0 
        input_node = random.choice(self.nodes)
        output_node = random.choice(self.nodes)

        while ((input_node.layer == output_node.layer) or (self.is_connection(input_node, output_node)))and attempts < 50:
            input_node = random.choice(self.nodes)
            output_node = random.choice(self.nodes)
            attempts += 1

        if attempts == 50:
            #print("failed attempt=50")
            return

        if input_node.layer > output_node.layer:
            temp = output_node
            output_node = input_node
            input_node = temp

        conn = Connection(input_node, output_node, conn_innovation(input_node.num, output_node.num))
        self.connections.append(conn)

        self.node_conns[input_node].append(conn)

        #print("success attempt=", attempts)

    def is_connection(self, n1, n2):
        if  n1 in self.node_conns:
            for c in self.node_conns[n1]:
                if c.output == n2:
                    return True
        if n2 in self.node_conns:
            for c in self.node_conns[n2]:
                if c.output == n1:
                    return True
        return False

    def randomise_weights(self):
        for conn in self.connections:
            conn.weight = random.gauss(0, 1)
        for conn in self.bias_connections:
            conn.weight = random.gauss(0, 1)

    def mutate(self):
        if random.random() < 0.95:
            for c in self.connections:
                c.mutate_weight()
            for c in self.bias_connections:
                c.mutate_weight()

        if random.random() < 0.1:
            self.add_connection()

        if random.random() < 0.01:
            self.add_node()
            
        
    def replicate(self):
        clone = Network(len(self.inputs), len(self.outputs), fill=False)

        clone.hidden_layers = self.hidden_layers
        clone.bias = self.bias.replicate()

        clone.node_innov = self.node_innov
        clone.conn_innov = self.conn_innov

        temp_node_map = {}

        for node in self.inputs:
            rep = node.replicate()
            clone.inputs.append(rep)
            clone.nodes.append(rep)
            temp_node_map[rep.num] = rep

        for node in self.outputs:
            rep = node.replicate()
            clone.outputs.append(rep)
            clone.nodes.append(rep)
            temp_node_map[rep.num] = rep

        for node in clone.inputs:
                clone.node_conns[node] = []

        for key in self.hiddens:
            node_list = []
            for node in self.hiddens[key]:
                rep = node.replicate()
                clone.node_conns[rep] = []
                temp_node_map[rep.num] = rep
                node_list.append(rep)
                clone.nodes.append(rep)

            clone.hiddens[key] = node_list

        for conn in self.connections:
            in_node = temp_node_map[conn.input.num]
            out_node = temp_node_map[conn.output.num]
            new_conn = Connection(in_node, out_node, conn.num)
            new_conn.weight = conn.weight
            new_conn.enabled = conn.enabled
            clone.node_conns[in_node].append(new_conn)
            clone.connections.append(new_conn)

        for conn in self.bias_connections:
            out_node = temp_node_map[conn.output.num]
            new_conn = Connection(clone.bias, out_node, conn.num)
            new_conn.weight = conn.weight
            clone.bias_connections.append(new_conn)

        for n in clone.nodes:
                clone.node_innovations.add(n.num)
            
        return clone
                    
    def __repr__(self):
        s = "bias:\n"
        s += "  node " + str(self.bias.num) + "\n"
        for c in self.bias_connections:
            s += "    conn " + str(c.num).center(2) + ": " + str(c.input.num).center(2) + " -> " + str(c.output.num).center(2) + " enabled=" + str(c.enabled) + " weight=" +str(c.weight)+"\n"
    
            
        s += "inputs:\n"
        for n in self.inputs:
            s += "  node " + str(n.num) + "\n"
            for c in self.node_conns[n]:
                s += "    conn " + str(c.num).center(2) + ": " + str(c.input.num).center(2) + " -> " + str(c.output.num).center(2) + " enabled=" + str(c.enabled) + " weight=" +str(c.weight)+"\n"

        for layer in range(1, self.hidden_layers+1):
            s += "layer " + str(layer) + ":\n"
            for n in self.hiddens[layer]:
                s += "  node " + str(n.num) + "\n"
                for c in self.node_conns[n]:
                    s += "    conn " + str(c.num).center(2) + ": " + str(c.input.num).center(2) + " -> " + str(c.output.num).center(2) + " enabled=" + str(c.enabled) + " weight=" +str(c.weight) + "\n"

        s += "outputs:\n"
        for n in self.outputs:
            s += "  node " + str(n.num) + "\n"
        s += str(self.hidden_layers)

        return s
            
        
