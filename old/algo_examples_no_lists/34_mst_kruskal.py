# Kruskal's Minimum Spanning Tree (MST) Algorithm
# A minimum spanning tree connects all nodes in a graph with the least total edge weight.
# Kruskal's algorithm works by sorting all edges by weight and greedily picking the smallest
# edge that does not form a cycle.
# Uses custom data structures from _structures.py instead of Python lists.

from _structures import IntArray, LinkedList


# --- Union-Find helper functions ---
# Union-Find (also called Disjoint Set Union) helps us quickly check whether two nodes
# are already connected, and merge two groups of nodes together.

# The parent array stores the "parent" of each node.
# If parent[x] == x, then x is the root of its group.
# Initially, every node is its own parent (each node is its own group).

# The rank array stores an approximate "depth" of each group's tree.
# We use rank to keep the trees balanced during merges, which makes operations faster.


def make_set(n):
    # Create a parent array and a rank array for n nodes (labeled 0 to n-1).
    # Each node starts as its own parent (root of its own group).
    # All ranks start at 0.
    parent = IntArray(n)
    rank = IntArray(n)
    for i in range(n):
        parent.set(i, i)  # each node is its own parent initially
        rank.set(i, 0)    # all ranks start at 0
    return parent, rank


def find(parent, x):
    # Follow parent links from x up to the root of its group.
    # The root is the node whose parent is itself.
    # This function also "flattens" the tree by pointing every visited node
    # directly to the root, making future lookups faster.
    while parent.get(x) != x:
        parent.set(x, parent.get(parent.get(x)))  # point x's parent to its grandparent (path compression)
        x = parent.get(x)                  # move up to the parent
    return x


def union(parent, rank, x, y):
    # Merge the groups containing x and y.
    # First, find the root of each group.
    root_x = find(parent, x)
    root_y = find(parent, y)

    # If they already share the same root, they are already connected.
    # No need to merge; return False to indicate no merge happened.
    if root_x == root_y:
        return False

    # Otherwise, attach the shorter tree under the taller tree (union by rank).
    # This keeps the trees balanced and operations fast.
    if rank.get(root_x) < rank.get(root_y):
        parent.set(root_x, root_y)
    elif rank.get(root_x) > rank.get(root_y):
        parent.set(root_y, root_x)
    else:
        # If ranks are equal, pick one as the new root and increase its rank by 1.
        parent.set(root_y, root_x)
        rank.set(root_x, rank.get(root_x) + 1)

    return True  # merge succeeded


# --- Kruskal's MST algorithm ---

def kruskal(num_nodes, edges):
    # Build a minimum spanning tree using Kruskal's algorithm.
    #
    # Parameters:
    #   num_nodes: total number of nodes (labeled 0 to num_nodes-1)
    #   edges: a list of [weight, node_a, node_b] for each edge in the graph
    #
    # Returns:
    #   mst_edges: LinkedList of edges in the MST, each as [weight, node_a, node_b]
    #   total_weight: sum of weights of all edges in the MST

    # Step 1: Sort all edges by weight (ascending).
    # We sort by the first element of each edge (the weight).
    # We use Python's sorted() built-in on the input list.
    # Note: sorted_edges is still a Python list; the edges input is a list.
    sorted_edges = sorted(edges, key=lambda e: e[0])

    # Step 2: Set up Union-Find for all nodes.
    parent, rank = make_set(num_nodes)

    # Step 3: Go through edges from smallest weight to largest.
    # For each edge, check if it connects two different components.
    # If yes, add it to the MST and merge the two components.
    # If no, skip it (adding it would create a cycle).
    mst_edges = LinkedList()
    total_weight = 0

    for edge in sorted_edges:
        weight = edge[0]
        node_a = edge[1]
        node_b = edge[2]

        # Check if node_a and node_b are in different groups.
        root_a = find(parent, node_a)
        root_b = find(parent, node_b)

        if root_a != root_b:
            # They are in different groups, so adding this edge won't create a cycle.
            mst_edges.append(edge)
            total_weight = total_weight + weight

            # Merge the two groups.
            union(parent, rank, root_a, root_b)

    return mst_edges, total_weight


# --- Example usage ---
# A simple graph with 4 nodes (0, 1, 2, 3) and 5 edges.
#
#       0 ---1--- 1
#       |        /|
#       4      3  2
#       |  /     |
#       2 ---5--- 3
#
# Edges: (0-1: weight 1), (0-2: weight 4), (1-2: weight 3), (1-3: weight 2), (2-3: weight 5)

if __name__ == "__main__":
    # Define the graph as a list of edges.
    # Each edge is [weight, node_a, node_b].
    num_nodes = 4
    edges = [
        [1, 0, 1],  # edge between node 0 and node 1 with weight 1
        [4, 0, 2],  # edge between node 0 and node 2 with weight 4
        [3, 1, 2],  # edge between node 1 and node 2 with weight 3
        [2, 1, 3],  # edge between node 1 and node 3 with weight 2
        [5, 2, 3],  # edge between node 2 and node 3 with weight 5
    ]

    # Run Kruskal's algorithm.
    mst_edges, total_weight = kruskal(num_nodes, edges)

    # Print the results.
    print("Edges in the Minimum Spanning Tree:")
    for edge in mst_edges:
        weight = edge[0]
        node_a = edge[1]
        node_b = edge[2]
        print("  Node {} -- Node {}  (weight {})".format(node_a, node_b, weight))

    print("Total MST weight:", total_weight)
