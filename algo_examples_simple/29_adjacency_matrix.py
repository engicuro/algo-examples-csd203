# Adjacency Matrix Representation of a Graph
#
# An adjacency matrix is a 2D list (table) where rows and columns
# represent vertices.  matrix[i][j] tells you whether there is an
# edge from vertex i to vertex j, and optionally how heavy that edge is.
#
# This file uses only basic Python: lists, loops, if/else, and simple
# functions.  No list comprehensions, no typing, no dataclasses.


def create_matrix(n):
    """Return an n x n matrix filled with zeros.

    Each row is a list of n zeros.  We build it with a plain loop
    so that every row is a separate list (important for correctness).
    """
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(0)
        matrix.append(row)
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
    """Return a list of all vertices that are directly connected to vertex."""
    neighbors = []
    for j in range(len(matrix[vertex])):
        if matrix[vertex][j] != 0:
            neighbors.append(j)
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
