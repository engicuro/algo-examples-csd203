"""
32_dijkstra.py - Dijkstra's Shortest Path Algorithm in Python

Dijkstra's algorithm finds the shortest path from a single source vertex
to all other vertices in a weighted graph with non-negative edge weights.
It uses a priority queue (min-heap) to greedily select the unvisited vertex
with the smallest known distance at each step.

Topics covered:
  - Graph representation as an adjacency list (dict of dicts)
  - Priority queue (heapq) for efficient minimum-distance selection
  - Distance table initialization and relaxation
  - Step-by-step trace showing the algorithm's progress
  - Path reconstruction via a predecessors map
"""

import heapq
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Graph representation
# ---------------------------------------------------------------------------

# We represent a weighted directed graph as a dict of dicts:
#   graph[u] = {v: weight, ...}
# meaning there is an edge from u to v with the given non-negative weight.
# An undirected edge is represented by adding entries in both directions.

Graph = Dict[str, Dict[str, int]]


def build_sample_graph() -> Graph:
    """Return a sample weighted graph for demonstration.

    The graph looks like this (edge labels show weights):

        A --1-- B --2-- D
        |        |       |
        4        3       1
        |        |       |
        C --5-- E --2-- F

    Returns:
        A dictionary-of-dictionaries adjacency list.
    """
    graph: Graph = {
        "A": {"B": 1, "C": 4},
        "B": {"A": 1, "D": 2, "E": 3},
        "C": {"A": 4, "E": 5},
        "D": {"B": 2, "F": 1},
        "E": {"B": 3, "C": 5, "F": 2},
        "F": {"D": 1, "E": 2},
    }
    return graph


# ---------------------------------------------------------------------------
# Core algorithm
# ---------------------------------------------------------------------------

def dijkstra(
    graph: Graph,
    source: str,
    target: Optional[str] = None,
    verbose: bool = False,
) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
    """Run Dijkstra's algorithm from *source* to all reachable vertices.

    Args:
        graph: Weighted directed graph as an adjacency dict.
               graph[u][v] = weight of edge u -> v (must be >= 0).
        source: The starting vertex.
        target: Optional early-stop target.  When provided, the algorithm
                terminates as soon as *target* is popped from the queue.
        verbose: When True, print a step-by-step trace of each iteration.

    Returns:
        A tuple (distances, predecessors):
            distances[v]  — shortest distance from source to v (infinity if unreachable).
            predecessors[v] — the vertex preceding v on the shortest path (None if v is
                              the source or unreachable).

    Raises:
        ValueError: If source or target is not present in the graph.
    """
    if source not in graph:
        raise ValueError(f"Source vertex '{source}' not found in graph.")
    if target is not None and target not in graph:
        raise ValueError(f"Target vertex '{target}' not found in graph.")

    # --- Initialise distances to infinity and predecessors to None ----------
    distances: Dict[str, int] = {vertex: float("inf") for vertex in graph}
    predecessors: Dict[str, Optional[str]] = {vertex: None for vertex in graph}
    distances[source] = 0

    # --- Priority queue stores (distance, vertex) tuples -------------------
    # heapq is a min-heap, so the vertex with the smallest distance is
    # always popped first — this is the greedy heart of Dijkstra's.
    # We also maintain a set of visited vertices to avoid re-processing.
    priority_queue: List[Tuple[int, str]] = [(0, source)]
    visited: set = set()

    if verbose:
        print(f"Source: {source}")
        print(f"Initial distances: {distances}")
        print(f"Priority queue:    {priority_queue}")
        print("-" * 50)

    step = 0

    while priority_queue:
        # Pop the vertex with the smallest tentative distance.
        # If we already visited it, skip (stale entry from an earlier push).
        current_dist, current_vertex = heapq.heappop(priority_queue)

        if current_vertex in visited:
            if verbose:
                print(f"Step {step}: SKIP {current_vertex} (already visited)")
            step += 1
            continue

        visited.add(current_vertex)
        step += 1

        if verbose:
            print(f"Step {step}: Visit '{current_vertex}' (distance = {current_dist})")

        # Early termination: if we popped the target, we are done.
        if target is not None and current_vertex == target:
            if verbose:
                print(f"  Reached target '{target}' — stopping early.")
            break

        # --- Relaxation step -----------------------------------------------
        # For each neighbour, check if going through current_vertex gives
        # a shorter path than the one currently known.
        for neighbour, weight in graph[current_vertex].items():
            if neighbour in visited:
                continue  # already finalized

            new_distance = current_dist + weight

            if verbose:
                old_dist = distances[neighbour]
                improved = new_distance < old_dist
                marker = " << IMPROVED" if improved else " (no improvement)"
                print(
                    f"  Check edge {current_vertex} -> {neighbour} "
                    f"(weight {weight}): "
                    f"{current_dist} + {weight} = {new_distance}"
                    f" vs current {old_dist}{marker}"
                )

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                predecessors[neighbour] = current_vertex
                heapq.heappush(priority_queue, (new_distance, neighbour))

                if verbose:
                    print(f"    -> Updated distance[{neighbour}] = {new_distance}")

        if verbose:
            print(f"  Distances after step {step}: {distances}")
            print()

    return distances, predecessors


# ---------------------------------------------------------------------------
# Path reconstruction
# ---------------------------------------------------------------------------

def reconstruct_path(
    predecessors: Dict[str, Optional[str]],
    source: str,
    target: str,
) -> List[str]:
    """Rebuild the shortest path from *source* to *target* using the
    predecessors map returned by dijkstra().

    Args:
        predecessors: The predecessors dict from dijkstra().
        source: The starting vertex.
        target: The destination vertex.

    Returns:
        A list of vertices forming the shortest path from source to target.
        Returns an empty list if no path exists.
    """
    if predecessors[target] is None and target != source:
        # Target is unreachable from source.
        return []

    path: List[str] = []
    current: Optional[str] = target

    while current is not None:
        path.append(current)
        if current == source:
            break
        current = predecessors[current]

    path.reverse()
    return path


# ---------------------------------------------------------------------------
# Pretty-printing helpers
# ---------------------------------------------------------------------------

def print_distances(distances: Dict[str, int], source: str) -> None:
    """Print the shortest distances from source to every vertex."""
    print(f"\nShortest distances from '{source}':")
    print(f"{'Vertex':<8} {'Distance':>10}")
    print("-" * 20)
    for vertex, dist in sorted(distances.items()):
        label = dist if dist != float("inf") else "unreachable"
        print(f"{vertex:<8} {label:>10}")


def print_path(path: List[str], distances: Dict[str, int], source: str, target: str) -> None:
    """Print the shortest path and its total cost."""
    if not path:
        print(f"\nNo path from '{source}' to '{target}'.")
        return

    cost = distances[target]
    path_str = " -> ".join(path)
    print(f"\nShortest path from '{source}' to '{target}':")
    print(f"  {path_str}")
    print(f"  Total cost: {cost}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Run Dijkstra's algorithm on the sample graph with a step-by-step trace."""
    print("=" * 60)
    print("Chapter 32 — Dijkstra's Shortest Path Algorithm")
    print("=" * 60)

    graph = build_sample_graph()

    # Show the graph structure
    print("\nGraph (adjacency list with weights):")
    for vertex, neighbours in sorted(graph.items()):
        edges = ", ".join(f"{n}({w})" for n, w in sorted(neighbours.items()))
        print(f"  {vertex} -> {edges}")

    source = "A"
    target = "F"

    # --- Full run with verbose trace --------------------------------------
    print(f"\n--- Running Dijkstra from '{source}' to '{target}' (verbose) ---")
    distances, predecessors = dijkstra(graph, source, target=target, verbose=True)

    # --- Print results ----------------------------------------------------
    print_distances(distances, source)

    # --- Reconstruct and print the shortest path --------------------------
    path = reconstruct_path(predecessors, source, target)
    print_path(path, distances, source, target)

    # --- Show paths to all vertices ---------------------------------------
    print("\n--- Shortest paths from 'A' to every vertex ---")
    for vertex in sorted(graph.keys()):
        path = reconstruct_path(predecessors, source, vertex)
        if path:
            print(f"  A -> {vertex}: {' -> '.join(path)}  (cost {distances[vertex]})")
        else:
            print(f"  A -> {vertex}: unreachable")

    # --- Run without verbose (quiet mode) ---------------------------------
    print("\n--- Quiet run (no trace) ---")
    quiet_distances, quiet_predecessors = dijkstra(graph, source)
    quiet_path = reconstruct_path(quiet_predecessors, source, target)
    print_path(quiet_path, quiet_distances, source, target)


if __name__ == "__main__":
    main()
