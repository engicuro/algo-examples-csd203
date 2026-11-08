"""
23_avl_tree.py - AVL Tree (Self-Balancing Binary Search Tree) in Python

An AVL tree is a self-balancing binary search tree where the height difference
between the left and right subtrees of any node (the balance factor) is at most 1.
After every insertion (or deletion), the tree checks balance factors and performs
rotations to restore the AVL property, guaranteeing O(log n) search, insert, and
delete operations even in the worst case.

Rotation cases:
  - Left-Left (LL):  right_rotate
  - Right-Right (RR): left_rotate
  - Left-Right (LR):  left_right_rotate (left-rotate left child, then right-rotate)
  - Right-Left (RL):  right_left_rotate (right-rotate right child, then left-rotate)
"""

from typing import Optional


class Node:
    """A node in an AVL tree.

    Attributes:
        value: The key stored in this node.
        left:  Reference to the left child node (values < self.value).
        right: Reference to the right child node (values > self.value).
        height: The height of this node in the tree (leaf = 1).
    """

    def __init__(self, value: int) -> None:
        """Initialise a node with a value and no children."""
        self.value: int = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.height: int = 1  # new node is a leaf


# ---------------------------------------------------------------------------
# Helper functions — O(1) each
# ---------------------------------------------------------------------------

def get_height(node: Optional[Node]) -> int:
    """Return the height of a node, treating None as height 0.

    Time complexity: O(1).
    """
    if node is None:
        return 0
    return node.height


def get_balance(node: Optional[Node]) -> int:
    """Return the balance factor of a node (left height - right height).

    A balance factor of +2 or -2 means the node is unbalanced and needs
    a rotation.  Time complexity: O(1).
    """
    if node is None:
        return 0
    return get_height(node.left) - get_height(node.right)


def update_height(node: Node) -> None:
    """Recalculate the height of a node from its children's heights.

    Time complexity: O(1).
    """
    node.height = 1 + max(get_height(node.left), get_height(node.right))


# ---------------------------------------------------------------------------
# Rotation functions — O(1) each (pointer reassignments only)
# ---------------------------------------------------------------------------

def right_rotate(z: Node) -> Node:
    """Perform a right rotation around node z.

    Used when the left subtree is too tall (Left-Left case).

         z                 y
        / \\               / \\
       y   T4    =>     x     z
      / \\                 / \\ / \\
     x   T3              T1 T2 T3 T4
    / \\
   T1  T2

    Time complexity: O(1).
    """
    y = z.left          # y is the left child of z
    t3 = y.right        # t3 is y's right subtree

    # Perform rotation
    y.right = z
    z.left = t3

    # Update heights (z first since it is now a child of y)
    update_height(z)
    update_height(y)

    return y  # new root of this subtree


def left_rotate(z: Node) -> Node:
    """Perform a left rotation around node z.

    Used when the right subtree is too tall (Right-Right case).

       z                   y
      / \\                / \\
     T1   y     =>      z    x
         / \\           / \\ / \\
        T2  x         T1 T2 T3 T4
           / \\
          T3  T4

    Time complexity: O(1).
    """
    y = z.right         # y is the right child of z
    t2 = y.left         # t2 is y's left subtree

    # Perform rotation
    y.left = z
    z.right = t2

    # Update heights (z first since it is now a child of y)
    update_height(z)
    update_height(y)

    return y  # new root of this subtree


def left_right_rotate(z: Node) -> Node:
    """Perform a left-right double rotation around node z.

    Used for the Left-Right case: the left child's right subtree is too tall.
    First left-rotate the left child, then right-rotate z.

       z                z              x
      / \\             / \\           /   \\
     y   T4  =>     x   T4  =>    y       z
    / \\             / \\           / \\   / \\
   T1  x           y  T3         T1 T2 T3 T4
      / \\         / \\
     T2  T3      T1  T2

    Time complexity: O(1).
    """
    z.left = left_rotate(z.left)
    return right_rotate(z)


def right_left_rotate(z: Node) -> Node:
    """Perform a right-left double rotation around node z.

    Used for the Right-Left case: the right child's left subtree is too tall.
    First right-rotate the right child, then left-rotate z.

       z                 z                x
      / \\              / \\             /   \\
     T1   y   =>     T1   x    =>     z       y
        / \\              / \\        / \\   / \\
       x   T4            T2  y      T1 T2 T3 T4
      / \\                   / \\
     T2  T3                T3  T4

    Time complexity: O(1).
    """
    z.right = right_rotate(z.right)
    return left_rotate(z)


# ---------------------------------------------------------------------------
# Insert — O(log n) time, O(log n) space for recursion stack
# ---------------------------------------------------------------------------

def insert(node: Optional[Node], value: int) -> Node:
    """Insert a value into the AVL tree rooted at *node* and rebalance.

    Standard BST insertion followed by height update and rotation if the
    balance factor violates the AVL invariant (|balance| > 1).

    Time complexity: O(log n) — tree height is O(log n).
    Space complexity: O(log n) — recursion depth.
    """
    # 1. Standard BST insertion
    if node is None:
        return Node(value)

    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    else:
        # Duplicate values are not inserted in this implementation
        return node

    # 2. Update height of the current ancestor node
    update_height(node)

    # 3. Get the balance factor
    balance = get_balance(node)

    # 4. Rebalance if needed — four cases

    # Left-Left case
    if balance > 1 and value < node.left.value:  # type: ignore[union-attr]
        return right_rotate(node)

    # Right-Right case
    if balance < -1 and value > node.right.value:  # type: ignore[union-attr]
        return left_rotate(node)

    # Left-Right case
    if balance > 1 and value > node.left.value:  # type: ignore[union-attr]
        return left_right_rotate(node)

    # Right-Left case
    if balance < -1 and value < node.right.value:  # type: ignore[union-attr]
        return right_left_rotate(node)

    return node


# ---------------------------------------------------------------------------
# Traversal — O(n) time, O(h) space for recursion stack
# ---------------------------------------------------------------------------

def inorder_traversal(node: Optional[Node], result: list[int]) -> None:
    """Append node values to *result* in inorder (sorted) order.

    Inorder traversal of a BST visits nodes in ascending order.
    Time complexity: O(n) — visits every node exactly once.
    Space complexity: O(h) — recursion stack, where h is the tree height.
    """
    if node is not None:
        inorder_traversal(node.left, result)
        result.append(node.value)
        inorder_traversal(node.right, result)


def print_balance_factors(node: Optional[Node]) -> None:
    """Print every node's value and its balance factor via inorder traversal.

    Useful for verifying that the AVL property (|balance| <= 1) holds
    for every node after insertions.
    """
    if node is not None:
        print_balance_factors(node.left)
        bf = get_balance(node)
        print(f"  Node {node.value:>3}  balance factor = {bf:+d}")
        print_balance_factors(node.right)


def print_tree(node: Optional[Node], prefix: str = "", is_left: bool = True) -> None:
    """Print the tree structure rotated 90 degrees for visual inspection.

    Each line shows a node value with indentation indicating depth.
    """
    if node is not None:
        print_tree(node.right, prefix + ("│   " if is_left else "    "), False)
        connector = "└── " if is_left else "┌── "
        print(f"{prefix}{connector}{node.value}")
        print_tree(node.left, prefix + ("    " if is_left else "│   "), True)


def main() -> None:
    """Demonstrate AVL tree insertions covering all four rotation cases."""
    print("=" * 60)
    print("Chapter 23 — AVL Tree (Self-Balancing BST)")
    print("=" * 60)

    root: Optional[Node] = None

    # ------------------------------------------------------------------
    # Case 1: Left-Left (LL) — insert 30, 20, 10
    # Triggers a right rotation at node 30.
    # ------------------------------------------------------------------
    print("\n--- Case 1: Left-Left (LL) — inserts 30, 20, 10 ---")
    for v in [30, 20, 10]:
        root = insert(root, v)

    print("Inorder traversal (sorted):")
    result: list[int] = []
    inorder_traversal(root, result)
    print(f"  {result}")

    print("Tree structure:")
    print_tree(root)

    print("Balance factors:")
    print_balance_factors(root)

    # ------------------------------------------------------------------
    # Case 2: Right-Right (RR) — insert 10, 20, 30 into a fresh tree
    # Triggers a left rotation at node 10.
    # ------------------------------------------------------------------
    print("\n--- Case 2: Right-Right (RR) — inserts 10, 20, 30 ---")
    root_rr: Optional[Node] = None
    for v in [10, 20, 30]:
        root_rr = insert(root_rr, v)

    print("Inorder traversal (sorted):")
    result_rr: list[int] = []
    inorder_traversal(root_rr, result_rr)
    print(f"  {result_rr}")

    print("Tree structure:")
    print_tree(root_rr)

    print("Balance factors:")
    print_balance_factors(root_rr)

    # ------------------------------------------------------------------
    # Case 3: Left-Right (LR) — insert 30, 10, 20
    # Triggers a left-right double rotation at node 30.
    # ------------------------------------------------------------------
    print("\n--- Case 3: Left-Right (LR) — inserts 30, 10, 20 ---")
    root_lr: Optional[Node] = None
    for v in [30, 10, 20]:
        root_lr = insert(root_lr, v)

    print("Inorder traversal (sorted):")
    result_lr: list[int] = []
    inorder_traversal(root_lr, result_lr)
    print(f"  {result_lr}")

    print("Tree structure:")
    print_tree(root_lr)

    print("Balance factors:")
    print_balance_factors(root_lr)

    # ------------------------------------------------------------------
    # Case 4: Right-Left (RL) — insert 10, 30, 20
    # Triggers a right-left double rotation at node 10.
    # ------------------------------------------------------------------
    print("\n--- Case 4: Right-Left (RL) — inserts 10, 30, 20 ---")
    root_rl: Optional[Node] = None
    for v in [10, 30, 20]:
        root_rl = insert(root_rl, v)

    print("Inorder traversal (sorted):")
    result_rl: list[int] = []
    inorder_traversal(root_rl, result_rl)
    print(f"  {result_rl}")

    print("Tree structure:")
    print_tree(root_rl)

    print("Balance factors:")
    print_balance_factors(root_rl)

    # ------------------------------------------------------------------
    # Combined demonstration — insert a larger mixed sequence
    # ------------------------------------------------------------------
    print("\n--- Combined: mixed insertions 50, 25, 75, 10, 30, 60, 80, 5, 15 ---")
    root_combined: Optional[Node] = None
    for v in [50, 25, 75, 10, 30, 60, 80, 5, 15]:
        root_combined = insert(root_combined, v)

    print("Inorder traversal (sorted):")
    result_combined: list[int] = []
    inorder_traversal(root_combined, result_combined)
    print(f"  {result_combined}")

    print("Tree structure:")
    print_tree(root_combined)

    print("Balance factors (all should be in {-1, 0, +1}):")
    print_balance_factors(root_combined)


if __name__ == "__main__":
    main()
