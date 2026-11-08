# Adjacency Matrix Representation of a Graph (No-List Version)
#
# An adjacency matrix is stored as a dictionary of dictionaries
# where matrix[i][j] tells you whether there is an edge
# from vertex i to vertex j, and optionally how heavy that edge is.
#
# This file uses only basic Python: dicts, loops, if/else, and simple
# functions.  No list comprehensions, no typing, no dataclasses.


def create_matrix(n):
    """Return an n x n matrix filled with zeros.

    We use a dict-of-dicts structure instead of a 2D list.
    """
    matrix = {}
    for i in range(n):
        matrix[i] = {}
        for j in range(n):
            matrix[i][j] = 0
    return matrix


def add_edge(matrix, vertex_a, vertex_b, weight=1):
    """Set matrix[vertex_a][vertex_b] to weight.

    For an undirected graph we also set the mirror entry so the
    matrix stays symmetric.
    """
    matrix[vertex_a][vertex_b] = weight
    # For undirected graphs, add the reverse edge too
    matrix[vertex_b][vertex_a] = weight


def display_matrix(matrix):
    """Print the matrix row by row in a readable format."""
    print("Adjacency Matrix:")
    # Print a header row showing column indices
    header = "    "
    for col in range(len(matrix)):
        header = header + str(col) + " "
    print(header)
    # Print each row with its row index
    for i in range(len(matrix)):
        row_str = str(i) + " | "
        for j in range(len(matrix[i])):
            row_str = row_str + str(matrix[i][j]) + " "
        print(row_str)


def has_edge(matrix, vertex_a, vertex_b):
    """Return True if there is an edge from vertex_a to vertex_b."""
    if matrix[vertex_a][vertex_b] != 0:
        return True
    return False


def get_neighbors(matrix, vertex):
    """Return a tuple of all vertices that are directly connected to vertex."""
    neighbors = ()
    for j in range(len(matrix[vertex])):
        if matrix[vertex][j] != 0:
            neighbors = neighbors + (j,)
    return neighbors


if __name__ == "__main__":
    # --- Example: a small undirected graph with 4 vertices ---
    #
    #   0 --- 1
    #   |     |
    #   2 --- 3
    #
    # Edges: (0,1), (0,2), (1,3), (2,3)

    num_vertices = 4
    graph = create_matrix(num_vertices)

    # Add edges one by one
    add_edge(graph, 0, 1, weight=1)
    add_edge(graph, 0, 2, weight=1)
    add_edge(graph, 1, 3, weight=1)
    add_edge(graph, 2, 3, weight=1)

    # Display the full matrix
    display_matrix(graph)

    # Check if specific edges exist
    print("")
    print("Edge 0 -> 1 exists?", has_edge(graph, 0, 1))
    print("Edge 1 -> 2 exists?", has_edge(graph, 1, 2))

    # List neighbors of each vertex
    print("")
    for v in range(num_vertices):
        neighbors = get_neighbors(graph, v)
        print("Neighbors of vertex", v, ":", neighbors)
