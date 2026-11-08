# Bucket Sort
# Distribute elements into buckets, sort each bucket with insertion sort,
# then concatenate all buckets in order. Works well for uniform data.

from _structures import IntArray, LinkedList


def insertion_sort_bucket(bucket):
    """Sort a small bucket using insertion sort."""
    for i in range(1, len(bucket)):
        key = bucket.get(i)
        j = i - 1
        while j >= 0 and bucket.get(j) > key:
            bucket.set(j + 1, bucket.get(j))
            j = j - 1
        bucket.set(j + 1, key)
    return bucket


def bucket_sort(arr):
    """Sort a list using bucket sort. Returns the number of comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    if n == 0:
        return comparisons, swaps

    # Find the maximum value to know how many buckets we need
    max_val = arr.get(0)
    for i in range(1, n):
        comparisons = comparisons + 1
        if arr.get(i) > max_val:
            max_val = arr.get(i)

    # Create empty buckets (one bucket for each possible value)
    num_buckets = max_val + 1
    buckets = []
    for b in range(num_buckets):
        buckets.append(LinkedList())

    # Distribute elements into buckets based on their value
    print("  Distributing into " + str(num_buckets) + " buckets...")
    for i in range(n):
        value = arr.get(i)
        buckets[value].append(value)

    # Print each non-empty bucket
    for b in range(num_buckets):
        if len(buckets[b]) > 0:
            print("  Bucket[" + str(b) + "]: " + str(buckets[b]))

    # Sort each bucket and concatenate
    result = LinkedList()
    for b in range(num_buckets):
        if len(buckets[b]) > 0:
            sorted_bucket = insertion_sort_bucket(buckets[b])
            for idx in range(len(sorted_bucket)):
                result.append(sorted_bucket.get(idx))

    # Copy result back into the original list
    for i in range(n):
        arr.set(i, result.get(i))

    return comparisons, swaps


if __name__ == "__main__":
    # Example usage
    numbers = IntArray(7)
    numbers.set(0, 4)
    numbers.set(1, 2)
    numbers.set(2, 2)
    numbers.set(3, 8)
    numbers.set(4, 3)
    numbers.set(5, 3)
    numbers.set(6, 1)
    print("Original list: " + str(numbers))
    print("Running bucket sort...\n")

    comps, swps = bucket_sort(numbers)

    print("\nSorted list: " + str(numbers))
    print("Total comparisons: " + str(comps))
    print("Total swaps: " + str(swps))
