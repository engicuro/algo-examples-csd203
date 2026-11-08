"""
27_edge_list.py - Edge List Graph Representation

An edge list is one of the simplest ways to represent a graph.
The graph is stored as a list (or set) of edges, where each edge
is a tuple (or named structure) of two vertices and optionally a weight.

Properties:
  - Space: O(E) — one entry per edge
  - Add edge: O(1) amortized (append to list)
  - Check if edge exists: O(E) — linear scan
  - Iterate all edges: O(E)
  - Iterate neighbors of a vertex: O(E) — must scan all edges
  - Not efficient for dense graphs or frequent edge lookups

Topics covered:
  - Edge list storage (list of tuples)
  - Directed and undirected edge insertion
  - Weighted and unweighted edges
  - Display / string representation
  - Vertex and edge queries
  - Basic graph operations (add/remove edge, has edge, neighbors)
"""

from __future__ import annotations

from typing import Any, Hashable


class EdgeListGraph:
    """Graph represented as an edge list.

    Each edge is stored as a tuple (u, v, weight) internally.
    For unweighted graphs, weight defaults to 1.

    Supports both directed and undirected graphs.
    """

    def __init__(self, directed: bool = False) -> None:
        """Initialize an empty graph.

        Args:
            directed: If True, edges are one-way (u -> v only).
                      If False, each edge is stored in both directions.
        """
        self._directed: bool = directed
        self._edges: list[tuple[Hashable, Hashable, float]] = []
        self._vertices: set[Hashable] = set()

    # ------------------------------------------------------------------ #
    #  Properties
    # ------------------------------------------------------------------ #

    @property
    def vertices(self) -> set[Hashable]:
        """Return the set of all vertices in the graph."""
        return self._vertices.copy()

    @property
    def edges(self) -> list[tuple[Hashable, Hashable, float]]:
        """Return a copy of the internal edge list."""
        return list(self._edges)

    @property
    def num_vertices(self) -> int:
        """Return the number of vertices."""
        return len(self._vertices)

    @property
    def num_edges(self) -> int:
        """Return the number of edges (counts each directed entry)."""
        return len(self._edges)

    # ------------------------------------------------------------------ #
    #  Core operations
    # ------------------------------------------------------------------ #

    def add_vertex(self, vertex: Hashable) -> None:
        """Add a single vertex to the graph if it does not already exist.

        Args:
            vertex: A hashable identifier for the vertex.
        """
        self._vertices.add(vertex)

    def add_edge(self, u: Hashable, v: Hashable, weight: float = 1.0) -> None:
        """Add an edge from u to v with the given weight — O(1) amortized.

        For undirected graphs, the reverse edge (v, u) is also added.
        Both vertices are registered in the vertex set automatically.

        Args:
            u: Source vertex.
            v: Destination vertex.
            weight: Edge weight (default 1.0 for unweighted graphs).
        """
        self._vertices.add(u)
        self._vertices.add(v)
        self._edges.append((u, v, weight))
        if not self._directed:
            self._edges.append((v, u, weight))

    def remove_edge(self, u: Hashable, v: Hashable, weight: float | None = None) -> bool:
        """Remove the edge (u, v) from the graph — O(E).

        For undirected graphs, removes both (u, v) and (v, u).

        Args:
            u: Source vertex.
            v: Destination vertex.
            weight: If provided, only remove the edge with this exact weight.
                    If None, remove any edge matching (u, v).

        Returns:
            True if at least one edge was removed, False otherwise.
        """
        removed = False

        # Build a new list excluding matching edges
        new_edges: list[tuple[Hashable, Hashable, float]] = []
        for edge in self._edges:
            eu, ev, ew = edge
            if eu == u and ev == v:
                if weight is not None and ew != weight:
                    new_edges.append(edge)
                else:
                    removed = True
                    continue  # skip this edge
            elif not self._directed and eu == v and ev == u:
                # For undirected, also skip the reverse edge
                if weight is not None and ew != weight:
                    new_edges.append(edge)
                else:
                    removed = True
                    continue
            else:
                new_edges.append(edge)

        self._edges = new_edges
        return removed

    def has_edge(self, u: Hashable, v: Hashable, weight: float | None = None) -> bool:
        """Return True if an edge (u, v) exists — O(E).

        Args:
            u: Source vertex.
            v: Destination vertex.
            weight: If provided, check for an edge with this exact weight.
                    If None, any weight matches.
        """
        for eu, ev, ew in self._edges:
            if eu == u and ev == v:
                if weight is None or ew == weight:
                    return True
        return False

    def neighbors(self, vertex: Hashable) -> list[tuple[Hashable, float]]:
        """Return all (neighbor, weight) pairs reachable from `vertex` — O(E).

        Args:
            vertex: The source vertex.

        Returns:
            List of (neighbor, weight) tuples.
        """
        result: list[tuple[Hashable, float]] = []
        for u, v, w in self._edges:
            if u == vertex:
                result.append((v, w))
        return result

    # ------------------------------------------------------------------ #
    #  Display
    # ------------------------------------------------------------------ #

    def display(self) -> str:
        """Return a human-readable string of the graph's edge list.

        Example:
            A --(1.0)--> B
            A --(1.0)--> C
            B --(1.0)--> A
            ...
        """
        if not self._edges:
            return "(empty graph)"

        lines: list[str] = []
        for u, v, w in self._edges:
            arrow = "->" if self._directed else "--"
            lines.append(f"  {u} {arrow} {v}  (weight={w})")
        return "\n".join(lines)

    def display_adjacency(self) -> str:
        """Return a grouped adjacency-view string from the edge list — O(E).

        Groups edges by source vertex for easier reading.
        """
        if not self._vertices:
            return "(empty graph)"

        lines: list[str] = []
        for vertex in sorted(self._vertices, key=str):
            nbrs = self.neighbors(vertex)
            if nbrs:
                nbr_strs = [f"{v}(w={w})" for v, w in nbrs]
                lines.append(f"  {vertex}: [{', '.join(nbr_strs)}]")
            else:
                lines.append(f"  {vertex}: []")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #  Utility
    # ------------------------------------------------------------------ #

    def clear(self) -> None:
        """Remove all vertices and edges from the graph."""
        self._edges.clear()
        self._vertices.clear()

    def is_directed(self) -> bool:
        """Return True if this is a directed graph."""
        return self._directed


def main() -> None:
    """Run edge list graph demonstrations."""
    print("=" * 60)
    print("Chapter 27 — Edge List Graph Representation")
    print("=" * 60)

    # ------------------------------------------------------------------ #
    #  1. Undirected unweighted graph
    # ------------------------------------------------------------------ #
    print("\n--- 1. Undirected Unweighted Graph ---")
    g = EdgeListGraph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")

    print(f"Vertices: {g.vertices}")
    print(f"Edge count: {g.num_edges}")
    print(f"Vertex count: {g.num_vertices}")
    print("\nEdge list:")
    print(g.display())
    print("\nAdjacency view:")
    print(g.display_adjacency())

    # ------------------------------------------------------------------ #
    #  2. Directed weighted graph
    # ------------------------------------------------------------------ #
    print("\n--- 2. Directed Weighted Graph ---")
    dg = EdgeListGraph(directed=True)
    dg.add_edge("S", "A", weight=5.0)
    dg.add_edge("S", "B", weight=3.0)
    dg.add_edge("A", "C", weight=2.0)
    dg.add_edge("B", "C", weight=1.0)
    dg.add_edge("C", "D", weight=4.0)

    print(f"Vertices: {dg.vertices}")
    print(f"Edge count: {dg.num_edges}")
    print("\nEdge list:")
    print(dg.display())
    print("\nAdjacency view:")
    print(dg.display_adjacency())

    # ------------------------------------------------------------------ #
    #  3. Edge queries
    # ------------------------------------------------------------------ #
    print("\n--- 3. Edge Queries ---")
    print(f"  g has edge A--B: {g.has_edge('A', 'B')}")
    print(f"  g has edge A--D: {g.has_edge('A', 'D')}")
    print(f"  dg has edge S->A: {dg.has_edge('S', 'A')}")
    print(f"  dg has edge A->S: {dg.has_edge('A', 'S')}")
    print(f"  Neighbors of A in g: {g.neighbors('A')}")
    print(f"  Neighbors of S in dg: {dg.neighbors('S')}")

    # ------------------------------------------------------------------ #
    #  4. Remove edge
    # ------------------------------------------------------------------ #
    print("\n--- 4. Remove Edge ---")
    print(f"  Before remove: g has edge A--B = {g.has_edge('A', 'B')}")
    g.remove_edge("A", "B")
    print(f"  After remove:  g has edge A--B = {g.has_edge('A', 'B')}")
    print(f"  Edge count after removal: {g.num_edges}")
    print("\n  Edge list after removal:")
    print(g.display())

    # ------------------------------------------------------------------ #
    #  5. Clear and empty graph
    # ------------------------------------------------------------------ #
    print("\n--- 5. Clear Graph ---")
    g.clear()
    print(f"  After clear() -> vertices: {g.vertices}, edges: {g.num_edges}")
    print(f"  Display: {g.display()}")

    # ------------------------------------------------------------------ #
    #  6. Weighted edge removal (specific weight)
    # ------------------------------------------------------------------ #
    print("\n--- 6. Remove Edge by Weight ---")
    wg = EdgeListGraph(directed=False)
    wg.add_edge("X", "Y", weight=1.0)
    wg.add_edge("X", "Y", weight=5.0)  # parallel edge with different weight
    wg.add_edge("Y", "Z", weight=2.0)
    print(f"  Before removal:\n{wg.display()}")
    wg.remove_edge("X", "Y", weight=1.0)
    print(f"  After removing X--Y with weight=1.0:\n{wg.display()}")


if __name__ == "__main__":
    main()
