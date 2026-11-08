# Merge Sort
# Split the tuple in half, sort each half, then merge them back together.
# Prints the tuple at each merge step so you can see how it builds up.


def merge(left, right):
    """Merge two sorted tuples into one sorted tuple. Returns the merged tuple and stats."""
    result = ()
    comparisons = 0
    swaps = 0  # Swaps are not really a thing in merge sort, but we count moves

    i = 0  # Index for the left tuple
    j = 0  # Index for the right tuple

    # Compare elements from both tuples and pick the smaller one
    while i < len(left) and j < len(right):
        comparisons = comparisons + 1
        if left[i] <= right[j]:
            result = result + (left[i],)
            i = i + 1
        else:
            result = result + (right[j],)
            j = j + 1
            swaps = swaps + 1

    # Add any remaining elements from the left tuple
    while i < len(left):
        result = result + (left[i],)
        i = i + 1

    # Add any remaining elements from the right tuple
    while j < len(right):
        result = result + (right[j],)
        j = j + 1

    return result, comparisons, swaps


def merge_sort(arr):
    """Sort a tuple using merge sort. Returns the sorted tuple, comparisons, and swaps."""
    # A tuple with 0 or 1 elements is already sorted
    if len(arr) <= 1:
        return arr, 0, 0

    # Split the tuple in half
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    print("  Splitting: " + str(arr) + " -> " + str(left_half) + " and " + str(right_half))

    # Sort each half recursively
    sorted_left, left_comps, left_swaps = merge_sort(left_half)
    sorted_right, right_comps, right_swaps = merge_sort(right_half)

    # Merge the two sorted halves
    merged, merge_comps, merge_swaps = merge(sorted_left, sorted_right)

    print("  Merging: " + str(sorted_left) + " + " + str(sorted_right) + " -> " + str(merged))

    total_comparisons = left_comps + right_comps + merge_comps
    total_swaps = left_swaps + right_swaps + merge_swaps

    return merged, total_comparisons, total_swaps


if __name__ == "__main__":
    # Example usage
    numbers = (38, 27, 43, 3, 9, 82, 10)
    print("Original tuple: " + str(numbers))
    print("Running merge sort...\n")

    sorted_numbers, comps, swps = merge_sort(numbers)

    print("\nSorted tuple: " + str(sorted_numbers))
    print("Total comparisons: " + str(comps))
    print("Total moves: " + str(swps))
