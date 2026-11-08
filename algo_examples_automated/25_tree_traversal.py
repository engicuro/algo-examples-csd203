"""
25_tree_traversal.py - Tree Traversal Algorithms in Python

Binary tree traversal is the process of visiting every node in a tree
exactly once in a systematic order. Traversals are fundamental to many
tree algorithms and are used in expression evaluation, serialization,
searching, and more.

Topics covered:
  - Node definition for a binary tree
  - BFS (level-order) traversal using a deque — O(n) time, O(w) space
  - DFS traversals: inorder, preorder, postorder (recursive) — O(n) time, O(h) space
  - Zigzag (spiral) traversal — O(n) time, O(w) space
  - Boundary traversal (left boundary + leaves + right boundary in reverse) — O(n) time, O(h) space
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional


class Node:
    """A node in a binary tree.

    Attributes:
        value: The data stored in this node.
        left:  Reference to the left child node (or None).
        right: Reference to the right child node (or None).
    """

    def __init__(self, value: int, left: Optional[Node] = None, right: Optional[Node] = None) -> None:
        """Initialize a tree node.

        Args:
            value: The integer value stored at this node.
            left:  Left child subtree (default None).
            right: Right child subtree (default None).
        """
        self.value: int = value
        self.left: Optional[Node] = left
        self.right: Optional[Node] = right

    def __repr__(self) -> str:
        """Return a concise string representation of the node."""
        return f"Node({self.value})"


# ---------------------------------------------------------------------------
# BFS — Level-Order Traversal
# ---------------------------------------------------------------------------

def bfs_level_order(root: Optional[Node]) -> List[int]:
    """Traverse the tree level by level using a queue (BFS).

    Visits nodes in breadth-first order: all nodes at depth d are visited
    before any node at depth d+1.

    Time complexity:  O(n) — every node is enqueued and dequeued once.
    Space complexity: O(w) — where w is the maximum width of the tree
                      (worst case O(n) for a complete tree).

    Args:
        root: The root node of the binary tree (or None for an empty tree).

    Returns:
        A list of node values in level-order.
    """
    if root is None:
        return []

    result: List[int] = []
    queue: deque[Node] = deque([root])  # deque gives O(1) popleft

    while queue:
        node = queue.popleft()          # O(1) amortised
        result.append(node.value)

        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)

    return result


# ---------------------------------------------------------------------------
# DFS — Inorder Traversal (Left, Root, Right)
# ---------------------------------------------------------------------------

def dfs_inorder(root: Optional[Node]) -> List[int]:
    """Traverse the tree in inorder (left subtree, root, right subtree).

    For a binary search tree this produces values in ascending sorted order.

    Time complexity:  O(n) — each node is visited exactly once.
    Space complexity: O(h) — recursion stack depth equals tree height h;
                      O(n) in the worst case (skewed tree), O(log n) for a
                      balanced tree.

    Args:
        root: The root node of the binary tree (or None for an empty tree).

    Returns:
        A list of node values in inorder sequence.
    """
    result: List[int] = []

    def _traverse(node: Optional[Node]) -> None:
        """Recurse left, visit node, recurse right."""
        if node is None:
            return
        _traverse(node.left)             # visit left subtree first
        result.append(node.value)        # then visit this node
        _traverse(node.right)            # finally visit right subtree

    _traverse(root)
    return result


# ---------------------------------------------------------------------------
# DFS — Preorder Traversal (Root, Left, Right)
# ---------------------------------------------------------------------------

def dfs_preorder(root: Optional[Node]) -> List[int]:
    """Traverse the tree in preorder (root, left subtree, right subtree).

    Preorder is useful for creating a copy of the tree or for prefix
    expression serialization.

    Time complexity:  O(n) — each node is visited exactly once.
    Space complexity: O(h) — recursion stack depth equals tree height h.

    Args:
        root: The root node of the binary tree (or None for an empty tree).

    Returns:
        A list of node values in preorder sequence.
    """
    result: List[int] = []

    def _traverse(node: Optional[Node]) -> None:
        """Visit node, then recurse left, then recurse right."""
        if node is None:
            return
        result.append(node.value)        # visit this node first
        _traverse(node.left)             # then left subtree
        _traverse(node.right)            # then right subtree

    _traverse(root)
    return result


# ---------------------------------------------------------------------------
# DFS — Postorder Traversal (Left, Right, Root)
# ---------------------------------------------------------------------------

def dfs_postorder(root: Optional[Node]) -> List[int]:
    """Traverse the tree in postorder (left subtree, right subtree, root).

    Postorder is useful for deleting a tree (children before parent) or
    for evaluating postfix expressions.

    Time complexity:  O(n) — each node is visited exactly once.
    Space complexity: O(h) — recursion stack depth equals tree height h.

    Args:
        root: The root node of the binary tree (or None for an empty tree).

    Returns:
        A list of node values in postorder sequence.
    """
    result: List[int] = []

    def _traverse(node: Optional[Node]) -> None:
        """Recurse left, recurse right, then visit node."""
        if node is None:
            return
        _traverse(node.left)             # visit left subtree first
        _traverse(node.right)            # then right subtree
        result.append(node.value)        # finally visit this node

    _traverse(root)
    return result


# ---------------------------------------------------------------------------
# Zigzag (Spiral) Traversal
# ---------------------------------------------------------------------------

def zigzag_traversal(root: Optional[Node]) -> List[List[int]]:
    """Traverse the tree in zigzag (spiral) order.

    Alternates direction at each level: left-to-right on even levels,
    right-to-left on odd levels (root is level 0).

    Time complexity:  O(n) — every node is processed exactly once.
    Space complexity: O(w) — the deque holds at most one level of nodes;
                      worst case O(n) for a complete tree.

    Args:
        root: The root node of the binary tree (or None for an empty tree).

    Returns:
        A list of lists, where each inner list contains the node values
        at that level in zigzag order.
    """
    if root is None:
        return []

    result: List[List[int]] = []
    queue: deque[Node] = deque([root])
    left_to_right: bool = True  # direction flag for the current level

    while queue:
        level_size = len(queue)
        level_values: List[int] = []

        for _ in range(level_size):
            node = queue.popleft()
            level_values.append(node.value)

            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        # Reverse the level values when traversing right-to-left
        if not left_to_right:
            level_values.reverse()  # O(k) for level of size k

        result.append(level_values)
        left_to_right = not left_to_right  # flip direction for next level

    return result


# ---------------------------------------------------------------------------
# Boundary Traversal
# ---------------------------------------------------------------------------

def boundary_traversal(root: Optional[Node]) -> List[int]:
    """Return the boundary traversal of a binary tree.

    The boundary consists of three parts visited in order:
      1. Left boundary — top-down (excluding leaves and the root is
         included only once via the root itself).
      2. All leaf nodes — visited left to right.
      3. Right boundary — bottom-up (excluding leaves, reversed).

    Time complexity:  O(n) — each node is visited a constant number of times.
    Space complexity: O(h) — recursion stack depth equals tree height h;
                      the output list stores all n nodes.

    Args:
        root: The root node of the binary tree (or None for an empty tree).

    Returns:
        A list of node values forming the boundary of the tree.
    """
    if root is None:
        return []

    boundary: List[int] = [root.value]  # root is always part of the boundary

    # --- 1. Left boundary (top-down, excluding leaves and root) ---
    def _left_boundary(node: Optional[Node]) -> None:
        """Collect left-boundary nodes (excluding leaves).

        We go down the left side preferentially; if no left child exists
        we go right. Leaf nodes are skipped.
        """
        if node is None or (node.left is None and node.right is None):
            return
        boundary.append(node.value)
        if node.left is not None:
            _left_boundary(node.left)
        else:
            _left_boundary(node.right)

    # --- 2. Leaf nodes (left to right via inorder scan) ---
    def _leaves(node: Optional[Node]) -> None:
        """Collect all leaf nodes using an inorder traversal."""
        if node is None:
            return
        _leaves(node.left)
        if node.left is None and node.right is None:
            boundary.append(node.value)
        _leaves(node.right)

    # --- 3. Right boundary (bottom-up, excluding leaves and root) ---
    def _right_boundary(node: Optional[Node]) -> None:
        """Collect right-boundary nodes (excluding leaves).

        Collected in reverse order by appending *after* the recursive
        call so that the list ends up bottom-up.
        """
        if node is None or (node.left is None and node.right is None):
            return
        if node.right is not None:
            _right_boundary(node.right)
        else:
            _right_boundary(node.left)
        boundary.append(node.value)  # append after recursion → bottom-up

    # Traverse left and right subtrees separately
    if root.left is not None:
        _left_boundary(root.left)
    if root.left is not None or root.right is not None:
        _leaves(root)
    if root.right is not None:
        _right_boundary(root.right)

    return boundary


# ---------------------------------------------------------------------------
# Helper: Pretty-print a tree structure (for demonstration)
# ---------------------------------------------------------------------------

def print_tree(root: Optional[Node], prefix: str = "", is_left: bool = True) -> None:
    """Print a visual representation of the binary tree.

    Recursively prints the right subtree first (top), then the current
    node, then the left subtree (bottom), with branch characters.

    Args:
        root:    The current node being printed.
        prefix:  Prefix string for indentation of child lines.
        is_left: Whether this node is a left child (affects branch char).
    """
    if root is None:
        return

    # Print right subtree first (it appears on top in the visual)
    if root.right is not None:
        new_prefix = prefix + ("│   " if is_left else "    ")
        print_tree(root.right, new_prefix, False)

    # Print current node
    connector = "└── " if prefix == "" else ("└── " if is_left else "┌── ")
    print(f"{prefix}{connector}{root.value}")

    # Print left subtree
    if root.left is not None:
        new_prefix = prefix + ("    " if is_left else "│   ")
        print_tree(root.left, new_prefix, True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Build a sample binary tree and demonstrate all traversal types."""
    print("=" * 60)
    print("Chapter 25 — Tree Traversal Algorithms")
    print("=" * 60)

    # Build the following binary tree:
    #
    #            1
    #          /   \\
    #         2     3
    #        / \\   / \\
    #       4   5 6   7
    #      /       \\
    #     8         9
    #
    # Structure:
    #         1
    #       /   \\
    #      2     3
    #     / \\   / \\
    #    4   5 6   7
    #   /       \\
    #  8         9

    root = Node(
        1,
        left=Node(
            2,
            left=Node(4, left=Node(8)),
            right=Node(5),
        ),
        right=Node(
            3,
            left=Node(6, right=Node(9)),
            right=Node(7),
        ),
    )

    # Visual tree
    print("\n--- Sample Binary Tree ---")
    print_tree(root)

    # BFS (Level-Order)
    print("\n--- BFS (Level-Order) Traversal ---")
    bfs_result = bfs_level_order(root)
    print(f"  Level-order: {bfs_result}")
    # Expected: [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # DFS Inorder
    print("\n--- DFS Inorder Traversal (Left, Root, Right) ---")
    inorder_result = dfs_inorder(root)
    print(f"  Inorder:     {inorder_result}")
    # Expected: [8, 4, 2, 5, 1, 6, 9, 3, 7]

    # DFS Preorder
    print("\n--- DFS Preorder Traversal (Root, Left, Right) ---")
    preorder_result = dfs_preorder(root)
    print(f"  Preorder:    {preorder_result}")
    # Expected: [1, 2, 4, 8, 5, 3, 6, 9, 7]

    # DFS Postorder
    print("\n--- DFS Postorder Traversal (Left, Right, Root) ---")
    postorder_result = dfs_postorder(root)
    print(f"  Postorder:   {postorder_result}")
    # Expected: [8, 4, 5, 2, 9, 6, 7, 3, 1]

    # Zigzag Traversal
    print("\n--- Zigzag (Spiral) Traversal ---")
    zigzag_result = zigzag_traversal(root)
    for level, vals in enumerate(zigzag_result):
        direction = "L→R" if level % 2 == 0 else "R→L"
        print(f"  Level {level} ({direction}): {vals}")
    # Level 0 (L→R): [1]
    # Level 1 (R→L): [3, 2]
    # Level 2 (L→R): [4, 5, 6, 7]
    # Level 3 (R→L): [9, 8]

    # Boundary Traversal
    print("\n--- Boundary Traversal ---")
    boundary_result = boundary_traversal(root)
    print(f"  Boundary:    {boundary_result}")
    # Left boundary (top-down): 1, 2, 4
    # Leaves (left to right):   8, 5, 9, 7
    # Right boundary (bottom-up, excl leaves & root): 3
    # Combined: [1, 2, 4, 8, 5, 9, 7, 3]


if __name__ == "__main__":
    main()
