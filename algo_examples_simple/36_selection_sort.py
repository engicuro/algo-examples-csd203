# Selection Sort
# Find the smallest element in the unsorted part and swap it to the front.
# Prints the list after each swap so you can see the steps.


def selection_sort(arr):
    """Sort a list using selection sort. Returns the number of comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    # Go through each position in the list
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
            temp = arr[i]
            arr[i] = arr[min_index]
            arr[min_index] = temp
            swaps = swaps + 1

        # Print the list after this step
        print("  Step " + str(i + 1) + ": " + str(arr))

    return comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = [64, 25, 12, 22, 11]
    print("Original list: " + str(numbers))
    print("Running selection sort...\n")

    comps, swps = selection_sort(numbers)

    print("\nSorted list: " + str(numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps: " + str(swps))
