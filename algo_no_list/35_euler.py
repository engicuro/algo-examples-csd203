# Euler Tour and Euler Cycle for Beginners
# =========================================
# An Euler tour visits every edge in a graph exactly once.
# An Euler cycle is an Euler tour that starts and ends at the same vertex.
#
# Conditions:
#   - Euler cycle exists  => every vertex has an even degree
#   - Euler tour exists   => exactly 0 or 2 vertices have an odd degree
#
# Hierholzer's algorithm builds the tour by walking until stuck,
# then splicing in side loops. It uses a tuple as a stack
# (concatenate to push, slice to pop from the end).


def _tuple_remove_first(t, val):
    """Return a new tuple with the first occurrence of val removed."""
    result = ()
    found = False
    for item in t:
        if not found and item == val:
            found = True
            continue
        result = result + (item,)
    return result


def degree(graph, vertex):
    """Return the degree of a vertex (number of edges touching it).

    In an undirected graph each edge appears in both adjacency tuples,
    so the length of the neighbor tuple equals the degree.
    """
    return len(graph[vertex])


def all_even_degrees(graph):
    """Return True if every vertex in the graph has an even degree."""
    for vertex in graph:
        if degree(graph, vertex) % 2 != 0:
            return False
    return True


def count_odd_degree_vertices(graph):
    """Return how many vertices have an odd degree."""
    odd_count = 0
    for vertex in graph:
        if degree(graph, vertex) % 2 != 0:
            odd_count += 1
    return odd_count


def euler_cycle_exists(graph):
    """Return True if the graph has an Euler cycle.

    An Euler cycle exists when every vertex has an even degree
    and the graph is connected (we skip the connectivity check here
    for simplicity — assume the graph is connected).
    """
    return all_even_degrees(graph)


def euler_tour_exists(graph):
    """Return True if the graph has an Euler tour (but not necessarily a cycle).

    An Euler tour exists when exactly 0 or 2 vertices have an odd degree.
    """
    odd_count = count_odd_degree_vertices(graph)
    return odd_count == 0 or odd_count == 2


def find_euler_tour(graph, start_vertex):
    """Find an Euler tour or cycle using Hierholzer's algorithm.

    Args:
        graph: dict mapping each vertex to a tuple of its neighbors.
        start_vertex: the vertex to start the tour from.

    Returns:
        A tuple of vertices representing the Euler tour/cycle.
    """
    # Make a copy of the graph so we can remove edges without modifying the original
    remaining = {}
    for vertex in graph:
        remaining[vertex] = tuple(graph[vertex])

    # Stack holds the current path we are exploring
    stack = (start_vertex,)
    # The final tour is built in reverse order
    tour = ()

    while len(stack) > 0:
        current = stack[-1]  # Look at the top of the stack

        if len(remaining[current]) > 0:
            # There are still unused edges from this vertex — walk one
            next_vertex = remaining[current][-1]
            remaining[current] = remaining[current][:-1]
            # Remove the reverse edge (since the graph is undirected)
            remaining[next_vertex] = _tuple_remove_first(remaining[next_vertex], current)
            stack = stack + (next_vertex,)
        else:
            # No more edges from this vertex — add it to the tour and backtrack
            tour = tour + (stack[-1],)
            stack = stack[:-1]

    # The tour is built backwards, so reverse it
    tour = tuple(reversed(tour))
    return tour


# ----- Example 1: A graph with an Euler cycle -------------------------
#
#   0 --- 1
#   |     |
#   3 --- 2
#
# Every vertex has degree 2 (even), so an Euler cycle exists.
# One possible cycle: 0 -> 1 -> 2 -> 3 -> 0

cycle_graph = {
    0: (1, 3),
    1: (0, 2),
    2: (1, 3),
    3: (0, 2),
}

print("=== Example 1: Euler Cycle ===")
print("Graph (adjacency tuple):")
for vertex in cycle_graph:
    print("  vertex", vertex, "connects to", cycle_graph[vertex])

print("All degrees even?", all_even_degrees(cycle_graph))
print("Euler cycle exists?", euler_cycle_exists(cycle_graph))

cycle = find_euler_tour(cycle_graph, 0)
print("Euler cycle:", cycle)
print()

# ----- Example 2: A graph with an Euler tour (but not a cycle) --------
#
#   0 --- 1 --- 2
#         |
#         3
#
# Vertex 0 has degree 1 (odd)
# Vertex 1 has degree 3 (odd)
# Vertex 2 has degree 1 (odd)  <-- wait, that's 3 odd vertices
# Let's fix the graph so exactly 2 vertices are odd.
#
#   0 --- 1 --- 2
#
# Vertex 0 has degree 1 (odd)
# Vertex 1 has degree 2 (even)
# Vertex 2 has degree 1 (odd)
# Exactly 2 odd-degree vertices => Euler tour exists (0 -> 1 -> 2).

tour_graph = {
    0: (1,),
    1: (0, 2),
    2: (1,),
}

print("=== Example 2: Euler Tour ===")
print("Graph (adjacency tuple):")
for vertex in tour_graph:
    print("  vertex", vertex, "connects to", tour_graph[vertex])

print("Number of odd-degree vertices:", count_odd_degree_vertices(tour_graph))
print("Euler tour exists?", euler_tour_exists(tour_graph))

tour = find_euler_tour(tour_graph, 0)
print("Euler tour:", tour)
print()

# ----- Example 3: A more complex Euler cycle --------------------------
#
#   0 --- 1 --- 2
#   |     |     |
#   3 --- 4 --- 5
#
# Each vertex has degree 2 or 3 — let's make sure all are even.
# Actually let's use a simple cycle of 6 vertices.
#
#   0 - 1 - 2
#   |       |
#   3 - 4 - 5
#
# Degrees: 0->2, 1->2, 2->2, 3->2, 4->2, 5->2  (all even)

big_cycle_graph = {
    0: (1, 3),
    1: (0, 2),
    2: (1, 5),
    3: (0, 4),
    4: (3, 5),
    5: (2, 4),
}

print("=== Example 3: Larger Euler Cycle ===")
print("Graph (adjacency tuple):")
for vertex in big_cycle_graph:
    print("  vertex", vertex, "connects to", big_cycle_graph[vertex])

print("All degrees even?", all_even_degrees(big_cycle_graph))
print("Euler cycle exists?", euler_cycle_exists(big_cycle_graph))

big_cycle = find_euler_tour(big_cycle_graph, 0)
print("Euler cycle:", big_cycle)
print()

# ----- Example 4: A graph with no Euler tour -------------------------
#
#   0 --- 1
#   |
#   2
#
# Vertex 0 has degree 2 (even)
# Vertex 1 has degree 1 (odd)
# Vertex 2 has degree 1 (odd)
# Wait — that's 2 odd vertices, so a tour DOES exist.
# Let's try a graph with 4 odd-degree vertices (no tour).
#
#   0 --- 1
#   |     |
#   2 --- 3
#   |
#   4
#
# Degrees: 0->2, 1->2, 2->3, 3->2, 4->1  => 2 odd vertices (2 and 4)
# Still a tour. Let's just show a disconnected case or 4 odd vertices.
#
#   0 --- 1     2 --- 3
#
# Degrees: 0->1, 1->1, 2->1, 3->1  => 4 odd vertices, no tour.

no_tour_graph = {
    0: (1,),
    1: (0,),
    2: (3,),
    3: (2,),
}

print("=== Example 4: No Euler Tour ===")
print("Graph (adjacency tuple):")
for vertex in no_tour_graph:
    print("  vertex", vertex, "connects to", no_tour_graph[vertex])

print("Number of odd-degree vertices:", count_odd_degree_vertices(no_tour_graph))
print("Euler tour exists?", euler_tour_exists(no_tour_graph))
print("(This graph is disconnected, so no Euler tour is possible.)")
