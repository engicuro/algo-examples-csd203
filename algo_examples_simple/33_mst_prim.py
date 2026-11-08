# Prim-Jarnik Minimum Spanning Tree Algorithm
# A simple implementation for beginners.
#
# What is a Minimum Spanning Tree (MST)?
#   Given a connected, weighted, undirected graph, an MST is a set of edges
#   that connects all vertices together with the minimum possible total edge weight.
#
# What is Prim-Jarnik's algorithm?
#   1. Start from any vertex.
#   2. Keep a list of candidate edges that connect visited vertices to unvisited ones.
#   3. Pick the candidate edge with the smallest weight.
#   4. Add that edge to the MST and mark the new vertex as visited.
#   5. Repeat until all vertices are visited.
#
# This version uses a plain list (not a heap) to find the minimum edge,
# making the code easy to read and understand.

import math


def prim_mst(graph, start_vertex):
    """Find the Minimum Spanning Tree of a graph using Prim-Jarnik's algorithm.

    Args:
        graph: A dictionary mapping each vertex to a list of (neighbor, weight) tuples.
               Example: {'A': [('B', 1), ('C', 4)], 'B': [('A', 1), ('C', 2)], ...}
        start_vertex: The vertex to start the algorithm from.

    Returns:
        A tuple of (mst_edges, total_weight) where:
            mst_edges is a list of (u, v, weight) tuples representing the MST edges,
            total_weight is the sum of all edge weights in the MST.
    """
    # Set of vertices that have been added to the MST so far
    visited = set()

    # List of edges in the MST — each edge is (vertex_u, vertex_v, weight)
    mst_edges = []

    # Total weight of all edges in the MST
    total_weight = 0

    # Begin from the start vertex
    visited.add(start_vertex)

    # We need exactly (number_of_vertices - 1) edges to span all vertices
    num_vertices = len(graph)

    # Keep growing the MST until all vertices are visited
    while len(visited) < num_vertices:
        # Search through all visited vertices for candidate edges
        # that lead to unvisited vertices.
        # We track the best (minimum weight) candidate found so far.
        best_edge = None       # (vertex_u, vertex_v, weight) of the best candidate
        best_weight = math.inf  # Start with infinity so any real weight is smaller

        # Look at every vertex that is already in the MST
        for vertex in visited:
            # Check all neighbors of this vertex
            for neighbor, weight in graph[vertex]:
                # Only consider edges that go to an unvisited vertex
                if neighbor not in visited:
                    # Is this edge lighter than the best we've found so far?
                    if weight < best_weight:
                        best_weight = weight
                        best_edge = (vertex, neighbor, weight)

        # If we found a valid candidate edge, add it to the MST
        if best_edge is not None:
            u, v, weight = best_edge
            mst_edges.append(best_edge)
            total_weight = total_weight + weight
            visited.add(v)
        else:
            # This means the graph is disconnected and we cannot reach all vertices.
            # For a connected graph, this branch should never be reached.
            print("Warning: Graph is disconnected. Cannot build a spanning tree.")
            break

    return mst_edges, total_weight


def print_mst(mst_edges, total_weight):
    """Print the edges of the MST and the total weight in a readable format."""
    print("Edges in the Minimum Spanning Tree:")
    for u, v, weight in mst_edges:
        print("  " + str(u) + " -- " + str(v) + "  (weight: " + str(weight) + ")")
    print("Total weight of MST: " + str(total_weight))


if __name__ == "__main__":
    # Example graph: 5 vertices (A, B, C, D, E) with weighted edges.
    #
    #       A
    #      / \
    #     1   4
    #    /     \
    #   B---2---C
    #   |       |
    #   3       5
    #   |       |
    #   D---1---E
    #
    # The graph is undirected, so each edge appears in both directions.

    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 3)],
        'C': [('A', 4), ('B', 2), ('E', 5)],
        'D': [('B', 3), ('E', 1)],
        'E': [('C', 5), ('D', 1)],
    }

    # Run Prim-Jarnik starting from vertex 'A'
    print("Running Prim-Jarnik MST starting from vertex 'A':")
    print("")

    mst_edges, total_weight = prim_mst(graph, 'A')

    print_mst(mst_edges, total_weight)
