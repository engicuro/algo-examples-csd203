# 26_graph_basics.py
# A beginner-friendly introduction to graph basics in Python.
# No list comprehensions, no typing, no dataclasses.
# Only basic Python: lists, loops, if/else, simple functions.


# ---------------------------------------------------------------------------
# What is a graph?
# ---------------------------------------------------------------------------
# A graph is a way to represent connections between things.
# Each "thing" is called a vertex (plural: vertices).
# Each "connection" between two vertices is called an edge.
#
# Example:
#   Vertices:  A, B, C
#   Edges:     A -- B,  B -- C
#   This means A is connected to B, and B is connected to C.
#
# Graphs are used to model:
#   - Social networks (people are vertices, friendships are edges)
#   - Road maps (cities are vertices, roads are edges)
#   - Computer networks (devices are vertices, cables are edges)


# ---------------------------------------------------------------------------
# Directed vs Undirected Graphs
# ---------------------------------------------------------------------------
# In an UNDIRECTED graph, edges go both ways.
#   If there is an edge between A and B, you can travel A -> B and B -> A.
#   Example: a two-way road between two cities.
#
# In a DIRECTED graph (also called a digraph), edges go one way only.
#   If there is an edge from A to B, you can only travel A -> B, not B -> A.
#   Example: a one-way street between two cities.


# ---------------------------------------------------------------------------
# Weighted vs Unweighted Graphs
# ---------------------------------------------------------------------------
# In an UNWEIGHTED graph, every edge is treated the same — no extra cost.
#   Example: simple friendships (each friendship counts as 1).
#
# In a WEIGHTED graph, each edge has a number (a weight) attached.
#   The weight can represent distance, cost, time, etc.
#   Example: roads between cities where the weight is the distance in miles.


# ---------------------------------------------------------------------------
# Simple dict-based graph representation
# ---------------------------------------------------------------------------
# We will use a Python dictionary where:
#   - Each KEY is a vertex (a string name).
#   - Each VALUE is a LIST of neighbors (the vertices it connects to).
#
# For weighted graphs, each neighbor is stored as a two-element list:
#   [neighbor_name, weight]
#
# Example of an unweighted graph:
#   {
#       "A": ["B", "C"],
#       "B": ["A"],
#       "C": ["A"]
#   }
# This means A connects to B and C, B connects to A, C connects to A.


def create_empty_graph():
    """Return an empty dictionary to represent a graph."""
    graph = {}
    return graph


def add_vertex(graph, vertex_name):
    """Add a vertex to the graph if it does not already exist.

    Args:
        graph:      The dictionary representing the graph.
        vertex_name: A string name for the new vertex.
    """
    if vertex_name not in graph:
        graph[vertex_name] = ()
        print("Added vertex: " + vertex_name)
    else:
        print("Vertex already exists: " + vertex_name)


def add_edge(graph, from_vertex, to_vertex):
    """Add an undirected edge between two vertices (unweighted).

    For an undirected graph, we add each vertex to the other's neighbor list.

    Args:
        graph:      The dictionary representing the graph.
        from_vertex: The first vertex name (string).
        to_vertex:   The second vertex name (string).
    """
    # Make sure both vertices exist first
    if from_vertex not in graph:
        add_vertex(graph, from_vertex)
    if to_vertex not in graph:
        add_vertex(graph, to_vertex)

    # Add to_vertex to from_vertex's neighbor list (if not already there)
    if to_vertex not in graph[from_vertex]:
        graph[from_vertex] = graph[from_vertex] + (to_vertex,)

    # Add from_vertex to to_vertex's neighbor list (undirected = both ways)
    if from_vertex not in graph[to_vertex]:
        graph[to_vertex] = graph[to_vertex] + (from_vertex,)

    print("Added edge: " + from_vertex + " -- " + to_vertex)


def add_directed_edge(graph, from_vertex, to_vertex):
    """Add a directed edge from from_vertex to to_vertex (unweighted).

    For a directed graph, we only add to_vertex to from_vertex's list.

    Args:
        graph:      The dictionary representing the graph.
        from_vertex: The source vertex name (string).
        to_vertex:   The destination vertex name (string).
    """
    if from_vertex not in graph:
        add_vertex(graph, from_vertex)
    if to_vertex not in graph:
        add_vertex(graph, to_vertex)

    if to_vertex not in graph[from_vertex]:
        graph[from_vertex] = graph[from_vertex] + (to_vertex,)

    print("Added directed edge: " + from_vertex + " -> " + to_vertex)


def add_weighted_edge(graph, from_vertex, to_vertex, weight):
    """Add an undirected weighted edge between two vertices.

    Each neighbor is stored as a two-element list: [neighbor_name, weight].

    Args:
        graph:      The dictionary representing the graph.
        from_vertex: The first vertex name (string).
        to_vertex:   The second vertex name (string).
        weight:      A number representing the cost/distance of this edge.
    """
    if from_vertex not in graph:
        add_vertex(graph, from_vertex)
    if to_vertex not in graph:
        add_vertex(graph, to_vertex)

    # Append [to_vertex, weight] to from_vertex's list if not duplicate
    pair_to = [to_vertex, weight]
    if pair_to not in graph[from_vertex]:
        graph[from_vertex] = graph[from_vertex] + (pair_to,)

    # Append [from_vertex, weight] to to_vertex's list (undirected = both ways)
    pair_from = [from_vertex, weight]
    if pair_from not in graph[to_vertex]:
        graph[to_vertex] = graph[to_vertex] + (pair_from,)

    print("Added weighted edge: " + from_vertex + " -- " + to_vertex + " (weight: " + str(weight) + ")")


def display_graph(graph):
    """Print every vertex and its neighbors in a readable format.

    Args:
        graph: The dictionary representing the graph.
    """
    print("\n--- Graph contents ---")
    for vertex in graph:
        neighbors = graph[vertex]
        print("  " + vertex + " connects to: " + str(neighbors))
    print("----------------------\n")


def get_neighbors(graph, vertex):
    """Return the list of neighbors for a given vertex.

    Args:
        graph:   The dictionary representing the graph.
        vertex:  The vertex name to look up.

    Returns:
        A list of neighbors, or an empty list if the vertex is not found.
    """
    if vertex in graph:
        return graph.get(vertex, ())
    else:
        print("Vertex not found: " + vertex)
        return []


def has_edge(graph, vertex_a, vertex_b):
    """Check if an undirected edge exists between vertex_a and vertex_b.

    Args:
        graph:    The dictionary representing the graph.
        vertex_a: The first vertex name.
        vertex_b: The second vertex name.

    Returns:
        True if the edge exists, False otherwise.
    """
    if vertex_a not in graph or vertex_b not in graph:
        return False
    return vertex_b in graph[vertex_a]


def count_vertices(graph):
    """Return the number of vertices in the graph."""
    return len(graph)


def count_edges(graph):
    """Return the number of edges in an undirected graph.

    Since each undirected edge is stored twice (once for each vertex),
    we divide the total neighbor count by 2.
    """
    total_neighbors = 0
    for vertex in graph:
        total_neighbors = total_neighbors + len(graph.get(vertex, ()))
    return total_neighbors // 2


# ---------------------------------------------------------------------------
# __main__ block — simple example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Graph Basics Examples ===\n")

    # --- Example 1: Undirected, unweighted graph ---
    print("--- Example 1: Undirected, unweighted graph ---")
    g1 = create_empty_graph()
    add_vertex(g1, "A")
    add_vertex(g1, "B")
    add_vertex(g1, "C")
    add_edge(g1, "A", "B")
    add_edge(g1, "B", "C")
    display_graph(g1)

    print("Number of vertices: " + str(count_vertices(g1)))
    print("Number of edges:    " + str(count_edges(g1)))
    print("Does A connect to B? " + str(has_edge(g1, "A", "B")))
    print("Does A connect to C? " + str(has_edge(g1, "A", "C")))
    print("Neighbors of B: " + str(get_neighbors(g1, "B")))

    # --- Example 2: Directed graph ---
    print("\n--- Example 2: Directed graph ---")
    g2 = create_empty_graph()
    add_vertex(g2, "X")
    add_vertex(g2, "Y")
    add_vertex(g2, "Z")
    add_directed_edge(g2, "X", "Y")   # X -> Y only
    add_directed_edge(g2, "Y", "Z")   # Y -> Z only
    display_graph(g2)

    print("X's neighbors (outgoing): " + str(get_neighbors(g2, "X")))
    print("Y's neighbors (outgoing): " + str(get_neighbors(g2, "Y")))
    print("Z's neighbors (outgoing): " + str(get_neighbors(g2, "Z")))
    print("Does X -> Y exist? " + str(has_edge(g2, "X", "Y")))
    print("Does Y -> X exist? " + str(has_edge(g2, "Y", "X")))

    # --- Example 3: Weighted graph ---
    print("\n--- Example 3: Weighted, undirected graph ---")
    g3 = create_empty_graph()
    add_vertex(g3, "Home")
    add_vertex(g3, "Store")
    add_vertex(g3, "Park")
    add_weighted_edge(g3, "Home", "Store", 5)    # 5 miles
    add_weighted_edge(g3, "Home", "Park", 3)     # 3 miles
    add_weighted_edge(g3, "Store", "Park", 7)    # 7 miles
    display_graph(g3)

    print("Home's neighbors: " + str(get_neighbors(g3, "Home")))
    print("Number of vertices: " + str(count_vertices(g3)))
    print("Number of edges:    " + str(count_edges(g3)))
