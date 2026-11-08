"""
18_binary_tree.py - Binary Tree Basics (No-List Version)

A binary tree is a tree where each node has at most two children:
a left child and a right child.

Topics covered:
  - Creating a node with value, left, and right
  - Inorder traversal  (left, root, right)
  - Preorder traversal (root, left, right)
  - Postorder traversal (left, right, root)
  - Level-order traversal (breadth-first, using a linked-list queue)
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
# Traversals
# ---------------------------------------------------------------------------
def inorder(node):
    """Inorder traversal: left subtree → current node → right subtree.

    For a binary search tree this visits nodes in sorted order.
    """
    if node is None:
        return
    # 1. Visit all nodes in the left subtree
    inorder(node.left)
    # 2. Visit (print) the current node
    print(node.value, end=" ")
    # 3. Visit all nodes in the right subtree
    inorder(node.right)


def preorder(node):
    """Preorder traversal: current node → left subtree → right subtree."""
    if node is None:
        return
    # 1. Visit (print) the current node first
    print(node.value, end=" ")
    # 2. Visit all nodes in the left subtree
    preorder(node.left)
    # 3. Visit all nodes in the right subtree
    preorder(node.right)


def postorder(node):
    """Postorder traversal: left subtree → right subtree → current node."""
    if node is None:
        return
    # 1. Visit all nodes in the left subtree
    postorder(node.left)
    # 2. Visit all nodes in the right subtree
    postorder(node.right)
    # 3. Visit (print) the current node last
    print(node.value, end=" ")


def level_order(root):
    """Level-order (breadth-first) traversal using a linked-list queue.

    How it works:
      1. Put the root in the queue.
      2. While the queue is not empty:
         a. Remove the first node from the queue.
         b. Process (print) that node's value.
         c. If it has a left child, add the left child to the queue.
         d. If it has a right child, add the right child to the queue.

    Uses a linked-list queue instead of a Python list.
    """
    if root is None:
        return

    # The "queue" — linked list of queue nodes
    head, tail = _queue_enqueue(None, None, root)

    while not _queue_is_empty(head):
        # Take the node at the front of the queue
        current, head = _queue_dequeue(head)

        # Process (print) this node
        print(current.value, end=" ")

        # Add children to the back of the queue
        if current.left is not None:
            head, tail = _queue_enqueue(head, tail, current.left)
        if current.right is not None:
            head, tail = _queue_enqueue(head, tail, current.right)


# ---------------------------------------------------------------------------
# Pretty print helper — shows tree structure rotated 90 degrees
# ---------------------------------------------------------------------------
def print_tree(node, indent="", is_right=False):
    """Print the binary tree rotated 90 degrees for easy visualization."""
    if node is None:
        return
    # Print right subtree first (it appears on top)
    print_tree(node.right, indent + ("    " if is_right else "│   "), True)
    # Print the current node
    connector = "└── " if is_right else "┌── "
    print(indent + connector + str(node.value))
    # Print left subtree (it appears on the bottom)
    print_tree(node.left, indent + ("    " if not is_right else "│   "), False)


# ---------------------------------------------------------------------------
# Main block — simple example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Chapter 18 — Binary Tree Traversals (No-List Version)")
    print("=" * 60)

    # Build a sample binary tree:
    #
    #         1
    #        / \
    #       2   3
    #      / \   \
    #     4   5   6
    #
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.right = Node(6)

    # Show the tree structure
    print("\nTree structure (rotated 90°):")
    print_tree(root)

    # Traversals
    print("\nInorder   (left, root, right):")
    inorder(root)
    print()  # expected: 4 2 5 1 3 6

    print("Preorder  (root, left, right):")
    preorder(root)
    print()  # expected: 1 2 4 5 3 6

    print("Postorder (left, right, root):")
    postorder(root)
    print()  # expected: 4 5 2 6 3 1

    print("Level-order (breadth-first, top to bottom, left to right):")
    level_order(root)
    print()  # expected: 1 2 3 4 5 6
