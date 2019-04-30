
node_innovations = -1
conn_innovations = -1

node_innov_dict = {}
conn_innov_dict = {}

setup = False

def setup_innovations(io):
    global node_innovations
    global conn_innovations
    global setup
    global node_innov_dict
    global conn_innov_dict
    
    node_innovations = (io[0] + io[1] + 1) - 1
    conn_innovations = ((io[0] + 1) * io[1]) - 1

    node_innov_dict = {}
    conn_innov_dict = {}

    setup = True

def node_innovation(before, after):

    global node_innovations
    global conn_innovations
    global setup

    if not setup: raise Exception()

    #print("Asking for", before, "to", after)
        
    tup = (before, after)

    if node_innov_dict.get(tup) != None:
        #print("gave", node_innov_dict[tup])
        return node_innov_dict[tup]
    else:
        node_innovations += 1
        node_innov_dict[tup] = node_innovations
        #print("gave", node_innovations)
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
    
        
    


