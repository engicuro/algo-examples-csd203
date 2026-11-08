# Sorting Algorithm Comparison
# Runs every sorting algorithm on the same data and counts comparisons and swaps.
# Prints a comparison table at the end.


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
            if arr[j] < arr[min_index]:
                min_index = j
        if min_index != i:
            temp = arr[i]
            arr[i] = arr[min_index]
            arr[min_index] = temp
            swaps = swaps + 1
    return comparisons, swaps


# ---- Insertion Sort ----

def insertion_sort(arr):
    """Insertion sort. Returns (comparisons, swaps)."""
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons = comparisons + 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps = swaps + 1
                j = j - 1
            else:
                break
        arr[j + 1] = key
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
            if arr[j] > arr[j + 1]:
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
                swaps = swaps + 1
                swapped = True
        if swapped is False:
            break
    return comparisons, swaps


# ---- Quick Sort ----

def quick_sort_partition(arr, low, high, comparisons, swaps):
    """Partition step for quick sort. Returns the pivot index."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        comparisons = comparisons + 1
        if arr[j] <= pivot:
            i = i + 1
            temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp
            swaps = swaps + 1
    temp = arr[i + 1]
    arr[i + 1] = arr[high]
    arr[high] = temp
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
    left, left_comps, left_swaps = merge_sort(arr[:mid])
    right, right_comps, right_swaps = merge_sort(arr[mid:])

    merged, merge_comps, merge_swaps = merge(left, right)

    total_comps = left_comps + right_comps + merge_comps
    total_swaps = left_swaps + right_swaps + merge_swaps

    return merged, total_comps, total_swaps


def merge(left, right):
    """Merge two sorted lists. Returns (merged, comparisons, swaps)."""
    result = []
    comparisons = 0
    swaps = 0
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        comparisons = comparisons + 1
        if left[i] <= right[j]:
            result.append(left[i])
            i = i + 1
        else:
            result.append(right[j])
            j = j + 1
            swaps = swaps + 1

    while i < len(left):
        result.append(left[i])
        i = i + 1

    while j < len(right):
        result.append(right[j])
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
        temp = arr[0]
        arr[0] = arr[i]
        arr[i] = temp
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
        if arr[left] > arr[largest]:
            largest = left

    if right < n:
        comparisons = comparisons + 1
        if arr[right] > arr[largest]:
            largest = right

    if largest != i:
        temp = arr[i]
        arr[i] = arr[largest]
        arr[largest] = temp
        swaps = swaps + 1
        comparisons, swaps = sift_down(arr, n, largest, comparisons, swaps)

    return comparisons, swaps


# ---- Bucket Sort ----

def insertion_sort_bucket(bucket):
    """Insertion sort for a small bucket."""
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j] > key:
            bucket[j + 1] = bucket[j]
            j = j - 1
        bucket[j + 1] = key
    return bucket


def bucket_sort(arr):
    """Bucket sort for positive integers. Returns (comparisons, swaps)."""
    comparisons = 0
    swaps = 0
    n = len(arr)

    if n == 0:
        return comparisons, swaps

    max_val = arr[0]
    for i in range(1, n):
        comparisons = comparisons + 1
        if arr[i] > max_val:
            max_val = arr[i]

    num_buckets = max_val + 1
    buckets = []
    for b in range(num_buckets):
        buckets.append([])

    for i in range(n):
        buckets[arr[i]].append(arr[i])

    result = []
    for b in range(num_buckets):
        if len(buckets[b]) > 0:
            sorted_bucket = insertion_sort_bucket(buckets[b])
            for item in sorted_bucket:
                result.append(item)

    for i in range(n):
        arr[i] = result[i]

    return comparisons, swaps


# ---- Radix Sort ----

def counting_sort_by_digit(arr, exp):
    """Counting sort subroutine for a specific digit position."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] = count[digit] + 1

    for i in range(1, 10):
        count[i] = count[i] + count[i - 1]

    i = n - 1
    while i >= 0:
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] = count[digit] - 1
        i = i - 1

    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr):
    """Radix sort for positive integers. Returns (comparisons, swaps).
    Comparisons are counted as digit extractions; swaps are counted as moves."""
    comparisons = 0
    swaps = 0

    if len(arr) == 0:
        return comparisons, swaps

    max_val = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]

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
    original = [64, 25, 12, 22, 11, 90, 3, 47, 58, 1]

    print("Sorting Algorithm Comparison")
    print("============================")
    print("Original data: " + str(original))
    print("Data size: " + str(len(original)))
    print("")

    # Store results: each entry is (name, comparisons, swaps)
    results = []

    # 1. Selection Sort
    data = list(original)  # Make a fresh copy
    comps, swps = selection_sort(data)
    results.append(("Selection Sort", comps, swps))
    print("Selection Sort  -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 2. Insertion Sort
    data = list(original)
    comps, swps = insertion_sort(data)
    results.append(("Insertion Sort", comps, swps))
    print("Insertion Sort  -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 3. Bubble Sort
    data = list(original)
    comps, swps = bubble_sort(data)
    results.append(("Bubble Sort", comps, swps))
    print("Bubble Sort     -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 4. Quick Sort
    data = list(original)
    comps, swps = quick_sort(data)
    results.append(("Quick Sort", comps, swps))
    print("Quick Sort      -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 5. Merge Sort
    data = list(original)
    sorted_data, comps, swps = merge_sort(data)
    results.append(("Merge Sort", comps, swps))
    print("Merge Sort      -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 6. Heap Sort
    data = list(original)
    comps, swps = heap_sort(data)
    results.append(("Heap Sort", comps, swps))
    print("Heap Sort       -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 7. Bucket Sort
    data = list(original)
    comps, swps = bucket_sort(data)
    results.append(("Bucket Sort", comps, swps))
    print("Bucket Sort     -> comparisons: " + str(comps) + ", swaps: " + str(swps))

    # 8. Radix Sort
    data = list(original)
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
    for name, comps, swps in results:
        print("{:<20} {:>12} {:>12}".format(name, comps, swps))
    print("=" * 55)
