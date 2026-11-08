"""
Kruskal's Algorithm — Minimum Spanning Tree (MST)
==================================================

Finds a minimum-weight spanning tree of a connected, undirected, weighted graph
using the Union-Find (Disjoint Set Union) data structure for efficient cycle
detection.

Algorithm overview:
    1. Sort all edges by weight in non-decreasing order.
    2. Iterate over sorted edges; for each edge (u, v, weight):
       - If u and v are in different components (no cycle formed), add the
         edge to the MST and merge their components.
       - Otherwise, skip the edge.
    3. Stop when the MST contains V - 1 edges (V = number of vertices).

Time complexity:  O(E log E)  — dominated by the edge sort.
Space complexity: O(V + E)

Union-Find uses path compression and union by rank for near-constant-time
find/union operations (amortized inverse Ackermann).
"""

from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Union-Find (Disjoint Set Union)
# ---------------------------------------------------------------------------

class UnionFind:
    """Disjoint Set Union with path compression and union by rank."""

    def __init__(self, n: int) -> None:
        """Initialise n singleton sets labelled 0 .. n-1."""
        self.parent: List[int] = list(range(n))
        self.rank: List[int] = [0] * n

    def find(self, x: int) -> int:
        """Return the representative (root) of the set containing x.

        Applies path compression so that future look-ups are faster.
        """
        # Iterative path compression: point every node along the path
        # directly to the root.
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x: int, y: int) -> bool:
        """Merge the sets containing x and y.

        Returns True if a merge happened (x and y were in different sets),
        False if they were already in the same set (would form a cycle).
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # Already in the same component — cycle detected.

        # Union by rank: attach the shorter tree under the taller one.
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


# ---------------------------------------------------------------------------
# Kruskal's MST
# ---------------------------------------------------------------------------

Edge = Tuple[Any, Any, float]  # (vertex_u, vertex_v, weight)


def kruskal(
    vertices: List[Any],
    edges: List[Edge],
) -> Tuple[List[Edge], float]:
    """Compute the Minimum Spanning Tree of a weighted undirected graph.

    Args:
        vertices: List of vertex identifiers (any hashable type).
        edges:    List of (u, v, weight) tuples representing undirected edges.

    Returns:
        A tuple (mst_edges, total_weight) where:
            mst_edges    — list of edges in the MST.
            total_weight — sum of weights of all MST edges.

    Raises:
        ValueError: If the graph is empty or a vertex in edges is unknown.

    Note:
        If the graph is disconnected, the result is a minimum spanning *forest*
        (MST for each connected component).
    """
    if not vertices:
        raise ValueError("Vertex list must not be empty.")

    # Map each vertex to a stable integer index for Union-Find.
    vertex_index: Dict[Any, int] = {v: i for i, v in enumerate(vertices)}

    # Validate that every edge endpoint is a known vertex.
    for u, v, w in edges:
        if u not in vertex_index or v not in vertex_index:
            raise ValueError(f"Edge ({u}, {v}, {w}) references an unknown vertex.")

    # Sort edges by weight — the greedy choice at the heart of Kruskal's.
    sorted_edges: List[Edge] = sorted(edges, key=lambda e: e[2])

    uf = UnionFind(len(vertices))
    mst_edges: List[Edge] = []
    total_weight: float = 0.0

    for u, v, weight in sorted_edges:
        # Adding this edge would connect two previously separate components
        # (no cycle), so include it in the MST.
        if uf.union(vertex_index[u], vertex_index[v]):
            mst_edges.append((u, v, weight))
            total_weight += weight
            # MST of a connected graph with V vertices has exactly V - 1 edges.
            if len(mst_edges) == len(vertices) - 1:
                break

    return mst_edges, total_weight


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example graph (undirected, weighted):
    #
    #       A ---1--- B
    #      / \       |
    #     4   3     2
    #    /     \     \
    #   D ---5--- C ---6
    #
    # Expected MST edges: A-B(1), B-C(2), A-D(4)  → total weight = 7

    vertices = ["A", "B", "C", "D"]
    edges = [
        ("A", "B", 1),
        ("A", "C", 3),
        ("A", "D", 4),
        ("B", "C", 2),
        ("C", "D", 5),
    ]

    print("Vertices:", vertices)
    print("Edges:", edges)

    mst_edges, total_weight = kruskal(vertices, edges)

    print("\nMinimum Spanning Tree edges:")
    for u, v, w in mst_edges:
        print(f"  {u} -- {v}  (weight {w})")
    print(f"Total MST weight: {total_weight}")
