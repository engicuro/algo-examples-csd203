# Bubble Sort
# Compare adjacent elements and swap them if they are in the wrong order.
# Repeat until the list is sorted. Stops early if no swaps happen in a pass.
# Prints the list after each pass so you can see the progress.
# Uses IntArray from _structures.py instead of a Python list.

from _structures import IntArray


def bubble_sort(arr):
    """Sort an IntArray using bubble sort. Returns the number of comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    # Go through the array multiple times
    for i in range(n):
        # Track whether we made any swaps in this pass
        swapped = False

        # Compare adjacent elements; each pass pushes the largest to the end
        for j in range(0, n - i - 1):
            comparisons = comparisons + 1
            if arr.get(j) > arr.get(j + 1):
                # Swap the two elements
                temp = arr.get(j)
                arr.set(j, arr.get(j + 1))
                arr.set(j + 1, temp)
                swaps = swaps + 1
                swapped = True

        # Print the array after this pass
        print("  Pass " + str(i + 1) + ": " + str(arr))

        # If no swaps happened, the array is already sorted
        if swapped is False:
            print("  -> No swaps this pass, list is sorted. Stopping early.")
            break

    return comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = IntArray(7)
    numbers.set(0, 64)
    numbers.set(1, 34)
    numbers.set(2, 25)
    numbers.set(3, 12)
    numbers.set(4, 22)
    numbers.set(5, 11)
    numbers.set(6, 90)
    print("Original list: " + str(numbers))
    print("Running bubble sort...\n")

    comps, swps = bubble_sort(numbers)

    print("\nSorted list: " + str(numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps: " + str(swps))
