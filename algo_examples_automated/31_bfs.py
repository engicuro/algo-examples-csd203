"""
31_bfs.py - Breadth-First Search (BFS) in Python

Breadth-First Search is a graph traversal algorithm that explores vertices
level by level, starting from a source node. It uses a queue (FIFO) to
ensure that all nodes at distance d are visited before any node at distance d+1.

Topics covered:
  - Queue-based BFS implementation (collections.deque)
  - Level-order traversal (grouping nodes by their distance from source)
  - Shortest path in an unweighted graph (tracking predecessors)
  - Reconstructing the shortest path from source to target
"""

from __future__ import annotations

from collections import deque
from typing import Any, Dict, List, Optional, Set


# ---------------------------------------------------------------------------
# Core BFS: level-order traversal
# ---------------------------------------------------------------------------

def bfs(graph: Dict[Any, List[Any]], start: Any) -> List[Any]:
    """Perform breadth-first traversal starting from *start*.

    Args:
        graph: Adjacency list mapping each node to its list of neighbours.
        start: The node from which BFS begins.

    Returns:
        A list of nodes in the order they were visited (level by level).
    """
    if start not in graph:
        return []

    visited: Set[Any] = set()          # tracks already-visited nodes
    queue: deque[Any] = deque([start]) # FIFO queue for BFS
    visited.add(start)
    order: List[Any] = []             # recording the visit order

    while queue:
        node = queue.popleft()         # dequeue the front node
        order.append(node)

        # Enqueue every unvisited neighbour
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    return order


# ---------------------------------------------------------------------------
# Level-order traversal: group nodes by their BFS depth
# ---------------------------------------------------------------------------

def bfs_levels(graph: Dict[Any, List[Any]], start: Any) -> List[List[Any]]:
    """Return nodes grouped by their distance (level) from *start*.

    Each inner list contains all nodes discovered at that BFS depth.

    Args:
        graph: Adjacency list.
        start: Starting node.

    Returns:
        A list of levels, where each level is a list of node values.
    """
    if start not in graph:
        return []

    visited: Set[Any] = {start}
    queue: deque[Any] = deque([start])
    levels: List[List[Any]] = []

    while queue:
        level_size = len(queue)         # number of nodes at current depth
        current_level: List[Any] = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node)

            for neighbour in graph[node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        levels.append(current_level)

    return levels


# ---------------------------------------------------------------------------
# Shortest path in an unweighted graph
# ---------------------------------------------------------------------------

def bfs_shortest_path(
    graph: Dict[Any, List[Any]],
    start: Any,
    target: Any,
) -> List[Any]:
    """Find the shortest path from *start* to *target* in an unweighted graph.

    BFS guarantees the shortest path (fewest edges) in an unweighted graph
    because it explores all nodes at distance d before any node at distance d+1.

    Args:
        graph: Adjacency list.
        start: Source node.
        target: Destination node.

    Returns:
        A list of nodes representing the shortest path from start to target,
        or an empty list if no path exists.
    """
    if start not in graph or target not in graph:
        return []

    if start == target:
        return [start]

    visited: Set[Any] = {start}
    queue: deque[Any] = deque([start])
    predecessor: Dict[Any, Optional[Any]] = {start: None}

    while queue:
        node = queue.popleft()

        # Early exit as soon as we reach the target
        if node == target:
            break

        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                predecessor[neighbour] = node
                queue.append(neighbour)

    # Reconstruct path by walking backwards from target to start
    if target not in predecessor:
        return []  # target was never reached

    path: List[Any] = []
    current: Any = target
    while current is not None:
        path.append(current)
        current = predecessor[current]

    path.reverse()
    return path


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example graph (undirected, unweighted):
    #
    #     0 --- 1 --- 3
    #     |     |     |
    #     2 --- 4 --- 5
    #
    # Adjacency list representation.
    graph: Dict[int, List[int]] = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 4],
        3: [1, 5],
        4: [1, 2, 5],
        5: [3, 4],
    }

    # --- Basic BFS traversal ---
    print("BFS traversal order (starting from node 0):")
    traversal = bfs(graph, 0)
    print(f"  {traversal}")
    # Expected: [0, 1, 2, 3, 4, 5]  (level 0, then level 1, then level 2)

    # --- Level-order traversal ---
    print("\nLevel-order traversal (grouped by distance from node 0):")
    levels = bfs_levels(graph, 0)
    for i, level in enumerate(levels):
        print(f"  Level {i}: {level}")
    # Expected:
    #   Level 0: [0]
    #   Level 1: [1, 2]
    #   Level 2: [3, 4, 5]

    # --- Shortest path ---
    print("\nShortest paths from node 0:")
    for target in range(6):
        path = bfs_shortest_path(graph, 0, target)
        print(f"  0 -> {target}: {path}  (length: {len(path) - 1} edges)")

    # --- Disconnected node example ---
    print("\nGraph with a disconnected node:")
    disconnected_graph: Dict[int, List[int]] = {
        0: [1],
        1: [0],
        2: [],       # node 2 is isolated
    }
    path = bfs_shortest_path(disconnected_graph, 0, 2)
    print(f"  Shortest path 0 -> 2: {path}")
    # Expected: []  (no path exists)
