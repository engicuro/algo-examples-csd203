"""
21_bst.py - Binary Search Tree (BST) Basics

A Binary Search Tree is a binary tree with this ordering rule:
  - Every value in the left subtree is LESS than the node's value.
  - Every value in the right subtree is GREATER than the node's value.
  - No duplicate values (for simplicity).

Topics covered:
  - Insert a value (follow the ordering rule to find the right spot)
  - Search for a value (use ordering to skip half the tree each step)
  - Delete a node (three cases: leaf, one child, two children)
  - Inorder traversal (visits values in sorted order)

All operations are explained step by step with comments.
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
# Insert
# ---------------------------------------------------------------------------
def insert(node, value):
    """Insert a value into the BST rooted at `node`.

    Steps:
      1. If the current spot is empty (node is None), create a new node here.
      2. If the value is less than the current node's value, go LEFT.
      3. If the value is greater than the current node's value, go RIGHT.
      4. If the value equals the current node's value, do nothing (no duplicates).

    We use recursion to repeat these steps at each level.
    """
    # Base case: found an empty spot — place the new node here
    if node is None:
        return Node(value)

    # If value is less, go to the left subtree
    if value < node.value:
        node.left = insert(node.left, value)

    # If value is greater, go to the right subtree
    elif value > node.value:
        node.right = insert(node.right, value)

    # If value is equal, we do nothing (BSTs typically don't allow duplicates)
    # else: pass  (uncomment if you want to handle duplicates)

    return node


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------
def search(node, value):
    """Search for a value in the BST.

    Returns True if found, False otherwise.

    Steps:
      1. If we reached an empty spot, the value is not in the tree.
      2. If the value matches the current node, we found it.
      3. If the value is less, search the left subtree.
      4. If the value is greater, search the right subtree.
    """
    # Base case: reached an empty spot — value not found
    if node is None:
        return False

    # Found it!
    if value == node.value:
        return True

    # Value is smaller — search left
    if value < node.value:
        return search(node.left, value)

    # Value is larger — search right
    return search(node.right, value)


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def delete(node, value):
    """Delete a node with the given value from the BST.

    There are three cases to handle:

    Case 1 — Leaf node (no children):
      Simply remove it by returning None to the parent.

    Case 2 — One child:
      Replace the node with its single child.

    Case 3 — Two children:
      1. Find the INORDER SUCCESSOR: the smallest value in the right subtree.
         (This is the next larger value after the one we are deleting.)
      2. Copy the successor's value into the current node.
      3. Delete the successor from the right subtree (it will be Case 1 or 2).

    Returns the (possibly updated) root of this subtree.
    """
    # Base case: value not found in this subtree
    if node is None:
        return None

    # Navigate to find the node to delete
    if value < node.value:
        # Value is in the left subtree
        node.left = delete(node.left, value)
    elif value > node.value:
        # Value is in the right subtree
        node.right = delete(node.right, value)
    else:
        # Found the node to delete — handle the three cases

        # --- Case 1: Leaf node (no children) ---
        if node.left is None and node.right is None:
            # Just remove this node by returning None to the parent
            return None

        # --- Case 2: One child ---
        # If there is no left child, replace with the right child
        if node.left is None:
            return node.right
        # If there is no right child, replace with the left child
        if node.right is None:
            return node.left

        # --- Case 3: Two children ---
        # Step 1: Find the inorder successor (smallest in the right subtree)
        successor = find_min(node.right)

        # Step 2: Copy the successor's value into this node
        node.value = successor.value

        # Step 3: Delete the successor from the right subtree
        # (The successor has no left child by definition, so this is Case 1 or 2)
        node.right = delete(node.right, successor.value)

    return node


def find_min(node):
    """Find the node with the smallest value in a BST.

    The smallest value is always the leftmost node.
    """
    current = node
    while current.left is not None:
        current = current.left
    return current


# ---------------------------------------------------------------------------
# Inorder Traversal
# ---------------------------------------------------------------------------
def inorder(node):
    """Inorder traversal of a BST visits nodes in sorted (ascending) order.

    Steps:
      1. Visit all nodes in the left subtree (smaller values).
      2. Visit the current node.
      3. Visit all nodes in the right subtree (larger values).
    """
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
    print("Chapter 21 — Binary Search Tree (BST)")
    print("=" * 60)

    # Build a BST by inserting values one at a time
    #
    # Inserting: 50, 30, 70, 20, 40, 60, 80
    #
    # Resulting tree:
    #         50
    #        /  \
    #      30    70
    #     / \   / \
    #   20  40 60  80
    #
    root = None
    values_to_insert = [50, 30, 70, 20, 40, 60, 80]
    print("\nInserting values: " + str(values_to_insert))
    for val in values_to_insert:
        root = insert(root, val)

    print("\nTree structure:")
    print_tree(root)

    # Inorder traversal (should print values in sorted order)
    print("\nInorder traversal (sorted order):")
    inorder(root)
    print()  # expected: 20 30 40 50 60 70 80

    # Search
    print("\n--- Search ---")
    for val in [40, 90, 20, 65]:
        found = search(root, val)
        print("  search(" + str(val) + ") -> " + str(found))

    # Delete a leaf node (20)
    print("\n--- Delete leaf node (20) ---")
    root = delete(root, 20)
    print("Inorder after deleting 20:")
    inorder(root)
    print()
    print_tree(root)

    # Delete a node with one child (70, which has only left child 60)
    print("\n--- Delete node with one child (70) ---")
    root = delete(root, 70)
    print("Inorder after deleting 70:")
    inorder(root)
    print()
    print_tree(root)

    # Delete a node with two children (50, the root)
    print("\n--- Delete node with two children (50, the root) ---")
    root = delete(root, 50)
    print("Inorder after deleting 50:")
    inorder(root)
    print()
    print_tree(root)
