# 16_recursion_tail.py
# Tail recursion examples with explanation, and how to convert to simple loops.
#
# What is tail recursion?
#   A function is tail-recursive if the recursive call is the LAST thing
#   the function does (there is nothing left to compute after the call returns).
#
# Why does it matter?
#   - Some languages optimize tail-recursive functions to avoid growing the
#     call stack (called "tail call optimization").
#   - Python does NOT do this optimization, so deep tail recursion can
#     still cause a stack overflow.
#   - However, understanding tail recursion helps you convert recursive
#     functions into simple loops, which Python prefers.
#
# Key ideas:
#   - Tail recursion: the recursive call is the final action.
#   - Non-tail recursion: work is done AFTER the recursive call returns.
#   - Conversion: use an "accumulator" parameter to carry the result forward,
#     then replace the recursion with a while loop.

from _structures import LinkedList


# ---- Tail-recursive factorial ----

def factorial_tail(n, accumulator=1):
    """Tail-recursive factorial.

    The recursive call is the LAST thing in the function.
    The 'accumulator' carries the running product forward.

    factorial_tail(5, 1)
      -> factorial_tail(4, 5)
      -> factorial_tail(3, 20)
      -> factorial_tail(2, 60)
      -> factorial_tail(1, 120)
      -> 120
    """
    # Base case: when n reaches 1 (or 0), return the accumulated result.
    if n <= 1:
        return accumulator

    # Tail-recursive case: pass the updated accumulator forward.
    # Nothing is left to do after this call returns.
    print("  factorial_tail(%d, acc=%d) -> factorial_tail(%d, acc=%d)" % (
        n, accumulator, n - 1, n * accumulator))
    return factorial_tail(n - 1, n * accumulator)


# ---- Non-tail-recursive factorial (for comparison) ----

def factorial_non_tail(n):
    """Non-tail-recursive factorial.

    The multiplication (n * ...) happens AFTER the recursive call returns,
    so this is NOT tail recursion.
    """
    if n <= 1:
        return 1

    # The recursive call is NOT the last thing -- we still multiply by n.
    print("  factorial(%d) = %d * factorial(%d)" % (n, n, n - 1))
    return n * factorial_non_tail(n - 1)


# ---- Converting tail recursion to a loop ----

def factorial_loop(n):
    """Convert tail-recursive factorial into a simple loop.

    This is what Python prefers: a loop instead of recursion.
    It uses constant memory (no growing call stack).
    """
    accumulator = 1
    print("  factorial_loop(%d): starting with acc=%d" % (n, accumulator))

    # The loop replaces the recursive calls.
    current = n
    while current > 1:
        print("    acc=%d * %d -> acc=%d" % (accumulator, current, accumulator * current))
        accumulator = accumulator * current
        current = current - 1

    print("  factorial_loop(%d) -> %d" % (n, accumulator))
    return accumulator


# ---- Tail-recursive sum of a list ----

def list_sum_tail(numbers, accumulator=0):
    """Tail-recursive sum of a list.

    Instead of slicing the list (which creates new lists), we use an index.
    """
    index = len(numbers) - 1  # start from the last element

    # We use a helper with an index so we avoid list slicing.
    return _list_sum_helper(numbers, index, accumulator)


def _list_sum_helper(numbers, index, accumulator):
    """Helper that walks backward through the list using tail recursion."""
    # Base case: we have processed all elements.
    if index < 0:
        return accumulator

    # Tail-recursive case: add current element to accumulator, move to previous.
    print("  sum_tail(index=%d, acc=%d) -> sum_tail(index=%d, acc=%d)" % (
        index, accumulator, index - 1, accumulator + numbers.get(index)))
    return _list_sum_helper(numbers, index - 1, accumulator + numbers.get(index))


# ---- Same sum converted to a loop ----

def list_sum_loop(numbers):
    """Convert the tail-recursive list sum into a simple loop."""
    accumulator = 0
    print("  list_sum_loop: starting with acc=%d" % accumulator)

    for i in range(len(numbers)):
        print("    acc=%d + numbers[%d]=%d -> acc=%d" % (
            accumulator, i, numbers.get(i), accumulator + numbers.get(i)))
        accumulator = accumulator + numbers.get(i)

    print("  list_sum_loop -> %d" % accumulator)
    return accumulator


if __name__ == "__main__":
    print("=== Tail-recursive factorial ===")
    print("factorial_tail(5) =", factorial_tail(5))

    print("\n=== Non-tail-recursive factorial (for comparison) ===")
    print("factorial_non_tail(5) =", factorial_non_tail(5))

    print("\n=== Tail-recursive factorial converted to a loop ===")
    print("factorial_loop(5) =", factorial_loop(5))

    print("\n=== Tail-recursive list sum ===")
    nums = LinkedList()
    for v in [1, 2, 3, 4, 5]:
        nums.append(v)
    print("List:", nums)
    print("list_sum_tail([1,2,3,4,5]) =", list_sum_tail(nums))

    print("\n=== Same sum using a loop ===")
    print("list_sum_loop([1,2,3,4,5]) =", list_sum_loop(nums))
