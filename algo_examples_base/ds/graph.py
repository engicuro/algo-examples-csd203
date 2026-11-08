class EdgeNode:
    def __init__(self, dest, weight=1):
        self.dest = dest
        self.weight = weight
        self.next = None

class VertexNode:
    def __init__(self, name):
        self.name = name
        self.edges_head = None
        self.next_vertex = None

    def add_edge(self, dest, weight=1):
        new_edge = EdgeNode(dest, weight)
        new_edge.next = self.edges_head
        self.edges_head = new_edge

class Graph:
    def __init__(self):
        self.vertices_head = None

    def add_vertex(self, name):
        if self.find_vertex(name) is not None:
            return
        v = VertexNode(name)
        v.next_vertex = self.vertices_head
        self.vertices_head = v

    def find_vertex(self, name):
        curr = self.vertices_head
        while curr is not None:
            if curr.name == name:
                return curr
            curr = curr.next_vertex
        return None

    def add_edge(self, u, v, weight=1):
        u_node = self.find_vertex(u)
        v_node = self.find_vertex(v)
        if u_node is None:
            self.add_vertex(u)
            u_node = self.find_vertex(u)
        if v_node is None:
            self.add_vertex(v)
            v_node = self.find_vertex(v)
        u_node.add_edge(v, weight)

    def display(self):
        v = self.vertices_head
        while v is not None:
            out = str(v.name) + ": "
            e = v.edges_head
            while e is not None:
                out += "(" + str(e.dest) + ", w=" + str(e.weight) + ") -> "
                e = e.next
            out += "None"
            print(out)
            v = v.next_vertex
