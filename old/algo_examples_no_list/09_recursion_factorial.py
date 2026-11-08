# 09_recursion_factorial.py
# Factorial using simple recursion.
# The factorial of n (written n!) is n * (n-1) * (n-2) * ... * 1.
# By definition, 0! = 1.
#
# Key ideas:
#   - Base case: when n is 0 or 1, return 1 (stop recursing).
#   - Recursive case: n * factorial(n - 1) (keep breaking the problem down).


def factorial(n):
    """Return the factorial of n using recursion."""
    # Base case: 0! = 1 and 1! = 1
    if n <= 1:
        print("  factorial(%d) -> 1  (base case)" % n)
        return 1

    # Recursive case: n! = n * (n-1)!
    print("  factorial(%d) = %d * factorial(%d)" % (n, n, n - 1))
    result = n * factorial(n - 1)
    print("  factorial(%d) -> %d  (returning)" % (n, result))
    return result


def factorial_with_trace(n):
    """Same as factorial but with indentation to show call depth."""
    # We use a helper so the user calls with just the number.
    return _factorial_helper(n, 0)


def _factorial_helper(n, depth):
    """Helper that tracks how deep we are in the recursion."""
    indent = "  " * depth  # two spaces per level of recursion

    # Base case
    if n <= 1:
        print("%sfactorial(%d) -> 1  (base case)" % (indent, n))
        return 1

    # Recursive case
    print("%sfactorial(%d) = %d * factorial(%d)" % (indent, n, n, n - 1))
    result = n * _factorial_helper(n - 1, depth + 1)
    print("%sfactorial(%d) -> %d" % (indent, n, result))
    return result


if __name__ == "__main__":
    print("=== Simple Factorial (no trace) ===")
    print("factorial(5) =", factorial(5))

    print("\n=== Factorial with Call Trace ===")
    factorial_with_trace(5)

    print("\n=== Factorial of 0 (edge case) ===")
    print("factorial(0) =", factorial(0))

    print("\n=== Factorial of 1 (edge case) ===")
    print("factorial(1) =", factorial(1))
