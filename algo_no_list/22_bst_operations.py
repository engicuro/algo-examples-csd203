"""
22_bst_operations.py - BST Operations: Min, Max, Successor, Predecessor, Validate

This file implements common BST operations:
  - Find minimum value (leftmost node)
  - Find maximum value (rightmost node)
  - Find the successor of a value (next larger value)
  - Find the predecessor of a value (next smaller value)
  - Validate that a tree is a valid BST

All implementations use simple loops and recursion — no fancy features.
"""


# ---------------------------------------------------------------------------
# Node class
# ---------------------------------------------------------------------------
class Node:
    """A node in a binary search tree."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# ---------------------------------------------------------------------------
# Insert (same as before — needed to build the tree)
# ---------------------------------------------------------------------------
def insert(node, value):
    """Insert a value into the BST."""
    if node is None:
        return Node(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    # If equal, do nothing (no duplicates)
    return node


# ---------------------------------------------------------------------------
# Find Minimum
# ---------------------------------------------------------------------------
def find_min(node):
    """Find the node with the smallest value in the BST.

    The smallest value is always the leftmost node.
    Keep going left until there is no left child.
    """
    if node is None:
        return None
    current = node
    while current.left is not None:
        current = current.left
    return current


# ---------------------------------------------------------------------------
# Find Maximum
# ---------------------------------------------------------------------------
def find_max(node):
    """Find the node with the largest value in the BST.

    The largest value is always the rightmost node.
    Keep going right until there is no right child.
    """
    if node is None:
        return None
    current = node
    while current.right is not None:
        current = current.right
    return current


# ---------------------------------------------------------------------------
# Find Successor
# ---------------------------------------------------------------------------
def find_successor(root, value):
    """Find the inorder successor of a given value in the BST.

    The inorder successor is the smallest value that is LARGER than the
    given value.  It is the "next value in sorted order".

    Two cases:
      Case A: The node has a right subtree.
        → The successor is the smallest value in the right subtree
          (go right once, then keep going left).
      Case B: The node has NO right subtree.
        → The successor is one of the ancestors.  We track the "last
          left turn" during the search for the node — that ancestor
          is the successor.
    """
    # First, find the node with the given value
    current = root
    successor = None  # this will hold our answer

    while current is not None:
        if value < current.value:
            # The current node is larger than our target — it could be
            # the successor, but there might be a smaller one further left.
            successor = current
            current = current.left
        elif value > current.value:
            # The current node is smaller than our target — successor
            # must be somewhere to the right.
            current = current.right
        else:
            # Found the node!
            # Case A: it has a right subtree — successor is the min of that subtree
            if current.right is not None:
                return find_min(current.right)
            # Case B: no right subtree — the successor is the one we tracked
            return successor

    # Value not found in the tree
    return None


# ---------------------------------------------------------------------------
# Find Predecessor
# ---------------------------------------------------------------------------
def find_predecessor(root, value):
    """Find the inorder predecessor of a given value in the BST.

    The inorder predecessor is the largest value that is SMALLER than the
    given value.  It is the "previous value in sorted order".

    Two cases:
      Case A: The node has a left subtree.
        → The predecessor is the largest value in the left subtree
          (go left once, then keep going right).
      Case B: The node has NO left subtree.
        → The predecessor is one of the ancestors.  We track the "last
          right turn" during the search for the node — that ancestor
          is the predecessor.
    """
    current = root
    predecessor = None  # this will hold our answer

    while current is not None:
        if value > current.value:
            # The current node is smaller than our target — it could be
            # the predecessor, but there might be a larger one further right.
            predecessor = current
            current = current.right
        elif value < current.value:
            # The current node is larger than our target — predecessor
            # must be somewhere to the left.
            current = current.left
        else:
            # Found the node!
            # Case A: it has a left subtree — predecessor is the max of that subtree
            if current.left is not None:
                return find_max(current.left)
            # Case B: no left subtree — the predecessor is the one we tracked
            return predecessor

    # Value not found in the tree
    return None


# ---------------------------------------------------------------------------
# Validate BST
# ---------------------------------------------------------------------------
def is_valid_bst(node, min_val=None, max_val=None):
    """Check whether a binary tree is a valid Binary Search Tree.

    The idea: every node must be within a valid range.
      - The root can be any value (no limits).
      - When we go LEFT, the node's value must be less than its parent.
        So we update the MAX allowed value.
      - When we go RIGHT, the node's value must be greater than its parent.
        So we update the MIN allowed value.

    Args:
        node:    the current node being checked.
        min_val: the minimum value this node is allowed to have (exclusive).
        max_val: the maximum value this node is allowed to have (exclusive).

    Returns True if the subtree rooted at `node` is a valid BST.
    """
    # An empty tree is a valid BST
    if node is None:
        return True

    # Check the current node's value against the allowed range
    if min_val is not None and node.value <= min_val:
        # Value is too small — violates the BST property
        return False
    if max_val is not None and node.value >= max_val:
        # Value is too large — violates the BST property
        return False

    # Recursively check left and right subtrees with updated ranges
    # Left subtree: all values must be < node.value, so max_val = node.value
    # Right subtree: all values must be > node.value, so min_val = node.value
    return (is_valid_bst(node.left, min_val, node.value) and
            is_valid_bst(node.right, node.value, max_val))


# ---------------------------------------------------------------------------
# Inorder traversal (for display)
# ---------------------------------------------------------------------------
def inorder(node):
    """Inorder traversal — prints values in sorted order for a valid BST."""
    if node is None:
        return
    inorder(node.left)
    print(node.value, end=" ")
    inorder(node.right)


# ---------------------------------------------------------------------------
# Pretty print helper
# ---------------------------------------------------------------------------
def print_tree(node, indent="", is_right=False):
    """Print the tree rotated 90 degrees for visualization."""
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
    print("Chapter 22 — BST Operations")
    print("=" * 60)

    # Build a BST
    #
    #         50
    #        /  \
    #      30    70
    #     / \   / \
    #   20  40 60  80
    #
    root = None
    for val in (50, 30, 70, 20, 40, 60, 80):
        root = insert(root, val)

    print("\nTree structure:")
    print_tree(root)

    # Find minimum and maximum
    print("\n--- Min and Max ---")
    min_node = find_min(root)
    max_node = find_max(root)
    print("  Minimum value: " + str(min_node.value))  # expected: 20
    print("  Maximum value: " + str(max_node.value))  # expected: 80

    # Find successor
    print("\n--- Successor (next larger value) ---")
    for val in (40, 90, 20, 65):
        succ = find_successor(root, val)
        if succ is not None:
            print("  Successor of " + str(val) + " is " + str(succ.value))
        else:
            print("  Successor of " + str(val) + " is None (no larger value)")

    # Find predecessor
    print("\n--- Predecessor (next smaller value) ---")
    for val in (40, 90, 20, 65):
        pred = find_predecessor(root, val)
        if pred is not None:
            print("  Predecessor of " + str(val) + " is " + str(pred.value))
        else:
            print("  Predecessor of " + str(val) + " is None (no smaller value)")

    # Validate BST
    print("\n--- Validate BST ---")
    print("  Is valid BST? " + str(is_valid_bst(root)))  # expected: True

    # Create an INVALID BST by manually breaking the rule
    # (make a left child larger than its parent)
    print("\n  Creating an invalid BST (left child 55 > parent 50)...")
    bad_root = Node(50)
    bad_root.left = Node(55)  # INVALID: 55 > 50
    bad_root.right = Node(70)
    print("  Is valid BST? " + str(is_valid_bst(bad_root)))  # expected: False

    # Show inorder traversal of valid BST (should be sorted)
    print("\nInorder traversal of valid BST (sorted order):")
    inorder(root)
    print()
