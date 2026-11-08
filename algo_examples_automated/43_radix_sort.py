"""
Radix Sort (LSD - Least Significant Digit)
==========================================

Radix sort is a non-comparative integer sorting algorithm that sorts numbers
by processing individual digits.  LSD (Least Significant Digit) radix sort
starts from the rightmost (least significant) digit and moves leftward,
using a stable sub-sort (counting sort) at each digit position.

Key properties:
    - Stable: equal elements preserve their original relative order.
    - Not in-place: requires auxiliary arrays for the counting sort passes.
    - Time complexity:  O(d * (n + k))
        d = number of digits in the largest number
        n = number of elements in the array
        k = radix (base), typically 10 for decimal digits
    - Space complexity: O(n + k)
        For the output array (n) and the count array (k) used in each pass.
    - Best-case, worst-case, and average-case are all O(d * (n + k))
      because every digit position is always processed regardless of input order.

Why radix sort matters:
    When the range of digit values (k) is small (e.g., base-10 digits 0-9)
    and the number of digits (d) is bounded, radix sort runs in linear time
    — faster than comparison-based sorts which are bounded by O(n log n).
    This makes it ideal for sorting fixed-width integers, strings, or
    records with integer keys.
"""

from typing import List


def counting_sort_for_radix(arr: List[int], exp: int) -> List[int]:
    """Sort ``arr`` stably by the digit at position ``exp`` using counting sort.

    ``exp`` is the positional multiplier:
        exp=1  → sorts by the ones (10^0) digit
        exp=10 → sorts by the tens (10^1) digit
        exp=100 → sorts by the hundreds (10^2) digit, and so on.

    This subroutine must be *stable* — elements with the same digit at
    position ``exp`` must retain their relative order from the input.
    Stability is what allows radix sort to correctly sort by progressively
    more significant digits: after sorting by a less significant digit,
    the order established for equal more-significant digits is preserved.

    Args:
        arr:  List of non-negative integers to sort by a single digit position.
        exp:  The digit position multiplier (1, 10, 100, …).

    Returns:
        A new list sorted by the digit at position ``exp``.
    """
    n = len(arr)
    output = [0] * n          # Output array that will hold the sorted result
    count = [0] * 10          # Count array for digits 0..9 (radix = 10)

    # --- Count occurrences of each digit at position exp ---
    # We extract the digit using (arr[i] // exp) % 10.
    # For exp=1 this gives the ones digit; for exp=10 the tens digit, etc.
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1

    # --- Transform count into cumulative counts ---
    # count[i] now holds the number of elements with digit <= i.
    # This tells us the *ending position* (1-indexed) for each digit
    # in the output array, which is essential for placing elements
    # in the correct order while maintaining stability.
    for i in range(1, 10):
        count[i] += count[i - 1]

    # --- Build the output array in reverse order ---
    # We iterate from the end of arr to the beginning so that elements
    # with the same digit retain their original relative order.
    # This reverse traversal is the key to stability in counting sort.
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        count[digit] -= 1
        output[count[digit]] = arr[i]

    # Copy the sorted output back into arr so the caller sees the result.
    for i in range(n):
        arr[i] = output[i]

    return arr


def radix_sort(arr: List[int]) -> List[int]:
    """Sort a list of non-negative integers using LSD radix sort.

    The algorithm processes digits from least significant to most significant,
    calling counting_sort_for_radix at each position.  After processing all
    digit positions, the array is fully sorted.

    Steps:
        1. Find the maximum value to determine how many digit positions exist.
        2. For each digit position (ones, tens, hundreds, …):
             a. Use counting sort to sort the array by that digit.
             b. The stability of counting sort preserves the order from
                previous (less significant) digit passes.
        3. After the most significant digit has been processed, the array
           is completely sorted.

    Why we stop at the maximum value:
        Numbers smaller than the maximum will have leading zeros at the
        higher digit positions.  Sorting by those leading zeros is a no-op
        (all elements have digit 0), so it doesn't change the array — but
        we still need to process up to the maximum value's digit count to
        ensure the most significant digit of the largest number is handled.

    Args:
        arr: List of non-negative integers to sort.

    Returns:
        The sorted list in ascending order.
    """
    if not arr:
        return arr

    # Find the maximum value — its number of digits determines
    # how many passes of counting sort we need.
    max_value = max(arr)

    # Process each digit position: 1 (ones), 10 (tens), 100 (hundreds), …
    # Stop when exp exceeds max_value because all digits have been processed.
    exp = 1
    while max_value // exp > 0:
        arr = counting_sort_for_radix(arr, exp)
        exp *= 10

    return arr


def radix_sort_visualized(arr: List[int]) -> List[int]:
    """Sort a list of non-negative integers using LSD radix sort, printing
    the array state after each digit-position pass for educational purposes.

    Visualization helps understand how radix sort progressively orders the
    data — first by ones, then by tens, then by hundreds, and so on —
    until the entire array is sorted.

    Args:
        arr: List of non-negative integers to sort.

    Returns:
        The sorted list in ascending order.
    """
    if not arr:
        print("Empty array — nothing to sort.")
        return arr

    max_value = max(arr)
    exp = 1
    pass_num = 1

    print(f"Initial array:  {arr}")
    print(f"Maximum value:  {max_value}")
    print(f"Digit passes needed: {len(str(max_value))}")
    print("-" * 50)

    while max_value // exp > 0:
        digit_name = _digit_position_name(exp)
        print(f"\nPass {pass_num} — sorting by {digit_name} (exp={exp}):")
        arr = counting_sort_for_radix(arr, exp)
        print(f"  Array state:  {arr}")
        exp *= 10
        pass_num += 1

    print("-" * 50)
    print(f"Final sorted array: {arr}")
    return arr


def _digit_position_name(exp: int) -> str:
    """Return a human-readable name for a digit position based on exp.

    Args:
        exp: The positional multiplier (1, 10, 100, …).

    Returns:
        A string like 'ones (10^0)', 'tens (10^1)', etc.
    """
    names = {1: "ones", 10: "tens", 100: "hundreds", 1000: "thousands",
             10000: "ten-thousands", 100000: "hundred-thousands"}
    if exp in names:
        return f"{names[exp]} (10^{len(str(exp)) - 1})"
    power = len(str(exp)) - 1
    return f"10^{power} position"


if __name__ == "__main__":
    # --- Example usage ---
    sample = [170, 45, 75, 90, 802, 24, 2, 66]

    print("=" * 50)
    print("  Radix Sort (LSD) — Educational Demo")
    print("=" * 50)

    # Demonstrate the basic sort
    data = sample.copy()
    sorted_data = radix_sort(data)
    print(f"\nBasic sort result: {sorted_data}")

    # Demonstrate the step-by-step visualization
    print("\n" + "=" * 50)
    print("  Step-by-step Visualization")
    print("=" * 50)
    data_viz = sample.copy()
    radix_sort_visualized(data_viz)

    # --- Complexity analysis summary ---
    #
    # Time Complexity:  O(d * (n + k))
    #   d = number of digits in the largest number
    #   n = number of elements
    #   k = radix (10 for decimal)
    #
    #   Each of the d passes does O(n + k) work:
    #     - O(n) to count digits and build the output
    #     - O(k) to compute cumulative counts
    #   Total: d passes × O(n + k) per pass = O(d * (n + k))
    #
    #   For fixed-width integers (e.g., 32-bit), d is constant,
    #   so radix sort runs in O(n) linear time.
    #
    # Space Complexity: O(n + k)
    #   - O(n) for the output array (reused across passes)
    #   - O(k) for the count array (10 entries for decimal digits)
    #   - O(n) for the input copy if we don't mutate in-place
    #   Total: O(n + k)
    #
    # Comparison with comparison-based sorts:
    #   - Merge sort:  O(n log n) time, O(n) space
    #   - Quick sort:  O(n log n) average, O(n) space
    #   - Radix sort:  O(d * (n + k)) time, O(n + k) space
    #   Radix sort wins when d is small relative to log n.
