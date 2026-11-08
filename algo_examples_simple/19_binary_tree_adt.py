"""
19_binary_tree_adt.py - Binary Tree ADT (Insert, Search, Delete)

A Binary Tree ADT (Abstract Data Type) provides basic operations:
  - insert(value):  add a new node to the tree
  - search(value):  check if a value exists in the tree
  - delete(value):  remove a node with the given value

This file uses a simple binary tree (NOT a binary search tree),
so insertion is done level-by-level (left to right) to keep the
tree complete.  This is a common approach for building a general
binary tree from scratch.

Key ideas:
  - Insert: find the first empty spot using level-order traversal.
  - Search: check every node (linear scan) since there is no ordering.
  - Delete: replace the deleted node's value with the deepest
            rightmost node's value, then remove that deepest node.
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
# Binary Tree ADT
# ---------------------------------------------------------------------------
class BinaryTree:
    """A simple binary tree with insert, search, and delete operations."""

    def __init__(self):
        self.root = None

    # ------------------------------------------------------------------
    # Insert: add a value at the first available position (level order)
    # ------------------------------------------------------------------
    def insert(self, value):
        """Insert a new node with `value` into the tree.

        We fill the tree level by level, left to right, so the tree
        stays "complete".  This uses a queue (list used as a queue).

        Steps:
          1. If the tree is empty, the new node becomes the root.
          2. Otherwise, walk the tree level by level.
          3. The first node that is missing a left or right child
             gets the new node attached there.
        """
        new_node = Node(value)

        # Special case: empty tree — new node is the root
        if self.root is None:
            self.root = new_node
            return

        # Use a simple list as a queue for level-order traversal
        queue = [self.root]
        front = 0  # index of the next element to process

        while front < len(queue):
            current = queue[front]
            front = front + 1

            # Try to insert as the left child
            if current.left is None:
                current.left = new_node
                return
            else:
                queue.append(current.left)

            # Try to insert as the right child
            if current.right is None:
                current.right = new_node
                return
            else:
                queue.append(current.right)

    # ------------------------------------------------------------------
    # Search: check if a value exists in the tree
    # ------------------------------------------------------------------
    def search(self, value):
        """Search for `value` in the tree.

        Returns True if found, False otherwise.
        Since this is a general binary tree (no ordering), we must
        check every node — we use level-order traversal.
        """
        if self.root is None:
            return False

        queue = [self.root]
        front = 0

        while front < len(queue):
            current = queue[front]
            front = front + 1

            # Check this node
            if current.value == value:
                return True

            # Add children to the queue for later checking
            if current.left is not None:
                queue.append(current.left)
            if current.right is not None:
                queue.append(current.right)

        # We checked every node and did not find the value
        return False

    # ------------------------------------------------------------------
    # Delete: remove a node with the given value
    # ------------------------------------------------------------------
    def delete(self, value):
        """Delete the node containing `value` from the tree.

        Strategy:
          1. Find the node to delete using level-order traversal.
          2. Find the deepest, rightmost node in the tree.
          3. Copy the deepest node's value into the node to delete.
          4. Remove the deepest node (it is now a duplicate).

        This keeps the tree structure valid (still complete).
        """
        if self.root is None:
            print("  Tree is empty — nothing to delete.")
            return

        # If the tree has only one node (the root)
        if self.root.left is None and self.root.right is None:
            if self.root.value == value:
                self.root = None
                print("  Deleted the only node (root). Tree is now empty.")
            else:
                print("  Value not found in tree.")
            return

        # First pass: find the node to delete and the deepest node
        node_to_delete = None
        deepest_node = None
        deepest_parent = None
        deepest_is_left = False

        queue = [self.root]
        front = 0

        while front < len(queue):
            current = queue[front]
            front = front + 1

            # Check if this is the node we want to delete
            if current.value == value and node_to_delete is None:
                node_to_delete = current

            # Track children and find the deepest node
            if current.left is not None:
                queue.append(current.left)
                deepest_parent = current
                deepest_is_left = True
            if current.right is not None:
                queue.append(current.right)
                deepest_parent = current
                deepest_is_left = False

        # If value was not found
        if node_to_delete is None:
            print("  Value not found in tree — nothing deleted.")
            return

        # The last element in the queue is the deepest, rightmost node
        deepest_node = queue[-1]

        # Copy the deepest node's value into the node to delete
        node_to_delete.value = deepest_node.value

        # Remove the deepest node from its parent
        if deepest_is_left:
            deepest_parent.left = None
        else:
            deepest_parent.right = None

        print("  Deleted value " + str(value) + ".")

    # ------------------------------------------------------------------
    # Helper: print tree structure
    # ------------------------------------------------------------------
    def print_tree(self, node, indent="", is_right=False):
        """Print the tree rotated 90 degrees for visualization."""
        if node is None:
            return
        self.print_tree(node.right, indent + ("    " if is_right else "│   "), True)
        connector = "└── " if is_right else "┌── "
        print(indent + connector + str(node.value))
        self.print_tree(node.left, indent + ("    " if not is_right else "│   "), False)

    # ------------------------------------------------------------------
    # Helper: inorder traversal (for display)
    # ------------------------------------------------------------------
    def inorder(self, node):
        """Inorder traversal for display purposes."""
        if node is None:
            return
        self.inorder(node.left)
        print(node.value, end=" ")
        self.inorder(node.right)


# ---------------------------------------------------------------------------
# Main block — simple example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Chapter 19 — Binary Tree ADT")
    print("=" * 60)

    tree = BinaryTree()

    # Insert values
    print("\n--- Inserting values: 1, 2, 3, 4, 5, 6 ---")
    for val in [1, 2, 3, 4, 5, 6]:
        tree.insert(val)

    print("Tree structure:")
    tree.print_tree(tree.root)

    print("\nInorder traversal:")
    tree.inorder(tree.root)
    print()

    # Search
    print("\n--- Search ---")
    for val in [3, 7, 1, 9]:
        found = tree.search(val)
        print("  search(" + str(val) + ") -> " + str(found))

    # Delete a leaf node
    print("\n--- Delete leaf node (4) ---")
    tree.delete(4)
    print("Inorder after deleting 4:")
    tree.inorder(tree.root)
    print()

    # Delete a node with one child
    print("\n--- Delete node with one child (5) ---")
    tree.delete(5)
    print("Inorder after deleting 5:")
    tree.inorder(tree.root)
    print()

    # Delete a node with two children
    print("\n--- Delete node with two children (2) ---")
    tree.delete(2)
    print("Inorder after deleting 2:")
    tree.inorder(tree.root)
    print()

    print("\nFinal tree structure:")
    tree.print_tree(tree.root)
