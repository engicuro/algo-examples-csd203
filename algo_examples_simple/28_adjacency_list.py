# Adjacency List Representation of a Graph
#
# An adjacency list stores a graph as a dictionary where:
#   - Each key is a vertex (node)
#   - Each value is a list of neighboring vertices
#
# This is efficient for sparse graphs (few edges compared to vertices).


def make_graph():
    """Return an empty graph (an empty dictionary)."""
    graph = {}
    return graph


def add_vertex(graph, vertex):
    """Add a vertex to the graph if it does not already exist."""
    # Only add the vertex if it is not already a key in the graph
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


def get_neighbors(graph, vertex):
    """Return the list of neighbors for a given vertex.

    Returns an empty list if the vertex is not in the graph.
    """
    if vertex in graph:
        return graph[vertex]
    else:
        return []


def has_edge(graph, vertex1, vertex2):
    """Return True if an edge exists between vertex1 and vertex2."""
    # Check that vertex1 is in the graph and vertex2 is in its neighbor list
    if vertex1 in graph:
        if vertex2 in graph[vertex1]:
            return True
    return False


# -------------------- Example usage --------------------
if __name__ == "__main__":
    # Create an empty graph
    my_graph = make_graph()

    # Add some vertices
    add_vertex(my_graph, "A")
    add_vertex(my_graph, "B")
    add_vertex(my_graph, "C")
    add_vertex(my_graph, "D")

    # Add edges (undirected)
    add_edge(my_graph, "A", "B")
    add_edge(my_graph, "A", "C")
    add_edge(my_graph, "B", "D")
    add_edge(my_graph, "C", "D")

    # Display the full adjacency list
    print("Adjacency list:")
    display(my_graph)

    # Find neighbors of a specific vertex
    print()
    print("Neighbors of A:", get_neighbors(my_graph, "A"))
    print("Neighbors of D:", get_neighbors(my_graph, "D"))

    # Check if specific edges exist
    print()
    print("Edge A -- B exists?", has_edge(my_graph, "A", "B"))
    print("Edge A -- D exists?", has_edge(my_graph, "A", "D"))
