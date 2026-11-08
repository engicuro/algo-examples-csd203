"""
26_graph_basics.py - Graph Basics in Python

A graph is a collection of vertices (nodes) connected by edges.
Graphs model pairwise relationships between objects and are foundational
to many algorithms (BFS, DFS, shortest path, MST, topological sort, etc.).

Topics covered:
  - Vertex and edge definitions
  - Directed vs undirected graphs
  - Weighted vs unweighted graphs
  - Adjacency list representation (dict of lists/dicts)
  - Adjacency matrix representation (2-D list)
  - Basic graph operations: add vertex, add edge, remove edge, display
  - Degree of a vertex (in-degree, out-degree for directed graphs)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple


# --------------------------------------------------------------------------- #
#  Vertex and Edge — conceptual building blocks
# --------------------------------------------------------------------------- #

class Vertex:
    """A vertex (node) in a graph.

    Attributes:
        label: A unique identifier for this vertex.
        data:  Optional payload stored at this vertex.
    """

    def __init__(self, label: Any, data: Any = None) -> None:
        self.label: Any = label
        self.data: Any = data

    def __repr__(self) -> str:
        return f"Vertex({self.label!r})"

    def __hash__(self) -> int:
        return hash(self.label)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vertex):
            return NotImplemented
        return self.label == other.label


class Edge:
    """An edge connecting two vertices in a graph.

    For a directed edge, source -> destination.
    For an undirected edge, source <-> destination (both directions).

    Attributes:
        source:      The starting vertex.
        destination: The ending vertex.
        weight:      Optional numeric weight/cost of the edge.
        directed:    True if this is a directed edge.
    """

    def __init__(
        self,
        source: Vertex,
        destination: Vertex,
        weight: Optional[float] = None,
        directed: bool = False,
    ) -> None:
        self.source: Vertex = source
        self.destination: Vertex = destination
        self.weight: Optional[float] = weight
        self.directed: bool = directed

    def __repr__(self) -> str:
        arrow = "->" if self.directed else "<->"
        wt = f" (weight={self.weight})" if self.weight is not None else ""
        return f"Edge({self.source.label!r} {arrow} {self.destination.label!r}{wt})"


# --------------------------------------------------------------------------- #
#  Graph — adjacency-list based representation
# --------------------------------------------------------------------------- #

class Graph:
    """Graph implemented with an adjacency list.

    The adjacency list is a dictionary mapping each vertex label to a dict
    of neighbour labels -> edge weight (or None for unweighted).

    Supports:
      - Directed and undirected graphs
      - Weighted and unweighted edges
      - Vertex and edge addition/removal
      - Degree computation (in-degree, out-degree, total degree)
    """

    def __init__(self, directed: bool = False, weighted: bool = False) -> None:
        self.directed: bool = directed
        self.weighted: bool = weighted
        # adjacency_list[vertex_label] -> {neighbour_label: weight_or_none}
        self.adjacency_list: Dict[Any, Dict[Any, Optional[float]]] = {}
        # Store Vertex objects for reference
        self.vertices: Dict[Any, Vertex] = {}

    # ------------------------------------------------------------------ #
    #  Vertex operations
    # ------------------------------------------------------------------ #

    def add_vertex(self, label: Any, data: Any = None) -> None:
        """Add a vertex with the given label if it does not already exist."""
        if label not in self.vertices:
            self.vertices[label] = Vertex(label, data)
            self.adjacency_list[label] = {}

    def remove_vertex(self, label: Any) -> None:
        """Remove a vertex and all edges incident to it — O(V)."""
        if label not in self.vertices:
            return

        # Remove all edges pointing *to* this vertex
        for other_label in self.adjacency_list:
            self.adjacency_list[other_label].pop(label, None)

        # Remove the vertex itself
        del self.adjacency_list[label]
        del self.vertices[label]

    def has_vertex(self, label: Any) -> bool:
        """Return True if a vertex with this label exists."""
        return label in self.vertices

    # ------------------------------------------------------------------ #
    #  Edge operations
    # ------------------------------------------------------------------ #

    def add_edge(
        self,
        source: Any,
        destination: Any,
        weight: Optional[float] = None,
    ) -> None:
        """Add an edge from source to destination.

        For undirected graphs, also adds the reverse edge.
        For weighted graphs, stores the weight; otherwise stores None.

        Raises:
            KeyError: If either vertex does not exist.
        """
        if source not in self.vertices:
            raise KeyError(f"Vertex {source!r} not found — add it first.")
        if destination not in self.vertices:
            raise KeyError(f"Vertex {destination!r} not found — add it first.")

        # Store weight only if the graph is weighted
        edge_weight = weight if self.weighted else None

        self.adjacency_list[source][destination] = edge_weight

        # For undirected graphs, add the reverse edge as well
        if not self.directed:
            self.adjacency_list[destination][source] = edge_weight

    def remove_edge(self, source: Any, destination: Any) -> None:
        """Remove the edge from source to destination.

        For undirected graphs, also removes the reverse edge.
        """
        self.adjacency_list.get(source, {}).pop(destination, None)
        if not self.directed:
            self.adjacency_list.get(destination, {}).pop(source, None)

    def has_edge(self, source: Any, destination: Any) -> bool:
        """Return True if an edge exists from source to destination."""
        return destination in self.adjacency_list.get(source, {})

    def get_edge_weight(self, source: Any, destination: Any) -> Optional[float]:
        """Return the weight of the edge (source, destination), or None."""
        return self.adjacency_list.get(source, {}).get(destination)

    # ------------------------------------------------------------------ #
    #  Degree helpers
    # ------------------------------------------------------------------ #

    def degree(self, label: Any) -> int:
        """Return the total degree of a vertex (number of incident edges).

        For directed graphs this is the sum of in-degree and out-degree.
        """
        out_deg = len(self.adjacency_list.get(label, {}))
        in_deg = sum(
            1 for other in self.adjacency_list if label in self.adjacency_list[other]
        )
        return out_deg + in_deg if self.directed else out_deg

    def out_degree(self, label: Any) -> int:
        """Return the out-degree of a vertex (edges going out)."""
        return len(self.adjacency_list.get(label, {}))

    def in_degree(self, label: Any) -> int:
        """Return the in-degree of a vertex (edges coming in).

        Meaningful for directed graphs; equals out-degree for undirected.
        """
        return sum(
            1 for other in self.adjacency_list if label in self.adjacency_list[other]
        )

    # ------------------------------------------------------------------ #
    #  Display
    # ------------------------------------------------------------------ #

    def display(self) -> str:
        """Return a readable string representation of the graph."""
        lines: List[str] = []
        edge_type = "directed" if self.directed else "undirected"
        weight_type = "weighted" if self.weighted else "unweighted"
        lines.append(f"Graph ({edge_type}, {weight_type}):")
        seen: Set[Tuple[Any, Any]] = set()
        for vertex_label, neighbours in self.adjacency_list.items():
            if neighbours:
                for neighbour, weight in neighbours.items():
                    # For undirected graphs, show each edge only once
                    if not self.directed:
                        key = tuple(sorted([vertex_label, neighbour]))
                        if key in seen:
                            continue
                        seen.add(key)
                    wt_str = f" [{weight}]" if weight is not None else ""
                    arrow = "->" if self.directed else "--"
                    lines.append(f"  {vertex_label}{arrow}{neighbour}{wt_str}")
            else:
                lines.append(f"  {vertex_label} (no edges)")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #  Utility
    # ------------------------------------------------------------------ #

    def vertex_count(self) -> int:
        """Return the number of vertices."""
        return len(self.vertices)

    def edge_count(self) -> int:
        """Return the number of edges.

        For undirected graphs each edge is counted once (stored in both
        directions in the adjacency list, so we divide by 2).
        """
        total = sum(len(nb) for nb in self.adjacency_list.values())
        return total if self.directed else total // 2

    def get_vertices(self) -> List[Any]:
        """Return a list of all vertex labels."""
        return list(self.vertices.keys())

    def get_edges(self) -> List[Edge]:
        """Return a list of all Edge objects in the graph."""
        edges: List[Edge] = []
        seen: Set[Tuple[Any, Any]] = set()
        for src, neighbours in self.adjacency_list.items():
            for dst, weight in neighbours.items():
                # For undirected graphs, avoid duplicate edges
                if not self.directed:
                    key = tuple(sorted([src, dst]))
                    if key in seen:
                        continue
                    seen.add(key)
                edges.append(
                    Edge(
                        self.vertices[src],
                        self.vertices[dst],
                        weight=weight,
                        directed=self.directed,
                    )
                )
        return edges


# --------------------------------------------------------------------------- #
#  Adjacency Matrix — alternative representation
# --------------------------------------------------------------------------- #

class AdjacencyMatrixGraph:
    """Graph implemented with an adjacency matrix (2-D list).

    Suitable for dense graphs where the number of edges approaches V².
    Matrix[i][j] stores the weight of edge (i, j), or None if no edge.

    Vertex labels are mapped to integer indices internally.
    """

    def __init__(self, num_vertices: int, directed: bool = False) -> None:
        self.num_vertices: int = num_vertices
        self.directed: bool = directed
        # None means "no edge"; a numeric value means an edge with that weight.
        self.matrix: List[List[Optional[float]]] = [
            [None] * num_vertices for _ in range(num_vertices)
        ]
        self.label_to_index: Dict[Any, int] = {}
        self.index_to_label: Dict[int, Any] = {}

    def add_vertex(self, label: Any) -> None:
        """Register a vertex label to an internal index."""
        if label in self.label_to_index:
            return
        idx = len(self.label_to_index)
        if idx >= self.num_vertices:
            raise OverflowError("Maximum vertex capacity reached.")
        self.label_to_index[label] = idx
        self.index_to_label[idx] = label

    def add_edge(
        self, source: Any, destination: Any, weight: Optional[float] = 1.0
    ) -> None:
        """Add an edge (optionally weighted) between two registered vertices."""
        if source not in self.label_to_index:
            raise KeyError(f"Vertex {source!r} not registered.")
        if destination not in self.label_to_index:
            raise KeyError(f"Vertex {destination!r} not registered.")
        i, j = self.label_to_index[source], self.label_to_index[destination]
        self.matrix[i][j] = weight
        if not self.directed:
            self.matrix[j][i] = weight

    def has_edge(self, source: Any, destination: Any) -> bool:
        """Return True if an edge exists from source to destination."""
        if source not in self.label_to_index or destination not in self.label_to_index:
            return False
        i, j = self.label_to_index[source], self.label_to_index[destination]
        return self.matrix[i][j] is not None

    def get_edge_weight(self, source: Any, destination: Any) -> Optional[float]:
        """Return the weight of the edge, or None if no edge exists."""
        if source not in self.label_to_index or destination not in self.label_to_index:
            return None
        i, j = self.label_to_index[source], self.label_to_index[destination]
        return self.matrix[i][j]

    def display(self) -> str:
        """Print the matrix with vertex labels as row/column headers."""
        labels = [self.index_to_label[i] for i in range(self.num_vertices)]
        header = "      " + "   ".join(f"{l:>4}" for l in labels)
        lines = [header, "      " + "----" * len(labels)]
        for i, label in enumerate(labels):
            row = "  " + f"{label:>4}" + " |"
            for val in self.matrix[i]:
                if val is None:
                    row += "    ."
                else:
                    row += f"{val:>5.1f}" if val != int(val) else f"{int(val):>5}"
            lines.append(row)
        return "\n".join(lines)


# --------------------------------------------------------------------------- #
#  Main — example usage
# --------------------------------------------------------------------------- #

def main() -> None:
    """Run graph basics demonstrations."""
    print("=" * 60)
    print("Chapter 26 — Graph Basics")
    print("=" * 60)

    # ------------------------------------------------------------------ #
    #  1. Undirected, unweighted graph
    # ------------------------------------------------------------------ #
    print("\n--- 1. Undirected, Unweighted Graph ---")
    g1 = Graph(directed=False, weighted=False)
    for v in ["A", "B", "C", "D", "E"]:
        g1.add_vertex(v)

    g1.add_edge("A", "B")
    g1.add_edge("A", "C")
    g1.add_edge("B", "D")
    g1.add_edge("C", "D")
    g1.add_edge("D", "E")

    print(g1.display())
    print(f"  Vertices: {g1.vertex_count()}, Edges: {g1.edge_count()}")
    print(f"  Degree of A: {g1.degree('A')}")
    print(f"  Degree of D: {g1.degree('D')}")
    print(f"  Has edge A-B? {g1.has_edge('A', 'B')}")
    print(f"  Has edge A-D? {g1.has_edge('A', 'D')}")

    # ------------------------------------------------------------------ #
    #  2. Directed, unweighted graph
    # ------------------------------------------------------------------ #
    print("\n--- 2. Directed, Unweighted Graph ---")
    g2 = Graph(directed=True, weighted=False)
    for v in ["S", "A", "B", "C", "T"]:
        g2.add_vertex(v)

    g2.add_edge("S", "A")
    g2.add_edge("S", "B")
    g2.add_edge("A", "C")
    g2.add_edge("B", "C")
    g2.add_edge("C", "T")

    print(g2.display())
    print(f"  Vertices: {g2.vertex_count()}, Edges: {g2.edge_count()}")
    print(f"  Out-degree of S: {g2.out_degree('S')}")
    print(f"  In-degree of C:  {g2.in_degree('C')}")
    print(f"  Total degree of C: {g2.degree('C')}")

    # ------------------------------------------------------------------ #
    #  3. Undirected, weighted graph
    # ------------------------------------------------------------------ #
    print("\n--- 3. Undirected, Weighted Graph ---")
    g3 = Graph(directed=False, weighted=True)
    for v in ["NYC", "LA", "CHI", "HOU"]:
        g3.add_vertex(v)

    g3.add_edge("NYC", "LA", weight=2451)
    g3.add_edge("NYC", "CHI", weight=713)
    g3.add_edge("LA", "CHI", weight=1745)
    g3.add_edge("LA", "HOU", weight=1374)
    g3.add_edge("CHI", "HOU", weight=925)

    print(g3.display())
    print(f"  Edge count: {g3.edge_count()}")
    print(f"  Weight NYC->LA: {g3.get_edge_weight('NYC', 'LA')}")
    print(f"  Weight LA->NYC: {g3.get_edge_weight('LA', 'NYC')}")  # same (undirected)

    # ------------------------------------------------------------------ #
    #  4. Directed, weighted graph
    # ------------------------------------------------------------------ #
    print("\n--- 4. Directed, Weighted Graph ---")
    g4 = Graph(directed=True, weighted=True)
    for v in ["A", "B", "C", "D"]:
        g4.add_vertex(v)

    g4.add_edge("A", "B", weight=4)
    g4.add_edge("A", "C", weight=2)
    g4.add_edge("B", "C", weight=5)
    g4.add_edge("B", "D", weight=10)
    g4.add_edge("C", "D", weight=3)

    print(g4.display())
    print(f"  Edge count: {g4.edge_count()}")
    print(f"  Weight A->C: {g4.get_edge_weight('A', 'C')}")
    print(f"  Has edge C->A? {g4.has_edge('C', 'A')}")  # False (directed)

    # ------------------------------------------------------------------ #
    #  5. Vertex and edge removal
    # ------------------------------------------------------------------ #
    print("\n--- 5. Vertex and Edge Removal ---")
    g1.remove_edge("A", "B")
    print("After removing edge A-B:")
    print(g1.display())

    g1.remove_vertex("E")
    print("\nAfter removing vertex E:")
    print(g1.display())
    print(f"  Vertices: {g1.vertex_count()}, Edges: {g1.edge_count()}")

    # ------------------------------------------------------------------ #
    #  6. Adjacency Matrix representation
    # ------------------------------------------------------------------ #
    print("\n--- 6. Adjacency Matrix Representation ---")
    mg = AdjacencyMatrixGraph(num_vertices=4, directed=False)
    for v in ["A", "B", "C", "D"]:
        mg.add_vertex(v)

    mg.add_edge("A", "B", weight=1)
    mg.add_edge("A", "C", weight=1)
    mg.add_edge("B", "D", weight=1)
    mg.add_edge("C", "D", weight=1)

    print(mg.display())
    print(f"  Has edge A-B? {mg.has_edge('A', 'B')}")
    print(f"  Has edge B-A? {mg.has_edge('B', 'A')}")  # True (undirected)
    print(f"  Weight A->C: {mg.get_edge_weight('A', 'C')}")

    # ------------------------------------------------------------------ #
    #  7. Edge list and vertex listing
    # ------------------------------------------------------------------ #
    print("\n--- 7. Listing Vertices and Edges ---")
    print(f"  Vertices in g4: {g4.get_vertices()}")
    print(f"  Edges in g4:")
    for e in g4.get_edges():
        print(f"    {e}")


if __name__ == "__main__":
    main()
