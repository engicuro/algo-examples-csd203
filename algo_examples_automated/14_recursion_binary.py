"""
14_recursion_binary.py
=====================
Recursion Topic: Binary (Branching) Recursion

Binary recursion is when a function makes TWO recursive calls per invocation.
The call tree branches into two at each level, forming a binary tree of
calls.  This is common in algorithms that split a problem into two
sub-problems.

Examples covered:
  1. Fibonacci — the classic binary recursion example
  2. Binary sum — split a list in half and sum each half
  3. Tree traversal — in-order traversal of a binary tree

Key observation: binary recursion typically has exponential time complexity
unless memoization or divide-and-conquer is used.
"""

from typing import List, Optional


# ---------------------------------------------------------------------------
# 1. Fibonacci (Binary Recursion)
# ---------------------------------------------------------------------------

def fibonacci(n: int) -> int:
    """Return the n-th Fibonacci number using binary recursion.

    Fibonacci definition:
      F(0) = 0
      F(1) = 1
      F(n) = F(n-1) + F(n-2)  for n >= 2

    Each call spawns TWO recursive calls — this is binary recursion.
    The call tree has exponential size: O(2^n) calls total.

    Args:
        n: The index in the Fibonacci sequence (0-indexed).

    Returns:
        The n-th Fibonacci number.
    """
    # Base cases: F(0) = 0, F(1) = 1
    if n <= 1:
        return n

    # Binary recursion: TWO recursive calls!
    # F(n) = F(n-1) + F(n-2)
    # This creates a binary tree of calls where each node has 2 children.
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_memo(n: int, memo: dict = None) -> int:
    """Memoized Fibonacci — same recurrence, but O(n) time.

    By caching results, each unique subproblem is solved only once,
    collapsing the exponential call tree into a linear chain.
    """
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        memo[n] = n
        return n

    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


# ---------------------------------------------------------------------------
# 2. Binary Sum (Divide and Conquer)
# ---------------------------------------------------------------------------

def binary_sum(lst: List[int], low: int = 0, high: Optional[int] = None) -> int:
    """Compute the sum of a list by splitting it in half (binary recursion).

    Instead of processing one element at a time (linear recursion), we
    split the list into two halves and sum each half independently.

    Base case:  one element → return it
    Recursive case: split into two halves, sum each half, add results

    Time complexity: O(n) — every element is visited exactly once.
    Space complexity: O(log n) — call stack depth is logarithmic.

    Args:
        lst:  The list of integers.
        low:  Start index of the current range (inclusive).
        high: End index of the current range (inclusive).

    Returns:
        The sum of all elements in the range.
    """
    if high is None:
        high = len(lst) - 1

    # Base case: empty range
    if low > high:
        return 0

    # Base case: single element
    if low == high:
        return lst[low]

    # Recursive case: split in the middle and sum each half
    mid = (low + high) // 2

    # TWO recursive calls — binary recursion!
    left_sum = binary_sum(lst, low, mid)         # sum of left half
    right_sum = binary_sum(lst, mid + 1, high)   # sum of right half

    return left_sum + right_sum


# ---------------------------------------------------------------------------
# 3. Binary Tree Traversal
# ---------------------------------------------------------------------------

class TreeNode:
    """A simple binary tree node."""

    def __init__(self, value: int, left: 'Optional[TreeNode]' = None, right: 'Optional[TreeNode]' = None):
        self.value = value
        self.left = left
        self.right = right


def inorder_traversal(node: Optional[TreeNode]) -> List[int]:
    """In-order traversal of a binary tree using binary recursion.

    Visit left subtree → current node → right subtree.

    Base case:  node is None → return empty list
    Recursive case: recurse left, visit node, recurse right

    Args:
        node: The root of the subtree to traverse.

    Returns:
        A list of values in in-order sequence.
    """
    # Base case: empty subtree
    if node is None:
        return []

    # Binary recursion: two recursive calls (left and right)
    # 1. Traverse left subtree
    # 2. Visit current node
    # 3. Traverse right subtree
    result = []
    result.extend(inorder_traversal(node.left))   # first recursive call
    result.append(node.value)                      # visit
    result.extend(inorder_traversal(node.right))   # second recursive call
    return result


def tree_height(node: Optional[TreeNode]) -> int:
    """Compute the height of a binary tree using binary recursion.

    Height = number of edges on the longest path from root to leaf.
    An empty tree has height -1; a single node has height 0.

    Base case:  node is None → return -1
    Recursive case: 1 + max(height(left), height(right))
    """
    if node is None:
        return -1

    # Binary recursion: compute height of both subtrees
    left_height = tree_height(node.left)
    right_height = tree_height(node.right)

    return 1 + max(left_height, right_height)


if __name__ == "__main__":
    print("=" * 55)
    print("Recursion Example: Binary (Branching) Recursion")
    print("=" * 55)

    # --- 1. Fibonacci ---
    print("\n--- 1. Fibonacci (Binary Recursion) ---")
    print("Call tree for fibonacci(5):")
    print("""
                          fib(5)
                        /        \\
                    fib(4)        fib(3)
                   /     \\        /    \\
               fib(3)   fib(2)  fib(2)  fib(1)
              /    \\    /   \\   /  \\
          fib(2) fib(1) fib(1) fib(0) fib(1) fib(0)
          /   \\
      fib(1) fib(0)
    """)

    for i in range(11):
        print(f"  fibonacci({i:>2}) = {fibonacci(i):>4}")

    # Show redundancy: fib(5) makes 15 calls total
    print(f"\n  Note: fibonacci(5) makes 15 total calls (many redundant)")
    print(f"  With memoization, it makes only 9 unique calls")

    # --- 2. Binary Sum ---
    print("\n--- 2. Binary Sum (Divide and Conquer) ---")
    nums = [1, 2, 3, 4, 5, 6, 7, 8]
    total = binary_sum(nums)
    print(f"  List: {nums}")
    print(f"  binary_sum({nums}) = {total}")
    print(f"  Verification (built-in sum): {sum(nums)}")
    assert total == sum(nums)

    # Trace the binary recursion
    print(f"\n  Call trace for binary_sum([1,2,3,4]):")
    print("    binary_sum([1,2,3,4], 0, 3)")
    print("      ├─ binary_sum([1,2,3,4], 0, 1)  ← left half")
    print("      │   ├─ binary_sum(..., 0, 0) → 1  [base case]")
    print("      │   └─ binary_sum(..., 1, 1) → 2  [base case]")
    print("      │   → 1 + 2 = 3")
    print("      └─ binary_sum([1,2,3,4], 2, 3)  ← right half")
    print("          ├─ binary_sum(..., 2, 2) → 3  [base case]")
    print("          └─ binary_sum(..., 3, 3) → 4  [base case]")
    print("          → 3 + 4 = 7")
    print("    → 3 + 7 = 10")

    # --- 3. Tree Traversal ---
    print("\n--- 3. Binary Tree Traversal ---")

    # Build a sample tree:
    #        4
    #       / \
    #      2   6
    #     / \ / \
    #    1  3 5  7
    root = TreeNode(4,
        left=TreeNode(2,
            left=TreeNode(1),
            right=TreeNode(3)),
        right=TreeNode(6,
            left=TreeNode(5),
            right=TreeNode(7)))

    print("  Tree structure:")
    print("        4")
    print("       / \\")
    print("      2   6")
    print("     / \\ / \\")
    print("    1  3 5  7")

    print(f"\n  In-order traversal:  {inorder_traversal(root)}")
    print(f"  Expected (sorted):   [1, 2, 3, 4, 5, 6, 7]")
    assert inorder_traversal(root) == [1, 2, 3, 4, 5, 6, 7]

    print(f"  Tree height: {tree_height(root)}")
    print(f"  Expected height: 2")
    assert tree_height(root) == 2

    # Compare binary vs linear recursion
    print("\n--- Binary vs Linear Recursion Comparison ---")
    print("""
  Linear recursion (one call per level):
    factorial(n) → factorial(n-1) → factorial(n-2) → ... → base
    Call chain: straight line, depth = n

  Binary recursion (two calls per level):
    fibonacci(n) → fibonacci(n-1) AND fibonacci(n-2)
    Call tree: branches at each level, total calls ≈ O(2^n)

  Divide-and-conquer (two calls, but each on half the input):
    binary_sum → binary_sum(left_half) + binary_sum(right_half)
    Call tree: balanced binary tree, depth = log₂(n), total calls = O(n)
    """)
