class Node:
    def __init__(self, id) -> None:
        self.min = 0
        self.max = 0
        self.id = id
        self.isterminal = True
        self.outneighs = set()
        self.inneighs = set()

class Edge:
    def __init__(self, vs : Node, ve : Node) -> None:
        self.start = vs
        self.end = ve

class Graph:
    def __init__(self, N : int, E : list):
        self.V = [Node(i) for i in range(N)]
        self.E = [Edge(self.V[e[0]], self.V[e[1]]) for e in E]

    def findneighs(self):
        for e in self.E:
            e.start.outneighs.add(e.end)
            e.start.isterminal = False

            e.end.inneighs.add(e.start)
    
