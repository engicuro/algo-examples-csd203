# Bubble Sort
# Compare adjacent elements and swap them if they are in the wrong order.
# Repeat until the tuple is sorted. Stops early if no swaps happen in a pass.
# Prints the tuple after each pass so you can see the progress.


def _tuple_swap(t, i, j):
    """Return a new tuple with elements at indices i and j swapped."""
    if i == j:
        return t
    return t[:i] + (t[j],) + t[i + 1:j] + (t[i],) + t[j + 1:]


def bubble_sort(arr):
    """Sort a tuple using bubble sort. Returns the sorted tuple, number of comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    # Go through the tuple multiple times
    for i in range(n):
        # Track whether we made any swaps in this pass
        swapped = False

        # Compare adjacent elements; each pass pushes the largest to the end
        for j in range(0, n - i - 1):
            comparisons = comparisons + 1
            if arr[j] > arr[j + 1]:
                # Swap the two elements
                arr = _tuple_swap(arr, j, j + 1)
                swaps = swaps + 1
                swapped = True

        # Print the tuple after this pass
        print("  Pass " + str(i + 1) + ": " + str(arr))

        # If no swaps happened, the tuple is already sorted
        if swapped is False:
            print("  -> No swaps this pass, tuple is sorted. Stopping early.")
            break

    return arr, comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = (64, 34, 25, 12, 22, 11, 90)
    print("Original tuple: " + str(numbers))
    print("Running bubble sort...\n")

    sorted_numbers, comps, swps = bubble_sort(numbers)

    print("\nSorted tuple: " + str(sorted_numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps: " + str(swps))
