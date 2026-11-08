"""
17_general_tree.py - General Tree (N-ary Tree) Concepts in Python

A general tree (or n-ary tree) is a tree data structure where each node
can have zero or more children. Unlike binary trees (which limit each
node to at most two children), general trees impose no upper bound on
the number of children per node.

Topics covered:
  - Node definition with a dynamic children list
  - Tree construction (building a sample general tree)
  - Preorder traversal (root → children left to right) — O(n)
  - Postorder traversal (children left to right → root) — O(n)
  - Height computation (max depth from root to leaf) — O(n)
  - Size computation (total node count) — O(n)
"""

from __future__ import annotations

from typing import List, Optional


class Node:
    """A node in a general (n-ary) tree."""

    def __init__(self, value: int) -> None:
        self.value: int = value
        self.children: List[Node] = []

    def __repr__(self) -> str:
        return f"Node({self.value})"


def build_sample_tree() -> Node:
    """Build and return a sample general tree.

    The constructed tree looks like:

            1
          / | \\
         2  3  4
        / \\    |
       5   6   7

    Returns:
        Node: The root of the sample tree.
    """
    # Level 0: root
    root = Node(1)

    # Level 1: children of root
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    root.children.extend([node2, node3, node4])

    # Level 2: children of node 2 and node 4
    node5 = Node(5)
    node6 = Node(6)
    node2.children.extend([node5, node6])

    node7 = Node(7)
    node4.children.append(node7)

    return root


def preorder(root: Optional[Node]) -> List[int]:
    """Return a list of node values in preorder — O(n).

    Visit the current node first, then recursively visit each child
    from left to right.

    Args:
        root: The root node of the tree (or subtree).

    Returns:
        A list of values in preorder traversal order.
    """
    if root is None:
        return []
    result: List[int] = [root.value]
    for child in root.children:
        result.extend(preorder(child))
    return result


def postorder(root: Optional[Node]) -> List[int]:
    """Return a list of node values in postorder — O(n).

    Recursively visit each child from left to right first, then visit
    the current node.

    Args:
        root: The root node of the tree (or subtree).

    Returns:
        A list of values in postorder traversal order.
    """
    if root is None:
        return []
    result: List[int] = []
    for child in root.children:
        result.extend(postorder(child))
    result.append(root.value)
    return result


def height(root: Optional[Node]) -> int:
    """Return the height of the tree (max number of edges on any root-to-leaf path).

    An empty tree (None) has height -1; a single-node tree has height 0.
    — O(n), where n is the number of nodes.

    Args:
        root: The root node of the tree (or subtree).

    Returns:
        The height of the tree.
    """
    if root is None:
        return -1
    if not root.children:
        return 0
    return 1 + max(height(child) for child in root.children)


def size(root: Optional[Node]) -> int:
    """Return the total number of nodes in the tree — O(n).

    Args:
        root: The root node of the tree (or subtree).

    Returns:
        The total node count.
    """
    if root is None:
        return 0
    return 1 + sum(size(child) for child in root.children)


def main() -> None:
    """Build a sample general tree and demonstrate all traversal and property functions."""
    print("=" * 60)
    print("Chapter 17 — General Tree (N-ary Tree)")
    print("=" * 60)

    root = build_sample_tree()

    # Tree structure reference:
    #          1
    #        / | \
    #       2  3  4
    #      / \    |
    #     5   6   7

    # Preorder traversal
    print(f"\nPreorder traversal:  {preorder(root)}")
    # Expected: [1, 2, 5, 6, 3, 4, 7]  (root first, then children left to right)

    # Postorder traversal
    print(f"Postorder traversal: {postorder(root)}")
    # Expected: [5, 6, 2, 3, 7, 4, 1]  (children left to right, root last)

    # Height
    print(f"Tree height:         {height(root)}")
    # Expected: 2  (path 1 → 2 → 5 or 1 → 2 → 6 or 1 → 4 → 7)

    # Size
    print(f"Total nodes:         {size(root)}")
    # Expected: 7


if __name__ == "__main__":
    main()
