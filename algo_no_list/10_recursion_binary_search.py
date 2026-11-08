# 10_recursion_binary_search.py
# Binary search using recursion.
# Binary search works on a SORTED tuple by repeatedly cutting the search
# range in half.  It is much faster than checking every element one by one.
#
# Key ideas:
#   - Base case 1: the item is found at the middle position.
#   - Base case 2: the search range is empty (low > high), item not found.
#   - Recursive case: compare the target with the middle element,
#     then search only the left half or the right half.


def binary_search(sorted_list, target, low, high):
    """Search for target in sorted_list[low..high] using recursion."""
    # Base case: the range is empty, so the item is not in the tuple.
    if low > high:
        print("  low=%d, high=%d -> range is empty, %d not found" % (low, high, target))
        return -1

    # Find the middle index of the current search range.
    mid = (low + high) // 2
    print("  low=%d, high=%d, mid=%d -> checking sorted_list[%d] = %d" % (
        low, high, mid, mid, sorted_list[mid]))

    # Base case: the middle element is the target.
    if sorted_list[mid] == target:
        print("  Found %d at index %d!" % (target, mid))
        return mid

    # Recursive case: target is smaller, search the left half.
    if target < sorted_list[mid]:
        print("  %d < %d, searching LEFT half (low=%d, high=%d)" % (
            target, sorted_list[mid], low, mid - 1))
        return binary_search(sorted_list, target, low, mid - 1)

    # Recursive case: target is larger, search the right half.
    print("  %d > %d, searching RIGHT half (low=%d, high=%d)" % (
        target, sorted_list[mid], mid + 1, high))
    return binary_search(sorted_list, target, mid + 1, high)


if __name__ == "__main__":
    # A sorted tuple of numbers to search through.
    numbers = (2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91)
    print("Sorted tuple:", numbers)
    print()

    print("=== Searching for 23 ===")
    position = binary_search(numbers, 23, 0, len(numbers) - 1)
    print("Result: index %d\n" % position)

    print("=== Searching for 7 (not in tuple) ===")
    position = binary_search(numbers, 7, 0, len(numbers) - 1)
    print("Result: index %d (means not found)\n" % position)

    print("=== Searching for 2 (first element) ===")
    position = binary_search(numbers, 2, 0, len(numbers) - 1)
    print("Result: index %d\n" % position)

    print("=== Searching for 91 (last element) ===")
    position = binary_search(numbers, 91, 0, len(numbers) - 1)
    print("Result: index %d\n" % position)
