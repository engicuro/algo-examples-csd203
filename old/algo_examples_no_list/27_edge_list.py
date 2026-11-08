# Edge List Representation of a Graph
# An edge list stores a graph as a list of edges.
# Each edge is a tuple: (from_vertex, to_vertex, weight)
# This is one of the simplest ways to represent a graph.


def add_edge(edge_list, from_vertex, to_vertex, weight=1):
    """Add an edge to the edge list.

    Args:
        edge_list: the list that holds all edges
        from_vertex: the starting vertex of the edge
        to_vertex: the ending vertex of the edge
        weight: the weight/cost of the edge (default is 1)
    """
    edge = (from_vertex, to_vertex, weight)
    edge_list = edge_list + (edge,)


def display_edges(edge_list):
    """Print all edges in the edge list.

    Each edge is shown as: from_vertex -> to_vertex (weight)
    """
    print("Edges in the graph:")
    for edge in edge_list:
        from_vertex = edge[0]
        to_vertex = edge[1]
        weight = edge[2]
        print("  " + str(from_vertex) + " -> " + str(to_vertex) + " (weight: " + str(weight) + ")")


def get_neighbors(edge_list, vertex):
    """Find all neighbors of a given vertex.

    A neighbor is any vertex that can be reached directly
    by an outgoing edge from the given vertex.

    Args:
        edge_list: the list that holds all edges
        vertex: the vertex whose neighbors we want to find

    Returns:
        A list of neighboring vertices
    """
    neighbors = ()
    for edge in edge_list:
        from_vertex = edge[0]
        to_vertex = edge[1]
        if from_vertex == vertex:
            neighbors = neighbors + (to_vertex,)
    return neighbors


def has_edge(edge_list, from_vertex, to_vertex):
    """Check if an edge exists from from_vertex to to_vertex.

    Args:
        edge_list: the list that holds all edges
        from_vertex: the starting vertex to look for
        to_vertex: the ending vertex to look for

    Returns:
        True if the edge exists, False otherwise
    """
    for edge in edge_list:
        if edge[0] == from_vertex and edge[1] == to_vertex:
            return True
    return False


def count_edges(edge_list):
    """Return the total number of edges in the graph.

    Args:
        edge_list: the list that holds all edges

    Returns:
        The number of edges
    """
    return len(edge_list)


def get_all_vertices(edge_list):
    """Collect all unique vertices that appear in the edge list.

    A vertex can appear as either a from_vertex or a to_vertex.

    Args:
        edge_list: the list that holds all edges

    Returns:
        A list of all unique vertices
    """
    vertices = ()
    for edge in edge_list:
        from_vertex = edge[0]
        to_vertex = edge[1]
        # Add from_vertex if we haven't seen it yet
        if from_vertex not in vertices:
            vertices = vertices + (from_vertex,)
        # Add to_vertex if we haven't seen it yet
        if to_vertex not in vertices:
            vertices = vertices + (to_vertex,)
    return vertices


# --- Main block: simple example usage ---
if __name__ == "__main__":
    # Create an empty edge list to represent our graph
    edges = ()

    # Add some edges (from, to, weight)
    # This graph looks like:
    #   A --1--> B
    #   A --3--> C
    #   B --2--> C
    #   C --1--> D
    #   D --4--> A
    add_edge(edges, "A", "B", 1)
    add_edge(edges, "A", "C", 3)
    add_edge(edges, "B", "C", 2)
    add_edge(edges, "C", "D", 1)
    add_edge(edges, "D", "A", 4)

    # Display all edges
    display_edges(edges)

    # Count the edges
    print("\nTotal number of edges: " + str(count_edges(edges)))

    # Get all vertices
    vertices = get_all_vertices(edges)
    print("All vertices: " + str(vertices))

    # Find neighbors of a vertex
    print("\nNeighbors of A: " + str(get_neighbors(edges, "A")))
    print("Neighbors of C: " + str(get_neighbors(edges, "C")))

    # Check if specific edges exist
    print("\nDoes edge A -> B exist? " + str(has_edge(edges, "A", "B")))
    print("Does edge B -> A exist? " + str(has_edge(edges, "B", "A")))
    print("Does edge C -> D exist? " + str(has_edge(edges, "C", "D")))
