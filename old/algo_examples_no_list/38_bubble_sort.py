# Bubble Sort
# Compare adjacent elements and swap them if they are in the wrong order.
# Repeat until the list is sorted. Stops early if no swaps happen in a pass.
# Prints the list after each pass so you can see the progress.


def bubble_sort(arr):
    """Sort a list using bubble sort. Returns the number of comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    # Go through the list multiple times
    for i in range(n):
        # Track whether we made any swaps in this pass
        swapped = False

        # Compare adjacent elements; each pass pushes the largest to the end
        for j in range(0, n - i - 1):
            comparisons = comparisons + 1
            if arr[j] > arr[j + 1]:
                # Swap the two elements
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
                swaps = swaps + 1
                swapped = True

        # Print the list after this pass
        print("  Pass " + str(i + 1) + ": " + str(arr))

        # If no swaps happened, the list is already sorted
        if swapped is False:
            print("  -> No swaps this pass, list is sorted. Stopping early.")
            break

    return comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print("Original list: " + str(numbers))
    print("Running bubble sort...\n")

    comps, swps = bubble_sort(numbers)

    print("\nSorted list: " + str(numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps: " + str(swps))
