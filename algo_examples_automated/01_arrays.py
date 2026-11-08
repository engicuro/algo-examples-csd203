"""
01_arrays.py - Array Basics in Python

Arrays (lists in Python) are ordered, mutable collections that store elements
contiguously in memory. Python lists are dynamic arrays that resize
automatically, but the underlying concept mirrors fixed-size arrays in
lower-level languages like C.

Topics covered:
  - Creation (literal, constructor, comprehension)
  - Indexing (positive and negative)
  - Slicing
  - Common operations: append, insert, delete, search, sort
"""

from typing import Any, List, Optional


def create_array() -> List[int]:
    """Demonstrate different ways to create an array (Python list)."""
    # Literal syntax
    arr1: List[int] = [10, 20, 30, 40, 50]

    # Using the list constructor from an iterable
    arr2: List[int] = list(range(1, 6))  # [1, 2, 3, 4, 5]

    # List comprehension — creates a list from an expression
    arr3: List[int] = [x * 2 for x in range(5)]  # [0, 2, 4, 6, 8]

    # Pre-allocated array of a given size filled with a default value
    arr4: List[Optional[int]] = [None] * 5  # [None, None, None, None, None]

    return arr1


def demonstrate_indexing(arr: List[int]) -> None:
    """Show positive and negative indexing into a list."""
    print(f"Array: {arr}")
    print(f"  First element (index 0):    {arr[0]}")
    print(f"  Last element  (index -1):   {arr[-1]}")
    print(f"  Third element  (index 2):   {arr[2]}")
    print(f"  Second-to-last (index -2):  {arr[-2]}")


def demonstrate_slicing(arr: List[int]) -> None:
    """Show Python slicing syntax: arr[start:stop:step]."""
    print(f"Array:            {arr}")
    print(f"  arr[1:4]:       {arr[1:4]}")      # elements at indices 1,2,3
    print(f"  arr[:3]:        {arr[:3]}")       # first three elements
    print(f"  arr[2:]:        {arr[2:]}")       # from index 2 to end
    print(f"  arr[::2]:       {arr[::2]}")      # every other element
    print(f"  arr[::-1]:      {arr[::-1]}")     # reversed copy
    print(f"  arr[1:5:2]:     {arr[1:5:2]}")   # indices 1,3


def demonstrate_append(arr: List[int], value: int) -> None:
    """Append a single element to the end of the list — O(1) amortized."""
    print(f"Before append({value}): {arr}")
    arr.append(value)
    print(f"After  append({value}): {arr}")


def demonstrate_insert(arr: List[int], index: int, value: int) -> None:
    """Insert value at a specific index, shifting elements right — O(n)."""
    print(f"Before insert({index}, {value}): {arr}")
    arr.insert(index, value)
    print(f"After  insert({index}, {value}): {arr}")


def demonstrate_delete(arr: List[int], value: int) -> None:
    """Delete the first occurrence of a value by index — O(n)."""
    print(f"Array before remove({value}): {arr}")
    if value in arr:
        arr.remove(value)
        print(f"Array after  remove({value}): {arr}")
    else:
        print(f"  {value} not found in array — no change.")


def demonstrate_pop(arr: List[int], index: int = -1) -> None:
    """Remove and return element at index (default last) — O(n) for middle."""
    print(f"Array before pop({index}): {arr}")
    removed = arr.pop(index)
    print(f"Popped value: {removed}, Array after: {arr}")


def demonstrate_search(arr: List[int], target: int) -> None:
    """Linear search for a target value — O(n). Returns the index or -1."""
    print(f"Searching for {target} in {arr}")
    for i, val in enumerate(arr):
        if val == target:
            print(f"  Found {target} at index {i}")
            return
    print(f"  {target} not found in array.")


def demonstrate_sort(arr: List[int]) -> None:
    """Sort the array in-place (ascending) and demonstrate sorted().

    Python uses Timsort — a hybrid merge/insertion sort — O(n log n).
    """
    print(f"Before sort: {arr}")
    arr.sort()                     # in-place sort
    print(f"After  sort (in-place): {arr}")

    # sorted() returns a new sorted list without modifying the original
    shuffled = [5, 3, 1, 4, 2]
    print(f"Original: {shuffled}")
    print(f"sorted(): {sorted(shuffled)}")
    print(f"Original unchanged: {shuffled}")


def demonstrate_common_operations() -> None:
    """Show additional common array operations."""
    arr: List[int] = [3, 1, 4, 1, 5, 9, 2, 6]

    # Length
    print(f"Array: {arr}")
    print(f"  len(arr): {len(arr)}")

    # Membership test — O(n)
    print(f"  5 in arr: {5 in arr}")
    print(f"  7 in arr: {7 in arr}")

    # Count occurrences
    print(f"  arr.count(1): {arr.count(1)}")

    # Find index of first occurrence
    print(f"  arr.index(9): {arr.index(9)}")

    # Concatenation
    print(f"  arr + [7, 8]: {arr + [7, 8]}")

    # Repetition
    print(f"  arr[:2] * 3:  {arr[:2] * 3}")


def main() -> None:
    """Run all array demonstrations."""
    print("=" * 60)
    print("Chapter 1 — Arrays (Python Lists)")
    print("=" * 60)

    # 1. Creation
    print("\n--- 1. Creation ---")
    arr = create_array()
    print(f"create_array() -> {arr}")

    # 2. Indexing
    print("\n--- 2. Indexing ---")
    demonstrate_indexing(arr)

    # 3. Slicing
    print("\n--- 3. Slicing ---")
    demonstrate_slicing(arr)

    # 4. Append
    print("\n--- 4. Append ---")
    demonstrate_append(arr.copy(), 60)

    # 5. Insert
    print("\n--- 5. Insert ---")
    demonstrate_insert(arr.copy(), 2, 99)

    # 6. Delete (remove)
    print("\n--- 6. Delete (remove) ---")
    demonstrate_delete(arr.copy(), 30)

    # 7. Pop
    print("\n--- 7. Pop ---")
    demonstrate_pop(arr.copy(), -1)
    demonstrate_pop(arr.copy(), 1)

    # 8. Search
    print("\n--- 8. Search ---")
    demonstrate_search(arr, 40)
    demonstrate_search(arr, 99)

    # 9. Sort
    print("\n--- 9. Sort ---")
    demonstrate_sort(arr.copy())

    # 10. Other common operations
    print("\n--- 10. Other Common Operations ---")
    demonstrate_common_operations()


if __name__ == "__main__":
    main()
