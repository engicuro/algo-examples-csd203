class EdgeNode:
    def __init__(self, dest):
        self.dest = dest
        self.next = None

class VertexNode:
    def __init__(self, name):
        self.name = name
        self.edges_head = None
        self.next_vertex = None

    def add_edge(self, dest):
        e = EdgeNode(dest)
        e.next = self.edges_head
        self.edges_head = e

    def degree(self):
        d = 0
        e = self.edges_head
        while e:
            d += 1
            e = e.next
        return d

class Graph:
    def __init__(self):
        self.vertices_head = None

    def add_vertex(self, name):
        if self.find_vertex(name): return
        v = VertexNode(name)
        v.next_vertex = self.vertices_head
        self.vertices_head = v

    def find_vertex(self, name):
        curr = self.vertices_head
        while curr:
            if curr.name == name: return curr
            curr = curr.next_vertex
        return None

    def add_edge(self, u, v):
        u_n = self.find_vertex(u); v_n = self.find_vertex(v)
        if not u_n: self.add_vertex(u); u_n = self.find_vertex(u)
        if not v_n: self.add_vertex(v); v_n = self.find_vertex(v)
        u_n.add_edge(v)
        v_n.add_edge(u)

    def has_eulerian_cycle(self):
        curr = self.vertices_head
        while curr:
            if curr.degree() % 2 != 0:
                return False
            curr = curr.next_vertex
        return True

if __name__ == "__main__":
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")
    print("Graph has Eulerian cycle:", g.has_eulerian_cycle())
