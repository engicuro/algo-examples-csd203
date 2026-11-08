"""
22_bst_operations.py - Advanced Binary Search Tree Operations in Python

A Binary Search Tree (BST) is a node-based binary tree data structure where
each node has at most two children, and for every node:
  - All values in the left subtree are less than the node's value.
  - All values in the right subtree are greater than the node's value.

This module demonstrates advanced BST operations:
  - Finding the minimum and maximum values
  - Finding the inorder successor and predecessor of a given value
  - Range query: collect all values within [low, high]
  - k-th smallest element (count-based recursive approach)
  - Validating the BST property

All operations leverage the BST ordering invariant for efficiency.
"""

from typing import List, Optional


class Node:
    """A node in a Binary Search Tree.

    Attributes:
        value: The key stored in this node.
        left:  Reference to the left child (values < self.value).
        right: Reference to the right child (values > self.value).
    """

    def __init__(self, value: int) -> None:
        self.value: int = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.value})"


# ---------------------------------------------------------------------------
# Minimum & Maximum
# ---------------------------------------------------------------------------

def find_min(root: Optional[Node]) -> Optional[int]:
    """Return the minimum value in the BST.

    Walk left from the root until no left child remains.
    Time complexity: O(h) where h is the height of the tree.
    - Best / average case (balanced): O(log n)
    - Worst case (skewed):           O(n)

    Args:
        root: The root node of the BST (or subtree).

    Returns:
        The minimum value, or None if the tree is empty.
    """
    if root is None:
        return None
    current = root
    while current.left is not None:
        current = current.left  # keep going left — smallest is leftmost
    return current.value


def find_max(root: Optional[Node]) -> Optional[int]:
    """Return the maximum value in the BST.

    Walk right from the root until no right child remains.
    Time complexity: O(h) where h is the height of the tree.
    - Best / average case (balanced): O(log n)
    - Worst case (skewed):           O(n)

    Args:
        root: The root node of the BST (or subtree).

    Returns:
        The maximum value, or None if the tree is empty.
    """
    if root is None:
        return None
    current = root
    while current.right is not None:
        current = current.right  # keep going right — largest is rightmost
    return current.value


# ---------------------------------------------------------------------------
# Successor & Predecessor
# ---------------------------------------------------------------------------

def find_successor(root: Optional[Node], value: int) -> Optional[int]:
    """Find the inorder successor of a given value in the BST.

    The inorder successor is the smallest value strictly greater than `value`.

    Approach:
      - Traverse from the root, tracking the last node where we turned left
        (that node is a candidate successor).
      - If the value exists and has a right subtree, the successor is the
        minimum value in that right subtree.
      - Otherwise, the tracked candidate is the successor.

    Time complexity: O(h) — one traversal from root to leaf.

    Args:
        root:  The root node of the BST.
        value: The value whose successor we seek.

    Returns:
        The successor value, or None if no successor exists.
    """
    successor: Optional[Node] = None
    current = root

    while current is not None:
        if value < current.value:
            # current.value is a candidate successor; go left for a smaller one
            successor = current
            current = current.left
        elif value > current.value:
            # successor must be above or to the right; go right
            current = current.right
        else:
            # Found the node — successor is the min of its right subtree
            if current.right is not None:
                return find_min(current.right)
            break

    return successor.value if successor is not None else None


def find_predecessor(root: Optional[Node], value: int) -> Optional[int]:
    """Find the inorder predecessor of a given value in the BST.

    The inorder predecessor is the largest value strictly less than `value`.

    Approach (mirror of successor):
      - Traverse from the root, tracking the last node where we turned right
        (that node is a candidate predecessor).
      - If the value exists and has a left subtree, the predecessor is the
        maximum value in that left subtree.
      - Otherwise, the tracked candidate is the predecessor.

    Time complexity: O(h).

    Args:
        root:  The root node of the BST.
        value: The value whose predecessor we seek.

    Returns:
        The predecessor value, or None if no predecessor exists.
    """
    predecessor: Optional[Node] = None
    current = root

    while current is not None:
        if value > current.value:
            # current.value is a candidate predecessor; go right for a larger one
            predecessor = current
            current = current.right
        elif value < current.value:
            # predecessor must be above or to the left; go left
            current = current.left
        else:
            # Found the node — predecessor is the max of its left subtree
            if current.left is not None:
                return find_max(current.left)
            break

    return predecessor.value if predecessor is not None else None


# ---------------------------------------------------------------------------
# Range Query
# ---------------------------------------------------------------------------

def range_query(root: Optional[Node], low: int, high: int) -> List[int]:
    """Collect all values in the BST that fall within [low, high] (inclusive).

    Uses the BST ordering to prune subtrees that cannot contain values in
    the target range, avoiding a full traversal.

    Time complexity: O(k + h) where k is the number of reported values.
    - We visit at most O(k + h) nodes: h nodes to reach the range boundaries,
      then k nodes inside the range plus their connecting paths.

    Args:
        root: The root node of the BST.
        low:  The lower bound of the range (inclusive).
        high: The upper bound of the range (inclusive).

    Returns:
        A sorted list of values within [low, high].
    """
    result: List[int] = []

    def _collect(node: Optional[Node]) -> None:
        """Inorder traversal with range pruning."""
        if node is None:
            return
        # Prune left subtree if node value is <= low (all left values are smaller)
        if node.value > low:
            _collect(node.left)
        # Include this node if it falls in range
        if low <= node.value <= high:
            result.append(node.value)
        # Prune right subtree if node value is >= high (all right values are larger)
        if node.value < high:
            _collect(node.right)

    _collect(root)
    return result


# ---------------------------------------------------------------------------
# k-th Smallest Element
# ---------------------------------------------------------------------------

def kth_smallest(root: Optional[Node], k: int) -> Optional[int]:
    """Return the k-th smallest value in the BST (1-indexed).

    Uses a count-based recursive approach: count nodes in the left subtree
    to determine whether the k-th smallest is in the left subtree, at the
    current node, or in the right subtree.

    Time complexity: O(n) worst case (unbalanced), O(h + k) average.
    Space complexity: O(h) for the recursion stack.

    Args:
        root: The root node of the BST.
        k:    The 1-based rank of the element to find.

    Returns:
        The k-th smallest value, or None if k is out of range.
    """
    def count_nodes(node: Optional[Node]) -> int:
        """Count total nodes in the subtree rooted at `node` — O(n)."""
        if node is None:
            return 0
        return 1 + count_nodes(node.left) + count_nodes(node.right)

    if root is None or k < 1:
        return None

    left_count = count_nodes(root.left)  # number of nodes smaller than root

    if k <= left_count:
        # k-th smallest is in the left subtree
        return kth_smallest(root.left, k)
    elif k == left_count + 1:
        # Root is the k-th smallest
        return root.value
    else:
        # k-th smallest is in the right subtree, adjust k
        return kth_smallest(root.right, k - left_count - 1)


# ---------------------------------------------------------------------------
# BST Validation
# ---------------------------------------------------------------------------

def is_valid_bst(root: Optional[Node]) -> bool:
    """Validate that a binary tree satisfies the BST property.

    A valid BST requires that for every node:
      - All values in the left subtree are strictly less than the node's value.
      - All values in the right subtree are strictly greater than the node's value.
      - Both subtrees are also valid BSTs.

    Approach: pass down a valid (low, high) range for each node's value.
    Time complexity:  O(n) — visit every node once.
    Space complexity: O(h) — recursion stack depth.

    Args:
        root: The root node of the binary tree.

    Returns:
        True if the tree is a valid BST, False otherwise.
    """
    def _validate(node: Optional[Node], low: float, high: float) -> bool:
        """Recursively check that node.value is within (low, high)."""
        if node is None:
            return True
        if node.value <= low or node.value >= high:
            return False
        # Left subtree must be < node.value; right subtree must be > node.value
        return _validate(node.left, low, node.value) and _validate(
            node.right, node.value, high
        )

    return _validate(root, float("-inf"), float("inf"))


# ---------------------------------------------------------------------------
# Helper: Insert (for building the tree in __main__)
# ---------------------------------------------------------------------------

def insert(root: Optional[Node], value: int) -> Node:
    """Insert a value into the BST and return the (possibly new) root.

    Time complexity: O(h).

    Args:
        root:  The root of the BST (or None for an empty tree).
        value: The value to insert.

    Returns:
        The root of the BST after insertion.
    """
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)
    # Duplicate values are ignored (no change)
    return root


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """Build a BST and demonstrate all advanced operations."""
    print("=" * 60)
    print("Chapter 22 — Advanced BST Operations")
    print("=" * 60)

    # Build the BST by inserting values
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    print(f"\nInserting values: {values}")
    root: Optional[Node] = None
    for v in values:
        root = insert(root, v)
    print("BST constructed.")

    # 1. Find Minimum
    print("\n--- 1. Find Minimum ---")
    print(f"  Minimum value: {find_min(root)}")  # Expected: 10

    # 2. Find Maximum
    print("\n--- 2. Find Maximum ---")
    print(f"  Maximum value: {find_max(root)}")  # Expected: 80

    # 3. Successor
    print("\n--- 3. Inorder Successor ---")
    for v in [10, 25, 50, 70, 80]:
        succ = find_successor(root, v)
        print(f"  Successor of {v}: {succ}")
    # Expected: 25, 30, 60, 80, None

    # 4. Predecessor
    print("\n--- 4. Inorder Predecessor ---")
    for v in [10, 25, 50, 70, 80]:
        pred = find_predecessor(root, v)
        print(f"  Predecessor of {v}: {pred}")
    # Expected: None, 20, 45, 60, 70

    # 5. Range Query
    print("\n--- 5. Range Query ---")
    low, high = 25, 65
    result = range_query(root, low, high)
    print(f"  Values in [{low}, {high}]: {result}")
    # Expected: [25, 30, 35, 40, 45, 50, 60]

    # 6. k-th Smallest
    print("\n--- 6. k-th Smallest ---")
    for k in [1, 3, 5, 7, 11]:
        val = kth_smallest(root, k)
        print(f"  {k}-th smallest: {val}")
    # Expected: 10, 25, 40, 60, 80

    # 7. Validate BST
    print("\n--- 7. Validate BST ---")
    print(f"  Is valid BST? {is_valid_bst(root)}")  # Expected: True

    # Test with an invalid tree
    print("\n  Testing with an invalid tree (swap two nodes)...")
    # Create a small invalid BST: root=10, left=5, right=3 (3 < 10 but is on right)
    bad_root = Node(10)
    bad_root.left = Node(5)
    bad_root.right = Node(3)  # violates BST property
    print(f"  Is valid BST? {is_valid_bst(bad_root)}")  # Expected: False


if __name__ == "__main__":
    main()
