"""
13_recursion_linear.py
=====================
Recursion Topic: Linear Recursion

Linear recursion is the simplest form of recursion: each function call
makes at most ONE recursive call (besides the current call).  The call
chain forms a straight line — no branching.

Examples covered:
  1. Sum of a list — accumulate elements recursively
  2. Find maximum — compare current element with max of the rest
  3. Power function — multiply base by itself n times recursively

All three have:
  - One base case (simplest input)
  - One recursive call that reduces the problem size by 1
  - O(n) time and O(n) space (call stack)
"""

from typing import List, Optional


# ---------------------------------------------------------------------------
# 1. Sum of a List
# ---------------------------------------------------------------------------

def recursive_sum(lst: List[int], index: int = 0) -> int:
    """Return the sum of all elements in a list using linear recursion.

    Base case:  index reaches the end of the list → return 0
    Recursive case: return lst[index] + sum of remaining elements

    Args:
        lst:    The list of integers to sum.
        index:  Current position in the list (used internally for recursion).

    Returns:
        The sum of all elements.
    """
    # Base case: we've processed all elements
    if index >= len(lst):
        return 0

    # Recursive case: current element + sum of the rest
    return lst[index] + recursive_sum(lst, index + 1)


# ---------------------------------------------------------------------------
# 2. Find Maximum
# ---------------------------------------------------------------------------

def recursive_max(lst: List[int], index: int = 0) -> Optional[int]:
    """Return the maximum element in a list using linear recursion.

    Base case:  only one element left → return it
    Recursive case: compare current element with max of the rest

    Args:
        lst:    The list of integers.
        index:  Current position in the list.

    Returns:
        The maximum element, or None if the list is empty.
    """
    # Base case: empty list
    if index >= len(lst):
        return None

    # Base case: last element — it is the max of a single-element list
    if index == len(lst) - 1:
        return lst[index]

    # Recursive case: find the max of the rest of the list
    max_of_rest = recursive_max(lst, index + 1)

    # Compare current element with the max of the rest
    return lst[index] if lst[index] > max_of_rest else max_of_rest


# ---------------------------------------------------------------------------
# 3. Power Function (base^exp)
# ---------------------------------------------------------------------------

def recursive_power(base: float, exp: int) -> float:
    """Compute base raised to the power exp using linear recursion.

    base^exp = base * base^(exp-1)

    Base case:  exp == 0 → return 1  (any number to the power 0 is 1)
    Recursive case: base * recursive_power(base, exp - 1)

    Args:
        base: The base number.
        exp:  The exponent (non-negative integer).

    Returns:
        base raised to the power exp.

    Raises:
        ValueError: If exp is negative.
    """
    if exp < 0:
        raise ValueError(f"Negative exponent not supported: {exp}")

    # Base case: anything raised to 0 is 1
    if exp == 0:
        return 1

    # Recursive case: base^exp = base * base^(exp-1)
    return base * recursive_power(base, exp - 1)


# ---------------------------------------------------------------------------
# 4. Alternative: Tail-recursive sum (preview of tail recursion)
# ---------------------------------------------------------------------------

def linear_sum_tail(lst: List[int], index: int = 0, accumulator: int = 0) -> int:
    """Tail-recursive version of list sum.

    In tail recursion, the recursive call is the LAST operation — there is
    no pending computation after the call returns.  This allows some
    languages/compilers to optimize away the call stack (tail-call
    elimination).  Python does NOT optimize tail calls, but the pattern
    is still useful to understand.

    Base case:  index >= len(lst) → return accumulator
    Recursive case: advance index, add current element to accumulator
    """
    if index >= len(lst):
        return accumulator
    return linear_sum_tail(lst, index + 1, accumulator + lst[index])


if __name__ == "__main__":
    print("=" * 55)
    print("Recursion Example: Linear Recursion")
    print("=" * 55)

    sample_list = [3, 7, 2, 9, 4, 1, 8, 5]
    print(f"\nSample list: {sample_list}")

    # 1. Sum
    total = recursive_sum(sample_list)
    print(f"\n1. Sum of list:")
    print(f"   recursive_sum({sample_list}) = {total}")
    print(f"   Verification (built-in sum): {sum(sample_list)}")
    assert total == sum(sample_list)

    # 2. Max
    maximum = recursive_max(sample_list)
    print(f"\n2. Maximum element:")
    print(f"   recursive_max({sample_list}) = {maximum}")
    print(f"   Verification (built-in max): {max(sample_list)}")
    assert maximum == max(sample_list)

    # Edge case: single element
    single = [42]
    print(f"\n   Edge case — single element {single}:")
    print(f"   recursive_max({single}) = {recursive_max(single)}")

    # Edge case: empty list
    empty: List[int] = []
    print(f"\n   Edge case — empty list {empty}:")
    print(f"   recursive_max({empty}) = {recursive_max(empty)}")

    # 3. Power
    print(f"\n3. Power function:")
    for base, exp in [(2, 10), (3, 4), (5, 0), (1.5, 3)]:
        result = recursive_power(base, exp)
        expected = base ** exp
        print(f"   {base}^{exp} = {result}  (expected: {expected}, match: {result == expected})")
        assert result == expected

    # 4. Tail-recursive sum
    print(f"\n4. Tail-recursive sum (same result, different pattern):")
    tail_total = linear_sum_tail(sample_list)
    print(f"   linear_sum_tail({sample_list}) = {tail_total}")
    assert tail_total == total

    # Visualize the call chain
    print("\n--- Call chain visualization: recursive_sum([3, 7, 2]) ---")
    print("  recursive_sum([3,7,2], index=0)")
    print("    → 3 + recursive_sum([3,7,2], index=1)")
    print("       → 7 + recursive_sum([3,7,2], index=2)")
    print("          → 2 + recursive_sum([3,7,2], index=3)")
    print("             → 0  [base case: index >= len(lst)]")
    print("          ← 2 + 0 = 2")
    print("       ← 7 + 2 = 9")
    print("    ← 3 + 9 = 12")
    print("  Result: 12")
