"""
12_recursion_analysis.py
========================
Recursion Topic: Analyzing Recursive Algorithms

This file demonstrates how to analyze recursive algorithms by:

  1. Drawing call trees (visualizing the recursion)
  2. Counting operations (comparisons, additions, etc.)
  3. Solving recurrence relations (e.g., T(n) = T(n-1) + O(1) for factorial)
  4. Analyzing Fibonacci — the classic example of redundant computation

Key concepts:
  - Call tree: a tree showing every recursive call made.
  - Operation count: how many basic operations the algorithm performs.
  - Recurrence relation: a mathematical equation describing the runtime.
  - Memoization: caching results to avoid redundant computation.

Recurrence relations covered:
  - Factorial:       T(n) = T(n-1) + O(1)  →  T(n) = O(n)
  - Fibonacci (naive): T(n) = T(n-1) + T(n-2) + O(1)  →  T(n) = O(2^n)
  - Fibonacci (memo):  T(n) = T(n-1) + O(1)  →  T(n) = O(n)
  - Binary search:    T(n) = T(n/2) + O(1)  →  T(n) = O(log n)
"""

from typing import Dict, List, Tuple
import time


# ---------------------------------------------------------------------------
# 1. Call Tree Visualization
# ---------------------------------------------------------------------------

def factorial_with_trace(n: int, depth: int = 0) -> int:
    """Compute factorial while printing the call tree.

    This helps visualize how recursion unfolds and resolves.
    """
    indent = "  " * depth
    print(f"{indent}factorial({n})  ← called")

    if n <= 1:
        print(f"{indent}→ return 1  [base case]")
        return 1

    result = n * factorial_with_trace(n - 1, depth + 1)
    print(f"{indent}→ return {n} * factorial({n-1}) = {result}")
    return result


# ---------------------------------------------------------------------------
# 2. Counting Operations
# ---------------------------------------------------------------------------

class OpCounter:
    """A simple counter that tracks the number of operations performed."""

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0


def factorial_counted(n: int, counter: OpCounter) -> int:
    """Factorial that counts each multiplication as one operation."""
    counter.increment()  # count this call
    if n <= 1:
        return 1
    return n * factorial_counted(n - 1, counter)


def fibonacci_counted(n: int, counter: OpCounter) -> int:
    """Naive recursive Fibonacci that counts each call as one operation.

    Note: this counts *calls*, not just multiplications — the number of
    calls grows exponentially with n.
    """
    counter.increment()  # count this call
    if n <= 1:
        return n
    return fibonacci_counted(n - 1, counter) + fibonacci_counted(n - 2, counter)


def fibonacci_memo_counted(n: int, counter: OpCounter, memo: Dict[int, int] = None) -> int:
    """Memoized Fibonacci that counts each *unique* call as one operation.

    With memoization, each value fib(0)..fib(n) is computed exactly once.
    """
    if memo is None:
        memo = {}
    counter.increment()

    if n in memo:
        return memo[n]

    if n <= 1:
        memo[n] = n
        return n

    memo[n] = fibonacci_memo_counted(n - 1, counter, memo) + fibonacci_memo_counted(n - 2, counter, memo)
    return memo[n]


# ---------------------------------------------------------------------------
# 3. Solving Recurrence Relations
# ---------------------------------------------------------------------------

def solve_factorial_recurrence(n: int) -> Tuple[int, int]:
    """Solve T(n) = T(n-1) + 1, T(0) = 1 for factorial.

    Returns (recursion_depth, total_operations).
    """
    # T(n) = T(n-1) + 1
    # T(n) = T(n-2) + 1 + 1
    # T(n) = T(n-k) + k
    # When k = n: T(n) = T(0) + n = 1 + n
    depth = n
    operations = n + 1  # n multiplications + 1 base case check
    return depth, operations


def solve_fibonacci_recurrence(n: int) -> Dict[str, int]:
    """Analyze the naive Fibonacci recurrence T(n) = T(n-1) + T(n-2) + 1.

    The exact solution is T(n) = 2 * F(n+1) - 1, where F is the Fibonacci
    sequence.  This grows as O(φ^n) where φ ≈ 1.618 (golden ratio).

    Returns a dict with analysis results.
    """
    # Compute Fibonacci numbers iteratively for the analysis
    if n <= 1:
        exact_calls = n + 1
    else:
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        # T(n) = 2 * F(n+1) - 1
        exact_calls = 2 * b - 1 if n > 0 else 1

    return {
        "n": n,
        "exact_calls_naive": exact_calls,
        "approx_exponential": f"O(φ^n) where φ ≈ 1.618",
        "memoized_calls": n + 1,  # each value computed once
    }


# ---------------------------------------------------------------------------
# 4. Operation counting comparison table
# ---------------------------------------------------------------------------

def print_operation_comparison(max_n: int = 15):
    """Print a table comparing operation counts for factorial vs Fibonacci."""
    print(f"\n{'n':>3}  {'Factorial calls':>16}  {'Fibonacci naive calls':>22}  {'Fibonacci memo calls':>20}")
    print("-" * 65)

    for n in range(max_n + 1):
        # Factorial
        c1 = OpCounter()
        factorial_counted(n, c1)
        fact_calls = c1.count

        # Fibonacci (naive) — skip large n to avoid long waits
        if n <= 30:
            c2 = OpCounter()
            fibonacci_counted(n, c2)
            fib_calls = c2.count
        else:
            fib_calls = "too many"

        # Fibonacci (memoized)
        c3 = OpCounter()
        fibonacci_memo_counted(n, c3)
        fib_memo_calls = c3.count

        print(f"{n:>3}  {fact_calls:>16}  {str(fib_calls):>22}  {fib_memo_calls:>20}")


if __name__ == "__main__":
    print("=" * 60)
    print("Recursion Analysis: Call Trees, Operation Counts & Recurrences")
    print("=" * 60)

    # --- 1. Call tree for factorial ---
    print("\n--- 1. Factorial Call Tree (n=4) ---")
    factorial_with_trace(4)

    # --- 2. Call tree for Fibonacci (small n to keep it manageable) ---
    print("\n--- 2. Fibonacci Call Tree (n=5, naive) ---")
    print("  fib(5)")
    print("  ├── fib(4)")
    print("  │   ├── fib(3)")
    print("  │   │   ├── fib(2)")
    print("  │   │   │   ├── fib(1) → 1")
    print("  │   │   │   └── fib(0) → 0")
    print("  │   │   └── fib(1) → 1")
    print("  │   └── fib(2)")
    print("  │       ├── fib(1) → 1")
    print("  │       └── fib(0) → 0")
    print("  └── fib(3)")
    print("      ├── fib(2)")
    print("      │   ├── fib(1) → 1")
    print("      │   └── fib(0) → 0")
    print("      └── fib(1) → 1")
    print(f"  Result: {fibonacci_counted(5, OpCounter())}")

    # --- 3. Operation counting ---
    print("\n--- 3. Operation Counting ---")
    for n in [5, 10, 15]:
        c = OpCounter()
        factorial_counted(n, c)
        print(f"  factorial({n}): {c.count} operations (calls)")

        c = OpCounter()
        fibonacci_counted(n, c)
        print(f"  fibonacci({n}) [naive]: {c.count} operations (calls)")

        c = OpCounter()
        fibonacci_memo_counted(n, c)
        print(f"  fibonacci({n}) [memo]:  {c.count} operations (calls)")
        print()

    # --- 4. Recurrence relation solutions ---
    print("--- 4. Solving Recurrence Relations ---")
    print("\n  Factorial recurrence:")
    print("    T(n) = T(n-1) + O(1),  T(0) = O(1)")
    print("    Solution: T(n) = O(n)")
    depth, ops = solve_factorial_recurrence(10)
    print(f"    For n=10: depth={depth}, operations≈{ops}")

    print("\n  Fibonacci recurrence (naive):")
    print("    T(n) = T(n-1) + T(n-2) + O(1)")
    print("    Solution: T(n) = O(φ^n)  where φ ≈ 1.618 (golden ratio)")
    info = solve_fibonacci_recurrence(10)
    print(f"    For n=10: exact naive calls = {info['exact_calls_naive']}")
    print(f"    Memoized calls = {info['memoized_calls']}")

    print("\n  Binary search recurrence:")
    print("    T(n) = T(n/2) + O(1)")
    print("    Solution: T(n) = O(log n)  (Master Theorem, Case 2)")

    # --- 5. Full comparison table ---
    print_operation_comparison(15)

    # --- 6. Timing comparison ---
    print("\n--- 5. Timing Comparison (n=30) ---")
    n = 30

    start = time.perf_counter()
    fibonacci_counted(n, OpCounter())
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    fibonacci_memo_counted(n, OpCounter())
    memo_time = time.perf_counter() - start

    print(f"  Fibonacci({n}) naive:  {naive_time:.6f}s")
    print(f"  Fibonacci({n}) memo:   {memo_time:.6f}s")
    if memo_time > 0:
        print(f"  Speedup: {naive_time / memo_time:.1f}x")
