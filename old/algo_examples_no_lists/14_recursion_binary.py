# 14_recursion_binary.py
# Binary recursion examples: Fibonacci and binary sum.
# "Binary recursion" means each function call makes TWO recursive calls.
# This creates a tree of calls, not a straight chain.
#
# Key ideas:
#   - Binary recursion often has exponential time complexity.
#   - Each call branches into two more calls.
#   - Print traces help visualize the branching tree.

from _structures import IntArray


# ---- Fibonacci (binary recursion) ----

def fibonacci(n, depth=0):
    """Return the nth Fibonacci number using binary recursion.

    Each call branches into TWO recursive calls: fib(n-1) and fib(n-2).
    This makes a tree of calls.
    """
    indent = "  " * depth  # indent to show depth in the call tree

    # Base cases
    if n <= 0:
        print("%sfib(%d) -> 0  (base case)" % (indent, n))
        return 0
    if n == 1:
        print("%sfib(%d) -> 1  (base case)" % (indent, n))
        return 1

    # Recursive case: two recursive calls!
    print("%sfib(%d) = fib(%d) + fib(%d)" % (indent, n, n - 1, n - 2))
    left = fibonacci(n - 1, depth + 1)
    right = fibonacci(n - 2, depth + 1)
    result = left + right
    print("%sfib(%d) -> %d  (%d + %d)" % (indent, n, result, left, right))
    return result


# ---- Binary sum: sum a list by splitting it in half ----

def binary_sum(numbers, low, high):
    """Return the sum of numbers[low..high] using binary recursion.

    Instead of taking one element off the front (linear recursion),
    we split the list in half and sum each half separately.
    This is closer to how a divide-and-conquer algorithm works.
    """
    # Base case: the range is empty.
    if low > high:
        return 0

    # Base case: only one element in the range.
    if low == high:
        print("  binary_sum(%s[%d:%d]) -> %d  (single element)" % (
            numbers, low, high, numbers.get(low)))
        return numbers.get(low)

    # Recursive case: split the range in half.
    mid = (low + high) // 2
    print("  binary_sum(%s[%d:%d]) -> binary_sum(%s[%d:%d]) + binary_sum(%s[%d:%d])" % (
        numbers, low, high, numbers, low, mid, numbers, mid + 1, high))

    left_sum = binary_sum(numbers, low, mid)
    right_sum = binary_sum(numbers, mid + 1, high)
    result = left_sum + right_sum
    print("  binary_sum(%s[%d:%d]) -> %d  (%d + %d)" % (
        numbers, low, high, result, left_sum, right_sum))
    return result


if __name__ == "__main__":
    print("=== Fibonacci (binary recursion) ===")
    print("fib(5):")
    result = fibonacci(5)
    print("fib(5) =", result)

    print("\n=== Binary sum of a list ===")
    nums = IntArray(6)
    values = [1, 2, 3, 4, 5, 6]
    for i in range(len(values)):
        nums.set(i, values[i])
    print("List:", nums)
    total = binary_sum(nums, 0, len(nums) - 1)
    print("Sum =", total)
