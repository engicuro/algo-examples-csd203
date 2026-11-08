"""
41_heap_sort.py - Heap Sort Algorithm

Heap sort works by first building a max-heap from the input
array, then repeatedly extracting the maximum element from
the heap and placing it at the end of the array. The heap
shrinks one element at a time until the array is sorted.

A max-heap is a complete binary tree where every parent node
is greater than or equal to its children. In Python we can
represent it implicitly in a list (parent at index i has
children at 2i+1 and 2i+2).

Time Complexity:
  - Best:    O(n log n)
  - Average: O(n log n)
  - Worst:   O(n log n) — heap operations are always O(log n)

Space Complexity: O(1) — sorts in-place, only uses a constant
  amount of extra memory for index variables.

Stability: NOT stable — the heapify process can reorder equal
  elements because it swaps distant elements during sifting.
"""

from typing import List


def _sift_down(arr: List[int], n: int, i: int) -> None:
    """Restore the max-heap property by sifting element at index i down.

    Assumes that the binary trees rooted at arr[i]'s children
    are already valid max-heaps.

    Args:
        arr: The list representing the heap (modified in-place).
        n: The size of the heap (number of elements to consider).
        i: The index of the element to sift down.
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check if right child exists and is greater than current largest
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If the largest is not the root, swap and continue sifting down
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _sift_down(arr, n, largest)


def heap_sort(arr: List[int]) -> List[int]:
    """Sort a list in-place using heap sort and return it.

    Args:
        arr: The list of integers to sort (modified in-place).

    Returns:
        The same list object, now sorted in ascending order.
    """
    n = len(arr)

    # Build a max-heap: start from the last non-leaf node
    # and sift each node down to its correct position
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, n, i)

    # Extract elements from the heap one by one
    for i in range(n - 1, 0, -1):
        # Move the current root (max) to the end of the unsorted portion
        arr[0], arr[i] = arr[i], arr[0]
        # Reduce heap size and restore the heap property
        _sift_down(arr, i, 0)

    return arr


def _heap_sort_verbose(arr: List[int]) -> List[int]:
    """Sort a list in-place using heap sort, printing heap state at key steps.

    This is a pedagogical variant that shows the heap after building
    and after each extraction, so the reader can trace the algorithm.

    Args:
        arr: The list of integers to sort (modified in-place).

    Returns:
        The same list object, now sorted in ascending order.
    """
    n = len(arr)

    print(f"  Initial array: {arr}")

    # Build max-heap
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, n, i)
    print(f"  After build_max_heap: {arr}")

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _sift_down(arr, i, 0)
        print(f"  After extracting max to index {i}: {arr}")

    return arr


if __name__ == "__main__":
    print("=" * 60)
    print("Heap Sort — Basic Usage")
    print("=" * 60)

    sample = [12, 11, 13, 5, 6, 7]
    print(f"Input:  {sample}")
    heap_sort(sample)
    print(f"Sorted: {sample}")

    print()
    print("=" * 60)
    print("Heap Sort — Step-by-Step Visualization")
    print("=" * 60)

    verbose_sample = [4, 10, 3, 5, 1]
    print(f"\nSorting {verbose_sample}:")
    _heap_sort_verbose(verbose_sample)
    print(f"Final result: {verbose_sample}")

    print()
    print("=" * 60)
    print("Heap Sort — Edge Cases")
    print("=" * 60)

    # Empty list
    empty: List[int] = []
    heap_sort(empty)
    assert empty == [], f"Expected [], got {empty}"
    print(f"Empty list:    {empty}  ✓")

    # Single element
    single = [42]
    heap_sort(single)
    assert single == [42], f"Expected [42], got {single}"
    print(f"Single element: {single}  ✓")

    # Already sorted
    already = [1, 2, 3, 4, 5]
    heap_sort(already)
    assert already == [1, 2, 3, 4, 5], f"Expected [1,2,3,4,5], got {already}"
    print(f"Already sorted: {already}  ✓")

    # Reverse sorted
    reverse = [5, 4, 3, 2, 1]
    heap_sort(reverse)
    assert reverse == [1, 2, 3, 4, 5], f"Expected [1,2,3,4,5], got {reverse}"
    print(f"Reverse sorted: {reverse}  ✓")

    # Duplicates
    dups = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    heap_sort(dups)
    assert dups == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9], f"Unexpected result: {dups}"
    print(f"With duplicates: {dups}  ✓")

    print()
    print("=" * 60)
    print("Heap Sort — In-Place Verification")
    print("=" * 60)

    original = [9, 7, 5, 3, 1]
    reference = sorted(original)
    arr = original[:]
    result = heap_sort(arr)
    assert result is arr, "heap_sort should return the same list object (in-place)"
    assert arr == reference, f"Expected {reference}, got {arr}"
    print(f"Original: {original}")
    print(f"Sorted:   {arr}")
    print(f"Returned same object: {result is arr}  ✓")
    print(f"Correctly sorted:     {arr == reference}  ✓")
