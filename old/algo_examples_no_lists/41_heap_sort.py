# Heap Sort
# Build a max heap from the list, then repeatedly extract the largest element.
# Uses a simple list (no heapq module). Prints the list after each extraction.

from _structures import IntArray


def heapify(arr, n, i):
    """Make sure the subtree rooted at index i is a max heap.
    n is the size of the heap. This function fixes one violation downward."""
    largest = i  # Start by assuming the root is the largest
    left = 2 * i + 1   # Left child index
    right = 2 * i + 2  # Right child index

    # Check if the left child exists and is bigger than the root
    if left < n and arr.get(left) > arr.get(largest):
        largest = left

    # Check if the right child exists and is bigger than the current largest
    if right < n and arr.get(right) > arr.get(largest):
        largest = right

    # If the largest is not the root, swap and continue heapifying
    if largest != i:
        temp = arr.get(i)
        arr.set(i, arr.get(largest))
        arr.set(largest, temp)

        # Recursively fix the affected subtree
        heapify(arr, n, largest)


def heap_sort(arr):
    """Sort a list using heap sort. Returns the number of comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    # Count comparisons and swaps during heapify by wrapping it
    # Build a max heap: start from the last non-leaf node and go backward
    for i in range(n // 2 - 1, -1, -1):
        comparisons, swaps = build_heap_count(arr, n, i, comparisons, swaps)

    print("  Max heap built: " + str(arr))

    # Extract elements one by one from the heap
    for i in range(n - 1, 0, -1):
        # Move the current root (max) to the end
        temp = arr.get(0)
        arr.set(0, arr.get(i))
        arr.set(i, temp)
        swaps = swaps + 1

        print("  Extracted max to position " + str(i) + ": " + str(arr))

        # Heapify the reduced heap
        comparisons, swaps = heapify_count(arr, i, 0, comparisons, swaps)

    return comparisons, swaps


def build_heap_count(arr, n, i, comparisons, swaps):
    """Heapify and count comparisons/swaps (iterative style for counting)."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n:
        comparisons = comparisons + 1
        if arr.get(left) > arr.get(largest):
            largest = left

    if right < n:
        comparisons = comparisons + 1
        if arr.get(right) > arr.get(largest):
            largest = right

    if largest != i:
        temp = arr.get(i)
        arr.set(i, arr.get(largest))
        arr.set(largest, temp)
        swaps = swaps + 1

        # Continue heapifying the affected subtree
        comparisons, swaps = build_heap_count(arr, n, largest, comparisons, swaps)

    return comparisons, swaps


def heapify_count(arr, n, i, comparisons, swaps):
    """Heapify and count comparisons/swaps."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n:
        comparisons = comparisons + 1
        if arr.get(left) > arr.get(largest):
            largest = left

    if right < n:
        comparisons = comparisons + 1
        if arr.get(right) > arr.get(largest):
            largest = right

    if largest != i:
        temp = arr.get(i)
        arr.set(i, arr.get(largest))
        arr.set(largest, temp)
        swaps = swaps + 1

        comparisons, swaps = heapify_count(arr, n, largest, comparisons, swaps)

    return comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = IntArray(6)
    numbers.set(0, 12)
    numbers.set(1, 11)
    numbers.set(2, 13)
    numbers.set(3, 5)
    numbers.set(4, 6)
    numbers.set(5, 7)
    print("Original list: " + str(numbers))
    print("Running heap sort...\n")

    comps, swps = heap_sort(numbers)

    print("\nSorted list: " + str(numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps: " + str(swps))
