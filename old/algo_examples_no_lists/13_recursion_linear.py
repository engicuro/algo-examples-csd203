# 13_recursion_linear.py
# Linear recursion examples: sum of list, find max, power function.
# "Linear recursion" means each function call makes at most ONE
# recursive call.  The recursion goes in a straight line, like a chain.
#
# Key ideas:
#   - Each call does a small piece of work, then passes the rest to
#     the next recursive call.
#   - The base case stops the chain.
#   - Results bubble back up through the chain as returns.

from _structures import LinkedList


def _linkedlist_from_list(values):
    """Build a LinkedList from a Python list of values."""
    result = LinkedList()
    for v in values:
        result.append(v)
    return result


# ---- Sum of a list ----

def list_sum(numbers):
    """Return the sum of all numbers in the list using recursion.

    Base case: empty list -> sum is 0.
    Recursive case: first element + sum of the rest.
    """
    # Base case: an empty list sums to 0.
    if len(numbers) == 0:
        return 0

    # Recursive case: add the first element to the sum of the rest.
    first = numbers.get(0)
    rest = LinkedList()
    for i in range(1, len(numbers)):
        rest.append(numbers.get(i))
    print("  list_sum(%s) = %d + list_sum(%s)" % (numbers, first, rest))
    result = first + list_sum(rest)
    print("  list_sum(%s) -> %d" % (numbers, result))
    return result


# ---- Find the maximum value in a list ----

def list_max(numbers):
    """Return the largest number in the list using recursion.

    Base case: a list with one element -> that element is the max.
    Recursive case: compare the first element with the max of the rest.
    """
    # Base case: only one element, it is the maximum.
    if len(numbers) == 1:
        print("  list_max(%s) -> %d  (only one element)" % (numbers, numbers.get(0)))
        return numbers.get(0)

    # Recursive case: find the max of the rest, then compare.
    first = numbers.get(0)
    rest = LinkedList()
    for i in range(1, len(numbers)):
        rest.append(numbers.get(i))
    print("  list_max(%s): comparing %d with max of %s" % (numbers, first, rest))
    max_of_rest = list_max(rest)

    if first > max_of_rest:
        print("  list_max(%s) -> %d  (%d > %d)" % (numbers, first, first, max_of_rest))
        return first
    else:
        print("  list_max(%s) -> %d  (%d >= %d)" % (numbers, max_of_rest, first, max_of_rest))
        return max_of_rest


# ---- Power function (base^exponent) ----

def power(base, exponent):
    """Return base raised to the exponent using recursion.

    Base case: exponent is 0 -> result is 1.
    Recursive case: base^exponent = base * base^(exponent-1).
    """
    # Base case: anything to the power of 0 is 1.
    if exponent <= 0:
        return 1

    # Recursive case: multiply base by base^(exponent-1).
    print("  power(%d, %d) = %d * power(%d, %d)" % (
        base, exponent, base, base, exponent - 1))
    result = base * power(base, exponent - 1)
    print("  power(%d, %d) -> %d" % (base, exponent, result))
    return result


if __name__ == "__main__":
    print("=== Sum of a list ===")
    nums = _linkedlist_from_list([1, 2, 3, 4, 5])
    print("List:", nums)
    total = list_sum(nums)
    print("Sum =", total)

    print("\n=== Find max in a list ===")
    nums2 = _linkedlist_from_list([7, 2, 9, 1, 5, 3])
    print("List:", nums2)
    biggest = list_max(nums2)
    print("Max =", biggest)

    print("\n=== Power function ===")
    print("2^5 =", power(2, 5))
