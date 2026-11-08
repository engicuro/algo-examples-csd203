"""
Adjacency Matrix Representation of a Graph.

This module demonstrates the adjacency matrix representation for graphs,
which uses a 2D list (matrix) to store edge information between vertices.

Space Complexity: O(V^2) where V is the number of vertices.
Time Complexity:
  - Add edge: O(1)
  - Remove edge: O(1)
  - Check if edge exists: O(1)
  - Get all neighbors of a vertex: O(V)
  - Iterate over all edges: O(V^2)
"""


class Graph:
    """Graph representation using an adjacency matrix (2D list).

    The adjacency matrix is a V x V 2D list where matrix[i][j] is 1
    (or the edge weight) if there is an edge from vertex i to vertex j,
    and 0 otherwise.

    Attributes:
        num_vertices (int): The number of vertices in the graph.
        matrix (list[list[int]]): The 2D adjacency matrix.
        directed (bool): Whether the graph is directed or undirected.
    """

    def __init__(self, num_vertices: int, directed: bool = False):
        """Initialize the graph with a given number of vertices.

        Args:
            num_vertices: The number of vertices in the graph (labeled 0 to num_vertices-1).
            directed: If True, the graph is directed. If False, edges are bidirectional.

        Space: O(V^2) for the matrix allocation.
        """
        self.num_vertices = num_vertices
        self.directed = directed
        # Initialize a V x V matrix filled with zeros (no edges)
        self.matrix: list[list[int]] = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        """Add an edge between vertex u and vertex v.

        For undirected graphs, the edge is added in both directions.
        For weighted graphs, the weight replaces the default value of 1.

        Args:
            u: The source vertex index.
            v: The destination vertex index.
            weight: The weight of the edge (default 1 for unweighted graphs).

        Raises:
            IndexError: If u or v is out of the valid vertex range.

        Time: O(1)
        """
        if u < 0 or u >= self.num_vertices or v < 0 or v >= self.num_vertices:
            raise IndexError(
                f"Vertex index out of range. Must be in [0, {self.num_vertices - 1}]."
            )
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight

    def remove_edge(self, u: int, v: int) -> None:
        """Remove the edge between vertex u and vertex v.

        For undirected graphs, the edge is removed in both directions.

        Args:
            u: The source vertex index.
            v: The destination vertex index.

        Time: O(1)
        """
        if u < 0 or u >= self.num_vertices or v < 0 or v >= self.num_vertices:
            raise IndexError(
                f"Vertex index out of range. Must be in [0, {self.num_vertices - 1}]."
            )
        self.matrix[u][v] = 0
        if not self.directed:
            self.matrix[v][u] = 0

    def has_edge(self, u: int, v: int) -> bool:
        """Check if an edge exists between vertex u and vertex v.

        Args:
            u: The source vertex index.
            v: The destination vertex index.

        Returns:
            True if an edge exists, False otherwise.

        Time: O(1)
        """
        if u < 0 or u >= self.num_vertices or v < 0 or v >= self.num_vertices:
            raise IndexError(
                f"Vertex index out of range. Must be in [0, {self.num_vertices - 1}]."
            )
        return self.matrix[u][v] != 0

    def get_neighbors(self, u: int) -> list[int]:
        """Get all neighbors of vertex u.

        Args:
            u: The vertex index.

        Returns:
            A list of vertex indices that are adjacent to u.

        Time: O(V) — must scan the entire row.
        """
        if u < 0 or u >= self.num_vertices:
            raise IndexError(
                f"Vertex index out of range. Must be in [0, {self.num_vertices - 1}]."
            )
        return [v for v in range(self.num_vertices) if self.matrix[u][v] != 0]

    def display(self) -> None:
        """Print the adjacency matrix in a readable format.

        The output includes row and column headers for easy interpretation.

        Time: O(V^2) — prints every cell in the matrix.
        """
        # Print column headers
        print("   ", end="")
        for j in range(self.num_vertices):
            print(f"{j:4}", end="")
        print()
        print("   " + "----" * self.num_vertices)

        # Print each row with its row header
        for i in range(self.num_vertices):
            print(f"{i:2} |", end="")
            for j in range(self.num_vertices):
                print(f"{self.matrix[i][j]:4}", end="")
            print()

    def get_edge_count(self) -> int:
        """Return the total number of edges in the graph.

        For undirected graphs, each edge is counted once (upper triangle only).

        Returns:
            The number of edges.

        Time: O(V^2)
        """
        count = 0
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self.matrix[i][j] != 0:
                    count += 1
        # For undirected graphs, each edge appears twice in the matrix
        return count if self.directed else count // 2

    def __str__(self) -> str:
        """Return a string representation of the adjacency matrix."""
        rows = []
        for row in self.matrix:
            rows.append(" ".join(str(val) for val in row))
        return "\n".join(rows)


def space_complexity_discussion() -> None:
    """Print a discussion of the space complexity of adjacency matrix representation.

    Key points:
        - A VxV matrix requires V^2 storage regardless of the number of edges.
        - This is efficient for dense graphs (where E ≈ V^2).
        - This is wasteful for sparse graphs (where E << V^2).
        - Compared to adjacency list (O(V + E)), the matrix uses more space when
          the graph is sparse.
        - The matrix allows O(1) edge lookup, which is its main advantage.
    """
    print("""
╔══════════════════════════════════════════════════════════════╗
║           SPACE COMPLEXITY DISCUSSION                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Adjacency Matrix: O(V^2) space                             ║
║                                                              ║
║  • V = number of vertices                                   ║
║  • The matrix is always V x V, regardless of edge count     ║
║                                                              ║
║  PROS:                                                      ║
║  • O(1) edge lookup / insertion / deletion                  ║
║  • Simple to implement and understand                       ║
║  • Efficient for dense graphs (E ≈ V^2)                     ║
║  • Cache-friendly due to contiguous memory layout           ║
║                                                              ║
║  CONS:                                                      ║
║  • Wastes space for sparse graphs (most entries are 0)      ║
║  • Adding a new vertex requires resizing the entire matrix  ║
║  • O(V^2) space even if graph has very few edges            ║
║                                                              ║
║  COMPARISON WITH ADJACENCY LIST:                            ║
║  • Adjacency list: O(V + E) space                          ║
║  • Matrix wins when E ≈ V^2 (dense graphs)                 ║
║  • List wins when E << V^2 (sparse graphs)                 ║
║                                                              ║
║  EXAMPLE:                                                   ║
║  • 1000 vertices, 2000 edges (sparse):                     ║
║    Matrix: 1,000,000 entries                               ║
║    List:   ~4,000 entries                                  ║
║    → Matrix uses ~250x more space                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    # ── Example 1: Undirected Unweighted Graph ──────────────────
    print("=" * 55)
    print("Example 1: Undirected Unweighted Graph")
    print("=" * 55)

    g = Graph(num_vertices=5, directed=False)
    g.add_edge(0, 1)
    g.add_edge(0, 4)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(1, 4)
    g.add_edge(2, 3)
    g.add_edge(3, 4)

    print(f"\nNumber of vertices: {g.num_vertices}")
    print(f"Number of edges: {g.get_edge_count()}")
    print(f"Is edge (0,1) present? {g.has_edge(0, 1)}")
    print(f"Is edge (2,4) present? {g.has_edge(2, 4)}")
    print(f"Neighbors of vertex 1: {g.get_neighbors(1)}")
    print(f"Neighbors of vertex 3: {g.get_neighbors(3)}")

    print("\nAdjacency Matrix:")
    g.display()

    # ── Example 2: Directed Weighted Graph ──────────────────────
    print("\n" + "=" * 55)
    print("Example 2: Directed Weighted Graph")
    print("=" * 55)

    dg = Graph(num_vertices=4, directed=True)
    dg.add_edge(0, 1, weight=5)
    dg.add_edge(0, 2, weight=3)
    dg.add_edge(1, 2, weight=2)
    dg.add_edge(2, 3, weight=7)
    dg.add_edge(3, 0, weight=1)

    print(f"\nNumber of vertices: {dg.num_vertices}")
    print(f"Number of edges: {dg.get_edge_count()}")
    print(f"Is edge (0,1) present? {dg.has_edge(0, 1)}")
    print(f"Is edge (1,0) present? {dg.has_edge(1, 0)}  (reverse direction)")
    print(f"Neighbors of vertex 0: {dg.get_neighbors(0)}")

    print("\nAdjacency Matrix:")
    dg.display()

    # ── Example 3: Remove an Edge ───────────────────────────────
    print("\n" + "=" * 55)
    print("Example 3: Remove an Edge")
    print("=" * 55)

    g.remove_edge(1, 4)
    print(f"\nAfter removing edge (1,4):")
    print(f"Is edge (1,4) present? {g.has_edge(1, 4)}")
    print(f"Number of edges: {g.get_edge_count()}")
    print(f"Neighbors of vertex 1: {g.get_neighbors(1)}")

    print("\nAdjacency Matrix:")
    g.display()

    # ── Space Complexity Discussion ─────────────────────────────
    space_complexity_discussion()
