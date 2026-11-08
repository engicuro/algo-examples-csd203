class EdgeNode:
    def __init__(self, dest):
        self.dest = dest
        self.next = None

class VertexNode:
    def __init__(self, name):
        self.name = name
        self.visited = False
        self.edges_head = None
        self.next_vertex = None

    def add_edge(self, dest):
        e = EdgeNode(dest)
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

    def add_edge(self, u, v):
        u_n = self.find_vertex(u); v_n = self.find_vertex(v)
        if not u_n: self.add_vertex(u); u_n = self.find_vertex(u)
        if not v_n: self.add_vertex(v); v_n = self.find_vertex(v)
        u_n.add_edge(v)
        v_n.add_edge(u)

    def reset_visited(self):
        curr = self.vertices_head
        while curr:
            curr.visited = False
            curr = curr.next_vertex

    def dfs(self, start_name):
        self.reset_visited()
        start = self.find_vertex(start_name)
        print("DFS Traversal:")
        self._dfs_rec(start)
        print()

    def _dfs_rec(self, vertex):
        if not vertex or vertex.visited: return
        vertex.visited = True
        print(vertex.name, end=" ")
        e = vertex.edges_head
        while e:
            neighbor = self.find_vertex(e.dest)
            self._dfs_rec(neighbor)
            e = e.next

class QueueNode:
    def __init__(self, val):
        self.val = val
        self.next = None

class Queue:
    def __init__(self):
        self.front = self.rear = None
    def enqueue(self, val):
        n = QueueNode(val)
        if not self.rear: self.front = self.rear = n
        else: self.rear.next = n; self.rear = n
    def dequeue(self):
        if not self.front: return None
        v = self.front.val
        self.front = self.front.next
        if not self.front: self.rear = None
        return v
    def is_empty(self): return self.front is None

def bfs(graph, start_name):
    graph.reset_visited()
    q = Queue()
    start = graph.find_vertex(start_name)
    if not start: return
    start.visited = True
    q.enqueue(start_name)
    print("BFS Traversal:")
    while not q.is_empty():
        curr_name = q.dequeue()
        print(curr_name, end=" ")
        curr_v = graph.find_vertex(curr_name)
        e = curr_v.edges_head
        while e:
            neighbor = graph.find_vertex(e.dest)
            if neighbor and not neighbor.visited:
                neighbor.visited = True
                q.enqueue(neighbor.name)
            e = e.next
    print()

if __name__ == "__main__":
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "E")
    g.dfs("A")
    bfs(g, "A")
