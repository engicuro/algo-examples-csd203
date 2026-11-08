"""
30_dfs.py - Depth-First Search (DFS) in Python

Depth-First Search is a fundamental graph traversal algorithm that explores
as far as possible along each branch before backtracking.

Topics covered:
  - Recursive DFS implementation
  - Iterative DFS implementation (using an explicit stack)
  - Traversal order (pre-order, post-order)
  - Connected components in an undirected graph
  - Cycle detection (undirected graph)
"""

from typing import Dict, List, Set


# ---------------------------------------------------------------------------
# Graph representation
# ---------------------------------------------------------------------------

def build_sample_graph() -> Dict[int, List[int]]:
    r"""Return an undirected graph as an adjacency list.

    The graph has two connected components:

        Component 1:  0 — 1 — 3
                      |   |
                      2 — 4

        Component 2:  5 — 6
                       \  |
                        7

    Returns:
        A dictionary mapping each node to a list of its neighbours.
    """
    graph: Dict[int, List[int]] = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 4],
        3: [1],
        4: [1, 2],
        5: [6, 7],
        6: [5, 7],
        7: [5, 6],
    }
    return graph


def build_directed_graph() -> Dict[int, List[int]]:
    """Return a directed graph (DAG) as an adjacency list.

        0 → 1 → 3
        ↓       ↑
        2 ------

    Returns:
        A dictionary mapping each node to a list of its outgoing neighbours.
    """
    graph: Dict[int, List[int]] = {
        0: [1, 2],
        1: [3],
        2: [3],
        3: [],
    }
    return graph


# ---------------------------------------------------------------------------
# Recursive DFS
# ---------------------------------------------------------------------------

def dfs_recursive(
    graph: Dict[int, List[int]],
    node: int,
    visited: Set[int],
    order: List[int],
) -> None:
    """Perform a recursive depth-first traversal starting from *node*.

    Args:
        graph:  Adjacency-list representation of the graph.
        node:   The current node being explored.
        visited: Set of already-visited nodes (mutated in place).
        order:   List recording the traversal order (mutated in place).

    Time complexity:  O(V + E)  — every vertex and edge is visited once.
    Space complexity: O(V)      — for the visited set and recursion stack.
    """
    visited.add(node)
    order.append(node)  # pre-order: record when the node is first encountered

    for neighbour in graph.get(node, []):
        if neighbour not in visited:
            dfs_recursive(graph, neighbour, visited, order)


# ---------------------------------------------------------------------------
# Iterative DFS
# ---------------------------------------------------------------------------

def dfs_iterative(graph: Dict[int, List[int]], start: int) -> List[int]:
    """Perform an iterative depth-first traversal using an explicit stack.

    This version mimics the recursive pre-order traversal.  Nodes are
    marked visited *when pushed* onto the stack to avoid duplicate entries.

    Args:
        graph: Adjacency-list representation of the graph.
        start: The node from which to begin the traversal.

    Returns:
        A list of nodes in the order they were visited (pre-order).

    Time complexity:  O(V + E)
    Space complexity: O(V)     — for the stack and visited set.
    """
    visited: Set[int] = set()
    order: List[int] = []
    stack: List[int] = [start]

    while stack:
        node = stack.pop()
        if node in visited:
            continue

        visited.add(node)
        order.append(node)  # pre-order: record on first visit

        # Push neighbours in reverse order so that the first neighbour
        # in the adjacency list is processed next (matching recursive order).
        for neighbour in reversed(graph.get(node, [])):
            if neighbour not in visited:
                stack.append(neighbour)

    return order


# ---------------------------------------------------------------------------
# Post-order DFS (iterative, two-stack approach)
# ---------------------------------------------------------------------------

def dfs_postorder(graph: Dict[int, List[int]], start: int) -> List[int]:
    """Return the post-order traversal of the graph starting from *start*.

    Post-order means a node is recorded *after* all its descendants have
    been fully explored.  This is useful for topological sorting and
    detecting cycles.

    Uses a two-stack iterative approach:
      - Stack 1 drives the traversal (pushing nodes in pre-order).
      - Stack 2 collects nodes in reverse post-order.
      - Reversing stack 2 yields the correct post-order.

    Args:
        graph: Adjacency-list representation of the graph.
        start: The starting node.

    Returns:
        A list of nodes in post-order.

    Time complexity:  O(V + E)
    Space complexity: O(V)
    """
    visited: Set[int] = set()
    stack1: List[int] = [start]
    stack2: List[int] = []  # collects nodes in reverse post-order

    while stack1:
        node = stack1.pop()
        if node in visited:
            continue
        visited.add(node)
        stack2.append(node)  # will be reversed at the end

        # Push neighbours in natural order so that the first neighbour
        # is processed last (and thus ends up deeper in stack2).
        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                stack1.append(neighbour)

    stack2.reverse()
    return stack2


# ---------------------------------------------------------------------------
# Connected components (undirected graph)
# ---------------------------------------------------------------------------

def connected_components(graph: Dict[int, List[int]]) -> List[List[int]]:
    """Find all connected components in an undirected graph.

    Each component is a list of nodes reachable from one another.
    Nodes within a component appear in DFS traversal order.

    Args:
        graph: Adjacency-list representation of an undirected graph.

    Returns:
        A list of components, where each component is a list of node IDs.

    Time complexity:  O(V + E)
    Space complexity: O(V)
    """
    visited: Set[int] = set()
    components: List[List[int]] = []

    for node in graph:
        if node not in visited:
            # Start a new DFS from this unvisited node — it belongs to a
            # new connected component.
            component: List[int] = []
            dfs_recursive(graph, node, visited, component)
            components.append(component)

    return components


# ---------------------------------------------------------------------------
# Cycle detection in an undirected graph
# ---------------------------------------------------------------------------

def has_cycle_undirected(graph: Dict[int, List[int]]) -> bool:
    """Detect whether an undirected graph contains a cycle.

    Uses recursive DFS.  A cycle exists if we encounter a neighbour that
    has already been visited and is *not* the parent of the current node.

    Args:
        graph: Adjacency-list representation of an undirected graph.

    Returns:
        True if the graph contains at least one cycle, False otherwise.

    Time complexity:  O(V + E)
    Space complexity: O(V)  — recursion stack depth.
    """
    visited: Set[int] = set()

    def _dfs(node: int, parent: int) -> bool:
        """Return True if a cycle is found in the subtree rooted at *node*."""
        visited.add(node)
        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                if _dfs(neighbour, node):
                    return True
            elif neighbour != parent:
                # Visited neighbour that is not the parent → back edge → cycle
                return True
        return False

    # Check every component (graph may be disconnected).
    for node in graph:
        if node not in visited:
            if _dfs(node, -1):
                return True
    return False


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

def main() -> None:
    """Run all DFS demonstrations."""
    print("=" * 60)
    print("Chapter 30 — Depth-First Search (DFS)")
    print("=" * 60)

    graph = build_sample_graph()

    # --- Recursive DFS ---
    print("\n--- Recursive DFS (pre-order) ---")
    visited_rec: Set[int] = set()
    order_rec: List[int] = []
    dfs_recursive(graph, 0, visited_rec, order_rec)
    print(f"  Start node 0 → traversal order: {order_rec}")
    print(f"  Visited nodes: {sorted(visited_rec)}")

    # --- Iterative DFS ---
    print("\n--- Iterative DFS (pre-order) ---")
    order_iter = dfs_iterative(graph, 0)
    print(f"  Start node 0 → traversal order: {order_iter}")

    # --- Post-order DFS ---
    print("\n--- Iterative DFS (post-order) ---")
    order_post = dfs_postorder(graph, 0)
    print(f"  Start node 0 → post-order: {order_post}")

    # --- Traversal from a different start node ---
    print("\n--- Iterative DFS starting from node 5 ---")
    order_from_5 = dfs_iterative(graph, 5)
    print(f"  Start node 5 → traversal order: {order_from_5}")

    # --- Connected components ---
    print("\n--- Connected Components ---")
    components = connected_components(graph)
    print(f"  Number of components: {len(components)}")
    for i, comp in enumerate(components, 1):
        print(f"  Component {i}: {comp}")

    # --- Cycle detection ---
    print("\n--- Cycle Detection (undirected) ---")
    print(f"  Graph has cycle: {has_cycle_undirected(graph)}")

    # --- Directed acyclic graph (no cycle) ---
    dag = build_directed_graph()
    print("\n--- Directed Acyclic Graph (DAG) ---")
    print(f"  DAG: {dag}")
    print(f"  DAG has cycle: {has_cycle_undirected(dag)}")

    # --- Directed graph with a cycle ---
    cyclic_dag: Dict[int, List[int]] = {
        0: [1],
        1: [2],
        2: [0],  # back edge creating a cycle
    }
    print("\n--- Directed Graph with Cycle ---")
    print(f"  Graph: {cyclic_dag}")
    # Note: has_cycle_undirected treats the graph as undirected,
    # so it will detect the cycle even in a directed representation.
    print(f"  (Treated as undirected) has cycle: {has_cycle_undirected(cyclic_dag)}")


if __name__ == "__main__":
    main()
