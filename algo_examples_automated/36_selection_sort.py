"""
36_selection_sort.py - Selection Sort Algorithm

Selection sort is a simple comparison-based sorting algorithm. It works by
dividing the list into a sorted prefix and an unsorted suffix. On each
iteration, it scans the unsorted suffix to find the minimum element and
swaps it into the correct position at the end of the sorted prefix.

Key characteristics:
  - In-place: requires no additional arrays (O(1) extra space).
  - Unstable: equal elements may change relative order during swaps.
  - Performance: always O(n²) comparisons regardless of input order.
    This makes it inefficient on large lists, but it is useful for
    educational purposes and for situations where write cost is high
    (it performs at most n-1 swaps).

Time complexity:
  - Best case:    O(n²)  — still scans the unsorted portion every pass.
  - Worst case:   O(n²)  — same as best; input order doesn't matter.
  - Average case: O(n²)  — nested loops over n elements.

Space complexity:
  - O(1) auxiliary — only a constant number of extra variables (index
    trackers and a temporary swap variable). The sort is performed
    in-place on the original list.

Why learn selection sort?
  - It illustrates the greedy paradigm: make the locally optimal choice
    (pick the minimum) at each step.
  - It is easy to understand and implement, making it a good starting
    point for learning sorting algorithms.
  - Its O(1) swap count is useful when writes are expensive (e.g.,
    flash memory with limited write cycles).
"""

from typing import List


def selection_sort(arr: List[int]) -> List[int]:
    """Sort a list of integers in ascending order using selection sort.

    The algorithm maintains two subarrays within the given list:
      1. The sorted prefix (left side), which grows by one element each pass.
      2. The unsorted suffix (right side), which shrinks by one element each pass.

    On each pass, the minimum element from the unsorted suffix is selected
    and swapped with the first element of the unsorted suffix, effectively
    extending the sorted prefix by one position.

    Args:
        arr: The list of integers to sort. Modified in-place.

    Returns:
        The same list object, now sorted in ascending order.

    Example:
        >>> selection_sort([64, 25, 12, 22, 11])
        [11, 12, 22, 25, 64]
    """
    n: int = len(arr)

    # Outer loop: the boundary between sorted and unsorted portions.
    # After each iteration, the element at index `i` is in its final
    # sorted position, so the sorted prefix grows from left to right.
    for i in range(n - 1):
        # Assume the first element of the unsorted portion is the minimum.
        # We will verify this by scanning the rest of the unsorted suffix.
        min_index: int = i

        # Inner loop: scan the unsorted suffix to find the true minimum.
        # Starting from i+1 because elements at indices 0..i-1 are already
        # sorted and in their final positions.
        for j in range(i + 1, n):
            # If we find an element smaller than our current minimum,
            # update min_index to track this new minimum's position.
            # We compare values, not indices, to ensure correctness.
            if arr[j] < arr[min_index]:
                min_index = j

        # Swap the found minimum element with the first element of the
        # unsorted portion. This places the minimum in its correct sorted
        # position and extends the sorted prefix by one.
        #
        # Why swap instead of insert? Swapping is O(1) and keeps the
        # algorithm in-place, avoiding the O(n) cost of shifting elements.
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


def selection_sort_visualized(arr: List[int]) -> List[int]:
    """Sort a list using selection sort and print the array state at each step.

    This helper is designed for educational purposes — it makes the
    algorithm's progress visible so learners can see how the sorted
    prefix grows and the unsorted suffix shrinks with each iteration.

    At each outer-loop iteration, the function prints:
      - The current pass number.
      - The array state before the pass.
      - Which element is being compared as the current minimum.
      - The result of the swap (if any).

    Args:
        arr: The list of integers to sort. Modified in-place.

    Returns:
        The same list object, now sorted in ascending order.
    """
    n: int = len(arr)

    print(f"Initial array: {arr}")
    print("-" * 50)

    for i in range(n - 1):
        min_index = i

        print(f"\nPass {i + 1}: Finding minimum in unsorted portion "
              f"arr[{i}:{n}] = {arr[i:]}")
        print(f"  Current sorted prefix:  {arr[:i]}")
        print(f"  Current unsorted suffix: {arr[i:]}")
        print(f"  Initial min candidate: arr[{min_index}] = {arr[min_index]}")

        # Scan the unsorted suffix for a smaller element.
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                print(f"    New minimum found: arr[{j}] = {arr[j]} "
                      f"(was arr[{min_index}] = {arr[min_index]})")
                min_index = j

        # Perform the swap if a smaller element was found.
        if min_index != i:
            print(f"  Swapping arr[{i}]={arr[i]} with arr[{min_index}]={arr[min_index]}")
            arr[i], arr[min_index] = arr[min_index], arr[i]
        else:
            print(f"  No swap needed — arr[{i}]={arr[i]} is already the minimum")

        print(f"  Array after pass {i + 1}: {arr}")
        print(f"  Sorted prefix after pass:  {arr[:i + 1]}")

    print("-" * 50)
    print(f"Final sorted array: {arr}")
    return arr


def main() -> None:
    """Demonstrate selection sort with a sample list."""
    sample: List[int] = [64, 25, 12, 22, 11]

    print("=" * 60)
    print("Selection Sort — Educational Demonstration")
    print("=" * 60)

    # Show the basic sort first
    print("\n--- Basic Sort ---")
    data: List[int] = sample.copy()
    print(f"Input:  {data}")
    selection_sort(data)
    print(f"Output: {data}")

    # Show the step-by-step visualization
    print("\n\n--- Step-by-Step Visualization ---")
    data2: List[int] = sample.copy()
    selection_sort_visualized(data2)

    # Demonstrate that the algorithm is in-place
    print("\n\n--- In-Place Verification ---")
    data3: List[int] = [5, 3, 1, 4, 2]
    print(f"Before sort: {data3}")
    result: List[int] = selection_sort(data3)
    print(f"After sort:  {result}")
    print(f"Same object? {result is data3}")  # Should be True (in-place)

    # Edge cases
    print("\n\n--- Edge Cases ---")
    print(f"Empty list:    {selection_sort([])}")
    print(f"Single element: {selection_sort([42])}")
    print(f"Already sorted: {selection_sort([1, 2, 3, 4, 5])}")
    print(f"Reverse sorted: {selection_sort([5, 4, 3, 2, 1])}")
    print(f"Duplicates:    {selection_sort([3, 1, 4, 1, 5, 9, 2, 6, 5])}")


if __name__ == "__main__":
    main()
