"""
39_quick_sort.py - Quick Sort Algorithm

Quick sort is a divide-and-conquer algorithm that works by
choosing a 'pivot' element and partitioning the array so that
elements less than the pivot go to its left and elements greater
go to its right. It then recursively sorts the two partitions.

This implementation uses the last element as the pivot and
sorts in-place using the Lomuto partition scheme.

Time Complexity:
  - Best:    O(n log n) — pivot always splits the array roughly in half
  - Average: O(n log n)
  - Worst:   O(n²) — pivot is always the smallest or largest element
    (e.g., already sorted list with last-element pivot)

Space Complexity: O(log n) average — recursion stack depth.
  O(n) worst case for deeply unbalanced partitions.

Stability: NOT stable — the in-place partitioning can reorder
  equal elements relative to their original positions.
"""

from typing import List


def _quick_sort_helper(arr: List[int], low: int, high: int) -> None:
    """Recursively sort arr[low..high] using quick sort.

    Args:
        arr: The list being sorted (modified in-place).
        low: Starting index of the sub-array to sort.
        high: Ending index of the sub-array to sort.
    """
    if low < high:
        # Partition the array and get the pivot's final position
        pivot_index = _partition(arr, low, high)
        # Recursively sort the left and right partitions
        _quick_sort_helper(arr, low, pivot_index - 1)
        _quick_sort_helper(arr, pivot_index + 1, high)


def _partition(arr: List[int], low: int, high: int) -> int:
    """Lomuto partition scheme: place pivot in its correct position.

    All elements <= pivot are moved to the left of the pivot,
    and all elements > pivot are moved to the right.

    Args:
        arr: The list being partitioned (modified in-place).
        low: Starting index of the sub-array.
        high: Index of the pivot element (last element).

    Returns:
        The final index of the pivot element.
    """
    pivot = arr[high]
    i = low - 1  # Index of the smaller element boundary
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    # Place the pivot in its correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr: List[int]) -> List[int]:
    """Sort a list in-place using quick sort and return it.

    This function creates a copy of the input list so that the
    original is not modified, providing a consistent interface
    with non-in-place sorting algorithms.

    Args:
        arr: The list of integers to sort.

    Returns:
        A new list containing the elements in sorted order.
    """
    # Work on a copy so the caller's original list is unchanged
    arr_copy = arr[:]
    _quick_sort_helper(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy


def _median_of_three(arr: List[int], low: int, high: int) -> int:
    """Return the index of the median of arr[low], arr[mid], arr[high].

    Args:
        arr: The list being examined.
        low: Starting index of the sub-array.
        high: Ending index of the sub-array.

    Returns:
        The index of the median-value element among the three candidates.
    """
    mid = (low + high) // 2
    candidates = [(arr[low], low), (arr[mid], mid), (arr[high], high)]
    candidates.sort(key=lambda x: x[0])
    return candidates[1][1]


def _median_of_three_partition(arr: List[int], low: int, high: int) -> int:
    """Lomuto partition with median-of-three pivot selection.

    Chooses the median of arr[low], arr[mid], and arr[high] as the
    pivot, swaps it to arr[high], then partitions as in the standard
    Lomuto scheme.

    Args:
        arr: The list being partitioned (modified in-place).
        low: Starting index of the sub-array.
        high: Ending index of the sub-array.

    Returns:
        The final index of the pivot element.
    """
    median_idx = _median_of_three(arr, low, high)
    arr[median_idx], arr[high] = arr[high], arr[median_idx]
    return _partition(arr, low, high)


def _median_of_three_quick_sort_helper(arr: List[int], low: int, high: int) -> None:
    """Recursively sort arr[low..high] using quick sort with
    median-of-three pivot selection.

    Args:
        arr: The list being sorted (modified in-place).
        low: Starting index of the sub-array to sort.
        high: Ending index of the sub-array to sort.
    """
    if low < high:
        pivot_index = _median_of_three_partition(arr, low, high)
        _median_of_three_quick_sort_helper(arr, low, pivot_index - 1)
        _median_of_three_quick_sort_helper(arr, pivot_index + 1, high)


def median_of_three_quick_sort(arr: List[int]) -> List[int]:
    """Sort a list using quick sort with median-of-three pivot selection.

    Creates a copy of the input so the original is not modified.

    Args:
        arr: The list of integers to sort.

    Returns:
        A new list containing the elements in sorted order.
    """
    arr_copy = arr[:]
    _median_of_three_quick_sort_helper(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy


def _partition_verbose(arr: List[int], low: int, high: int) -> int:
    """Lomuto partition with step-by-step printing.

    Prints the array state at each swap so the partitioning
    process is visible.

    Args:
        arr: The list being partitioned (modified in-place).
        low: Starting index of the sub-array.
        high: Index of the pivot element (last element).

    Returns:
        The final index of the pivot element.
    """
    pivot = arr[high]
    print(f"  Partition arr[{low}..{high}], pivot = arr[{high}] = {pivot}")
    print(f"  Before: {arr[low:high + 1]}")
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            if i != j:
                arr[i], arr[j] = arr[j], arr[i]
                print(f"    Swap arr[{i}] and arr[{j}]: {arr[low:high + 1]}")
            else:
                print(f"    arr[{j}] = {arr[j]} <= pivot, no swap needed")
        else:
            print(f"    arr[{j}] = {arr[j]} > pivot, skip")
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    print(f"  Place pivot at index {i + 1}: {arr[low:high + 1]}")
    return i + 1


def _quick_sort_verbose(arr: List[int], low: int, high: int, depth: int = 0) -> None:
    """Recursively sort arr[low..high] with verbose partition printing.

    Args:
        arr: The list being sorted (modified in-place).
        low: Starting index of the sub-array to sort.
        high: Ending index of the sub-array to sort.
        depth: Current recursion depth (for indentation).
    """
    if low < high:
        indent = "  " * depth
        print(f"{indent}Sort arr[{low}..{high}]: {arr[low:high + 1]}")
        pivot_index = _partition_verbose(arr, low, high)
        print(f"{indent}Pivot placed at index {pivot_index}, array now: {arr}")
        _quick_sort_verbose(arr, low, pivot_index - 1, depth + 1)
        _quick_sort_verbose(arr, pivot_index + 1, high, depth + 1)


if __name__ == "__main__":
    print("=" * 60)
    print("Quick Sort Algorithm")
    print("=" * 60)

    # --- Basic Usage ---
    print("\n--- Basic Usage ---")
    sample = [10, 7, 8, 9, 1, 5]
    print(f"Original list: {sample}")
    sorted_list = quick_sort(sample)
    print(f"Sorted list:   {sorted_list}")
    print(f"Original unchanged: {sample}")

    # --- Step-by-step Visualization ---
    print("\n--- Step-by-step Partition Visualization ---")
    viz = [10, 7, 8, 9, 1, 5]
    print(f"Original: {viz}")
    _quick_sort_verbose(viz, 0, len(viz) - 1)
    print(f"Final sorted: {viz}")

    # --- Edge Cases ---
    print("\n--- Edge Cases ---")

    print("\n  Empty list:")
    empty = []
    result = quick_sort(empty)
    print(f"    quick_sort([]) -> {result}")

    print("\n  Single element:")
    single = [42]
    result = quick_sort(single)
    print(f"    quick_sort([42]) -> {result}")

    print("\n  Already sorted:")
    already_sorted = [1, 2, 3, 4, 5]
    result = quick_sort(already_sorted)
    print(f"    quick_sort([1, 2, 3, 4, 5]) -> {result}")

    print("\n  Reverse sorted:")
    reverse_sorted = [5, 4, 3, 2, 1]
    result = quick_sort(reverse_sorted)
    print(f"    quick_sort([5, 4, 3, 2, 1]) -> {result}")

    print("\n  Duplicates:")
    duplicates = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    result = quick_sort(duplicates)
    print(f"    quick_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) -> {result}")

    # --- In-place Verification ---
    print("\n--- In-place Verification ---")
    in_place_test = [64, 34, 25, 12, 22, 11, 90]
    in_place_copy = in_place_test[:]
    in_place_result = quick_sort(in_place_test)
    print(f"  Original list:  {in_place_copy}")
    print(f"  quick_sort() returned: {in_place_result}")
    print(f"  Original unchanged:   {in_place_test}")
    print(f"  Returned is a new list: {in_place_result is not in_place_test}")
    print(f"  Returned is sorted: {in_place_result == sorted(in_place_copy)}")

    # --- Median-of-Three Pivot Selection ---
    print("\n--- Median-of-Three Pivot Selection ---")
    mot_test = [10, 7, 8, 9, 1, 5]
    print(f"  Original: {mot_test}")
    mot_result = median_of_three_quick_sort(mot_test)
    print(f"  Sorted (median-of-three): {mot_result}")

    # Show that median-of-three avoids worst-case on already-sorted input
    print("\n  Worst-case scenario (already sorted) — last-element pivot")
    print("  would degrade to O(n^2). Median-of-three mitigates this:")
    worst_case = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"    Input: {worst_case}")
    mot_worst = median_of_three_quick_sort(worst_case)
    print(f"    Median-of-three sorted: {mot_worst}")

    print("\n" + "=" * 60)
