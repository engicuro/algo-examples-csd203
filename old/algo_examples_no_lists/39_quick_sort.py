# Quick Sort
# Pick a pivot, put smaller elements on the left and larger on the right,
# then sort each side recursively. Prints the list at each partition step.

from _structures import IntArray


def quick_sort_helper(arr, low, high, comparisons, swaps):
    """Recursively sort the part of the list between low and high indices."""
    if low < high:
        # Partition the list and get the pivot's final position
        pivot_index, comparisons, swaps = partition(arr, low, high, comparisons, swaps)

        print("  After partition (pivot=" + str(arr.get(pivot_index)) + "): " + str(arr))

        # Sort the left side of the pivot
        comparisons, swaps = quick_sort_helper(arr, low, pivot_index - 1, comparisons, swaps)

        # Sort the right side of the pivot
        comparisons, swaps = quick_sort_helper(arr, pivot_index + 1, high, comparisons, swaps)

    return comparisons, swaps


def partition(arr, low, high, comparisons, swaps):
    """Put the pivot in its correct place and return its index."""
    # Use the last element as the pivot
    pivot = arr.get(high)

    # i tracks where the smaller elements end
    i = low - 1

    for j in range(low, high):
        comparisons = comparisons + 1
        if arr.get(j) <= pivot:
            i = i + 1
            # Swap arr[i] and arr[j]
            temp = arr.get(i)
            arr.set(i, arr.get(j))
            arr.set(j, temp)
            swaps = swaps + 1

    # Put the pivot in its correct position
    temp = arr.get(i + 1)
    arr.set(i + 1, arr.get(high))
    arr.set(high, temp)
    swaps = swaps + 1

    return i + 1, comparisons, swaps


def quick_sort(arr):
    """Sort a list using quick sort. Returns the number of comparisons and swaps."""
    print("  Initial list: " + str(arr))
    comparisons, swaps = quick_sort_helper(arr, 0, len(arr) - 1, 0, 0)
    return comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = IntArray(6)
    numbers.set(0, 10)
    numbers.set(1, 7)
    numbers.set(2, 8)
    numbers.set(3, 9)
    numbers.set(4, 1)
    numbers.set(5, 5)
    print("Original list: " + str(numbers))
    print("Running quick sort...\n")

    comps, swps = quick_sort(numbers)

    print("\nSorted list: " + str(numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps: " + str(swps))
