"""Adjacency List Representation of a Graph.

This module demonstrates an adjacency list graph implementation using
a dictionary of lists. It supports adding edges (directed and undirected),
displaying the graph structure, and querying neighbors of a vertex.
"""


class Graph:
    """Graph represented as an adjacency list (dict of lists).

    Attributes:
        adjacency_list (dict): Maps each vertex to a list of its neighbors.
        directed (bool): If True, edges are directed; otherwise undirected.
    """

    def __init__(self, directed=False):
        """Initialize an empty graph.

        Args:
            directed: If True, the graph is directed (default: False).
        """
        self.adjacency_list = {}
        self.directed = directed

    def add_vertex(self, vertex):
        """Add a vertex to the graph if it does not already exist.

        Args:
            vertex: The vertex to add (must be hashable).
        """
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, u, v):
        """Add an edge between vertices u and v.

        For undirected graphs, the edge is added in both directions.
        Vertices are created automatically if they do not exist.

        Args:
            u: The source vertex.
            v: The destination vertex.
        """
        self.add_vertex(u)
        self.add_vertex(v)
        self.adjacency_list[u].append(v)
        if not self.directed:
            self.adjacency_list[v].append(u)

    def display(self):
        """Print the adjacency list representation of the graph."""
        for vertex, neighbors in self.adjacency_list.items():
            print(f"{vertex} -> {neighbors}")

    def neighbors(self, vertex):
        """Return the list of neighbors for a given vertex.

        Args:
            vertex: The vertex whose neighbors to retrieve.

        Returns:
            list: The list of neighboring vertices.

        Raises:
            KeyError: If the vertex does not exist in the graph.
        """
        if vertex not in self.adjacency_list:
            raise KeyError(f"Vertex '{vertex}' not found in the graph.")
        return self.adjacency_list[vertex]

    def vertices(self):
        """Return a list of all vertices in the graph.

        Returns:
            list: All vertices.
        """
        return list(self.adjacency_list.keys())

    def edges(self):
        """Return a list of all edges in the graph.

        For undirected graphs, each edge appears once (u, v) where u <= v
        to avoid duplicates.

        Returns:
            list: List of (u, v) tuples representing edges.
        """
        seen = set()
        result = []
        for u, neighbors in self.adjacency_list.items():
            for v in neighbors:
                if self.directed:
                    result.append((u, v))
                else:
                    pair = tuple(sorted([u, v]))
                    if pair not in seen:
                        seen.add(pair)
                        result.append(pair)
        return result


if __name__ == "__main__":
    # --- Undirected Graph Example ---
    print("=== Undirected Graph ===")
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")
    g.add_edge("D", "E")

    print("Adjacency list:")
    g.display()

    print("\nVertices:", g.vertices())
    print("Edges:", g.edges())
    print("Neighbors of A:", g.neighbors("A"))
    print("Neighbors of D:", g.neighbors("D"))

    # --- Directed Graph Example ---
    print("\n=== Directed Graph ===")
    dg = Graph(directed=True)
    dg.add_edge(1, 2)
    dg.add_edge(1, 3)
    dg.add_edge(2, 4)
    dg.add_edge(3, 4)
    dg.add_edge(4, 5)

    print("Adjacency list:")
    dg.display()

    print("\nVertices:", dg.vertices())
    print("Edges:", dg.edges())
    print("Neighbors of 1:", dg.neighbors(1))
    print("Neighbors of 4:", dg.neighbors(4))

    # --- KeyError on missing vertex ---
    print("\n=== Error Handling ---")
    try:
        g.neighbors("Z")
    except KeyError as e:
        print(f"Caught expected error: {e}")
