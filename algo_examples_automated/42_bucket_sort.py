"""
42_bucket_sort.py — Bucket Sort Algorithm

Bucket sort is a distribution-based sorting algorithm that partitions an
array into a number of "buckets." Each bucket is then sorted individually
— either with a different sorting algorithm or by recursively applying
bucket sort — and the sorted buckets are concatenated to produce the
final sorted output.

How it works (step by step):
  1. Create k empty buckets (lists).
  2. Scatter: iterate over the input and place each element into the
     appropriate bucket based on its value (mapping function).
  3. Sort each non-empty bucket individually.
  4. Gather: concatenate all buckets in order to form the sorted result.

Time complexity:
  - Average case:  O(n + k)  where n = number of elements, k = num buckets
  - Worst case:    O(n²)     when all elements land in a single bucket
  - Best case:     O(n + k)  when elements are uniformly distributed

Space complexity:
  - O(n + k) — we store all n elements across k buckets plus the output.

When bucket sort is most effective:
  - Input is uniformly distributed over a known range (e.g., floats in [0,1)).
  - The number of buckets k is chosen to be roughly proportional to n.
  - The mapping function distributes elements evenly across buckets.

Why bucket sort matters:
  - It achieves linear average-case time, beating the O(n log n) comparison
    lower bound — but only under the assumption of uniform distribution.
  - It is a stable sort (preserves relative order of equal elements) when
    the per-bucket sort is stable.
  - It is NOT an in-place sort; it requires extra memory for the buckets.
"""

from typing import List, Callable, Optional


def insertion_sort(bucket: List[float]) -> List[float]:
    """Sort a single bucket using insertion sort.

    Insertion sort is chosen for individual buckets because:
      - It is simple and stable (preserves relative order of equal elements).
      - It performs well on small arrays (low overhead, no recursion).
      - It is adaptive: nearly-sorted buckets are sorted in near-O(n) time.

    Args:
        bucket: A list of elements to sort in place.

    Returns:
        The sorted bucket (same list object, sorted in place).
    """
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        # Shift elements that are greater than key one position right
        while j >= 0 and bucket[j] > key:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key
    return bucket


def bucket_sort(arr: List[float], num_buckets: int = 10) -> List[float]:
    """Sort a list of numbers using the bucket sort algorithm.

    Each element is mapped to a bucket index by multiplying its normalized
    value (element / max_value) by the number of buckets.  After distribution,
    each bucket is sorted with insertion sort, and all buckets are concatenated.

    Args:
        arr: The list of numbers (int or float) to sort.
        num_buckets: The number of buckets to create (default: 10).

    Returns:
        A new list containing all elements from arr in sorted order.

    Raises:
        ValueError: If num_buckets is less than 1.
    """
    if num_buckets < 1:
        raise ValueError(f"num_buckets must be >= 1, got {num_buckets}")

    n = len(arr)
    if n <= 1:
        return list(arr)

    # --- Step 1: Find the range of input values ---
    # We need the maximum value to normalize elements into bucket indices.
    # Using max(arr) ensures the mapping covers the full range.
    max_value = max(arr)

    # Edge case: all elements are the same (max == min == 0 or constant)
    if max_value == 0:
        return list(arr)

    # --- Step 2: Create empty buckets ---
    # Each bucket is a list that will hold elements falling into that range.
    buckets: List[List[float]] = [[] for _ in range(num_buckets)]

    # --- Step 3: Scatter — distribute elements into buckets ---
    # Mapping function: bucket_index = int((element / max_value) * num_buckets)
    # Clamped to [0, num_buckets - 1] to handle edge cases where element == max_value.
    for element in arr:
        # Normalize element to [0, 1) then scale to bucket range
        index = int((element / max_value) * num_buckets)
        # Clamp the last element into the final bucket
        index = min(index, num_buckets - 1)
        buckets[index].append(element)

    # --- Step 4: Sort each bucket using insertion sort ---
    # Insertion sort is efficient for small lists and is stable.
    for bucket in buckets:
        insertion_sort(bucket)

    # --- Step 5: Gather — concatenate all buckets in order ---
    sorted_arr: List[float] = []
    for bucket in buckets:
        sorted_arr.extend(bucket)

    return sorted_arr


def visualize_bucket_sort(arr: List[float], num_buckets: int = 10) -> None:
    """Run bucket sort with step-by-step visualization of each phase.

    This helper prints the state of the buckets after distribution and after
    sorting each bucket, making it easy to understand how the algorithm works.

    Args:
        arr: The list of numbers to sort.
        num_buckets: The number of buckets to use.
    """
    n = len(arr)
    if n <= 1:
        print(f"Input has {n} element(s) — already sorted: {arr}")
        return

    print(f"Input array ({n} elements): {arr}")
    print(f"Number of buckets: {num_buckets}")
    print()

    max_value = max(arr)
    buckets: List[List[float]] = [[] for _ in range(num_buckets)]

    # --- Phase 1: Distribution ---
    print("--- Phase 1: Distribution ---")
    for element in arr:
        index = int((element / max_value) * num_buckets)
        index = min(index, num_buckets - 1)
        buckets[index].append(element)
        print(f"  Element {element:>6.2f} -> bucket[{index}]  "
              f"(index = int({element} / {max_value}) * {num_buckets} = {index})")

    print()
    print("Buckets after distribution:")
    for i, bucket in enumerate(buckets):
        print(f"  bucket[{i:>2}]: {bucket if bucket else '(empty)'}")
    print()

    # --- Phase 2: Sort individual buckets ---
    print("--- Phase 2: Sort each bucket (using insertion sort) ---")
    for i, bucket in enumerate(buckets):
        if bucket:
            print(f"  Sorting bucket[{i}]: {bucket}")
            insertion_sort(bucket)
            print(f"  Sorted  bucket[{i}]: {bucket}")
        else:
            print(f"  bucket[{i}] is empty — skipping")
    print()

    # --- Phase 3: Concatenation ---
    print("--- Phase 3: Concatenation ---")
    sorted_arr: List[float] = []
    for i, bucket in enumerate(buckets):
        if bucket:
            print(f"  Appending bucket[{i}]: {bucket}")
        sorted_arr.extend(bucket)
    print()
    print(f"Final sorted array: {sorted_arr}")


def main() -> None:
    """Demonstrate bucket sort on sample lists of floats and integers."""
    print("=" * 64)
    print("Bucket Sort — Educational Demonstration")
    print("=" * 64)

    # --- Example 1: Uniformly distributed floats in [0, 1) ---
    # This is the ideal case for bucket sort — elements spread evenly
    # across buckets, giving near-linear O(n + k) performance.
    print("\n>>> Example 1: Uniform floats in [0, 1)")
    floats: List[float] = [0.42, 0.32, 0.75, 0.12, 0.98, 0.55, 0.23, 0.67, 0.88, 0.01]
    result = bucket_sort(floats, num_buckets=5)
    print(f"  Original: {floats}")
    print(f"  Sorted:   {result}")

    # --- Example 2: Integers in a known range ---
    # Integers are mapped to buckets by normalizing against the max value.
    print("\n>>> Example 2: Integers in range [1, 100]")
    integers: List[float] = [42, 15, 73, 8, 91, 27, 56, 34, 62, 10]
    result_int = bucket_sort(integers, num_buckets=5)
    print(f"  Original: {integers}")
    print(f"  Sorted:   {result_int}")

    # --- Example 3: Edge case — all identical elements ---
    print("\n>>> Example 3: All identical elements")
    identical: List[float] = [5, 5, 5, 5, 5]
    result_id = bucket_sort(identical, num_buckets=3)
    print(f"  Original: {identical}")
    print(f"  Sorted:   {result_id}")

    # --- Example 4: Edge case — single element ---
    print("\n>>> Example 4: Single element")
    single: List[float] = [42]
    result_single = bucket_sort(single)
    print(f"  Original: {single}")
    print(f"  Sorted:   {result_single}")

    # --- Example 5: Empty list ---
    print("\n>>> Example 5: Empty list")
    empty: List[float] = []
    result_empty = bucket_sort(empty)
    print(f"  Original: {empty}")
    print(f"  Sorted:   {result_empty}")

    # --- Visualization Example ---
    print("\n" + "=" * 64)
    print(">>> Step-by-step visualization")
    print("=" * 64)
    vis_data: List[float] = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    visualize_bucket_sort(vis_data, num_buckets=5)


if __name__ == "__main__":
    main()
