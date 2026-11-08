"""
18_binary_tree.py - Binary Tree Concepts in Python

A binary tree is a hierarchical data structure where each node has at most
two children — referred to as the left child and the right child.

Topics covered:
  - Node definition
  - Tree construction
  - Traversals: inorder, preorder, postorder (recursive), level-order (iterative)
  - Properties: node count, emptiness check, height
"""

from __future__ import annotations

from collections import deque
from typing import Any, Optional


class Node:
    """A node in a binary tree.

    Attributes:
        value: The data stored in this node.
        left: Reference to the left child node (or None).
        right: Reference to the right child node (or None).
    """

    def __init__(self, value: Any, left: Optional[Node] = None, right: Optional[Node] = None) -> None:
        """Initialize a node with a value and optional left/right children."""
        self.value: Any = value
        self.left: Optional[Node] = left
        self.right: Optional[Node] = right

    def __repr__(self) -> str:
        """Return a concise string representation of the node."""
        return f"Node({self.value!r})"


# ---------------------------------------------------------------------------
# Tree construction
# ---------------------------------------------------------------------------

def create_sample_tree() -> Node:
    """Build and return a fixed sample binary tree.

    The tree structure:
           1
          / \\
         2   3
        / \\   \\
       4   5   6

    Returns:
        The root Node of the sample tree.
    """
    # Level 3 (leaves)
    node4: Node = Node(4)
    node5: Node = Node(5)
    node6: Node = Node(6)

    # Level 2
    node2: Node = Node(2, left=node4, right=node5)
    node3: Node = Node(3, right=node6)

    # Level 1 (root)
    root: Node = Node(1, left=node2, right=node3)

    return root


# ---------------------------------------------------------------------------
# Traversals
# ---------------------------------------------------------------------------

def inorder_traversal(root: Optional[Node]) -> list[Any]:
    """Return a list of values visited in inorder (left, root, right).

    Time complexity:  O(n) — each node is visited exactly once.
    Space complexity: O(h) — recursion stack depth equals tree height h.
                       Worst case O(n) for a skewed tree; O(log n) for a balanced tree.
    """
    result: list[Any] = []
    if root is None:
        return result
    result.extend(inorder_traversal(root.left))
    result.append(root.value)
    result.extend(inorder_traversal(root.right))
    return result


def preorder_traversal(root: Optional[Node]) -> list[Any]:
    """Return a list of values visited in preorder (root, left, right).

    Time complexity:  O(n) — each node is visited exactly once.
    Space complexity: O(h) — recursion stack depth equals tree height h.
    """
    result: list[Any] = []
    if root is None:
        return result
    result.append(root.value)
    result.extend(preorder_traversal(root.left))
    result.extend(preorder_traversal(root.right))
    return result


def postorder_traversal(root: Optional[Node]) -> list[Any]:
    """Return a list of values visited in postorder (left, right, root).

    Time complexity:  O(n) — each node is visited exactly once.
    Space complexity: O(h) — recursion stack depth equals tree height h.
    """
    result: list[Any] = []
    if root is None:
        return result
    result.extend(postorder_traversal(root.left))
    result.extend(postorder_traversal(root.right))
    result.append(root.value)
    return result


def level_order_traversal(root: Optional[Node]) -> list[Any]:
    """Return a list of values visited level by level (breadth-first).

    Uses a deque as a queue for iterative traversal.

    Time complexity:  O(n) — each node is enqueued and dequeued once.
    Space complexity: O(w) — maximum width of the tree (queue size).
                       Worst case O(n) for a complete tree's last level.
    """
    result: list[Any] = []
    if root is None:
        return result

    queue: deque[Node] = deque([root])
    while queue:
        current: Node = queue.popleft()
        result.append(current.value)
        if current.left is not None:
            queue.append(current.left)
        if current.right is not None:
            queue.append(current.right)

    return result


# ---------------------------------------------------------------------------
# Property functions
# ---------------------------------------------------------------------------

def count_nodes(root: Optional[Node]) -> int:
    """Return the total number of nodes in the tree — O(n)."""
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def is_empty(root: Optional[Node]) -> bool:
    """Return True if the tree has no nodes — O(1)."""
    return root is None


def get_height(root: Optional[Node]) -> int:
    """Return the height of the tree (number of edges on the longest root-to-leaf path).

    An empty tree has height -1. A single-node tree has height 0.

    Time complexity:  O(n) — every node is visited once.
    Space complexity: O(h) — recursion stack depth.
    """
    if root is None:
        return -1
    return 1 + max(get_height(root.left), get_height(root.right))


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """Build a sample binary tree and demonstrate all traversals and properties."""
    print("=" * 60)
    print("Chapter 18 — Binary Tree")
    print("=" * 60)

    root: Node = create_sample_tree()
    print(f"\nSample tree structure:")
    print(f"       1")
    print(f"      / \\")
    print(f"     2   3")
    print(f"    / \\   \\")
    print(f"   4   5   6")

    # Traversals
    print(f"\n--- Traversals ---")
    print(f"  Inorder   (left, root, right):  {inorder_traversal(root)}")
    print(f"  Preorder  (root, left, right):  {preorder_traversal(root)}")
    print(f"  Postorder (left, right, root):  {postorder_traversal(root)}")
    print(f"  Level-order (BFS, top-down):    {level_order_traversal(root)}")

    # Properties
    print(f"\n--- Properties ---")
    print(f"  is_empty():  {is_empty(root)}")
    print(f"  count_nodes(): {count_nodes(root)}")
    print(f"  get_height():  {get_height(root)}")

    # Edge cases
    print(f"\n--- Edge Cases ---")
    empty_root: Optional[Node] = None
    print(f"  Empty tree is_empty():  {is_empty(empty_root)}")
    print(f"  Empty tree count_nodes(): {count_nodes(empty_root)}")
    print(f"  Empty tree get_height():  {get_height(empty_root)}")
    print(f"  Empty tree inorder:       {inorder_traversal(empty_root)}")
    print(f"  Empty tree level-order:   {level_order_traversal(empty_root)}")


if __name__ == "__main__":
    main()
