# 30_dfs.py
# A beginner-friendly introduction to Depth-First Search (DFS) in Python.
# Uses custom data structures from _structures.py instead of Python lists.

from _structures import LinkedList, SimpleSet


# ---------------------------------------------------------------------------
# What is Depth-First Search (DFS)?
# ---------------------------------------------------------------------------
# DFS is a way to visit every vertex in a graph.
# It goes as deep as possible down one path before backtracking.
#
# Think of it like exploring a maze:
#   - You pick a direction and keep going until you hit a dead end.
#   - Then you back up and try a different direction.
#   - You mark each room you visit so you don't go there again.
#
# DFS uses a stack (or recursion, which uses the call stack implicitly).
# At each step, we visit a vertex, then recursively visit all its
# unvisited neighbors.


# ---------------------------------------------------------------------------
# Recursive DFS
# ---------------------------------------------------------------------------

def dfs_recursive(graph, start_vertex, visited):
    """Visit vertices in depth-first order starting from start_vertex.

    This function modifies the visited set in place and prints
    each vertex as it is visited.

    Args:
        graph:         A dictionary mapping each vertex to a list of neighbors.
        start_vertex:  The vertex to start the search from.
        visited:       A set (or list) of vertices already visited.
    """
    # Mark the current vertex as visited
    visited.add(start_vertex)

    # Print the vertex to show the order we visit it
    print("  Visited: " + start_vertex)

    # Look at every neighbor of the current vertex
    for neighbor in graph[start_vertex]:
        # Only visit neighbors we have not seen yet
        if not visited.contains(neighbor):
            dfs_recursive(graph, neighbor, visited)


# ---------------------------------------------------------------------------
# Collect DFS order into a list (instead of just printing)
# ---------------------------------------------------------------------------

def dfs_collect(graph, start_vertex, visited, order):
    """Visit vertices in depth-first order and collect them into a list.

    This version stores the visited order in the 'order' list
    instead of printing directly.

    Args:
        graph:         A dictionary mapping each vertex to a list of neighbors.
        start_vertex:  The vertex to start the search from.
        visited:       A set of vertices already visited.
        order:         A list that records the visit order.
    """
    # Mark the current vertex as visited and record it
    visited.add(start_vertex)
    order.append(start_vertex)

    # Explore each unvisited neighbor
    for neighbor in graph[start_vertex]:
        if not visited.contains(neighbor):
            dfs_collect(graph, neighbor, visited, order)


# ---------------------------------------------------------------------------
# Find all connected components in an undirected graph
# ---------------------------------------------------------------------------

def find_connected_components(graph):
    """Find all connected components in an undirected graph.

    A connected component is a group of vertices where every vertex
    can reach every other vertex in the same group.

    We run DFS from every unvisited vertex. Each new DFS call
    discovers one connected component.

    Args:
        graph: A dictionary mapping each vertex to a list of neighbors.

    Returns:
        A list of components, where each component is a list of vertices.
    """
    # Keep track of every vertex we have already visited
    visited = SimpleSet()

    # This will hold all the connected components we find
    components = LinkedList()

    # Try starting a DFS from every vertex in the graph
    for vertex in graph:
        # If we have not visited this vertex yet, it belongs to a
        # new connected component
        if not visited.contains(vertex):
            # Collect the vertices in this component
            component = LinkedList()
            dfs_collect(graph, vertex, visited, component)
            components.append(component)

    return components


# ---------------------------------------------------------------------------
# Helper: build a simple undirected graph
# ---------------------------------------------------------------------------

def make_graph():
    """Return an empty graph (an empty dictionary)."""
    graph = {}
    return graph


def add_vertex(graph, vertex):
    """Add a vertex to the graph if it does not already exist."""
    if vertex not in graph:
        graph[vertex] = []


def add_edge(graph, vertex1, vertex2):
    """Add an undirected edge between vertex1 and vertex2.

    Since the graph is undirected, we add each vertex to the
    other's neighbor list.
    """
    # Make sure both vertices exist in the graph
    if vertex1 not in graph:
        add_vertex(graph, vertex1)
    if vertex2 not in graph:
        add_vertex(graph, vertex2)

    # Add vertex2 to vertex1's neighbor list (if not already there)
    if vertex2 not in graph[vertex1]:
        graph[vertex1].append(vertex2)

    # Add vertex1 to vertex2's neighbor list (if not already there)
    if vertex1 not in graph[vertex2]:
        graph[vertex2].append(vertex1)


def display(graph):
    """Print every vertex and its list of neighbors."""
    for vertex in graph:
        neighbors = graph[vertex]
        print(vertex, "->", neighbors)


# ---------------------------------------------------------------------------
# __main__ block — simple example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== DFS Examples ===\n")

    # --- Example 1: DFS from a start vertex ---
    print("--- Example 1: DFS from vertex A ---")

    # Build a simple graph:
    #
    #     A --- B --- D
    #     |         |
    #     C ---------+
    #
    # Adjacency list:
    #   A: [B, C]
    #   B: [A, D]
    #   C: [A, D]
    #   D: [B, C]

    g1 = make_graph()
    add_vertex(g1, "A")
    add_vertex(g1, "B")
    add_vertex(g1, "C")
    add_vertex(g1, "D")
    add_edge(g1, "A", "B")
    add_edge(g1, "A", "C")
    add_edge(g1, "B", "D")
    add_edge(g1, "C", "D")

    print("Graph structure:")
    display(g1)
    print()

    # Run DFS starting from vertex A
    print("DFS visit order starting from A:")
    visited_set = SimpleSet()
    dfs_recursive(g1, "A", visited_set)
    print()

    # --- Example 2: Collect DFS order into a list ---
    print("--- Example 2: Collect DFS order into a list ---")

    visited_set2 = SimpleSet()
    order_list = LinkedList()
    dfs_collect(g1, "A", visited_set2, order_list)
    print("Visit order:", order_list)
    print()

    # --- Example 3: Find connected components ---
    print("--- Example 3: Find connected components ---")

    # Build a graph with two separate groups:
    #
    #   Group 1:  A --- B
    #             |
    #             C
    #
    #   Group 2:  X --- Y
    #             |
    #             Z
    #
    #   (No edges between Group 1 and Group 2)

    g2 = make_graph()
    add_vertex(g2, "A")
    add_vertex(g2, "B")
    add_vertex(g2, "C")
    add_vertex(g2, "X")
    add_vertex(g2, "Y")
    add_vertex(g2, "Z")
    add_edge(g2, "A", "B")
    add_edge(g2, "A", "C")
    add_edge(g2, "X", "Y")
    add_edge(g2, "X", "Z")

    print("Graph structure:")
    display(g2)

    # Find all connected components
    components = find_connected_components(g2)
    print("Number of connected components:", len(components))
    i = 1
    for component in components:
        print("  Component " + str(i) + ": " + str(component))
        i = i + 1
    print()

    # --- Example 4: DFS on a graph with one isolated vertex ---
    print("--- Example 4: Graph with an isolated vertex ---")

    # Build a graph where "D" has no edges
    #
    #   A --- B
    #   |
    #   C     D  (D is isolated)

    g3 = make_graph()
    add_vertex(g3, "A")
    add_vertex(g3, "B")
    add_vertex(g3, "C")
    add_vertex(g3, "D")
    add_edge(g3, "A", "B")
    add_edge(g3, "A", "C")

    print("Graph structure:")
    display(g3)

    components3 = find_connected_components(g3)
    print("Number of connected components:", len(components3))
    i = 1
    for component in components3:
        print("  Component " + str(i) + ": " + str(component))
        i = i + 1
