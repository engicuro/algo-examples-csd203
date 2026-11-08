"""
09_recursion_factorial.py
=========================
Recursion Topic: Factorial Function

The factorial of a non-negative integer n (written as n!) is the product of all
positive integers less than or equal to n.

  n! = n × (n-1) × (n-2) × ... × 2 × 1
  0! = 1  (by definition)

This example demonstrates the two essential parts of every recursive function:

  1. Base case  – the simplest input that can be answered directly without
     further recursion.  For factorial, 0! = 1 and 1! = 1.
  2. Recursive case – the function calls itself with a *smaller* argument,
     moving toward the base case.  n! = n × (n-1)!

Time complexity : O(n)
Space complexity: O(n)  (call stack depth)
"""


def factorial(n: int) -> int:
    """Return n! using recursion.

    Args:
        n: A non-negative integer.

    Returns:
        The factorial of n.

    Raises:
        ValueError: If n is negative.
    """
    # --- Base case ---
    # When n is 0 or 1, we know the answer immediately: 0! = 1 and 1! = 1.
    # This stops the recursion from continuing indefinitely.
    if n <= 1:
        return 1

    # --- Recursive case ---
    # n! = n × (n-1)!
    # We reduce the problem size by 1 on each call, guaranteeing we reach
    # the base case after exactly n recursive calls.
    if n < 0:
        raise ValueError(f"Factorial is not defined for negative numbers: {n}")
    return n * factorial(n - 1)


def factorial_iterative(n: int) -> int:
    """Return n! using an iterative loop (for comparison).

    This is the equivalent iterative version that avoids the call-stack
    overhead of the recursive approach.
    """
    if n < 0:
        raise ValueError(f"Factorial is not defined for negative numbers: {n}")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    print("=" * 55)
    print("Recursion Example: Factorial")
    print("=" * 55)

    # Demonstrate the base case and a few recursive cases
    for i in range(11):
        result = factorial(i)
        print(f"  {i}! = {result}")

    print()

    # Compare recursive vs iterative results
    print("Verification (recursive == iterative):")
    for i in range(11):
        assert factorial(i) == factorial_iterative(i), f"Mismatch at {i}!"
        print(f"  {i}!  ✓  (both return {factorial(i)})")

    # Show the call stack in action
    print()
    print("Call stack trace for factorial(5):")
    print("  factorial(5)")
    print("    → 5 * factorial(4)")
    print("         → 4 * factorial(3)")
    print("              → 3 * factorial(2)")
    print("                   → 2 * factorial(1)")
    print("                        → 1  (base case reached)")
    print("                   ← 2 * 1 = 2")
    print("              ← 3 * 2 = 6")
    print("         ← 4 * 6 = 24")
    print("    ← 5 * 24 = 120")
    print("  Result: 120")
