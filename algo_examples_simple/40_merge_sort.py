# Merge Sort
# Split the list in half, sort each half, then merge them back together.
# Prints the list at each merge step so you can see how it builds up.


def merge(left, right):
    """Merge two sorted lists into one sorted list. Returns the merged list and stats."""
    result = []
    comparisons = 0
    swaps = 0  # Swaps are not really a thing in merge sort, but we count moves

    i = 0  # Index for the left list
    j = 0  # Index for the right list

    # Compare elements from both lists and pick the smaller one
    while i < len(left) and j < len(right):
        comparisons = comparisons + 1
        if left[i] <= right[j]:
            result.append(left[i])
            i = i + 1
        else:
            result.append(right[j])
            j = j + 1
            swaps = swaps + 1

    # Add any remaining elements from the left list
    while i < len(left):
        result.append(left[i])
        i = i + 1

    # Add any remaining elements from the right list
    while j < len(right):
        result.append(right[j])
        j = j + 1

    return result, comparisons, swaps


def merge_sort(arr):
    """Sort a list using merge sort. Returns the sorted list, comparisons, and swaps."""
    # A list with 0 or 1 elements is already sorted
    if len(arr) <= 1:
        return arr, 0, 0

    # Split the list in half
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
    numbers = [38, 27, 43, 3, 9, 82, 10]
    print("Original list: " + str(numbers))
    print("Running merge sort...\n")

    sorted_numbers, comps, swps = merge_sort(numbers)

    print("\nSorted list: " + str(sorted_numbers))
    print("Total comparisons: " + str(comps))
    print("Total moves: " + str(swps))
