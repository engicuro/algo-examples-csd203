"""
35_euler.py - Euler's Tour and Euler's Cycle in Graphs

An Eulerian trail (Euler tour) visits every edge of a graph exactly once.
An Eulerian cycle (Euler circuit) is an Eulerian trail that starts and ends
at the same vertex.

Topics covered:
  - Detection conditions for Eulerian trail and Eulerian cycle
  - Hierholzer's algorithm for finding an Eulerian cycle/trail
  - Directed and undirected graph variants
  - Example graphs with step-by-step walkthroughs

References:
  - Hierholzer, 1873 — original algorithm for Eulerian circuits
  - Conditions based on vertex degrees (undirected) or in/out-degree balance (directed)
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Graph representation helpers
# ---------------------------------------------------------------------------

def build_undirected_graph(edges: List[Tuple[int, int]]) -> Dict[int, List[int]]:
    """Build an adjacency list for an undirected graph from an edge list.

    Each edge (u, v) adds v to u's neighbours and u to v's neighbours.
    Self-loops (u == v) are counted once but contribute 2 to the degree.

    Args:
        edges: List of (u, v) pairs representing undirected edges.

    Returns:
        Dictionary mapping each vertex to a list of adjacent vertices.
    """
    graph: Dict[int, List[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        if u != v:
            graph[v].append(u)
    return dict(graph)


def build_directed_graph(edges: List[Tuple[int, int]]) -> Dict[int, List[int]]:
    """Build an adjacency list for a directed graph from an edge list.

    Each edge (u, v) adds v to u's out-neighbour list only.

    Args:
        edges: List of (u, v) pairs representing directed edges u -> v.

    Returns:
        Dictionary mapping each vertex to a list of out-neighbours.
    """
    graph: Dict[int, List[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        # Ensure every vertex appears in the dict, even if it has no out-edges
        if v not in graph:
            graph[v] = []
    return dict(graph)


# ---------------------------------------------------------------------------
# Degree computation
# ---------------------------------------------------------------------------

def undirected_degrees(graph: Dict[int, List[int]]) -> Dict[int, int]:
    """Return the degree of every vertex in an undirected graph.

    Self-loops contribute 2 to the degree of their vertex.

    Args:
        graph: Adjacency list of an undirected graph.

    Returns:
        Dictionary mapping vertex -> degree.
    """
    degrees: Dict[int, int] = {}
    for vertex, neighbours in graph.items():
        # Count self-loops separately because they appear once in the list
        # but contribute 2 to the degree.
        self_loops = sum(1 for n in neighbours if n == vertex)
        degrees[vertex] = len(neighbours) + self_loops
    return degrees


def directed_in_out_degrees(
    graph: Dict[int, List[int]],
) -> Tuple[Dict[int, int], Dict[int, int]]:
    """Return in-degree and out-degree for every vertex in a directed graph.

    Args:
        graph: Adjacency list of a directed graph (out-neighbours only).

    Returns:
        Tuple of (in_degree, out_degree) dictionaries.
    """
    out_degree: Dict[int, int] = {v: len(nb) for v, nb in graph.items()}
    in_degree: Dict[int, int] = defaultdict(int)
    for vertex, neighbours in graph.items():
        for neighbour in neighbours:
            in_degree[neighbour] += 1
    # Ensure every vertex appears in both dicts
    all_vertices = set(graph.keys()) | set(in_degree.keys())
    return (
        {v: in_degree.get(v, 0) for v in all_vertices},
        {v: out_degree.get(v, 0) for v in all_vertices},
    )


# ---------------------------------------------------------------------------
# Connectivity helper (for undirected graphs)
# ---------------------------------------------------------------------------

def _undirected_is_connected_excluding_isolated(
    graph: Dict[int, List[int]],
) -> bool:
    """Check whether the non-isolated vertices of an undirected graph are connected.

    Isolated vertices (degree 0) are ignored — they do not affect the existence
    of an Eulerian trail/cycle.

    Uses BFS from the first non-isolated vertex and verifies all other
    non-isolated vertices are reachable.

    Args:
        graph: Adjacency list of an undirected graph.

    Returns:
        True if all non-isolated vertices belong to a single connected component.
    """
    degrees = undirected_degrees(graph)
    non_isolated = {v for v, d in degrees.items() if d > 0}
    if not non_isolated:
        return True  # trivially connected (no edges)

    start = next(iter(non_isolated))
    visited: set[int] = set()
    queue: deque[int] = deque([start])
    visited.add(start)

    while queue:
        current = queue.popleft()
        for neighbour in graph.get(current, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    # Every non-isolated vertex must have been visited
    return non_isolated.issubset(visited)


# ---------------------------------------------------------------------------
# Detection conditions
# ---------------------------------------------------------------------------

def has_eulerian_cycle_undirected(graph: Dict[int, List[int]]) -> bool:
    """Check whether an undirected graph has an Eulerian cycle.

    Conditions (all must hold):
      1. Every vertex with non-zero degree has even degree.
      2. All non-isolated vertices belong to a single connected component.

    Args:
        graph: Adjacency list of an undirected graph.

    Returns:
        True if the graph contains an Eulerian cycle.
    """
    if not graph:
        return False

    degrees = undirected_degrees(graph)

    # Condition 1: all non-zero-degree vertices must have even degree
    for vertex, degree in degrees.items():
        if degree > 0 and degree % 2 != 0:
            return False

    # Condition 2: connectivity of non-isolated vertices
    return _undirected_is_connected_excluding_isolated(graph)


def has_eulerian_trail_undirected(graph: Dict[int, List[int]]) -> bool:
    """Check whether an undirected graph has an Eulerian trail (but not necessarily
    a cycle).

    Conditions (all must hold):
      1. Zero or exactly two vertices have odd degree.
      2. All non-isolated vertices belong to a single connected component.

    If exactly two vertices have odd degree, the trail starts at one and ends
    at the other. If all vertices have even degree, the trail is a cycle.

    Args:
        graph: Adjacency list of an undirected graph.

    Returns:
        True if the graph contains an Eulerian trail.
    """
    if not graph:
        return False

    degrees = undirected_degrees(graph)

    # Condition 1: count odd-degree vertices
    odd_degree_count = sum(1 for d in degrees.values() if d % 2 != 0)
    if odd_degree_count not in (0, 2):
        return False

    # Condition 2: connectivity of non-isolated vertices
    return _undirected_is_connected_excluding_isolated(graph)


def has_eulerian_cycle_directed(graph: Dict[int, List[int]]) -> bool:
    """Check whether a directed graph has an Eulerian cycle.

    Conditions (all must hold):
      1. Every vertex has equal in-degree and out-degree.
      2. All vertices with non-zero degree belong to a single strongly-connected
         component (when considering the underlying undirected graph, this reduces
         to checking weak connectivity of non-isolated vertices — sufficient for
         the degree-balanced case).

    Args:
        graph: Adjacency list of a directed graph.

    Returns:
        True if the graph contains an Eulerian cycle.
    """
    if not graph:
        return False

    in_deg, out_deg = directed_in_out_degrees(graph)

    # Condition 1: in-degree == out-degree for every vertex
    for vertex in set(in_deg.keys()) | set(out_deg.keys()):
        if in_deg.get(vertex, 0) != out_deg.get(vertex, 0):
            return False

    # Condition 2: weak connectivity of non-isolated vertices
    # Build an undirected view and check connectivity
    undirected: Dict[int, List[int]] = defaultdict(list)
    for u, neighbours in graph.items():
        for v in neighbours:
            undirected[u].append(v)
            undirected[v].append(u)

    return _undirected_is_connected_excluding_isolated(dict(undirected))


def has_eulerian_trail_directed(graph: Dict[int, List[int]]) -> bool:
    """Check whether a directed graph has an Eulerian trail (but not necessarily
    a cycle).

    Conditions (all must hold):
      1. At most one vertex has out_degree - in_degree == 1  (potential start).
      2. At most one vertex has in_degree - out_degree == 1  (potential end).
      3. All other vertices have equal in-degree and out-degree.
      4. All non-isolated vertices belong to a single weakly-connected component.

    Args:
        graph: Adjacency list of a directed graph.

    Returns:
        True if the graph contains an Eulerian trail.
    """
    if not graph:
        return False

    in_deg, out_deg = directed_in_out_degrees(graph)
    all_vertices = set(in_deg.keys()) | set(out_deg.keys())

    start_candidates = 0
    end_candidates = 0

    for vertex in all_vertices:
        diff = out_deg.get(vertex, 0) - in_deg.get(vertex, 0)
        if diff == 1:
            start_candidates += 1
        elif diff == -1:
            end_candidates += 1
        elif diff != 0:
            return False  # any other imbalance disqualifies the graph

    # Valid configurations: cycle (0/0) or trail (1/1)
    if not ((start_candidates == 0 and end_candidates == 0) or
            (start_candidates == 1 and end_candidates == 1)):
        return False

    # Weak connectivity check
    undirected: Dict[int, List[int]] = defaultdict(list)
    for u, neighbours in graph.items():
        for v in neighbours:
            undirected[u].append(v)
            undirected[v].append(u)

    return _undirected_is_connected_excluding_isolated(dict(undirected))


# ---------------------------------------------------------------------------
# Hierholzer's algorithm
# ---------------------------------------------------------------------------

def hierholzer_undirected_cycle(
    graph: Dict[int, List[int]],
) -> Optional[List[int]]:
    """Find an Eulerian cycle in an undirected graph using Hierholzer's algorithm.

    Hierholzer's algorithm (1873) works by:
      1. Starting from any vertex, following unused edges until returning to
         the start (forming a closed sub-tour).
      2. If any vertex on the tour still has unused edges, starting a new
         sub-tour from that vertex and splicing it into the existing tour.
      3. Repeating until all edges are consumed.

    The algorithm runs in O(E) time — each edge is visited exactly once.

    Args:
        graph: Adjacency list of an undirected graph. The caller must ensure
               the graph satisfies the Eulerian cycle conditions.

    Returns:
        A list of vertices representing the Eulerian cycle (first == last),
        or None if no cycle exists.
    """
    if not has_eulerian_cycle_undirected(graph):
        return None

    # Work on a mutable copy so we can consume edges
    remaining: Dict[int, deque[int]] = {
        v: deque(neighbours) for v, neighbours in graph.items()
    }

    # Pick any vertex that has edges
    start = next(v for v, nb in remaining.items() if nb)
    cycle: List[int] = []
    stack: List[int] = [start]

    while stack:
        current = stack[-1]
        if remaining.get(current):
            # Follow an unused edge
            next_vertex = remaining[current].popleft()
            # Remove the reverse edge (current from next_vertex's list)
            remaining[next_vertex].remove(current)
            stack.append(next_vertex)
        else:
            # No more unused edges from current — add to cycle and backtrack
            cycle.append(stack.pop())

    # The cycle is built in reverse; reverse it to get the correct order
    cycle.reverse()
    return cycle


def hierholzer_directed_cycle(
    graph: Dict[int, List[int]],
) -> Optional[List[int]]:
    """Find an Eulerian cycle in a directed graph using Hierholzer's algorithm.

    The directed variant is structurally identical to the undirected version,
    except that only forward edges are consumed (no reverse-edge removal).

    Args:
        graph: Adjacency list of a directed graph. The caller must ensure
               the graph satisfies the directed Eulerian cycle conditions.

    Returns:
        A list of vertices representing the Eulerian cycle (first == last),
        or None if no cycle exists.
    """
    if not has_eulerian_cycle_directed(graph):
        return None

    remaining: Dict[int, deque[int]] = {
        v: deque(neighbours) for v, neighbours in graph.items()
    }

    start = next(v for v, nb in remaining.items() if nb)
    cycle: List[int] = []
    stack: List[int] = [start]

    while stack:
        current = stack[-1]
        if remaining.get(current):
            next_vertex = remaining[current].popleft()
            stack.append(next_vertex)
        else:
            cycle.append(stack.pop())

    cycle.reverse()
    return cycle


def hierholzer_undirected_trail(
    graph: Dict[int, List[int]],
) -> Optional[List[int]]:
    """Find an Eulerian trail in an undirected graph using Hierholzer's algorithm.

    If the graph has exactly two odd-degree vertices, the trail starts at one
    of them and ends at the other. If all degrees are even, it finds a cycle.

    Args:
        graph: Adjacency list of an undirected graph.

    Returns:
        A list of vertices representing the Eulerian trail, or None if no trail
        exists.
    """
    if not has_eulerian_trail_undirected(graph):
        return None

    degrees = undirected_degrees(graph)
    odd_vertices = [v for v, d in degrees.items() if d % 2 != 0]

    # Start from an odd-degree vertex if one exists; otherwise any vertex
    start = odd_vertices[0] if odd_vertices else next(
        v for v, nb in graph.items() if nb
    )

    remaining: Dict[int, deque[int]] = {
        v: deque(neighbours) for v, neighbours in graph.items()
    }

    trail: List[int] = []
    stack: List[int] = [start]

    while stack:
        current = stack[-1]
        if remaining.get(current):
            next_vertex = remaining[current].popleft()
            remaining[next_vertex].remove(current)
            stack.append(next_vertex)
        else:
            trail.append(stack.pop())

    trail.reverse()
    return trail


def hierholzer_directed_trail(
    graph: Dict[int, List[int]],
) -> Optional[List[int]]:
    """Find an Eulerian trail in a directed graph using Hierholzer's algorithm.

    If the graph has a vertex with out_degree - in_degree == 1, the trail
    starts there. If it has a vertex with in_degree - out_degree == 1, the
    trail ends there. Otherwise it finds a cycle.

    Args:
        graph: Adjacency list of a directed graph.

    Returns:
        A list of vertices representing the Eulerian trail, or None if no trail
        exists.
    """
    if not has_eulerian_trail_directed(graph):
        return None

    in_deg, out_deg = directed_in_out_degrees(graph)
    all_vertices = set(in_deg.keys()) | set(out_deg.keys())

    start = next(
        (v for v in all_vertices if out_deg.get(v, 0) - in_deg.get(v, 0) == 1),
        next(
            (v for v, nb in graph.items() if nb),
            None,
        ),
    )
    if start is None:
        return None

    remaining: Dict[int, deque[int]] = {
        v: deque(neighbours) for v, neighbours in graph.items()
    }

    trail: List[int] = []
    stack: List[int] = [start]

    while stack:
        current = stack[-1]
        if remaining.get(current):
            next_vertex = remaining[current].popleft()
            stack.append(next_vertex)
        else:
            trail.append(stack.pop())

    trail.reverse()
    return trail


# ---------------------------------------------------------------------------
# Pretty-printing helpers
# ---------------------------------------------------------------------------

def print_graph(title: str, graph: Dict[int, List[int]]) -> None:
    """Print a graph's adjacency list in a readable format."""
    print(f"{title}:")
    for vertex in sorted(graph.keys()):
        print(f"  {vertex} -> {graph[vertex]}")
    print()


def print_eulerian_result(
    name: str,
    cycle: Optional[List[int]],
) -> None:
    """Print the result of an Eulerian cycle/trail computation."""
    if cycle is None:
        print(f"  {name}: No Eulerian cycle/trail exists.")
    else:
        edge_count = len(cycle) - 1
        print(f"  {name}: {' -> '.join(map(str, cycle))}")
        print(f"    ({edge_count} edge{'s' if edge_count != 1 else ''} traversed)")


# ---------------------------------------------------------------------------
# Example graphs
# ---------------------------------------------------------------------------

def example_cycle_graph() -> Dict[int, List[int]]:
    """Return a simple triangle (3-cycle) — has an Eulerian cycle.

        0 --- 1
         \\  /
          2

    All vertices have degree 2 (even) and the graph is connected.
    """
    return build_undirected_graph([(0, 1), (1, 2), (2, 0)])


def example_trail_graph() -> Dict[int, List[int]]:
    """Return a graph with an Eulerian trail but no Eulerian cycle.

        0 --- 1 --- 2
              |
              3

    Vertices 0 and 2 have degree 1 (odd); vertices 1 and 3 have degree 3 (odd).
    Wait — that gives 4 odd-degree vertices, which is too many. Let's use a
    simpler example:

        0 --- 1 --- 2

    Vertices 0 and 2 have degree 1 (odd); vertex 1 has degree 2 (even).
    Exactly two odd-degree vertices → Eulerian trail exists (0 → 1 → 2).
    """
    return build_undirected_graph([(0, 1), (1, 2)])


def example_königsberg_bridge() -> Dict[int, List[int]]:
    """Return a multigraph inspired by the historical Königsberg bridge problem.

    The original Königsberg graph has four landmasses (vertices) connected by
    seven bridges (edges). All four vertices have odd degree, so neither an
    Eulerian cycle nor an Eulerian trail exists — this is the graph that
    motivated Euler's 1736 paper.

    Simplified version with 4 vertices and 7 edges:
        0 -- 1 (3 parallel edges)
        0 -- 2 (1 edge)
        1 -- 3 (1 edge)
        2 -- 3 (1 edge)
        1 -- 2 (1 edge)
    """
    return build_undirected_graph([
        (0, 1), (0, 1), (0, 1),  # three parallel edges
        (0, 2),
        (1, 3),
        (2, 3),
        (1, 2),
    ])


def example_directed_cycle() -> Dict[int, List[int]]:
    """Return a directed graph with an Eulerian cycle.

        0 → 1 → 2 → 0

    Every vertex has in-degree == out-degree == 1.
    """
    return build_directed_graph([(0, 1), (1, 2), (2, 0)])


def example_directed_trail() -> Dict[int, List[int]]:
    """Return a directed graph with an Eulerian trail but no cycle.

        0 → 1 → 2

    Vertex 0: out=1, in=0  (start candidate)
    Vertex 1: out=1, in=1
    Vertex 2: out=0, in=1  (end candidate)
    """
    return build_directed_graph([(0, 1), (1, 2)])


def example_directed_no_eulerian() -> Dict[int, List[int]]:
    """Return a directed graph with no Eulerian trail or cycle.

        0 → 1, 0 → 2, 1 → 2

    Vertex 0: out=2, in=0  (imbalance of +2)
    Vertex 1: out=1, in=1
    Vertex 2: out=0, in=2  (imbalance of -2)
    """
    return build_directed_graph([(0, 1), (0, 2), (1, 2)])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Run all Eulerian graph demonstrations."""
    print("=" * 64)
    print("Chapter 35 — Euler's Tour and Euler's Cycle")
    print("=" * 64)

    # ----- Undirected: Eulerian Cycle -----
    print("\n--- Undirected Graph: Eulerian Cycle ---")
    g_cycle = example_cycle_graph()
    print_graph("Triangle graph (3-cycle)", g_cycle)
    print(f"  Has Eulerian cycle: {has_eulerian_cycle_undirected(g_cycle)}")
    print(f"  Has Eulerian trail:  {has_eulerian_trail_undirected(g_cycle)}")
    result = hierholzer_undirected_cycle(g_cycle)
    print_eulerian_result("Hierholzer cycle", result)

    # ----- Undirected: Eulerian Trail -----
    print("\n--- Undirected Graph: Eulerian Trail ---")
    g_trail = example_trail_graph()
    print_graph("Path graph 0-1-2", g_trail)
    print(f"  Has Eulerian cycle: {has_eulerian_cycle_undirected(g_trail)}")
    print(f"  Has Eulerian trail:  {has_eulerian_trail_undirected(g_trail)}")
    result = hierholzer_undirected_trail(g_trail)
    print_eulerian_result("Hierholzer trail", result)

    # ----- Undirected: Königsberg (no Eulerian path) -----
    print("\n--- Undirected Graph: Königsberg Bridge Problem ---")
    g_konigsberg = example_königsberg_bridge()
    print_graph("Königsberg-inspired multigraph", g_konigsberg)
    degrees = undirected_degrees(g_konigsberg)
    print(f"  Degrees: {degrees}")
    print(f"  Has Eulerian cycle: {has_eulerian_cycle_undirected(g_konigsberg)}")
    print(f"  Has Eulerian trail:  {has_eulerian_trail_undirected(g_konigsberg)}")
    result = hierholzer_undirected_cycle(g_konigsberg)
    print_eulerian_result("Hierholzer cycle", result)
    result = hierholzer_undirected_trail(g_konigsberg)
    print_eulerian_result("Hierholzer trail", result)

    # ----- Directed: Eulerian Cycle -----
    print("\n--- Directed Graph: Eulerian Cycle ---")
    dg_cycle = example_directed_cycle()
    print_graph("Directed 3-cycle (0→1→2→0)", dg_cycle)
    in_deg, out_deg = directed_in_out_degrees(dg_cycle)
    print(f"  In-degrees:  {in_deg}")
    print(f"  Out-degrees: {out_deg}")
    print(f"  Has Eulerian cycle: {has_eulerian_cycle_directed(dg_cycle)}")
    print(f"  Has Eulerian trail:  {has_eulerian_trail_directed(dg_cycle)}")
    result = hierholzer_directed_cycle(dg_cycle)
    print_eulerian_result("Hierholzer directed cycle", result)

    # ----- Directed: Eulerian Trail -----
    print("\n--- Directed Graph: Eulerian Trail ---")
    dg_trail = example_directed_trail()
    print_graph("Directed path (0→1→2)", dg_trail)
    in_deg, out_deg = directed_in_out_degrees(dg_trail)
    print(f"  In-degrees:  {in_deg}")
    print(f"  Out-degrees: {out_deg}")
    print(f"  Has Eulerian cycle: {has_eulerian_cycle_directed(dg_trail)}")
    print(f"  Has Eulerian trail:  {has_eulerian_trail_directed(dg_trail)}")
    result = hierholzer_directed_trail(dg_trail)
    print_eulerian_result("Hierholzer directed trail", result)

    # ----- Directed: No Eulerian path -----
    print("\n--- Directed Graph: No Eulerian Trail or Cycle ---")
    dg_none = example_directed_no_eulerian()
    print_graph("Directed graph with imbalanced degrees", dg_none)
    in_deg, out_deg = directed_in_out_degrees(dg_none)
    print(f"  In-degrees:  {in_deg}")
    print(f"  Out-degrees: {out_deg}")
    print(f"  Has Eulerian cycle: {has_eulerian_cycle_directed(dg_none)}")
    print(f"  Has Eulerian trail:  {has_eulerian_trail_directed(dg_none)}")
    result = hierholzer_directed_cycle(dg_none)
    print_eulerian_result("Hierholzer directed cycle", result)
    result = hierholzer_directed_trail(dg_none)
    print_eulerian_result("Hierholzer directed trail", result)

    # ----- Summary of detection conditions -----
    print("\n" + "=" * 64)
    print("Summary of Detection Conditions")
    print("=" * 64)
    print("""
Undirected Graph:
  Eulerian Cycle:  All non-zero-degree vertices have even degree AND
                   the non-isolated vertices are connected.
  Eulerian Trail:  Exactly 0 or 2 vertices have odd degree AND
                   the non-isolated vertices are connected.

Directed Graph:
  Eulerian Cycle:  Every vertex has in-degree == out-degree AND
                   the non-isolated vertices are weakly connected.
  Eulerian Trail:  At most 1 vertex has out-in == +1 (start),
                   at most 1 vertex has in-out == +1 (end),
                   all other vertices are balanced, AND
                   the non-isolated vertices are weakly connected.

Hierholzer's Algorithm:
  - Time complexity:  O(E) — each edge is visited exactly once.
  - Space complexity: O(E) — for the adjacency-list copy and the stack.
  - Uses a stack-based DFS; edges are consumed as they are traversed.
  - When a vertex has no remaining outgoing edges, it is appended to
    the result and the algorithm backtracks, building the cycle/trail
    in reverse.
""")


if __name__ == "__main__":
    main()
