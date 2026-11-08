# Insertion Sort
# Pick each element and shift it left until it is in the correct position.
# Prints the list after each insertion so you can see the steps.
# Uses IntArray from _structures.py instead of a Python list.

from _structures import IntArray


def insertion_sort(arr):
    """Sort an IntArray using insertion sort. Returns the number of comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    # Start from the second element (index 1)
    # The first element is already "sorted" by itself
    for i in range(1, n):
        # The element we want to insert into the sorted part
        key = arr.get(i)

        # Start comparing with the element just before the current one
        j = i - 1

        # Shift elements one position to the right while they are bigger than key
        while j >= 0:
            comparisons = comparisons + 1
            if arr.get(j) > key:
                arr.set(j + 1, arr.get(j))
                swaps = swaps + 1
                j = j - 1
            else:
                # Found the right spot, stop shifting
                break

        # Place the key in its correct position
        arr.set(j + 1, key)

        # Print the array after this step
        print("  Step " + str(i) + ": " + str(arr))

    return comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = IntArray(5)
    numbers.set(0, 12)
    numbers.set(1, 11)
    numbers.set(2, 13)
    numbers.set(3, 5)
    numbers.set(4, 6)
    print("Original list: " + str(numbers))
    print("Running insertion sort...\n")

    comps, swps = insertion_sort(numbers)

    print("\nSorted list: " + str(numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps/shifts: " + str(swps))
