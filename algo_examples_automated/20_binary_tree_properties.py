"""
20_binary_tree_properties.py - Binary Tree Property Computations

This module demonstrates common property computations on binary trees,
including node counts, height, diameter, and level-order traversal.

Topics covered:
  - Node definition and tree construction
  - Counting total nodes — O(n)
  - Counting leaf nodes — O(n)
  - Counting internal (non-leaf) nodes — O(n)
  - Computing tree height — O(n)
  - Computing tree diameter (longest path between any two nodes) — O(n)
  - Level-order (breadth-first) traversal — O(n)
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional


class Node:
    """A node in a binary tree."""

    def __init__(self, value: int, left: Optional[Node] = None, right: Optional[Node] = None) -> None:
        self.value: int = value
        self.left: Optional[Node] = left
        self.right: Optional[Node] = right


def count_nodes(root: Optional[Node]) -> int:
    """Return the total number of nodes in the tree — O(n)."""
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def count_leaf_nodes(root: Optional[Node]) -> int:
    """Return the number of leaf nodes (nodes with no children) — O(n)."""
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    return count_leaf_nodes(root.left) + count_leaf_nodes(root.right)


def count_internal_nodes(root: Optional[Node]) -> int:
    """Return the number of internal nodes (nodes with at least one child) — O(n)."""
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 0
    return 1 + count_internal_nodes(root.left) + count_internal_nodes(root.right)


def get_height(root: Optional[Node]) -> int:
    """Return the height of the tree (number of edges on the longest root-to-leaf path).

    An empty tree has height -1; a single-node tree has height 0.
    — O(n).
    """
    if root is None:
        return -1
    return 1 + max(get_height(root.left), get_height(root.right))


def get_diameter(root: Optional[Node]) -> int:
    """Return the diameter of the tree — the number of edges on the longest path
    between any two nodes — O(n).

    The diameter may or may not pass through the root. At each node, the longest
    path through that node is left_height + right_height + 2 (the two downward
    edges from the node to the deepest leaf in each subtree).
    """
    _diameter: int = 0

    def _height(node: Optional[Node]) -> int:
        """Helper: compute height while updating the global diameter candidate."""
        nonlocal _diameter
        if node is None:
            return -1
        left_h = _height(node.left)
        right_h = _height(node.right)
        # Longest path through this node spans both subtrees
        _diameter = max(_diameter, left_h + right_h + 2)
        return 1 + max(left_h, right_h)

    _height(root)
    return _diameter


def level_order_traversal(root: Optional[Node]) -> List[List[int]]:
    """Return a list of levels, where each level is a list of node values — O(n).

    Uses a deque-based BFS to visit nodes level by level.
    """
    if root is None:
        return []

    result: List[List[int]] = []
    queue: deque[Node] = deque([root])

    while queue:
        level_size: int = len(queue)
        level: List[int] = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.value)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        result.append(level)

    return result


def main() -> None:
    """Build a sample binary tree and demonstrate all property functions."""
    print("=" * 60)
    print("Chapter 20 — Binary Tree Properties")
    print("=" * 60)

    # Build the following tree:
    #          1
    #        /   \
    #       2     3
    #      / \     \
    #     4   5     6
    #        /
    #       7
    root = Node(
        1,
        left=Node(
            2,
            left=Node(4),
            right=Node(5, left=Node(7)),
        ),
        right=Node(
            3,
            right=Node(6),
        ),
    )

    # 1. Total node count
    print(f"\nTotal nodes:       {count_nodes(root)}")          # 7

    # 2. Leaf node count
    print(f"Leaf nodes:        {count_leaf_nodes(root)}")       # 3 (4, 7, 6)

    # 3. Internal node count
    print(f"Internal nodes:    {count_internal_nodes(root)}")   # 4 (1, 2, 3, 5)

    # 4. Height
    print(f"Tree height:       {get_height(root)}")             # 3

    # 5. Diameter
    # The longest path is 4 -> 2 -> 5 -> 7 (3 edges) or 7 -> 5 -> 2 -> 1 -> 3 -> 6 (5 edges)
    # Diameter = 5 edges (path: 4-2-1-3-6 or 7-5-2-1-3-6)
    print(f"Tree diameter:     {get_diameter(root)}")            # 5

    # 6. Level-order traversal
    print(f"\nLevel-order traversal:")
    levels = level_order_traversal(root)
    for i, level in enumerate(levels):
        print(f"  Level {i}: {level}")


if __name__ == "__main__":
    main()
