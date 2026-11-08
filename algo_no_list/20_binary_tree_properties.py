"""
20_binary_tree_properties.py - Binary Tree Properties

This file computes common properties of a binary tree using simple
recursive functions:
  - Count all nodes
  - Count leaf nodes (nodes with no children)
  - Count internal nodes (nodes with at least one child)
  - Compute the tree diameter (longest path between any two nodes)

All functions use basic recursion — no fancy Python features.
"""


# ---------------------------------------------------------------------------
# Node class
# ---------------------------------------------------------------------------
class Node:
    """A node in a binary tree."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------
def count_nodes(node):
    """Count the total number of nodes in the tree.

    Base case: if node is None, return 0.
    Recursive case: 1 + count of left subtree + count of right subtree.
    """
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


def count_leaves(node):
    """Count the number of leaf nodes (nodes with no children).

    A leaf is a node where both left and right are None.
    """
    if node is None:
        return 0
    if node.left is None and node.right is None:
        # This is a leaf node
        return 1
    # Not a leaf — count leaves in both subtrees
    return count_leaves(node.left) + count_leaves(node.right)


def count_internal(node):
    """Count the number of internal nodes (nodes with at least one child).

    An internal node has at least one non-None child.
    """
    if node is None:
        return 0
    if node.left is None and node.right is None:
        # This is a leaf, not internal
        return 0
    # This node is internal — count it plus internal nodes in both subtrees
    return 1 + count_internal(node.left) + count_internal(node.right)


def tree_height(node):
    """Return the height of the tree (number of edges on the longest root-to-leaf path).

    Used as a helper for the diameter calculation.
    """
    if node is None:
        return -1
    left_height = tree_height(node.left)
    right_height = tree_height(node.right)
    # Height is 1 + the taller child's height
    if left_height > right_height:
        return 1 + left_height
    else:
        return 1 + right_height


def tree_diameter(node):
    """Compute the diameter of the tree.

    The diameter is the number of edges on the longest path between
    any two nodes in the tree.  This path may or may not pass through
    the root.

    For each node, the longest path through that node is:
      left_height + right_height + 2
    (the two edges from the node down to the deepest leaf in each subtree).

    We check this at every node and keep the maximum.
    """
    if node is None:
        return -1  # empty tree has diameter -1 (no edges)

    # Diameter of left subtree (best path entirely within left)
    left_diameter = tree_diameter(node.left)
    # Diameter of right subtree (best path entirely within right)
    right_diameter = tree_diameter(node.right)

    # Longest path that passes through this node
    path_through_root = tree_height(node.left) + tree_height(node.right) + 2

    # The diameter is the maximum of these three possibilities
    best = path_through_root
    if left_diameter > best:
        best = left_diameter
    if right_diameter > best:
        best = right_diameter

    return best


# ---------------------------------------------------------------------------
# Pretty print helper
# ---------------------------------------------------------------------------
def print_tree(node, indent="", is_right=False):
    """Print the binary tree rotated 90 degrees."""
    if node is None:
        return
    print_tree(node.right, indent + ("    " if is_right else "│   "), True)
    connector = "└── " if is_right else "┌── "
    print(indent + connector + str(node.value))
    print_tree(node.left, indent + ("    " if not is_right else "│   "), False)


# ---------------------------------------------------------------------------
# Main block — simple example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Chapter 20 — Binary Tree Properties")
    print("=" * 60)

    # Build a sample binary tree:
    #
    #         1
    #        / \
    #       2   3
    #      / \
    #     4   5
    #        /
    #       6
    #
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.left.right.left = Node(6)

    print("\nTree structure:")
    print_tree(root)

    # Count nodes
    print("\nTotal nodes:     " + str(count_nodes(root)))  # expected: 6

    # Count leaves
    print("Leaf nodes:      " + str(count_leaves(root)))    # expected: 3 (nodes 3, 4, 6)

    # Count internal nodes
    print("Internal nodes:  " + str(count_internal(root)))  # expected: 3 (nodes 1, 2, 5)

    # Tree height
    print("Tree height:     " + str(tree_height(root)))     # expected: 3

    # Tree diameter
    # The longest path is from node 4 to node 3: 4-2-1-3 (3 edges)
    # or from node 6 to node 3: 6-5-2-1-3 (4 edges)  <-- this is longer
    print("Tree diameter:   " + str(tree_diameter(root)))   # expected: 4
