class Node:
    # A structure to Node for graph
    def __init__(self, name: str, tickername: str, uid: int):
        self.uid = uid
        self.name = name
        self.ticker = tickername
        self.value = 0

    def setValue(self, x):
        # Essential to set the impact for epicenter first
        self.value = x

    def impactValue(self, impact):
        self.value += impact

class Connection:
    def __init__(self, node1: Node, node2: Node, rivalry=1, dependence=1, i_similarity=1):
        self.rivalry = rivalry
        self.dependence = dependence
        self.i_similarity = i_similarity

    def propagate(self, from_node, to_node):
        to_node.value = from_node*self.rivalry + from_node*self.dependence + from_node*self.i_similarity

class GraphDB:
    # Acts as a main DB for all records in Graph
    def __init__(self):
        self.nodes: dict = {}
        self.connections: dict = {}
        self.totalNodes = 0
        self.nodeuid = 0

    def getNewUID(self):
        self.nodeuid += 1
        return self.nodeuid
    
    def addNode(self, name, tickername, uid = getNewUID) -> Node:
        node = Node(name=name, tickername=tickername, uid=uid)
        self.nodes[node.uid] = node
        self.connections[node.name] = set()
        return node
    
    def registerConnection(self, node1, node2):
        try:
            if node2.name not in self.connections[node1]:
                self.connections[node1].add(node2.name)
                print('connection established')
            if node1.name not in self.connections[node2]:
                self.connections[node2].add(node1.name)
                print('connection established')
            
        except Exception as e:
            print("Error Occured")




        
