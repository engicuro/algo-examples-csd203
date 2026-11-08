# 13_recursion_linear.py
# Linear recursion examples: sum of sequence, find max, power function.
# "Linear recursion" means each function call makes at most ONE
# recursive call.  The recursion goes in a straight line, like a chain.
#
# Key ideas:
#   - Each call does a small piece of work, then passes the rest to
#     the next recursive call.
#   - The base case stops the chain.
#   - Results bubble back up through the chain as returns.


# ---- Sum of a sequence ----

def sequence_sum(numbers, index=0):
    """Return the sum of all numbers using recursion (index-based).

    Base case: reached end of sequence -> sum is 0.
    Recursive case: current element + sum of the rest.
    """
    # Base case: we've gone past the end of the sequence.
    if index >= len(numbers):
        return 0

    # Recursive case: add the current element to the sum of the rest.
    current = numbers[index]
    print("  sequence_sum at index %d (value=%d)" % (index, current))
    result = current + sequence_sum(numbers, index + 1)
    print("  sequence_sum at index %d -> %d" % (index, result))
    return result


# ---- Find the maximum value in a sequence ----

def sequence_max(numbers, index=0):
    """Return the largest number in the sequence using recursion (index-based).

    Base case: only one element left -> that element is the max.
    Recursive case: compare the current element with the max of the rest.
    """
    # Base case: only one element left, it is the maximum.
    if index >= len(numbers) - 1:
        print("  sequence_max at index %d -> %d  (only one element)" % (index, numbers[index]))
        return numbers[index]

    # Recursive case: find the max of the rest, then compare.
    current = numbers[index]
    print("  sequence_max at index %d: comparing %d with max of rest" % (index, current))
    max_of_rest = sequence_max(numbers, index + 1)

    if current > max_of_rest:
        print("  sequence_max at index %d -> %d  (%d > %d)" % (index, current, current, max_of_rest))
        return current
    else:
        print("  sequence_max at index %d -> %d  (%d >= %d)" % (index, max_of_rest, current, max_of_rest))
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
    print("=== Sum of a sequence ===")
    nums = (1, 2, 3, 4, 5)
    print("Sequence:", nums)
    total = sequence_sum(nums)
    print("Sum =", total)

    print("\n=== Find max in a sequence ===")
    nums2 = (7, 2, 9, 1, 5, 3)
    print("Sequence:", nums2)
    biggest = sequence_max(nums2)
    print("Max =", biggest)

    print("\n=== Power function ===")
    print("2^5 =", power(2, 5))
