"""
21_bst.py - Binary Search Tree (BST) in Python

A Binary Search Tree is a node-based binary tree data structure where each
node has at most two children, and the following invariant holds:
  - All values in the left subtree are less than the node's value.
  - All values in the right subtree are greater than the node's value.
  - Both left and right subtrees are also BSTs.

Operations and their average / worst-case time complexities:
  - Insert:  O(log n) average, O(n) worst (degenerate tree)
  - Search:  O(log n) average, O(n) worst
  - Delete:  O(log n) average, O(n) worst
  - Inorder traversal: O(n) — visits every node exactly once

Topics covered:
  - Node definition
  - Insert (iterative)
  - Search (iterative)
  - Delete (handling all three cases: leaf, one child, two children)
  - Inorder traversal (recursive, yields sorted order)
"""

from __future__ import annotations

from typing import List, Optional


class Node:
    """A single node in a Binary Search Tree."""

    def __init__(self, value: int) -> None:
        self.value: int = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.value})"


class BST:
    """Binary Search Tree with insert, search, delete, and inorder traversal."""

    def __init__(self) -> None:
        self.root: Optional[Node] = None

    # ------------------------------------------------------------------ #
    #  Insert
    # ------------------------------------------------------------------ #
    def insert(self, value: int) -> None:
        """Insert a value into the BST.

        Iteratively walks down the tree to find the correct leaf position.
        Average O(log n); worst O(n) for a degenerate (sorted-input) tree.
        """
        new_node = Node(value)

        # Empty tree — the new node becomes the root
        if self.root is None:
            self.root = new_node
            return

        # Walk down the tree to find the insertion point
        current: Node = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right
            else:
                # Duplicate value — BSTs typically do not store duplicates
                return

    # ------------------------------------------------------------------ #
    #  Search
    # ------------------------------------------------------------------ #
    def search(self, value: int) -> bool:
        """Search for a value in the BST.

        Iteratively compares the target with the current node and descends
        left or right accordingly.
        Average O(log n); worst O(n).
        """
        current = self.root
        while current is not None:
            if value == current.value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return False

    # ------------------------------------------------------------------ #
    #  Delete
    # ------------------------------------------------------------------ #
    def delete(self, value: int) -> None:
        """Delete a value from the BST.

        Handles three cases for the node to be deleted:
          Case 1 — Leaf node (no children):
              Simply remove the node by setting the parent's pointer to None.
          Case 2 — Node with one child:
              Replace the node with its single child, bypassing the node.
          Case 3 — Node with two children:
              Find the inorder successor (smallest value in the right subtree),
              copy its value into the node to be deleted, then delete the
              inorder successor (which will always be Case 1 or Case 2).
        Average O(log n); worst O(n).
        """
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node: Optional[Node], value: int) -> Optional[Node]:
        """Recursively delete value from the subtree rooted at node."""
        if node is None:
            return None  # Value not found — nothing to do

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Found the node to delete — handle the three cases

            # Case 1: Leaf node (no children) — simply remove it
            if node.left is None and node.right is None:
                return None

            # Case 2: Node with exactly one child — bypass the node
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Case 3: Node with two children
            #   1. Find the inorder successor (min value in right subtree)
            #   2. Copy the successor's value into this node
            #   3. Delete the successor from the right subtree
            successor = self._find_min(node.right)
            node.value = successor.value
            node.right = self._delete_recursive(node.right, successor.value)

        return node

    def _find_min(self, node: Node) -> Node:
        """Find the node with the minimum value in a subtree.

        The minimum is always the leftmost node. O(h) where h is the height.
        """
        current = node
        while current.left is not None:
            current = current.left
        return current

    # ------------------------------------------------------------------ #
    #  Inorder Traversal
    # ------------------------------------------------------------------ #
    def inorder(self) -> List[int]:
        """Return a list of values from an inorder traversal.

        Inorder traversal of a BST visits nodes in ascending sorted order.
        Time complexity: O(n) — every node is visited exactly once.
        Space complexity: O(h) for the recursion stack, where h is the height.
        """
        result: List[int] = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: Optional[Node], result: List[int]) -> None:
        """Helper: recursively traverse left, visit, then right."""
        if node is None:
            return
        self._inorder_recursive(node.left, result)
        result.append(node.value)
        self._inorder_recursive(node.right, result)


def main() -> None:
    """Demonstrate BST operations: insert, search, delete (all three cases), and inorder traversal."""
    print("=" * 60)
    print("Chapter 21 — Binary Search Tree")
    print("=" * 60)

    bst = BST()

    # --- Build the tree ---
    values = [50, 30, 70, 20, 40, 60, 80]
    print(f"\nInserting values: {values}")
    for v in values:
        bst.insert(v)

    print(f"Inorder traversal (sorted): {bst.inorder()}")

    # --- Search demonstrations ---
    print("\n--- Search ---")
    for target in [40, 99]:
        found = bst.search(target)
        print(f"  search({target}) -> {found}")

    # --- Delete Case 1: Leaf node (20 has no children) ---
    print("\n--- Delete Case 1: Leaf node (20) ---")
    print(f"Before delete: {bst.inorder()}")
    bst.delete(20)
    print(f"After  delete: {bst.inorder()}")

    # --- Delete Case 2: Node with one child (30 has only right child 40) ---
    print("\n--- Delete Case 2: Node with one child (30) ---")
    print(f"Before delete: {bst.inorder()}")
    bst.delete(30)
    print(f"After  delete: {bst.inorder()}")

    # --- Delete Case 3: Node with two children (50 is the root with two children) ---
    print("\n--- Delete Case 3: Node with two children (50, the root) ---")
    print(f"Before delete: {bst.inorder()}")
    bst.delete(50)
    print(f"After  delete: {bst.inorder()}")

    # --- Final tree state ---
    print(f"\nFinal inorder traversal: {bst.inorder()}")


if __name__ == "__main__":
    main()
