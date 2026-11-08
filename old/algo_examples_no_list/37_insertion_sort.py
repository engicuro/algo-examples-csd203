# Insertion Sort
# Pick each element and shift it left until it is in the correct position.
# Prints the list after each insertion so you can see the steps.


def insertion_sort(arr):
    """Sort a list using insertion sort. Returns the number of comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    # Start from the second element (index 1)
    # The first element is already "sorted" by itself
    for i in range(1, n):
        # The element we want to insert into the sorted part
        key = arr[i]

        # Start comparing with the element just before the current one
        j = i - 1

        # Shift elements one position to the right while they are bigger than key
        while j >= 0:
            comparisons = comparisons + 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps = swaps + 1
                j = j - 1
            else:
                # Found the right spot, stop shifting
                break

        # Place the key in its correct position
        arr[j + 1] = key

        # Print the list after this step
        print("  Step " + str(i) + ": " + str(arr))

    return comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = [12, 11, 13, 5, 6]
    print("Original list: " + str(numbers))
    print("Running insertion sort...\n")

    comps, swps = insertion_sort(numbers)

    print("\nSorted list: " + str(numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps/shifts: " + str(swps))
