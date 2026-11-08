"""
10_recursion_binary_search.py
=============================
Recursion Topic: Binary Search (Divide and Conquer)

Binary search finds the position of a target value within a sorted array.
It works by repeatedly dividing the search interval in half — a classic
"divide and conquer" strategy.

Divide and Conquer Approach:
  1. DIVIDE  – Compare the target with the middle element.
  2. CONQUER – Recurse into the half where the target could be.
  3. COMBINE – No combination needed; the answer is found directly.

Base cases:
  - The element is found at the middle index.
  - The search range is empty (low > high) → element not in array.

Time complexity : O(log n)  — each call halves the search space.
Space complexity: O(log n)   — recursive call stack depth.
"""

from typing import List, Optional


def binary_search(arr: List[int], target: int, low: int = 0, high: Optional[int] = None) -> Optional[int]:
    """Search for target in a sorted list using recursion.

    Args:
        arr:    A sorted list of integers (ascending order).
        target: The value to find.
        low:    Lower bound of the current search range (inclusive).
        high:   Upper bound of the current search range (inclusive).
                Defaults to len(arr) - 1 on first call.

    Returns:
        The index of target if found, otherwise None.
    """
    # Initialize high on the first call
    if high is None:
        high = len(arr) - 1

    # --- Base case 1: search range is empty ---
    # If low exceeds high, the target is not present in the array.
    # This is the "not found" termination condition.
    if low > high:
        return None

    # --- Divide: compute the middle index ---
    mid = (low + high) // 2

    # --- Base case 2: target found at mid ---
    if arr[mid] == target:
        return mid

    # --- Conquer: recurse into the appropriate half ---
    # If target is smaller than the middle element, it must be in the
    # left half (if present at all).  Otherwise, search the right half.
    if target < arr[mid]:
        # Search the left sub-array: [low .. mid-1]
        return binary_search(arr, target, low, mid - 1)
    else:
        # Search the right sub-array: [mid+1 .. high]
        return binary_search(arr, target, mid + 1, high)


def binary_search_iterative(arr: List[int], target: int) -> Optional[int]:
    """Iterative version of binary search for comparison."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif target < arr[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return None


if __name__ == "__main__":
    print("=" * 55)
    print("Recursion Example: Binary Search")
    print("=" * 55)

    sorted_list = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]
    print(f"Sorted array: {sorted_list}")
    print()

    targets = [23, 2, 91, 50, 100]
    for target in targets:
        idx = binary_search(sorted_list, target)
        if idx is not None:
            print(f"  binary_search({sorted_list}, {target}) → index {idx}")
        else:
            print(f"  binary_search({sorted_list}, {target}) → not found (None)")

    print()
    print("Divide-and-conquer trace for searching 23 in [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]:")
    print("  Call 1: low=0,  high=10, mid=5,  arr[5]=23 → FOUND at index 5")
    print()
    print("Divide-and-conquer trace for searching 50 (not present):")
    print("  Call 1: low=0,  high=10, mid=5,  arr[5]=23 → 50 > 23 → search right [6..10]")
    print("  Call 2: low=6,  high=10, mid=8,  arr[8]=56 → 50 < 56 → search left [6..7]")
    print("  Call 3: low=6,  high=7,  mid=6,  arr[6]=38 → 50 > 38 → search right [7..7]")
    print("  Call 4: low=7,  high=7,  mid=7,  arr[7]=45 → 50 > 45 → search right [8..7]")
    print("  Call 5: low=8,  high=7  → low > high → NOT FOUND (base case)")
    print()
    print(f"Verification: recursive == iterative for all targets: {all(binary_search(sorted_list, t) == binary_search_iterative(sorted_list, t) for t in targets)}")
