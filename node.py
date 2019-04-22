class Node(object):

    def __init__(self):
        self.node = True

    def is_input(self):
        return isinstance(self, Input)

    def is_hidden(self):
        return isinstance(self, Hidden)

    def is_output(self):
        return isinstance(self, Output)

class Input(Node):

    def __init__(self):
        super().__init__()

class Output(Node):

    def __init__(self):
        super().__init__()

class Hidden(Node):

    def __init__(self):
        super().__init__()

class Bias(Node):

    def __init__(self):
        super().__init__()

class Connection(object):

    def __init__(self, input, output, innovation):
        self.input = input
        self.output = output

        self.weight = 1

        self.enabled = True
        self.innovation = innovation

class Network(object):

    def __init__(self, inputs, outputs):

        self.inputs = []
        self.hiddens = []
        self.outputs = []
        
        self.nodes = []
        self.connections = []

        for i in range(inputs):
            node = Input()
            self.inputs.append(node)
            self.nodes.append(node)

        for i in range(outputs):
            node = Output()
            self.outputs.append(node)
            self.nodes.append(node)

        for i in range(inputs):
            for j in range(outputs):
                connection = Connection(self.inputs[i], self.outputs[j])
                self.connections.append(connection)

    def feed_forward(inputs):
        return 0

        

        

