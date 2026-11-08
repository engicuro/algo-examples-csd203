class EdgeNode:
    def __init__(self, dest, weight):
        self.dest = dest
        self.weight = weight
        self.next = None

class VertexNode:
    def __init__(self, name):
        self.name = name
        self.dist = float('inf')
        self.visited = False
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

    def dijkstra(self, start_name):
        curr = self.vertices_head
        while curr:
            curr.dist = float('inf')
            curr.visited = False
            curr = curr.next_vertex
        
        start = self.find_vertex(start_name)
        if not start: return
        start.dist = 0

        while True:
            # find min unvisited vertex
            min_v = None
            curr = self.vertices_head
            while curr:
                if not curr.visited:
                    if min_v is None or curr.dist < min_v.dist:
                        min_v = curr
                curr = curr.next_vertex

            if min_v is None or min_v.dist == float('inf'):
                break

            min_v.visited = True
            e = min_v.edges_head
            while e:
                neighbor = self.find_vertex(e.dest)
                if neighbor and not neighbor.visited:
                    if min_v.dist + e.weight < neighbor.dist:
                        neighbor.dist = min_v.dist + e.weight
                e = e.next

        curr = self.vertices_head
        while curr:
            print("Shortest dist from", start_name, "to", curr.name, ":", curr.dist)
            curr = curr.next_vertex

if __name__ == "__main__":
    g = Graph()
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "C", 1)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 8)
    g.add_edge("C", "E", 10)
    g.add_edge("D", "E", 2)
    g.dijkstra("A")
