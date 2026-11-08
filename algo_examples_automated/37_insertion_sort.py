"""
37_insertion_sort.py - Insertion Sort Algorithm

Insertion sort builds the sorted list one element at a time by
taking each element and inserting it into its correct position
within the already-sorted portion (shifting elements as needed).

It is similar to how you might sort a hand of playing cards —
pick up one card at a time and place it in the right position.

Time Complexity:
  - Best:    O(n) — list is already sorted, each element is inserted in O(1)
  - Average: O(n²)
  - Worst:   O(n²) — list is reverse-sorted

Space Complexity: O(1) — sorts in-place, only uses a constant amount
  of extra memory.

Stability: STABLE — equal elements retain their original relative order
  because we shift elements right rather than swapping past equals.
"""

from typing import List


def insertion_sort(arr: List[int]) -> List[int]:
    """Sort a list in-place using insertion sort and return it.

    Args:
        arr: The list of integers to sort (modified in-place).

    Returns:
        The same list object, now sorted in ascending order.
    """
    # Start from the second element; the first element is trivially sorted
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Shift elements of arr[0..i-1] that are greater than key
        # one position to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        # Place the key in its correct position
        arr[j + 1] = key
    return arr


def insertion_sort_step_by_step(arr: List[int]) -> List[int]:
    """Sort a list using insertion sort and print the array state at each step.

    This helper is designed for educational purposes — it makes the
    algorithm's progress visible so learners can see how the sorted
    prefix grows one element at a time as each new element is inserted
    into its correct position.

    At each outer-loop iteration, the function prints:
      - The current pass number.
      - The key being inserted.
      - The shifting process (elements moved right).
      - The array state after the insertion.

    Args:
        arr: The list of integers to sort. Modified in-place.

    Returns:
        The same list object, now sorted in ascending order.
    """
    print(f"Initial array: {arr}")
    print("-" * 50)

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        print(f"\nPass {i}: Inserting key={key} into sorted portion arr[:{i}]={arr[:i]}")

        # Shift elements greater than key one position to the right
        shifted = False
        while j >= 0 and arr[j] > key:
            print(f"  arr[{j}]={arr[j]} > key={key} — shift arr[{j}] right to arr[{j + 1}]")
            arr[j + 1] = arr[j]
            j -= 1
            shifted = True

        # Place the key in its correct position
        arr[j + 1] = key

        if shifted:
            print(f"  Placed key={key} at index {j + 1}")
        else:
            print(f"  No shift needed — key={key} already in correct position")

        print(f"  Array after pass {i}: {arr}")

    print("-" * 50)
    print(f"Final sorted array: {arr}")
    return arr


def main() -> None:
    """Demonstrate insertion sort with a sample list."""
    sample: List[int] = [64, 25, 12, 22, 11]

    print("=" * 60)
    print("Insertion Sort — Educational Demonstration")
    print("=" * 60)

    # Show the basic sort first
    print("\n--- Basic Sort ---")
    data: List[int] = sample.copy()
    print(f"Input:  {data}")
    insertion_sort(data)
    print(f"Output: {data}")

    # Show the step-by-step visualization
    print("\n\n--- Step-by-Step Visualization ---")
    data2: List[int] = sample.copy()
    insertion_sort_step_by_step(data2)

    # Demonstrate that the algorithm is in-place
    print("\n\n--- In-Place Verification ---")
    data3: List[int] = [5, 3, 1, 4, 2]
    print(f"Before sort: {data3}")
    result: List[int] = insertion_sort(data3)
    print(f"After sort:  {result}")
    print(f"Same object? {result is data3}")  # Should be True (in-place)

    # Edge cases
    print("\n\n--- Edge Cases ---")
    print(f"Empty list:    {insertion_sort([])}")
    print(f"Single element: {insertion_sort([42])}")
    print(f"Already sorted: {insertion_sort([1, 2, 3, 4, 5])}")
    print(f"Reverse sorted: {insertion_sort([5, 4, 3, 2, 1])}")
    print(f"Duplicates:    {insertion_sort([3, 1, 4, 1, 5, 9, 2, 6, 5])}")


if __name__ == "__main__":
    main()
