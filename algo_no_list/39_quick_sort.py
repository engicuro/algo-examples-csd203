# Quick Sort
# Pick a pivot, put smaller elements on the left and larger on the right,
# then sort each side recursively. Prints the tuple at each partition step.


def _tuple_swap(t, i, j):
    """Return a new tuple with elements at indices i and j swapped."""
    if i == j:
        return t
    return t[:i] + (t[j],) + t[i + 1:j] + (t[i],) + t[j + 1:]


def quick_sort_helper(arr, low, high, comparisons, swaps):
    """Recursively sort the part of the tuple between low and high indices."""
    if low < high:
        # Partition the tuple and get the pivot's final position
        pivot_index, arr, comparisons, swaps = partition(arr, low, high, comparisons, swaps)

        print("  After partition (pivot=" + str(arr[pivot_index]) + "): " + str(arr))

        # Sort the left side of the pivot
        arr, comparisons, swaps = quick_sort_helper(arr, low, pivot_index - 1, comparisons, swaps)

        # Sort the right side of the pivot
        arr, comparisons, swaps = quick_sort_helper(arr, pivot_index + 1, high, comparisons, swaps)

    return arr, comparisons, swaps


def partition(arr, low, high, comparisons, swaps):
    """Put the pivot in its correct place and return its index."""
    # Use the last element as the pivot
    pivot = arr[high]

    # i tracks where the smaller elements end
    i = low - 1

    for j in range(low, high):
        comparisons = comparisons + 1
        if arr[j] <= pivot:
            i = i + 1
            # Swap arr[i] and arr[j]
            arr = _tuple_swap(arr, i, j)
            swaps = swaps + 1

    # Put the pivot in its correct position
    arr = _tuple_swap(arr, i + 1, high)
    swaps = swaps + 1

    return i + 1, arr, comparisons, swaps


def quick_sort(arr):
    """Sort a tuple using quick sort. Returns the sorted tuple, number of comparisons and swaps."""
    print("  Initial tuple: " + str(arr))
    arr, comparisons, swaps = quick_sort_helper(arr, 0, len(arr) - 1, 0, 0)
    return arr, comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = (10, 7, 8, 9, 1, 5)
    print("Original tuple: " + str(numbers))
    print("Running quick sort...\n")

    sorted_numbers, comps, swps = quick_sort(numbers)

    print("\nSorted tuple: " + str(sorted_numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps: " + str(swps))
