"""
25_tree_traversal.py - Tree Traversal: BFS and DFS (No-List Version)

This file demonstrates two main categories of tree traversal:

  BFS (Breadth-First Search) / Level-Order Traversal:
    Visit nodes level by level, from top to bottom, left to right.
    Uses a linked-list queue instead of a Python list.

  DFS (Depth-First Search):
    Visit nodes by going as deep as possible before backtracking.
    Three variants:
      - Inorder  (left, root, right)
      - Preorder (root, left, right)
      - Postorder(left, right, root)

All implementations avoid Python list type.
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
# Linked-list queue for BFS
# ---------------------------------------------------------------------------
class _QueueNode:
    """A node in the linked-list queue used for BFS."""
    def __init__(self, tree_node):
        self.tree_node = tree_node
        self.next = None


def _queue_enqueue(head, tail, tree_node):
    """Add a tree node to the back of the linked-list queue."""
    qnode = _QueueNode(tree_node)
    if tail is None:
        return qnode, qnode
    tail.next = qnode
    return head, qnode


def _queue_dequeue(head):
    """Remove and return the front tree node from the linked-list queue."""
    if head is None:
        return None, None
    return head.tree_node, head.next


def _queue_is_empty(head):
    return head is None


# ---------------------------------------------------------------------------
# BFS (Level-Order Traversal) using a linked-list queue
# ---------------------------------------------------------------------------
def bfs_level_order(root):
    """Breadth-first (level-order) traversal using a linked-list queue.

    How it works:
      1. Put the root in the queue.
      2. While the queue is not empty:
         a. Remove the first node from the queue.
         b. Process (print) that node's value.
         c. Add its left child to the queue (if it exists).
         d. Add its right child to the queue (if it exists).

    Uses a linked-list queue instead of a Python list.
    """
    if root is None:
        return

    # The "queue" — linked list of queue nodes
    head, tail = _queue_enqueue(None, None, root)

    while not _queue_is_empty(head):
        # Take the node at the front of the queue
        current, head = _queue_dequeue(head)

        # Process this node
        print(current.value, end=" ")

        # Add children to the back of the queue
        if current.left is not None:
            head, tail = _queue_enqueue(head, tail, current.left)
        if current.right is not None:
            head, tail = _queue_enqueue(head, tail, current.right)


# ---------------------------------------------------------------------------
# DFS: Inorder Traversal (left, root, right)
# ---------------------------------------------------------------------------
def dfs_inorder(node):
    """Depth-first inorder traversal.

    Visit order: left subtree → current node → right subtree.

    For a Binary Search Tree, this visits values in sorted order.
    """
    if node is None:
        return
    dfs_inorder(node.left)       # 1. Visit left subtree
    print(node.value, end=" ")   # 2. Visit current node
    dfs_inorder(node.right)      # 3. Visit right subtree


# ---------------------------------------------------------------------------
# DFS: Preorder Traversal (root, left, right)
# ---------------------------------------------------------------------------
def dfs_preorder(node):
    """Depth-first preorder traversal.

    Visit order: current node → left subtree → right subtree.

    Preorder is useful for creating a copy of the tree or for prefix
    expression evaluation.
    """
    if node is None:
        return
    print(node.value, end=" ")   # 1. Visit current node first
    dfs_preorder(node.left)      # 2. Visit left subtree
    dfs_preorder(node.right)     # 3. Visit right subtree


# ---------------------------------------------------------------------------
# DFS: Postorder Traversal (left, right, root)
# ---------------------------------------------------------------------------
def dfs_postorder(node):
    """Depth-first postorder traversal.

    Visit order: left subtree → right subtree → current node.

    Postorder is useful for deleting a tree (delete children before parent)
    or for postfix expression evaluation.
    """
    if node is None:
        return
    dfs_postorder(node.left)     # 1. Visit left subtree
    dfs_postorder(node.right)    # 2. Visit right subtree
    print(node.value, end=" ")   # 3. Visit current node last


# ---------------------------------------------------------------------------
# Pretty print helper
# ---------------------------------------------------------------------------
def print_tree(node, indent="", is_right=False):
    """Print the binary tree rotated 90 degrees for visualization."""
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
    print("Chapter 25 — Tree Traversal: BFS and DFS (No-List Version)")
    print("=" * 60)

    # Build a sample binary tree:
    #
    #         1
    #        / \
    #       2   3
    #      / \   \
    #     4   5   6
    #    /
    #   7
    #
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.right = Node(6)
    root.left.left.left = Node(7)

    # Show the tree
    print("\nTree structure:")
    print_tree(root)

    # BFS (Level-order)
    print("\n--- BFS (Level-Order Traversal) ---")
    print("  Visits nodes level by level, top to bottom, left to right:")
    bfs_level_order(root)
    print()  # expected: 1 2 3 4 5 6 7

    # DFS Inorder
    print("\n--- DFS Inorder (left, root, right) ---")
    print("  Visits left subtree first, then root, then right subtree:")
    dfs_inorder(root)
    print()  # expected: 7 4 2 5 1 3 6

    # DFS Preorder
    print("\n--- DFS Preorder (root, left, right) ---")
    print("  Visits root first, then left subtree, then right subtree:")
    dfs_preorder(root)
    print()  # expected: 1 2 4 7 5 3 6

    # DFS Postorder
    print("\n--- DFS Postorder (left, right, root) ---")
    print("  Visits left subtree, then right subtree, then root:")
    dfs_postorder(root)
    print()  # expected: 7 4 5 2 6 3 1

    # --- Comparison of all four traversals side by side ---
    print("\n--- Summary of all four traversals ---")
    print("  BFS (level-order):  ", end="")
    bfs_level_order(root)
    print()

    print("  DFS Inorder:        ", end="")
    dfs_inorder(root)
    print()

    print("  DFS Preorder:       ", end="")
    dfs_preorder(root)
    print()

    print("  DFS Postorder:      ", end="")
    dfs_postorder(root)
    print()

    # --- Simple example: use BFS to count nodes level by level ---
    print("\n--- BFS with level tracking ---")
    if root is not None:
        head, tail = _queue_enqueue(None, None, root)
        current_level = 0
        level_count = 1  # number of nodes at the current level

        print("  Level " + str(current_level) + ": ", end="")

        while not _queue_is_empty(head):
            # Process all nodes at the current level
            nodes_this_level = level_count
            level_count = 0  # reset for the next level

            for _ in range(nodes_this_level):
                current, head = _queue_dequeue(head)
                print(current.value, end=" ")

                # Add children for the next level
                if current.left is not None:
                    head, tail = _queue_enqueue(head, tail, current.left)
                    level_count = level_count + 1
                if current.right is not None:
                    head, tail = _queue_enqueue(head, tail, current.right)
                    level_count = level_count + 1

            current_level = current_level + 1
            if not _queue_is_empty(head):
                print("\n  Level " + str(current_level) + ": ", end="")
        print()
