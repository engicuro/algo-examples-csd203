# Bucket Sort
# Distribute elements into buckets, sort each bucket with insertion sort,
# then concatenate all buckets in order. Works well for uniform data.


def _tuple_set(t, i, val):
    """Return a new tuple with element at index i set to val."""
    return t[:i] + (val,) + t[i + 1:]


def insertion_sort_bucket(bucket):
    """Sort a small bucket using insertion sort. Returns a sorted tuple."""
    result = ()
    for i in range(len(bucket)):
        result = result + (bucket[i],)

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result = _tuple_set(result, j + 1, result[j])
            j = j - 1
        result = _tuple_set(result, j + 1, key)
    return result


def bucket_sort(arr):
    """Sort a tuple of positive integers using bucket sort. Returns the sorted tuple, number of comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    if n == 0:
        return (), comparisons, swaps

    # Find the maximum value to know how many buckets we need
    max_val = arr[0]
    for i in range(1, n):
        comparisons = comparisons + 1
        if arr[i] > max_val:
            max_val = arr[i]

    # Create empty buckets (one bucket for each possible value)
    num_buckets = max_val + 1
    buckets = ()
    for b in range(num_buckets):
        buckets = buckets + ((),)

    # Distribute elements into buckets based on their value
    print("  Distributing into " + str(num_buckets) + " buckets...")
    for i in range(n):
        value = arr[i]
        buckets = _tuple_set(buckets, value, buckets[value] + (value,))

    # Print each non-empty bucket
    for b in range(num_buckets):
        if len(buckets[b]) > 0:
            print("  Bucket[" + str(b) + "]: " + str(buckets[b]))

    # Sort each bucket and concatenate
    result = ()
    for b in range(num_buckets):
        if len(buckets[b]) > 0:
            sorted_bucket = insertion_sort_bucket(buckets[b])
            for item in sorted_bucket:
                result = result + (item,)

    return result, comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = (4, 2, 2, 8, 3, 3, 1)
    print("Original tuple: " + str(numbers))
    print("Running bucket sort...\n")

    sorted_numbers, comps, swps = bucket_sort(numbers)

    print("\nSorted tuple: " + str(sorted_numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps: " + str(swps))
