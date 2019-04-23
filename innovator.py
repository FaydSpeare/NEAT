
node_innovations = -1
conn_innovations = -1

node_innov_dict = {}
conn_innov_dict = {}

setup = False

def setup_innovations(inputs, outputs):
    global node_innovations
    global conn_innovations
    global setup
    
    node_innovations = (inputs + outputs + 1) - 1
    conn_innovations = ((inputs+1)*outputs) - 1
    setup = True

def node_innovation(before, after):

    global node_innovations
    global conn_innovations
    global setup

    if not setup: raise Exception()

    print("Asking for", before, "to", after)
        
    tup = (before, after)

    if node_innov_dict.get(tup) != None:
        print("gave", node_innov_dict[tup])
        return node_innov_dict[tup]
    else:
        node_innovations += 1
        node_innov_dict[tup] = node_innovations
        print("gave", node_innovations)
        return node_innovations

def conn_innovation(start, end):

    global node_innovations
    global conn_innovations
    global setup

    if not setup: raise Exception()
    
    tup = (start, end)

    if conn_innov_dict.get(tup) != None:
        return conn_innov_dict[tup]
    else:
        conn_innovations += 1
        conn_innov_dict[tup] = conn_innovations
        return conn_innovations
    
        
    


