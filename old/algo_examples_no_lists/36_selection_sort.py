# Selection Sort
# Find the smallest element in the unsorted part and swap it to the front.
# Prints the list after each swap so you can see the steps.
# Uses IntArray from _structures.py instead of a Python list.

from _structures import IntArray


def selection_sort(arr):
    """Sort an IntArray using selection sort. Returns the number of comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    # Go through each position in the array
    for i in range(n):
        # Assume the current position holds the minimum
        min_index = i

        # Look for a smaller element in the remaining unsorted part
        for j in range(i + 1, n):
            comparisons = comparisons + 1
            if arr.get(j) < arr.get(min_index):
                min_index = j

        # Swap the found minimum with the element at position i
        if min_index != i:
            temp = arr.get(i)
            arr.set(i, arr.get(min_index))
            arr.set(min_index, temp)
            swaps = swaps + 1

        # Print the array after this step
        print("  Step " + str(i + 1) + ": " + str(arr))

    return comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = IntArray(5)
    numbers.set(0, 64)
    numbers.set(1, 25)
    numbers.set(2, 12)
    numbers.set(3, 22)
    numbers.set(4, 11)
    print("Original list: " + str(numbers))
    print("Running selection sort...\n")

    comps, swps = selection_sort(numbers)

    print("\nSorted list: " + str(numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps: " + str(swps))
