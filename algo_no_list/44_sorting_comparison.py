# Sorting Algorithm Comparison
# Runs every sorting algorithm on the same data and counts comparisons and swaps.
# Prints a comparison table at the end.


# ---- Selection Sort ----

def _tuple_swap(t, i, j):
    """Return a new tuple with elements at indices i and j swapped."""
    if i == j:
        return t
    return t[:i] + (t[j],) + t[i + 1:j] + (t[i],) + t[j + 1:]


def selection_sort(arr):
    """Selection sort. Returns (sorted_tuple, comparisons, swaps)."""
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            comparisons = comparisons + 1
            if arr[j] < arr[min_index]:
                min_index = j
        if min_index != i:
            arr = _tuple_swap(arr, i, min_index)
            swaps = swaps + 1
    return arr, comparisons, swaps


# ---- Insertion Sort ----

def _tuple_set(t, i, val):
    """Return a new tuple with element at index i set to val."""
    return t[:i] + (val,) + t[i + 1:]


def insertion_sort(arr):
    """Insertion sort. Returns (sorted_tuple, comparisons, swaps)."""
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons = comparisons + 1
            if arr[j] > key:
                arr = _tuple_set(arr, j + 1, arr[j])
                swaps = swaps + 1
                j = j - 1
            else:
                break
        arr = _tuple_set(arr, j + 1, key)
    return arr, comparisons, swaps


# ---- Bubble Sort ----

def bubble_sort(arr):
    """Bubble sort with early termination. Returns (sorted_tuple, comparisons, swaps)."""
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons = comparisons + 1
            if arr[j] > arr[j + 1]:
                arr = _tuple_swap(arr, j, j + 1)
                swaps = swaps + 1
                swapped = True
        if swapped is False:
            break
    return arr, comparisons, swaps


# ---- Quick Sort ----

def quick_sort_partition(arr, low, high, comparisons, swaps):
    """Partition step for quick sort. Returns the pivot index."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        comparisons = comparisons + 1
        if arr[j] <= pivot:
            i = i + 1
            arr = _tuple_swap(arr, i, j)
            swaps = swaps + 1
    arr = _tuple_swap(arr, i + 1, high)
    swaps = swaps + 1
    return i + 1, arr, comparisons, swaps


def quick_sort_helper(arr, low, high, comparisons, swaps):
    """Recursive quick sort helper."""
    if low < high:
        pivot_index, arr, comparisons, swaps = quick_sort_partition(arr, low, high, comparisons, swaps)
        arr, comparisons, swaps = quick_sort_helper(arr, low, pivot_index - 1, comparisons, swaps)
        arr, comparisons, swaps = quick_sort_helper(arr, pivot_index + 1, high, comparisons, swaps)
    return arr, comparisons, swaps


def quick_sort(arr):
    """Quick sort. Returns (sorted_tuple, comparisons, swaps)."""
    arr, comparisons, swaps = quick_sort_helper(arr, 0, len(arr) - 1, 0, 0)
    return arr, comparisons, swaps


# ---- Merge Sort ----

def merge(left, right):
    """Merge two sorted tuples. Returns (merged, comparisons, swaps)."""
    result = ()
    comparisons = 0
    swaps = 0
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        comparisons = comparisons + 1
        if left[i] <= right[j]:
            result = result + (left[i],)
            i = i + 1
        else:
            result = result + (right[j],)
            j = j + 1
            swaps = swaps + 1

    while i < len(left):
        result = result + (left[i],)
        i = i + 1

    while j < len(right):
        result = result + (right[j],)
        j = j + 1

    return result, comparisons, swaps


def merge_sort(arr):
    """Merge sort. Returns (sorted_tuple, comparisons, swaps)."""
    if len(arr) <= 1:
        return arr, 0, 0

    mid = len(arr) // 2
    left, left_comps, left_swaps = merge_sort(arr[:mid])
    right, right_comps, right_swaps = merge_sort(arr[mid:])

    merged, merge_comps, merge_swaps = merge(left, right)

    total_comps = left_comps + right_comps + merge_comps
    total_swaps = left_swaps + right_swaps + merge_swaps

    return merged, total_comps, total_swaps


# ---- Heap Sort ----

def sift_down(arr, n, i, comparisons, swaps):
    """Move the element at index i down to its correct heap position."""
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
        arr, comparisons, swaps = sift_down(arr, n, largest, comparisons, swaps)

    return arr, comparisons, swaps


def heap_sort(arr):
    """Heap sort. Returns (sorted_tuple, comparisons, swaps)."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        arr, comparisons, swaps = sift_down(arr, n, i, comparisons, swaps)

    # Extract max elements one by one
    for i in range(n - 1, 0, -1):
        arr = _tuple_swap(arr, 0, i)
        swaps = swaps + 1
        arr, comparisons, swaps = sift_down(arr, i, 0, comparisons, swaps)

    return arr, comparisons, swaps


# ---- Bucket Sort ----

def insertion_sort_bucket(bucket):
    """Insertion sort for a small bucket. Returns a sorted tuple."""
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
    """Bucket sort for positive integers. Returns (sorted_tuple, comparisons, swaps)."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    if n == 0:
        return (), comparisons, swaps

    max_val = arr[0]
    for i in range(1, n):
        comparisons = comparisons + 1
        if arr[i] > max_val:
            max_val = arr[i]

    num_buckets = max_val + 1
    buckets = ()
    for b in range(num_buckets):
        buckets = buckets + ((),)

    for i in range(n):
        buckets = _tuple_set(buckets, arr[i], buckets[arr[i]] + (arr[i],))

    result = ()
    for b in range(num_buckets):
        if len(buckets[b]) > 0:
            sorted_bucket = insertion_sort_bucket(buckets[b])
            for item in sorted_bucket:
                result = result + (item,)

    return result, comparisons, swaps


# ---- Radix Sort ----

def counting_sort_by_digit(arr, exp):
    """Counting sort subroutine for a specific digit position. Returns sorted tuple."""
    n = len(arr)
    output = (0,) * n
    count = (0,) * 10

    for i in range(n):
        digit = (arr[i] // exp) % 10
        count = _tuple_set(count, digit, count[digit] + 1)

    for i in range(1, 10):
        count = _tuple_set(count, i, count[i] + count[i - 1])

    i = n - 1
    while i >= 0:
        digit = (arr[i] // exp) % 10
        output = _tuple_set(output, count[digit] - 1, arr[i])
        count = _tuple_set(count, digit, count[digit] - 1)
        i = i - 1

    return output


def radix_sort(arr):
    """Radix sort for positive integers. Returns (sorted_tuple, comparisons, swaps).
    Comparisons are counted as digit extractions; swaps are counted as moves."""
    comparisons = 0
    swaps = 0

    if len(arr) == 0:
        return (), comparisons, swaps

    max_val = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]

    exp = 1
    while max_val // exp > 0:
        # Count digit extractions as comparisons
        for i in range(len(arr)):
            comparisons = comparisons + 1
        arr = counting_sort_by_digit(arr, exp)
        # Count moves as swaps
        swaps = swaps + len(arr)
        exp = exp * 10

    return arr, comparisons, swaps


# ---- Main: Run all algorithms and compare ----

if __name__ == "__main__":
    # The same data for every algorithm
    original = (64, 25, 12, 22, 11, 90, 3, 47, 58, 1)

    print("Sorting Algorithm Comparison")
    print("============================")
    print("Original data: " + str(original))
    print("Data size: " + str(len(original)))
    print("")

    # Store results: each entry is (name, comparisons, swaps)
    results = ()

    # 1. Selection Sort
    data = tuple(original)  # Make a fresh copy
    data, comps, swps = selection_sort(data)
    results = results + (("Selection Sort", comps, swps),)
    print("Selection Sort  -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 2. Insertion Sort
    data = tuple(original)
    data, comps, swps = insertion_sort(data)
    results = results + (("Insertion Sort", comps, swps),)
    print("Insertion Sort  -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 3. Bubble Sort
    data = tuple(original)
    data, comps, swps = bubble_sort(data)
    results = results + (("Bubble Sort", comps, swps),)
    print("Bubble Sort     -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 4. Quick Sort
    data = tuple(original)
    data, comps, swps = quick_sort(data)
    results = results + (("Quick Sort", comps, swps),)
    print("Quick Sort      -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 5. Merge Sort
    data = tuple(original)
    data, comps, swps = merge_sort(data)
    results = results + (("Merge Sort", comps, swps),)
    print("Merge Sort      -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 6. Heap Sort
    data = tuple(original)
    data, comps, swps = heap_sort(data)
    results = results + (("Heap Sort", comps, swps),)
    print("Heap Sort       -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 7. Bucket Sort
    data = tuple(original)
    data, comps, swps = bucket_sort(data)
    results = results + (("Bucket Sort", comps, swps),)
    print("Bucket Sort     -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 8. Radix Sort
    data = tuple(original)
    data, comps, swps = radix_sort(data)
    results = results + (("Radix Sort", comps, swps),)
    print("Radix Sort      -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # Print a formatted comparison table
    print("")
    print("=" * 55)
    print("COMPARISON TABLE")
    print("=" * 55)
    print("{:<20} {:>12} {:>12}".format("Algorithm", "Comparisons", "Swaps"))
    print("-" * 55)
    for name, comps, swps in results:
        print("{:<20} {:>12} {:>12}".format(name, comps, swps))
    print("=" * 55)
