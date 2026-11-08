# Heap Sort
# Build a max heap from the tuple, then repeatedly extract the largest element.
# Uses a simple tuple (no heapq module). Prints the tuple after each extraction.


def _tuple_swap(t, i, j):
    """Return a new tuple with elements at indices i and j swapped."""
    if i == j:
        return t
    return t[:i] + (t[j],) + t[i + 1:j] + (t[i],) + t[j + 1:]


def _tuple_set(t, i, val):
    """Return a new tuple with element at index i set to val."""
    return t[:i] + (val,) + t[i + 1:]


def heapify(arr, n, i):
    """Make sure the subtree rooted at index i is a max heap.
    n is the size of the heap. This function fixes one violation downward."""
    largest = i  # Start by assuming the root is the largest
    left = 2 * i + 1   # Left child index
    right = 2 * i + 2  # Right child index

    # Check if the left child exists and is bigger than the root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check if the right child exists and is bigger than the current largest
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If the largest is not the root, swap and continue heapifying
    if largest != i:
        arr = _tuple_swap(arr, i, largest)

        # Recursively fix the affected subtree
        arr = heapify(arr, n, largest)

    return arr


def build_heap_count(arr, n, i, comparisons, swaps):
    """Heapify and count comparisons/swaps (iterative style for counting)."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n:
        comparisons = comparisons + 1
        if arr[left] > arr[largest]:
            largest = left

    if right < n:
        comparisons = comparisons + 1
        if arr[right] > arr[largest]:
            largest = right

    if largest != i:
        arr = _tuple_swap(arr, i, largest)
        swaps = swaps + 1

        # Continue heapifying the affected subtree
        arr, comparisons, swaps = build_heap_count(arr, n, largest, comparisons, swaps)

    return arr, comparisons, swaps


def heapify_count(arr, n, i, comparisons, swaps):
    """Heapify and count comparisons/swaps."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n:
        comparisons = comparisons + 1
        if arr[left] > arr[largest]:
            largest = left

    if right < n:
        comparisons = comparisons + 1
        if arr[right] > arr[largest]:
            largest = right

    if largest != i:
        arr = _tuple_swap(arr, i, largest)
        swaps = swaps + 1

        arr, comparisons, swaps = heapify_count(arr, n, largest, comparisons, swaps)

    return arr, comparisons, swaps


def heap_sort(arr):
    """Sort a tuple using heap sort. Returns the sorted tuple, number of comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    # Count comparisons and swaps during heapify by wrapping it
    # Build a max heap: start from the last non-leaf node and go backward
    for i in range(n // 2 - 1, -1, -1):
        arr, comparisons, swaps = build_heap_count(arr, n, i, comparisons, swaps)

    print("  Max heap built: " + str(arr))

    # Extract elements one by one from the heap
    for i in range(n - 1, 0, -1):
        # Move the current root (max) to the end
        arr = _tuple_swap(arr, 0, i)
        swaps = swaps + 1

        print("  Extracted max to position " + str(i) + ": " + str(arr))

        # Heapify the reduced heap
        arr, comparisons, swaps = heapify_count(arr, i, 0, comparisons, swaps)

    return arr, comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = (12, 11, 13, 5, 6, 7)
    print("Original tuple: " + str(numbers))
    print("Running heap sort...\n")

    sorted_numbers, comps, swps = heap_sort(numbers)

    print("\nSorted tuple: " + str(sorted_numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps: " + str(swps))
