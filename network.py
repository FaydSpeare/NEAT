from node import *

class Network(object):

    def __init__(self, inputs, outputs, fill=True):

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

        if fill:
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

        attempts = 0 
        input_node = random.choice(self.nodes)
        output_node = random.choice(self.nodes)

        while ((input_node.layer == output_node.layer) or (self.is_connection(input_node, output_node)))and attempts < 50:
            input_node = random.choice(self.nodes)
            output_node = random.choice(self.nodes)
            attempts += 1

        if attempts == 50:
            print("failed attempt=50")
            return

        if input_node.layer > output_node.layer:
            temp = output_node
            output_node = input_node
            input_node = temp

        conn = Connection(input_node, output_node, 1)
        self.connections.append(conn)

        self.node_conns[input_node].append(conn)

        print("success attempt=", attempts)

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
        if random.random() < 0.8:
            for c in self.connections:
                c.mutate_weight()
            for c in self.bias_connections:
                c.mutate_weight()

        if random.random() < 0.05:
            self.add_connection()

        if random.random() < 0.01:
            self.add_node()

    # Child will take the structure of this network
    def crossover(self, net):
        pass

    def replicate(self):
        clone = Network(len(self.inputs), len(self.outputs), fill=False)

        clone.hidden_layers = self.hidden_layers
        clone.bias = self.bias.replicate()

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

        '''
        for i in range(len(clone.inputs)):
            for j in range(len(clone.outputs)):
                connection = Connection(clone.inputs[i], clone.outputs[j], 1)
                clone.node_conns[clone.inputs[i]].append(connection)
                clone.connections.append(connection)
        

        for i in range(len(clone.outputs)):
            connection = Connection(clone.bias, clone.outputs[i], 1)
            clone.bias_connections.append(connection)
        '''

        for key in self.hiddens:
            node_list = []
            for node in self.hiddens[key]:
                rep = node.replicate()
                clone.node_conns[rep] = []
                temp_node_map[rep.num] = rep
                node_list.append(rep)

            clone.hiddens[key] = node_list

        for conn in self.connections:
            in_node = temp_node_map[conn.input.num]
            out_node = temp_node_map[conn.output.num]
            new_conn = Connection(in_node, out_node, 1, num=conn.num)
            new_conn.weight = conn.weight
            new_conn.enabled = conn.enabled
            clone.node_conns[in_node].append(new_conn)
            clone.connections.append(new_conn)

        for conn in self.bias_connections:
            out_node = temp_node_map[conn.output.num]
            new_conn = Connection(clone.bias, out_node, 1, num=conn.num)
            new_conn.weight = conn.weight
            clone.bias_connections.append(new_conn)
            


        return clone
            

        
                
            

        
        
    def __repr__(self):
        s = "bias:\n"
        s += "  node " + str(self.bias.num) + "\n"
        for c in self.bias_connections:
            s += "    conn " + str(c.num) + ": " + str(c.input.num) + " -> " + str(c.output.num) + "\n"
    
            
        s += "inputs:\n"
        for n in self.inputs:
            s += "  node " + str(n.num) + "\n"
            for c in self.node_conns[n]:
                s += "    conn " + str(c.num) + ": " + str(c.input.num) + " -> " + str(c.output.num) + " enabled=" + str(c.enabled) + "\n"

        for layer in range(1, self.hidden_layers+1):
            s += "layer " + str(layer) + ":\n"
            for n in self.hiddens[layer]:
                s += "  node " + str(n.num) + "\n"
                for c in self.node_conns[n]:
                    s += "    conn " + str(c.num) + ": " + str(c.input.num) + " -> " + str(c.output.num) + " enabled=" + str(c.enabled) + "\n"

        s += "outputs:\n"
        for n in self.outputs:
            s += "  node " + str(n.num) + "\n"
        s += str(self.hidden_layers)

        return s
            
        
