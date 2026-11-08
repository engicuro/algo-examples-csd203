class EdgeNode:
    def __init__(self, dest, weight):
        self.dest = dest
        self.weight = weight
        self.next = None

class VertexNode:
    def __init__(self, name):
        self.name = name
        self.key = float('inf')
        self.parent = None
        self.in_mst = False
        self.edges_head = None
        self.next_vertex = None

    def add_edge(self, dest, weight):
        e = EdgeNode(dest, weight)
        e.next = self.edges_head
        self.edges_head = e

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

    def add_edge(self, u, v, weight):
        u_n = self.find_vertex(u); v_n = self.find_vertex(v)
        if not u_n: self.add_vertex(u); u_n = self.find_vertex(u)
        if not v_n: self.add_vertex(v); v_n = self.find_vertex(v)
        u_n.add_edge(v, weight)
        v_n.add_edge(u, weight)

    def prim_mst(self, start_name):
        curr = self.vertices_head
        while curr:
            curr.key = float('inf')
            curr.in_mst = False
            curr.parent = None
            curr = curr.next_vertex

        start = self.find_vertex(start_name)
        if not start: return
        start.key = 0

        while True:
            min_v = None
            curr = self.vertices_head
            while curr:
                if not curr.in_mst:
                    if min_v is None or curr.key < min_v.key:
                        min_v = curr
                curr = curr.next_vertex

            if min_v is None or min_v.key == float('inf'):
                break

            min_v.in_mst = True
            e = min_v.edges_head
            while e:
                neighbor = self.find_vertex(e.dest)
                if neighbor and not neighbor.in_mst:
                    if e.weight < neighbor.key:
                        neighbor.key = e.weight
                        neighbor.parent = min_v.name
                e = e.next

        print("Prim MST Edges:")
        curr = self.vertices_head
        while curr:
            if curr.parent:
                print(curr.parent, "-", curr.name, "weight:", curr.key)
            curr = curr.next_vertex

if __name__ == "__main__":
    g = Graph()
    g.add_edge("A", "B", 2)
    g.add_edge("A", "C", 3)
    g.add_edge("B", "C", 1)
    g.add_edge("B", "D", 4)
    g.add_edge("C", "D", 5)
    g.prim_mst("A")
