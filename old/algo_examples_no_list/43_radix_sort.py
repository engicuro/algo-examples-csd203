# Radix Sort (LSD - Least Significant Digit)
# Sorts positive integers by processing digits from right to left.
# Uses a simple counting sort subroutine for each digit position.
# Prints the list after sorting by each digit.


def counting_sort_by_digit(arr, exp):
    """Sort arr based on the digit at the given exponent place (1=ones, 10=tens, etc.).
    exp is 1, 10, 100, etc. This is the counting sort subroutine for radix sort."""
    n = len(arr)
    output = [0] * n  # Output array to hold sorted results
    count = [0] * 10  # Count array for digits 0-9

    # Count how many times each digit appears at this position
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] = count[digit] + 1

    # Change count[i] so it contains the actual position of this digit in output
    for i in range(1, 10):
        count[i] = count[i] + count[i - 1]

    # Build the output array by placing elements in their correct position
    # Go backward to keep the sort stable
    i = n - 1
    while i >= 0:
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] = count[digit] - 1
        i = i - 1

    # Copy the output array back into arr
    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr):
    """Sort a list of positive integers using radix sort.
    Returns the number of passes (digit positions processed)."""
    if len(arr) == 0:
        return 0

    # Find the maximum number to know how many digits we need to process
    max_val = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]

    # Do counting sort for each digit position (ones, tens, hundreds, ...)
    exp = 1
    passes = 0

    while max_val // exp > 0:
        passes = passes + 1
        print("  Pass " + str(passes) + " (sorting by " + str(exp) + "s place): " + str(arr))
        counting_sort_by_digit(arr, exp)
        print("  After pass " + str(passes) + ": " + str(arr))
        exp = exp * 10

    return passes


if __name__ == "__main__":
    # Example usage
    numbers = [170, 45, 75, 90, 802, 24, 2, 66]
    print("Original list: " + str(numbers))
    print("Running radix sort...\n")

    num_passes = radix_sort(numbers)

    print("\nSorted list: " + str(numbers))
    print("Total passes: " + str(num_passes))
