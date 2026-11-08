"""
40_merge_sort.py - Merge Sort Algorithm

Merge sort is a divide-and-conquer algorithm that works by
recursively splitting the list into halves, sorting each half,
and then merging the two sorted halves back together.

It is one of the most reliable sorting algorithms with a
guaranteed O(n log n) time complexity in all cases.

Time Complexity:
  - Best:    O(n log n)
  - Average: O(n log n)
  - Worst:   O(n log n) — always divides the array in half

Space Complexity: O(n) — requires auxiliary space for the
  temporary arrays used during merging.

Stability: STABLE — during the merge step, when two elements
  are equal, the element from the left (earlier) sub-array is
  placed first, preserving original relative order.
"""

from typing import List


def _merge(left: List[int], right: List[int]) -> List[int]:
    """Merge two sorted lists into a single sorted list.

    Args:
        left: A sorted list of integers.
        right: A sorted list of integers.

    Returns:
        A new list containing all elements from left and right
        in sorted ascending order.
    """
    merged: List[int] = []
    i = 0  # Pointer into left
    j = 0  # Pointer into right

    # Compare elements from both lists and take the smaller one
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append any remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort(arr: List[int]) -> List[int]:
    """Sort a list using merge sort and return a new sorted list.

    This is NOT an in-place sort — it returns a new list and
    leaves the original unchanged.

    Args:
        arr: The list of integers to sort.

    Returns:
        A new list containing the elements in sorted ascending order.
    """
    # Base case: a list of 0 or 1 elements is already sorted
    if len(arr) <= 1:
        return arr[:]

    # Split the list into two halves
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    # Merge the two sorted halves
    return _merge(left_half, right_half)


if __name__ == "__main__":
    # --- Basic usage ---
    sample = [38, 27, 43, 3, 9, 82, 10]
    print("Original:", sample)
    sorted_sample = merge_sort(sample)
    print("Sorted:  ", sorted_sample)
    print()

    # --- Step-by-step visualization ---
    # Show the divide steps by tracing the recursion manually
    def merge_sort_visualized(arr: list[int], depth: int = 0) -> list[int]:
        """Merge sort with printed divide/merge steps for visualization."""
        indent = "  " * depth
        if len(arr) <= 1:
            print(f"{indent}Base case → {arr}")
            return arr[:]
        mid = len(arr) // 2
        print(f"{indent}Split {arr} → {arr[:mid]} | {arr[mid:]}")
        left = merge_sort_visualized(arr[:mid], depth + 1)
        right = merge_sort_visualized(arr[mid:], depth + 1)
        merged = _merge(left, right)
        print(f"{indent}Merge {left} + {right} → {merged}")
        return merged

    print("=== Step-by-step visualization ===")
    merge_sort_visualized([38, 27, 43, 3, 9, 82, 10])
    print()

    # --- Edge cases ---
    print("=== Edge cases ===")

    # Empty list
    empty: list[int] = []
    result = merge_sort(empty)
    print(f"Empty list:  {empty} → {result}")
    assert result == [], f"Expected [], got {result}"

    # Single element
    single = [42]
    result = merge_sort(single)
    print(f"Single elem: {single} → {result}")
    assert result == [42], f"Expected [42], got {result}"

    # Already sorted
    already = [1, 2, 3, 4, 5]
    result = merge_sort(already)
    print(f"Already sorted: {already} → {result}")
    assert result == [1, 2, 3, 4, 5], f"Expected [1,2,3,4,5], got {result}"

    # Reverse sorted
    reverse = [5, 4, 3, 2, 1]
    result = merge_sort(reverse)
    print(f"Reverse sorted: {reverse} → {result}")
    assert result == [1, 2, 3, 4, 5], f"Expected [1,2,3,4,5], got {result}"

    # Duplicates
    dups = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    result = merge_sort(dups)
    print(f"Duplicates: {dups} → {result}")
    assert result == sorted(dups), f"Expected {sorted(dups)}, got {result}"

    print()

    # --- Verify non-in-place (returns a new list) ---
    print("=== Non-in-place verification ===")
    original = [5, 2, 8, 1]
    original_id = id(original)
    result = merge_sort(original)
    result_id = id(result)
    print(f"Original list: {original} (id={original_id})")
    print(f"Returned list: {result} (id={result_id})")
    assert original_id != result_id, "merge_sort should return a NEW list, not the same object"
    assert original == [5, 2, 8, 1], "Original list should be unchanged"
    print("✓ merge_sort returns a new list and leaves the original unchanged")
