"""
33_mst_prim.py - Prim-Jarník Minimum Spanning Tree Algorithm

Prim's algorithm (also known as Prim-Jarník) builds a minimum spanning
tree (MST) for a weighted undirected graph by greedily growing a single
tree from an arbitrary start vertex.  At each step it adds the cheapest
edge that connects a vertex inside the tree to a vertex outside it.

A min-priority queue (binary heap) is used to select the next vertex
efficiently — O((V + E) log V) time.

Topics covered:
  - Graph representation (adjacency list with weights)
  - Priority-queue–driven greedy selection
  - Step-by-step trace of every push / pop / relaxation
  - MST edge collection and total weight computation
"""

import heapq
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Graph type:  adjacency list where graph[u] = [(weight, v), ...]
# ---------------------------------------------------------------------------
Graph = Dict[str, List[Tuple[int, str]]]


def prim_mst(graph: Graph, start: str = "A") -> Tuple[List[Tuple[str, str, int]], int]:
    """Compute the Minimum Spanning Tree using Prim-Jarník's algorithm.

    Parameters
    ----------
    graph : dict
        Adjacency list mapping each vertex to a list of (weight, neighbor)
        tuples.  The graph must be undirected — every edge (u, v, w) must
        appear in both graph[u] and graph[v].
    start : str
        The vertex from which to begin growing the MST.

    Returns
    -------
    mst_edges : list of (u, v, weight)
        The edges that form the MST.
    total_weight : int
        Sum of the MST edge weights.

    Example
    -------
    >>> graph = {
    ...     "A": [(2, "B"), (3, "C")],
    ...     "B": [(2, "A"), (1, "C"), (4, "D")],
    ...     "C": [(3, "A"), (1, "B"), (5, "D")],
    ...     "D": [(4, "B"), (5, "C")],
    ... }
    >>> prim_mst(graph, "A")
    ([('A', 'B', 2), ('B', 'C', 1), ('B', 'D', 4)], 7)
    """
    # Track which vertices have already been added to the MST.
    in_mst: set[str] = set()

    # The priority queue holds (weight, vertex, parent) tuples.
    # We use a min-heap so the cheapest frontier edge is always first.
    # Start with the initial vertex — its key is 0 and it has no parent.
    heap: list[tuple[int, str, str | None]] = [(0, start, None)]

    mst_edges: List[Tuple[str, str, int]] = []
    total_weight: int = 0

    print(f"\n{'=' * 60}")
    print(f"Prim-Jarník MST — starting from vertex '{start}'")
    print(f"{'=' * 60}")
    print(f"  Graph vertices : {sorted(graph.keys())}")
    print(f"  Edges (u, v, w):")
    for u in sorted(graph):
        for w, v in sorted(graph[u]):
            if u < v:  # print each undirected edge once
                print(f"    {u} -- {v}  (weight {w})")
    print(f"{'-' * 60}")

    step = 0

    while heap and len(in_mst) < len(graph):
        # Pop the vertex with the smallest connecting edge weight.
        weight, vertex, parent = heapq.heappop(heap)

        # Skip vertices already absorbed into the MST.
        if vertex in in_mst:
            print(f"\n  Step {step}: POP ({weight}, '{vertex}', parent={parent}) — SKIP (already in MST)")
            step += 1
            continue

        # Accept this vertex into the MST.
        in_mst.add(vertex)
        if parent is not None:
            mst_edges.append((parent, vertex, weight))
            total_weight += weight
            print(f"\n  Step {step}: POP ({weight}, '{vertex}', parent='{parent}') — ACCEPT")
            print(f"    → Add edge {parent} -- {vertex} (weight {weight}) to MST")
        else:
            # This is the start vertex; no edge to add.
            print(f"\n  Step {step}: POP ({weight}, '{vertex}', parent=None) — ACCEPT (start vertex)")

        print(f"    MST so far: {mst_edges}")
        print(f"    MST weight: {total_weight}")
        print(f"    In-MST set : {sorted(in_mst)}")

        # Examine all neighbors of the newly added vertex.
        for edge_weight, neighbor in sorted(graph[vertex]):
            if neighbor not in in_mst:
                heapq.heappush(heap, (edge_weight, neighbor, vertex))
                print(f"    PUSH ({edge_weight}, '{neighbor}', parent='{vertex}') onto priority queue")

        step += 1

    # --- Result ---
    print(f"\n{'=' * 60}")
    print(f"MST complete — {len(mst_edges)} edge(s), total weight = {total_weight}")
    print(f"{'=' * 60}")
    for u, v, w in mst_edges:
        print(f"  {u} -- {v}  (weight {w})")

    return mst_edges, total_weight


def build_sample_graph() -> Graph:
    """Return a sample undirected weighted graph for demonstration.

    The graph is a classic 5-vertex example where the MST is unambiguous.

        A ---2--- B ---4--- D
        |  \\     |       / |
        3   1    5     6   2
        |    \\   |   /    |
        C ---1-- E --3-- F

    Edges:
        A-B:2  A-C:3  A-E:1
        B-C:4  B-D:5
        C-E:1  C-F:6
        D-F:2
        E-F:3
    """
    graph: Graph = {
        "A": [(2, "B"), (3, "C"), (1, "E")],
        "B": [(2, "A"), (4, "C"), (5, "D")],
        "C": [(3, "A"), (4, "B"), (1, "E"), (6, "F")],
        "D": [(5, "B"), (2, "F")],
        "E": [(1, "A"), (1, "C"), (3, "F")],
        "F": [(6, "C"), (2, "D"), (3, "E")],
    }
    return graph


def build_small_graph() -> Graph:
    """Return a small 4-vertex graph for a quick trace."""
    graph: Graph = {
        "A": [(2, "B"), (3, "C")],
        "B": [(2, "A"), (1, "C"), (4, "D")],
        "C": [(3, "A"), (1, "B"), (5, "D")],
        "D": [(4, "B"), (5, "C")],
    }
    return graph


def main() -> None:
    """Run Prim-Jarník MST demonstrations with two sample graphs."""
    print("\n" + "=" * 60)
    print("Prim-Jarník Minimum Spanning Tree Algorithm")
    print("=" * 60)

    # --- Demo 1: Small 4-vertex graph ---
    print("\n>>> Demo 1: Small graph (4 vertices)")
    small_graph = build_small_graph()
    edges, weight = prim_mst(small_graph, start="A")
    assert weight == 7, f"Expected total weight 7, got {weight}"
    assert len(edges) == 3, f"Expected 3 MST edges, got {len(edges)}"
    print(f"\n✓ Verified: MST weight = {weight}, edges = {edges}")

    # --- Demo 2: Larger 6-vertex graph ---
    print("\n\n>>> Demo 2: Larger graph (6 vertices)")
    graph = build_sample_graph()
    edges, weight = prim_mst(graph, start="A")
    assert weight == 9, f"Expected total weight 9, got {weight}"
    assert len(edges) == 5, f"Expected 5 MST edges, got {len(edges)}"
    print(f"\n✓ Verified: MST weight = {weight}, edges = {edges}")

    print("\n" + "=" * 60)
    print("All demonstrations complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
