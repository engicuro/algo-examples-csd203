"""
19_binary_tree_adt.py - Binary Tree ADT Operations in Python

A binary tree is a hierarchical data structure where each node has at most
two children (left and right). This module demonstrates core Binary Tree
Abstract Data Type (ADT) operations using a level-order insertion strategy
to keep the tree complete.

Topics covered:
  - Node definition
  - Level-order insertion (keeps tree complete) — O(n)
  - Search (iterative BFS) — O(n)
  - Deletion (replace with deepest node) — O(n)
  - Height computation — O(n)
  - Depth of a given node — O(n)
  - Balance check (height-balanced tree) — O(n)
"""

from __future__ import annotations

from collections import deque
from typing import Optional


class Node:
    """A node in a binary tree.

    Attributes:
        value: The data stored in this node.
        left: Reference to the left child node (or None).
        right: Reference to the right child node (or None).
    """

    def __init__(self, value: int) -> None:
        """Initialize a node with a value and no children."""
        self.value: int = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.value})"


def insert(root: Optional[Node], value: int) -> Node:
    """Insert a value into the binary tree level-order to keep it complete.

    Uses BFS (queue) to find the first available spot — the leftmost
    open position in the last level, or the first node missing a child.

    Time complexity:  O(n) — may visit every node in the worst case.
    Space complexity: O(n) — queue holds at most one level of nodes.

    Args:
        root: The root of the tree (or None for an empty tree).
        value: The integer value to insert.

    Returns:
        The root node of the tree (unchanged if root was not None).
    """
    new_node = Node(value)

    if root is None:
        return new_node

    queue: deque[Node] = deque([root])

    while queue:
        current = queue.popleft()

        if current.left is None:
            current.left = new_node
            return root
        else:
            queue.append(current.left)

        if current.right is None:
            current.right = new_node
            return root
        else:
            queue.append(current.right)

    return root  # unreachable in practice


def search(root: Optional[Node], target: int) -> bool:
    """Search for a target value in the binary tree (iterative BFS).

    Traverses the tree level by level until the value is found or
    all nodes have been visited.

    Time complexity:  O(n) — worst case visits every node.
    Space complexity: O(n) — queue holds at most one level of nodes.

    Args:
        root: The root of the tree (or None for an empty tree).
        target: The value to search for.

    Returns:
        True if the value exists in the tree, False otherwise.
    """
    if root is None:
        return False

    queue: deque[Node] = deque([root])

    while queue:
        current = queue.popleft()

        if current.value == target:
            return True

        if current.left is not None:
            queue.append(current.left)
        if current.right is not None:
            queue.append(current.right)

    return False


def delete(root: Optional[Node], target: int) -> Optional[Node]:
    """Delete a node with the given value from the binary tree.

    Strategy: find the deepest (last) node via BFS, replace the target
    node's value with the deepest node's value, then remove the deepest
    node. This preserves the complete-tree shape.

    Time complexity:  O(n) — two BFS passes over all nodes.
    Space complexity: O(n) — queue holds at most one level of nodes.

    Args:
        root: The root of the tree (or None for an empty tree).
        target: The value of the node to delete.

    Returns:
        The root of the modified tree, or None if the tree is empty.
    """
    if root is None:
        return None

    # If the tree has only one node
    if root.left is None and root.right is None:
        if root.value == target:
            return None
        return root

    # First BFS: find the target node and the deepest node.
    target_node: Optional[Node] = None
    deepest_node: Optional[Node] = None
    deepest_parent: Optional[Node] = None
    deepest_is_left: bool = False

    queue: deque[tuple[Node, Optional[Node], bool]] = deque()
    queue.append((root, None, False))  # (node, parent, is_left_child)

    while queue:
        current, parent, is_left = queue.popleft()

        if current.value == target:
            target_node = current

        deepest_node = current
        deepest_parent = parent
        deepest_is_left = is_left

        if current.left is not None:
            queue.append((current.left, current, True))
        if current.right is not None:
            queue.append((current.right, current, False))

    # Target not found — nothing to delete
    if target_node is None:
        return root

    # Replace target's value with the deepest node's value
    target_node.value = deepest_node.value  # type: ignore[union-attr]

    # Remove the deepest node
    if deepest_parent is not None:
        if deepest_is_left:
            deepest_parent.left = None
        else:
            deepest_parent.right = None

    return root


def height(root: Optional[Node]) -> int:
    """Compute the height of the binary tree.

    Height is defined as the number of edges on the longest path from
    the root to a leaf. An empty tree has height -1; a single node has
    height 0.

    Time complexity:  O(n) — visits every node once.
    Space complexity: O(h) — recursion stack, where h is the height.
                      Worst case O(n) for a skewed tree.

    Args:
        root: The root of the tree (or None for an empty tree).

    Returns:
        The height of the tree.
    """
    if root is None:
        return -1

    left_height = height(root.left)
    right_height = height(root.right)

    return 1 + max(left_height, right_height)


def depth(root: Optional[Node], target: int, current_depth: int = 0) -> int:
    """Find the depth of a node with the given value (distance from root).

    Uses DFS recursion. The depth of the root is 0.

    Time complexity:  O(n) — may visit every node.
    Space complexity: O(h) — recursion stack, where h is the height.

    Args:
        root: The root of the tree (or None for an empty tree).
        target: The value whose depth we want to find.
        current_depth: The depth of the current node (used internally).

    Returns:
        The depth of the target node, or -1 if not found.
    """
    if root is None:
        return -1

    if root.value == target:
        return current_depth

    # Search left subtree
    left_depth = depth(root.left, target, current_depth + 1)
    if left_depth != -1:
        return left_depth

    # Search right subtree
    return depth(root.right, target, current_depth + 1)


def is_balanced(root: Optional[Node]) -> bool:
    """Check whether the binary tree is height-balanced.

    A tree is height-balanced if, for every node, the absolute difference
    between the heights of its left and right subtrees is at most 1.

    Time complexity:  O(n) — single post-order traversal.
    Space complexity: O(h) — recursion stack, where h is the height.

    Args:
        root: The root of the tree (or None for an empty tree).

    Returns:
        True if the tree is height-balanced, False otherwise.
    """

    def _check_balance(node: Optional[Node]) -> int:
        """Return the height of the subtree if balanced, or -2 if unbalanced.

        Returns:
            Height of the subtree (>= -1) if balanced,
            -2 if the subtree is unbalanced.
        """
        if node is None:
            return -1

        left_height = _check_balance(node.left)
        if left_height == -2:
            return -2  # propagate unbalance upward

        right_height = _check_balance(node.right)
        if right_height == -2:
            return -2  # propagate unbalance upward

        if abs(left_height - right_height) > 1:
            return -2  # unbalanced at this node

        return 1 + max(left_height, right_height)

    return _check_balance(root) != -2


def print_tree(root: Optional[Node], prefix: str = "", is_left: bool = True) -> None:
    """Pretty-print the binary tree structure (visual aid).

    Args:
        root: The root of the tree (or None for an empty tree).
        prefix: Prefix string for the current line (used internally).
        is_left: Whether the current node is a left child (used internally).
    """
    if root is None:
        return

    connector = "├── " if is_left else "└── "
    print(f"{prefix}{connector}{root.value}")

    new_prefix = prefix + ("│   " if is_left else "    ")
    children = []
    if root.left is not None:
        children.append(root.left)
    if root.right is not None:
        children.append(root.right)

    for i, child in enumerate(children):
        is_last = (i == len(children) - 1)
        # For the last child printed, use "└──" style; otherwise "├──"
        if len(children) == 2:
            if child == root.left:
                print_tree(root.left, new_prefix, True)
                print_tree(root.right, new_prefix, False)
            return
        print_tree(child, new_prefix, is_last)


def main() -> None:
    """Demonstrate all Binary Tree ADT operations with clear output."""
    print("=" * 60)
    print("Chapter 19 — Binary Tree ADT Operations")
    print("=" * 60)

    # 1. Build a tree by inserting values level-order
    print("\n--- 1. Building a complete binary tree via level-order insertion ---")
    values = [10, 5, 15, 3, 7, 12, 18, 1, 4]
    root: Optional[Node] = None
    for v in values:
        root = insert(root, v)

    print(f"Inserted values: {values}")
    print("Tree structure:")
    print_tree(root)

    # 2. Search
    print("\n--- 2. Search ---")
    targets = [7, 99, 1, 18]
    for t in targets:
        found = search(root, t)
        print(f"  search({t}) -> {'Found' if found else 'Not found'}")

    # 3. Height
    print("\n--- 3. Height ---")
    print(f"  Height of tree: {height(root)}")

    # 4. Depth
    print("\n--- 4. Depth of specific nodes ---")
    depth_targets = [10, 5, 18, 1, 99]
    for t in depth_targets:
        d = depth(root, t)
        if d != -1:
            print(f"  depth({t}) = {d}")
        else:
            print(f"  depth({t}) = not found (-1)")

    # 5. Is balanced
    print("\n--- 5. Balance check ---")
    print(f"  is_balanced: {is_balanced(root)}")

    # 6. Delete
    print("\n--- 6. Delete node 7 ---")
    root = delete(root, 7)
    print("Tree after deleting 7:")
    print_tree(root)
    print(f"  search(7) -> {'Found' if search(root, 7) else 'Not found'}")
    print(f"  Height after deletion: {height(root)}")
    print(f"  is_balanced after deletion: {is_balanced(root)}")

    # 7. Delete root
    print("\n--- 7. Delete root node (10) ---")
    root = delete(root, 10)
    print("Tree after deleting root (10):")
    print_tree(root)
    print(f"  Height: {height(root)}")
    print(f"  is_balanced: {is_balanced(root)}")

    # 8. Build an unbalanced tree to demonstrate is_balanced
    print("\n--- 8. Unbalanced tree example ---")
    unbalanced_root: Optional[Node] = None
    for v in [1, 2, 3, 4, 5]:
        unbalanced_root = insert(unbalanced_root, v)
    print("Unbalanced tree (inserted 1,2,3,4,5 in order — becomes a chain):")
    print_tree(unbalanced_root)
    print(f"  Height: {height(unbalanced_root)}")
    print(f"  is_balanced: {is_balanced(unbalanced_root)}")

    # 9. Build a balanced tree
    print("\n--- 9. Balanced tree example ---")
    balanced_root: Optional[Node] = None
    for v in [4, 2, 6, 1, 3, 5, 7]:
        balanced_root = insert(balanced_root, v)
    print("Balanced tree (inserted 4,2,6,1,3,5,7):")
    print_tree(balanced_root)
    print(f"  Height: {height(balanced_root)}")
    print(f"  is_balanced: {is_balanced(balanced_root)}")


if __name__ == "__main__":
    main()
