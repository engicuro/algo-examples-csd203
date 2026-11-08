# Breadth-First Search (BFS) for Beginners
# BFS explores a graph level by level, starting from a given vertex.
# It uses a queue (first-in, first-out) to decide which vertex to visit next.
# This file shows two things:
#   1. BFS traversal order (which vertices are visited and in what order)
#   2. Shortest path in an unweighted graph (using parent tracking)


def bfs_traversal(graph, start):
    """Perform BFS on a graph starting from 'start'.

    graph: a dict where each key is a vertex and its value is a list of
           neighboring vertices (adjacency list).
    start: the vertex where BFS begins.

    Returns a list of vertices in the order they were visited.
    """
    # 'visited' keeps track of which vertices we have already seen
    visited = set()
    # 'queue' holds vertices we have discovered but not yet explored
    queue = ()

    # Mark the start vertex as visited and add it to the queue
    visited = visited | {start}
    queue = queue + (start,)

    # Continue until there are no more vertices to explore
    while len(queue) > 0:
        # Remove the first vertex from the queue (FIFO order)
        current = queue[0]
        queue = queue[1:]

        # Look at every neighbor of the current vertex
        for neighbor in graph[current]:
            # Only process neighbors we haven't visited yet
            if neighbor not in visited:
                # Mark it as visited
                visited = visited | {neighbor}
                # Add it to the queue so we can explore its neighbors later
                queue = queue + (neighbor,)

    return visited


def bfs_shortest_path(graph, start, goal):
    """Find the shortest path between 'start' and 'goal' in an unweighted graph.

    Because BFS explores vertices level by level, the first time it reaches
    the goal vertex, it has found the shortest path (fewest edges).

    graph: adjacency list (dict of vertex -> list of neighbors)
    start: the vertex to begin from
    goal:  the vertex we want to reach

    Returns a list of vertices forming the shortest path from start to goal.
    Returns an empty list if no path exists.
    """
    # 'parent' maps each visited vertex to the vertex we came from.
    # This lets us trace back from the goal to the start once we find it.
    parent = {}
    # 'visited' keeps track of vertices we have already enqueued
    visited = set()
    # 'queue' holds vertices waiting to be explored
    queue = ()

    # Start BFS from the 'start' vertex
    visited = visited | {start}
    queue = queue + (start,)
    # The start vertex has no parent (it is the beginning of the path)
    parent[start] = None

    while len(queue) > 0:
        # Take the next vertex from the front of the queue
        current = queue[0]
        queue = queue[1:]

        # If we reached the goal, we are done — reconstruct the path
        if current == goal:
            path = ()
            # Walk backwards from goal to start using the parent map
            vertex = goal
            while vertex is not None:
                path = path + (vertex,)
                vertex = parent[vertex]
            # The path is built backwards, so reverse it
            path = tuple(reversed(path))
            return path

        # Explore all neighbors of the current vertex
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited = visited | {neighbor}
                queue = queue + (neighbor,)
                # Record how we got to this neighbor
                parent[neighbor] = current

    # If we exit the loop, the goal was never reached
    return []


# ---- Example usage ----
if __name__ == "__main__":
    # A simple unweighted graph drawn as an adjacency list.
    #
    #     A --- B --- E
    #     |     |
    #     C     D
    #
    # Edges: A-B, A-C, B-D, B-E, C-D
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "D"],
        "D": ["B", "C"],
        "E": ["B"],
    }

    # --- Part 1: BFS traversal order ---
    print("BFS traversal starting from A:")
    order = bfs_traversal(graph, "A")
    print(order)
    # Expected: ['A', 'B', 'C', 'D', 'E']
    # BFS visits A first, then its neighbors B and C, then their neighbors D and E.

    print()

    # --- Part 2: Shortest path ---
    start_vertex = "A"
    goal_vertex = "E"
    print("Shortest path from A to E:")
    path = bfs_shortest_path(graph, start_vertex, goal_vertex)
    print(path)
    # Expected: ['A', 'B', 'E']
    # The shortest path has 2 edges: A -> B -> E.

    print()

    # Another shortest path example
    print("Shortest path from C to E:")
    path2 = bfs_shortest_path(graph, "C", "E")
    print(path2)
    # Expected: ['C', 'A', 'B', 'E'] or ['C', 'D', 'B', 'E']
    # Both have 3 edges — BFS finds one of the shortest paths.
