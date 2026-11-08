# Selection Sort
# Find the smallest element in the unsorted part and swap it to the front.
# Prints the tuple after each swap so you can see the steps.


def _tuple_swap(t, i, j):
    """Return a new tuple with elements at indices i and j swapped."""
    if i == j:
        return t
    return t[:i] + (t[j],) + t[i + 1:j] + (t[i],) + t[j + 1:]


def _tuple_set(t, i, val):
    """Return a new tuple with element at index i set to val."""
    return t[:i] + (val,) + t[i + 1:]


def selection_sort(arr):
    """Sort a tuple using selection sort. Returns the sorted tuple, number of comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    # Go through each position in the tuple
    for i in range(n):
        # Assume the current position holds the minimum
        min_index = i

        # Look for a smaller element in the remaining unsorted part
        for j in range(i + 1, n):
            comparisons = comparisons + 1
            if arr[j] < arr[min_index]:
                min_index = j

        # Swap the found minimum with the element at position i
        if min_index != i:
            arr = _tuple_swap(arr, i, min_index)
            swaps = swaps + 1

        # Print the tuple after this step
        print("  Step " + str(i + 1) + ": " + str(arr))

    return arr, comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = (64, 25, 12, 22, 11)
    print("Original tuple: " + str(numbers))
    print("Running selection sort...\n")

    sorted_numbers, comps, swps = selection_sort(numbers)

    print("\nSorted tuple: " + str(sorted_numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps: " + str(swps))
