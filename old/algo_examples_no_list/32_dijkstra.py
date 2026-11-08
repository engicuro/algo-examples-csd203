# Dijkstra's Algorithm - Shortest Path Finder
# This file teaches Dijkstra's algorithm using only basic Python.
# No external libraries except `math`. No list comprehensions, no typing.

import math


def build_graph():
    """Return a graph as a dictionary.
    Each key is a vertex name (string).
    Each value is a list of (neighbor, weight) tuples.
    """
    graph = {}

    # Vertex A connects to B (cost 1) and C (cost 4)
    graph["A"] = [("B", 1), ("C", 4)]

    # Vertex B connects to A (cost 1), C (cost 2), and D (cost 6)
    graph["B"] = [("A", 1), ("C", 2), ("D", 6)]

    # Vertex C connects to A (cost 4), B (cost 2), and D (cost 3)
    graph["C"] = [("A", 4), ("B", 2), ("D", 3)]

    # Vertex D connects to B (cost 6) and C (cost 3)
    graph["D"] = [("B", 6), ("C", 3)]

    return graph


def find_smallest_unvisited(distances, visited):
    """Find the unvisited vertex with the smallest known distance.

    distances: a dict mapping each vertex to its current shortest distance.
    visited: a set of vertices we have already processed.

    Returns the vertex name (string) with the smallest distance,
    or None if all vertices have been visited.
    """
    smallest_vertex = None
    smallest_distance = math.inf  # Start with "infinity"

    for vertex in distances:
        # Skip vertices we have already visited
        if vertex in visited:
            continue
        # Update if this vertex has a smaller distance than our current best
        if distances[vertex] < smallest_distance:
            smallest_distance = distances[vertex]
            smallest_vertex = vertex

    return smallest_vertex


def dijkstra(graph, start):
    """Run Dijkstra's algorithm from the start vertex.

    graph: a dict of vertex -> list of (neighbor, weight) tuples.
    start: the name of the starting vertex (string).

    Returns two dicts:
      - distances: shortest distance from start to every vertex.
      - previous: for each vertex, which vertex comes before it on the
        shortest path (used to reconstruct paths).
    """
    # Step 1: Set every vertex's distance to infinity, except the start (0).
    distances = {}
    previous = {}
    for vertex in graph:
        distances[vertex] = math.inf
        previous[vertex] = None
    distances[start] = 0

    # Step 2: Keep track of which vertices we have already processed.
    visited = set()

    # Step 3: Process every vertex one by one.
    while len(visited) < len(graph):
        # Find the unvisited vertex closest to the start.
        current = find_smallest_unvisited(distances, visited)

        # If there are no reachable unvisited vertices left, we are done.
        if current is None:
            break

        # Mark the current vertex as visited.
        visited.add(current)

        # Step 4: Look at each neighbor of the current vertex.
        for neighbor, weight in graph[current]:
            # Skip neighbors we have already visited.
            if neighbor in visited:
                continue

            # Calculate the distance to this neighbor through the current vertex.
            new_distance = distances[current] + weight

            # If this new path is shorter than what we knew before, update it.
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current

    return distances, previous


def get_shortest_path(previous, start, target):
    """Reconstruct the shortest path from start to target.

    previous: a dict mapping each vertex to the vertex before it on the
              shortest path (as returned by dijkstra).
    start: the starting vertex name.
    target: the destination vertex name.

    Returns a list of vertex names from start to target, or an empty list
    if there is no path.
    """
    path = ()
    current = target

    # Walk backwards from the target to the start using the previous dict.
    while current is not None:
        path = path + (current,)
        current = previous[current]

    # Reverse the path so it goes from start to target.
    path = tuple(reversed(path))

    # If the first vertex in the path is not the start, there is no path.
    if path[0] != start:
        return []

    return path


def print_distances(distances, start):
    """Print the shortest distance from start to every vertex."""
    print("Shortest distances from vertex '{}':".format(start))
    for vertex in distances:
        distance = distances[vertex]
        if distance == math.inf:
            print("  {}: unreachable".format(vertex))
        else:
            print("  {}: {}".format(vertex, distance))


def print_path(path, target):
    """Print the shortest path to the target vertex."""
    if len(path) == 0:
        print("There is no path to {}.".format(target))
    else:
        path_string = " -> ".join(path)
        print("Shortest path to {}: {}".format(target, path_string))


# ---------------------------------------------------------------
# Main block: run a simple example when this file is executed.
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Build the graph
    my_graph = build_graph()

    # Pick the start vertex
    start_vertex = "A"

    # Run Dijkstra's algorithm
    distances, previous = dijkstra(my_graph, start_vertex)

    # Print all shortest distances from the start vertex
    print_distances(distances, start_vertex)

    print("")

    # Print the shortest path to a specific target vertex
    target_vertex = "D"
    path = get_shortest_path(previous, start_vertex, target_vertex)
    print_path(path, target_vertex)
