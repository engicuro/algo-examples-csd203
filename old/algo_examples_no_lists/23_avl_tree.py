"""
23_avl_tree.py - AVL Tree Basics

An AVL tree is a self-balancing binary search tree.  After every insert,
the tree checks the balance factor of each node and performs rotations
to keep the tree balanced.

Balance factor = height(left subtree) - height(right subtree)
A node is balanced if its balance factor is -1, 0, or 1.
If the balance factor becomes 2 or -2, we rotate to rebalance.

Four rotation cases:
  1. Left-Left (LL):   right rotate
  2. Right-Right (RR): left rotate
  3. Left-Right (LR):  left rotate left child, then right rotate node
  4. Right-Left (RL):  right rotate right child, then left rotate node

Topics covered:
  - Node with height tracking
  - Left rotation and right rotation
  - Insert with rebalancing
  - Inorder traversal (shows sorted order)
"""

import math


# ---------------------------------------------------------------------------
# Node class — each node stores its height for balance calculations
# ---------------------------------------------------------------------------
class Node:
    """A node in an AVL tree.

    In addition to value, left, and right (like a regular BST node),
    each node stores its height so we can quickly compute balance factors.
    """

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # new node starts with height 1 (a leaf)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def get_height(node):
    """Return the height of a node.  A None node has height 0."""
    if node is None:
        return 0
    return node.height


def get_balance(node):
    """Return the balance factor of a node.

    Balance factor = height(left subtree) - height(right subtree)
    A balanced node has a balance factor of -1, 0, or 1.
    """
    if node is None:
        return 0
    return get_height(node.left) - get_height(node.right)


def update_height(node):
    """Recalculate and store the height of a node based on its children.

    Height = 1 + max(height of left child, height of right child).
    """
    if node is None:
        return
    left_height = get_height(node.left)
    right_height = get_height(node.right)
    if left_height > right_height:
        node.height = 1 + left_height
    else:
        node.height = 1 + right_height


# ---------------------------------------------------------------------------
# Rotations
# ---------------------------------------------------------------------------
def right_rotate(y):
    """Right rotation around node `y`.

    Before:          After:
        y              x
       / \\            / \\
      x   T3   →    T1   y
     / \\                 / \\
    T1  T2             T2   T3

    This fixes a Left-Left (LL) imbalance.
    """
    x = y.left
    t2 = x.right

    # Perform rotation
    x.right = y
    y.left = t2

    # Update heights (y is now below x, so update y first)
    update_height(y)
    update_height(x)

    # x is the new root of this subtree
    return x


def left_rotate(x):
    """Left rotation around node `x`.

    Before:          After:
      x                y
     / \\              / \\
    T1   y    →     x   T3
        / \\        / \\
       T2  T3    T1   T2

    This fixes a Right-Right (RR) imbalance.
    """
    y = x.right
    t2 = y.left

    # Perform rotation
    y.left = x
    x.right = t2

    # Update heights (x is now below y, so update x first)
    update_height(x)
    update_height(y)

    # y is the new root of this subtree
    return y


# ---------------------------------------------------------------------------
# Insert with rebalancing
# ---------------------------------------------------------------------------
def insert(node, value):
    """Insert a value into the AVL tree and rebalance if needed.

    Steps:
      1. Perform a standard BST insert.
      2. Update the height of the current node.
      3. Compute the balance factor.
      4. If unbalanced, determine which of the 4 cases it is and
         perform the appropriate rotation(s).

    The four imbalance cases:
      LL: balance > 1 AND value < node.left.value  → right rotate
      RR: balance < -1 AND value > node.right.value → left rotate
      LR: balance > 1 AND value > node.left.value   → left rotate left child, then right rotate
      RL: balance < -1 AND value < node.right.value → right rotate right child, then left rotate
    """
    # Step 1: Standard BST insert
    if node is None:
        return Node(value)

    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    else:
        # Duplicate values are not allowed in this BST
        return node

    # Step 2: Update height of this ancestor node
    update_height(node)

    # Step 3: Get the balance factor
    balance = get_balance(node)

    # Step 4: Rebalance if needed

    # Case 1: Left-Left (LL) — the left subtree is too tall
    # and the new value was inserted into the left subtree's left side
    if balance > 1 and value < node.left.value:
        return right_rotate(node)

    # Case 2: Right-Right (RR) — the right subtree is too tall
    # and the new value was inserted into the right subtree's right side
    if balance < -1 and value > node.right.value:
        return left_rotate(node)

    # Case 3: Left-Right (LR) — the left subtree is too tall
    # but the new value was inserted into the left subtree's right side
    if balance > 1 and value > node.left.value:
        node.left = left_rotate(node.left)
        return right_rotate(node)

    # Case 4: Right-Left (RL) — the right subtree is too tall
    # but the new value was inserted into the right subtree's left side
    if balance < -1 and value < node.right.value:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    # No rebalancing needed — return the unchanged node
    return node


# ---------------------------------------------------------------------------
# Inorder Traversal
# ---------------------------------------------------------------------------
def inorder(node):
    """Inorder traversal — prints values in sorted order."""
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
    print("Chapter 23 — AVL Tree")
    print("=" * 60)

    # Insert values that would create an unbalanced BST if inserted
    # in sorted order (1, 2, 3, 4, 5, 6, 7 would be a linked list).
    # The AVL tree will rotate to stay balanced.
    #
    # We insert in this order: 10, 20, 30, 40, 50, 25
    #
    # After inserting 10, 20, 30 (sorted), the RR case triggers
    # a left rotation at 10, making 20 the root.
    #
    # After inserting 40, 50, another RR case triggers a left rotation.
    #
    # Inserting 25 triggers an RL case (right-left imbalance).
    #
    root = None
    values = [10, 20, 30, 40, 50, 25]
    print("\nInserting values: " + str(values))
    for val in values:
        root = insert(root, val)
        print("  After inserting " + str(val) + ":")
        print_tree(root)
        print()

    # Final tree
    print("Final AVL tree structure:")
    print_tree(root)

    # Inorder traversal (should print sorted order)
    print("\nInorder traversal (sorted order):")
    inorder(root)
    print()  # expected: 10 20 25 30 40 50

    # Show heights and balance factors
    print("\nNode heights and balance factors:")
    print("  Node 10: height=" + str(get_height(root.left.left)) +
          ", balance=" + str(get_balance(root.left.left)))
    print("  Node 25: height=" + str(get_height(root.left.right)) +
          ", balance=" + str(get_balance(root.left.right)))
    print("  Node 20: height=" + str(get_height(root.left)) +
          ", balance=" + str(get_balance(root.left)))
    print("  Node 40: height=" + str(get_height(root.right.left)) +
          ", balance=" + str(get_balance(root.right.left)))
    print("  Node 50: height=" + str(get_height(root.right.right)) +
          ", balance=" + str(get_balance(root.right.right)))
    print("  Node 30: height=" + str(get_height(root)) +
          ", balance=" + str(get_balance(root)))
