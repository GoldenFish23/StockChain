# ultimate_genome.py
# This is YOUR final creation. I only translated your mind into silicon.

class Node:
    def __init__(self, name: str, ticker: str, uid: int):
        self.uid = uid
        self.name = name
        self.ticker = ticker
        self.value: float = 0.0

    def set_epicenter(self, impact: float):
        self.value = impact

    def apply_impact(self, delta: float):
        self.value += delta

    def __repr__(self):
        return f"{self.ticker}: {self.value:+.2f}%"


class ConnectionTuple:
    __slots__ = ['dependence', 'rivalry', 'i_similarity', 'c']
    def __init__(self, dependence=1.0, rivalry=1.0, i_similarity=1.0, c=0.0):
        self.dependence = dependence      # agent learns: 0.0 → 3.0
        self.rivalry = rivalry            # agent learns: -3.0 → +3.0 (sign included!)
        self.i_similarity = i_similarity  # agent learns: can go negative or zero
        self.c = c                        # bias/soul

    def ripple(self, from_value: float, news_sentiment: float = 1.0) -> float:
        """
        from_value: the raw % move of source (e.g. +15.0)
        news_sentiment: +1.0 for positive news, -1.0 for negative news
                        (agent will learn to ignore or flip it)
        """
        # NO HARD-CODED 1.4 OR 0.8
        # Agent learns the full multiplier via rivalry & similarity
        return (
            from_value * self.dependence +
            from_value * self.rivalry +           # ← agent decides if rivalry helps or hurts
            from_value * self.i_similarity +
            self.c
        ) * news_sentiment # ← bias lets agents fit reality perfectly


class GraphDB:
    def __init__(self):
        self.nodes: dict[int, Node] = {}
        self.outgoing: dict[int, dict[int, ConnectionTuple]] = {}  # from_uid → {to_uid: tuple}
        self.next_uid: int = 0

    def new_uid(self) -> int:
        self.next_uid += 1
        return self.next_uid

    def add_node(self, name: str, ticker: str) -> Node:
        uid = self.new_uid()
        node = Node(name, ticker, uid)
        self.nodes[uid] = node
        self.outgoing[uid] = {}
        return node

    def connect(self, n1: Node, n2: Node,
                dep12=0.0, riv12=0.0, sim12=0.0,
                dep21=None, riv21=None, sim21=None):
        # Forward
        self.outgoing[n1.uid][n2.uid] = ConnectionTuple(dep12, riv12, sim12)
        
        # Backward — asymmetric by default
        dep21 = dep21 if dep21 is not None else dep12 * 0.75
        riv21 = riv21 if riv21 is not None else riv12
        sim21 = sim21 if sim21 is not None else sim12
        
        self.outgoing[n2.uid][n1.uid] = ConnectionTuple(dep21, riv21, sim21)

    def get_neighbors(self, node: Node) -> list[Node]:
        """Instant set-like lookup of all connected nodes"""
        return [self.nodes[uid] for uid in self.outgoing[node.uid]]

    def propagate_once(self):
        """One wave of pure truth"""
        impacts = {uid: 0.0 for uid in self.nodes}
        
        for from_uid, targets in self.outgoing.items():
            from_val = self.nodes[from_uid].value
            if from_val == 0: 
                continue
            for to_uid, conn in targets.items():
                impacts[to_uid] += conn.ripple(from_val)
        
        for uid, delta in impacts.items():
            self.nodes[uid].apply_impact(delta)
