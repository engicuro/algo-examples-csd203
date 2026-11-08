"""
38_bubble_sort.py - Bubble Sort Algorithm

Bubble sort repeatedly steps through the list, compares adjacent
elements, and swaps them if they are in the wrong order.
Each pass "bubbles" the largest unsorted element to its
correct position at the end of the list.

An optimization is included: if no swaps occur during a pass,
the list is already sorted and we can terminate early.

Time Complexity:
  - Best:    O(n) — list is already sorted (with early termination)
  - Average: O(n²)
  - Worst:   O(n²) — list is reverse-sorted

Space Complexity: O(1) — sorts in-place, only uses a constant amount
  of extra memory for temporary swap variable.

Stability: STABLE — adjacent swaps only occur when the left element
  is strictly greater than the right, so equal elements are never
  reordered relative to each other.
"""

from typing import List


def bubble_sort(arr: List[int]) -> List[int]:
    """Sort a list in-place using bubble sort and return it.

    Args:
        arr: The list of integers to sort (modified in-place).

    Returns:
        The same list object, now sorted in ascending order.
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        # Each pass places the next-largest element at the end,
        # so we can shrink the inner loop boundary by i each time
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # Early termination: if no swaps happened, the list is sorted
        if not swapped:
            break
    return arr


def bubble_sort_visualized(arr: List[int]) -> List[int]:
    """Sort a list using bubble sort and print the array state at each step.

    This helper is designed for educational purposes — it makes the
    algorithm's progress visible so learners can see how each pass
    "bubbles" the largest unsorted element to its correct position.

    At each outer-loop iteration, the function prints:
      - The current pass number.
      - The array state before the pass.
      - Each comparison and swap that occurs.
      - The array state after the pass.

    Args:
        arr: The list of integers to sort. Modified in-place.

    Returns:
        The same list object, now sorted in ascending order.
    """
    n: int = len(arr)

    print(f"Initial array: {arr}")
    print("-" * 50)

    for i in range(n):
        swapped = False

        print(f"\nPass {i + 1}: Comparing adjacent elements in arr[0:{n - i}]")
        print(f"  Array before pass: {arr}")

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                print(f"    arr[{j}]={arr[j]} > arr[{j+1}]={arr[j+1]} — swapping")
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
            else:
                print(f"    arr[{j}]={arr[j]} <= arr[{j+1}]={arr[j+1]} — no swap")

        print(f"  Array after pass {i + 1}: {arr}")

        if not swapped:
            print(f"  No swaps occurred — list is already sorted. Early termination.")
            break

    print("-" * 50)
    print(f"Final sorted array: {arr}")
    return arr


def main() -> None:
    """Demonstrate bubble sort with a sample list."""
    sample: List[int] = [64, 34, 25, 12, 22, 11, 90]

    print("=" * 60)
    print("Bubble Sort — Educational Demonstration")
    print("=" * 60)

    # Show the basic sort first
    print("\n--- Basic Sort ---")
    data: List[int] = sample.copy()
    print(f"Input:  {data}")
    bubble_sort(data)
    print(f"Output: {data}")

    # Show the step-by-step visualization
    print("\n\n--- Step-by-Step Visualization ---")
    data2: List[int] = sample.copy()
    bubble_sort_visualized(data2)

    # Demonstrate that the algorithm is in-place
    print("\n\n--- In-Place Verification ---")
    data3: List[int] = [5, 3, 1, 4, 2]
    print(f"Before sort: {data3}")
    result: List[int] = bubble_sort(data3)
    print(f"After sort:  {result}")
    print(f"Same object? {result is data3}")  # Should be True (in-place)

    # Edge cases
    print("\n\n--- Edge Cases ---")
    print(f"Empty list:    {bubble_sort([])}")
    print(f"Single element: {bubble_sort([42])}")
    print(f"Already sorted: {bubble_sort([1, 2, 3, 4, 5])}")
    print(f"Reverse sorted: {bubble_sort([5, 4, 3, 2, 1])}")
    print(f"Duplicates:    {bubble_sort([3, 1, 4, 1, 5, 9, 2, 6, 5])}")


if __name__ == "__main__":
    main()
