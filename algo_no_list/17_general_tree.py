"""
17_general_tree.py - General Tree (N-ary Tree) Basics

A general tree is a tree where each node can have any number of children.
We represent each node with a value and a tuple of child nodes.

Topics covered:
  - Creating a node
  - Adding a child to a node
  - Preorder traversal (visit root, then children left to right)
  - Postorder traversal (visit children left to right, then root)
  - Height of the tree (longest path from root to a leaf)
  - Size of the tree (total number of nodes)
"""

import math


# ---------------------------------------------------------------------------
# Node class
# ---------------------------------------------------------------------------
class Node:
    """A node in a general tree.

    Each node stores a value and a tuple of its children.
    A leaf node has an empty children tuple.
    """

    def __init__(self, value):
        self.value = value
        self.children = ()  # tuple of child Node objects


# ---------------------------------------------------------------------------
# Basic operations
# ---------------------------------------------------------------------------
def add_child(parent, child_value):
    """Create a new node with child_value and add it as a child of parent.

    Returns the newly created child node so the caller can keep a reference.
    """
    new_node = Node(child_value)
    parent.children = parent.children + (new_node,)
    return new_node


def size(node):
    """Count the total number of nodes in the tree rooted at `node`.

    Base case: if node is None, return 0.
    Recursive case: 1 (for this node) + size of each child subtree.
    """
    if node is None:
        return 0
    count = 1  # count this node itself
    for child in node.children:
        count = count + size(child)
    return count


def height(node):
    """Return the height of the tree rooted at `node`.

    Height = the number of edges on the longest path from node down to a leaf.
    A leaf node has height 0.  An empty tree (None) has height -1.
    """
    if node is None:
        return -1
    if len(node.children) == 0:
        # This is a leaf node — no children, so height is 0.
        return 0
    # Find the maximum height among all children, then add 1 for the edge
    # from this node down to that child.
    max_child_height = 0
    for child in node.children:
        child_height = height(child)
        if child_height > max_child_height:
            max_child_height = child_height
    return 1 + max_child_height


# ---------------------------------------------------------------------------
# Traversals
# ---------------------------------------------------------------------------
def preorder(node):
    """Preorder traversal: visit the current node FIRST, then visit each child.

    For a general tree this means:
      1. Process (print) the current node's value.
      2. Recursively preorder-traverse each child from left to right.
    """
    if node is None:
        return
    # Step 1: process this node
    print(node.value, end=" ")
    # Step 2: recurse into each child
    for child in node.children:
        preorder(child)


def postorder(node):
    """Postorder traversal: visit all children FIRST, then visit the current node.

    For a general tree this means:
      1. Recursively postorder-traverse each child from left to right.
      2. Process (print) the current node's value.
    """
    if node is None:
        return
    # Step 1: recurse into each child first
    for child in node.children:
        postorder(child)
    # Step 2: process this node after all its children are done
    print(node.value, end=" ")


# ---------------------------------------------------------------------------
# Pretty print helper — shows tree structure with indentation
# ---------------------------------------------------------------------------
def print_tree(node, prefix="", is_last=True):
    """Print the tree structure with indentation so you can see the shape.

    prefix  : the string printed before the current node's line
    is_last : True if this node is the last child of its parent
    """
    if node is None:
        return
    # Choose a connector symbol
    if prefix == "":
        # Root node — no connector
        print(node.value)
    else:
        connector = "└── " if is_last else "├── "
        print(prefix + connector + str(node.value))

    # Build the prefix for children
    if prefix == "":
        child_prefix = ""
    else:
        child_prefix = prefix + ("    " if is_last else "│   ")

    # Print each child
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        # Last child gets the "last" connector
        is_this_last = (i == child_count - 1)
        print_tree(child, child_prefix, is_this_last)


# ---------------------------------------------------------------------------
# Main block — simple example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Chapter 17 — General Tree (N-ary Tree)")
    print("=" * 60)

    # Build a sample tree:
    #
    #           A
    #        /  |  \
    #       B   C   D
    #      / \      |
    #     E   F     G
    #
    root = Node("A")
    b = add_child(root, "B")
    c = add_child(root, "C")
    d = add_child(root, "D")
    add_child(b, "E")
    add_child(b, "F")
    add_child(d, "G")

    # Show the tree structure
    print("\nTree structure:")
    print_tree(root)

    # Size
    print(f"\nSize (total nodes): {size(root)}")  # expected: 7

    # Height
    print(f"Height (longest root-to-leaf edges): {height(root)}")  # expected: 2

    # Traversals
    print("\nPreorder traversal  (root first, then children):")
    preorder(root)
    print()  # newline

    print("Postorder traversal (children first, then root):")
    postorder(root)
    print()  # newline

    # Verify size and height on a subtree
    print(f"\nSize of subtree rooted at 'B': {size(b)}")  # expected: 3 (B, E, F)
    print(f"Height of subtree rooted at 'B': {height(b)}")  # expected: 1
