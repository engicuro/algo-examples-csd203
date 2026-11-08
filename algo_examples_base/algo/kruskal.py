class EdgeRecord:
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight
        self.next = None

class SubsetNode:
    def __init__(self, name):
        self.name = name
        self.parent = name
        self.rank = 0
        self.next = None

class DisjointSet:
    def __init__(self):
        self.head = None

    def make_set(self, name):
        if self.find_node(name): return
        n = SubsetNode(name)
        n.next = self.head
        self.head = n

    def find_node(self, name):
        curr = self.head
        while curr:
            if curr.name == name: return curr
            curr = curr.next_vertex if hasattr(curr, 'next_vertex') else curr.next
        return None

    def find(self, name):
        node = self.find_node(name)
        if not node: return None
        curr = node
        while curr.parent != curr.name:
            curr = self.find_node(curr.parent)
        return curr.name

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            node_u = self.find_node(root_u)
            node_v = self.find_node(root_v)
            if node_u.rank < node_v.rank:
                node_u.parent = root_v
            elif node_u.rank > node_v.rank:
                node_v.parent = root_u
            else:
                node_v.parent = root_u
                node_u.rank += 1

def kruskal(edges_head):
    # Sort edges linked list using insertion sort
    sorted_edges = None
    curr = edges_head
    while curr:
        nxt = curr.next
        if sorted_edges is None or sorted_edges.weight >= curr.weight:
            curr.next = sorted_edges
            sorted_edges = curr
        else:
            s = sorted_edges
            while s.next and s.next.weight < curr.weight:
                s = s.next
            curr.next = s.next
            s.next = curr
        curr = nxt

    ds = DisjointSet()
    curr = sorted_edges
    while curr:
        ds.make_set(curr.u)
        ds.make_set(curr.v)
        curr = curr.next

    print("Kruskal MST Edges:")
    curr = sorted_edges
    while curr:
        if ds.find(curr.u) != ds.find(curr.v):
            print(curr.u, "-", curr.v, "weight:", curr.weight)
            ds.union(curr.u, curr.v)
        curr = curr.next

if __name__ == "__main__":
    e1 = EdgeRecord("A", "B", 10)
    e2 = EdgeRecord("A", "C", 6)
    e3 = EdgeRecord("A", "D", 5)
    e4 = EdgeRecord("C", "D", 4)
    e5 = EdgeRecord("B", "D", 15)
    e1.next = e2; e2.next = e3; e3.next = e4; e4.next = e5
    kruskal(e1)
