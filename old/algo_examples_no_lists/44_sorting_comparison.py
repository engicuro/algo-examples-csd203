# Sorting Algorithm Comparison
# Runs every sorting algorithm on the same data and counts comparisons and swaps.
# Prints a comparison table at the end.

from _structures import IntArray, LinkedList


# ---- Selection Sort ----

def selection_sort(arr):
    """Selection sort. Returns (comparisons, swaps)."""
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            comparisons = comparisons + 1
            if arr.get(j) < arr.get(min_index):
                min_index = j
        if min_index != i:
            temp = arr.get(i)
            arr.set(i, arr.get(min_index))
            arr.set(min_index, temp)
            swaps = swaps + 1
    return comparisons, swaps


# ---- Insertion Sort ----

def insertion_sort(arr):
    """Insertion sort. Returns (comparisons, swaps)."""
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(1, n):
        key = arr.get(i)
        j = i - 1
        while j >= 0:
            comparisons = comparisons + 1
            if arr.get(j) > key:
                arr.set(j + 1, arr.get(j))
                swaps = swaps + 1
                j = j - 1
            else:
                break
        arr.set(j + 1, key)
    return comparisons, swaps


# ---- Bubble Sort ----

def bubble_sort(arr):
    """Bubble sort with early termination. Returns (comparisons, swaps)."""
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons = comparisons + 1
            if arr.get(j) > arr.get(j + 1):
                temp = arr.get(j)
                arr.set(j, arr.get(j + 1))
                arr.set(j + 1, temp)
                swaps = swaps + 1
                swapped = True
        if swapped is False:
            break
    return comparisons, swaps


# ---- Quick Sort ----

def quick_sort_partition(arr, low, high, comparisons, swaps):
    """Partition step for quick sort. Returns the pivot index."""
    pivot = arr.get(high)
    i = low - 1
    for j in range(low, high):
        comparisons = comparisons + 1
        if arr.get(j) <= pivot:
            i = i + 1
            temp = arr.get(i)
            arr.set(i, arr.get(j))
            arr.set(j, temp)
            swaps = swaps + 1
    temp = arr.get(i + 1)
    arr.set(i + 1, arr.get(high))
    arr.set(high, temp)
    swaps = swaps + 1
    return i + 1, comparisons, swaps


def quick_sort_helper(arr, low, high, comparisons, swaps):
    """Recursive quick sort helper."""
    if low < high:
        pivot_index, comparisons, swaps = quick_sort_partition(arr, low, high, comparisons, swaps)
        comparisons, swaps = quick_sort_helper(arr, low, pivot_index - 1, comparisons, swaps)
        comparisons, swaps = quick_sort_helper(arr, pivot_index + 1, high, comparisons, swaps)
    return comparisons, swaps


def quick_sort(arr):
    """Quick sort. Returns (comparisons, swaps)."""
    return quick_sort_helper(arr, 0, len(arr) - 1, 0, 0)


# ---- Merge Sort ----

def merge_sort(arr):
    """Merge sort. Returns (sorted_list, comparisons, swaps)."""
    if len(arr) <= 1:
        return arr, 0, 0

    mid = len(arr) // 2
    left_half = IntArray(mid)
    for i in range(mid):
        left_half.set(i, arr.get(i))
    right_half = IntArray(len(arr) - mid)
    for i in range(len(arr) - mid):
        right_half.set(i, arr.get(mid + i))

    left, left_comps, left_swaps = merge_sort(left_half)
    right, right_comps, right_swaps = merge_sort(right_half)

    merged, merge_comps, merge_swaps = merge(left, right)

    total_comps = left_comps + right_comps + merge_comps
    total_swaps = left_swaps + right_swaps + merge_swaps

    return merged, total_comps, total_swaps


def merge(left, right):
    """Merge two sorted lists. Returns (merged, comparisons, swaps)."""
    result = LinkedList()
    comparisons = 0
    swaps = 0
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        comparisons = comparisons + 1
        if left.get(i) <= right.get(j):
            result.append(left.get(i))
            i = i + 1
        else:
            result.append(right.get(j))
            j = j + 1
            swaps = swaps + 1

    while i < len(left):
        result.append(left.get(i))
        i = i + 1

    while j < len(right):
        result.append(right.get(j))
        j = j + 1

    return result, comparisons, swaps


# ---- Heap Sort ----

def heap_sort(arr):
    """Heap sort. Returns (comparisons, swaps)."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        comparisons, swaps = sift_down(arr, n, i, comparisons, swaps)

    # Extract max elements one by one
    for i in range(n - 1, 0, -1):
        temp = arr.get(0)
        arr.set(0, arr.get(i))
        arr.set(i, temp)
        swaps = swaps + 1
        comparisons, swaps = sift_down(arr, i, 0, comparisons, swaps)

    return comparisons, swaps


def sift_down(arr, n, i, comparisons, swaps):
    """Move the element at index i down to its correct heap position."""
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
        comparisons, swaps = sift_down(arr, n, largest, comparisons, swaps)

    return comparisons, swaps


# ---- Bucket Sort ----

def insertion_sort_bucket(bucket):
    """Insertion sort for a small bucket."""
    for i in range(1, len(bucket)):
        key = bucket.get(i)
        j = i - 1
        while j >= 0 and bucket.get(j) > key:
            bucket.set(j + 1, bucket.get(j))
            j = j - 1
        bucket.set(j + 1, key)
    return bucket


def bucket_sort(arr):
    """Bucket sort for positive integers. Returns (comparisons, swaps)."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    if n == 0:
        return comparisons, swaps

    max_val = arr.get(0)
    for i in range(1, n):
        comparisons = comparisons + 1
        if arr.get(i) > max_val:
            max_val = arr.get(i)

    num_buckets = max_val + 1
    buckets = []
    for b in range(num_buckets):
        buckets.append(LinkedList())

    for i in range(n):
        buckets[arr.get(i)].append(arr.get(i))

    result = LinkedList()
    for b in range(num_buckets):
        if len(buckets[b]) > 0:
            sorted_bucket = insertion_sort_bucket(buckets[b])
            for idx in range(len(sorted_bucket)):
                result.append(sorted_bucket.get(idx))

    for i in range(n):
        arr.set(i, result.get(i))

    return comparisons, swaps


# ---- Radix Sort ----

def counting_sort_by_digit(arr, exp):
    """Counting sort subroutine for a specific digit position."""
    n = len(arr)
    output = IntArray(n)
    count = IntArray(10)

    for i in range(n):
        digit = (arr.get(i) // exp) % 10
        count.set(digit, count.get(digit) + 1)

    for i in range(1, 10):
        count.set(i, count.get(i) + count.get(i - 1))

    i = n - 1
    while i >= 0:
        digit = (arr.get(i) // exp) % 10
        output.set(count.get(digit) - 1, arr.get(i))
        count.set(digit, count.get(digit) - 1)
        i = i - 1

    for i in range(n):
        arr.set(i, output.get(i))


def radix_sort(arr):
    """Radix sort for positive integers. Returns (comparisons, swaps).
    Comparisons are counted as digit extractions; swaps are counted as moves."""
    comparisons = 0
    swaps = 0

    if len(arr) == 0:
        return comparisons, swaps

    max_val = arr.get(0)
    for i in range(1, len(arr)):
        if arr.get(i) > max_val:
            max_val = arr.get(i)

    exp = 1
    while max_val // exp > 0:
        # Count digit extractions as comparisons
        for i in range(len(arr)):
            comparisons = comparisons + 1
        counting_sort_by_digit(arr, exp)
        # Count moves as swaps
        swaps = swaps + len(arr)
        exp = exp * 10

    return comparisons, swaps


# ---- Main: Run all algorithms and compare ----

if __name__ == "__main__":
    # The same data for every algorithm
    original = IntArray(10)
    original.set(0, 64)
    original.set(1, 25)
    original.set(2, 12)
    original.set(3, 22)
    original.set(4, 11)
    original.set(5, 90)
    original.set(6, 3)
    original.set(7, 47)
    original.set(8, 58)
    original.set(9, 1)

    print("Sorting Algorithm Comparison")
    print("============================")
    print("Original data: " + str(original))
    print("Data size: " + str(len(original)))
    print("")

    # Store results: each entry is (name, comparisons, swaps)
    results = LinkedList()

    # 1. Selection Sort
    data = IntArray(len(original))
    for i in range(len(original)):
        data.set(i, original.get(i))
    comps, swps = selection_sort(data)
    results.append(("Selection Sort", comps, swps))
    print("Selection Sort  -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 2. Insertion Sort
    data = IntArray(len(original))
    for i in range(len(original)):
        data.set(i, original.get(i))
    comps, swps = insertion_sort(data)
    results.append(("Insertion Sort", comps, swps))
    print("Insertion Sort  -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 3. Bubble Sort
    data = IntArray(len(original))
    for i in range(len(original)):
        data.set(i, original.get(i))
    comps, swps = bubble_sort(data)
    results.append(("Bubble Sort", comps, swps))
    print("Bubble Sort     -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 4. Quick Sort
    data = IntArray(len(original))
    for i in range(len(original)):
        data.set(i, original.get(i))
    comps, swps = quick_sort(data)
    results.append(("Quick Sort", comps, swps))
    print("Quick Sort      -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 5. Merge Sort
    data = IntArray(len(original))
    for i in range(len(original)):
        data.set(i, original.get(i))
    sorted_data, comps, swps = merge_sort(data)
    results.append(("Merge Sort", comps, swps))
    print("Merge Sort      -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 6. Heap Sort
    data = IntArray(len(original))
    for i in range(len(original)):
        data.set(i, original.get(i))
    comps, swps = heap_sort(data)
    results.append(("Heap Sort", comps, swps))
    print("Heap Sort       -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 7. Bucket Sort
    data = IntArray(len(original))
    for i in range(len(original)):
        data.set(i, original.get(i))
    comps, swps = bucket_sort(data)
    results.append(("Bucket Sort", comps, swps))
    print("Bucket Sort     -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 8. Radix Sort
    data = IntArray(len(original))
    for i in range(len(original)):
        data.set(i, original.get(i))
    comps, swps = radix_sort(data)
    results.append(("Radix Sort", comps, swps))
    print("Radix Sort      -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # Print a formatted comparison table
    print("")
    print("=" * 55)
    print("COMPARISON TABLE")
    print("=" * 55)
    print("{:<20} {:>12} {:>12}".format("Algorithm", "Comparisons", "Swaps"))
    print("-" * 55)
    for i in range(len(results)):
        name, comps, swps = results.get(i)
        print("{:<20} {:>12} {:>12}".format(name, comps, swps))
    print("=" * 55)
