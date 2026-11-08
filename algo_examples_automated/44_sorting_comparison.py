"""
44_sorting_comparison.py - Sorting Algorithm Comparison & Benchmark

This module benchmarks and compares six sorting algorithms:
  - Selection Sort (36_selection_sort)
  - Insertion Sort (37_insertion_sort)
  - Bubble Sort   (38_bubble_sort)
  - Quick Sort    (39_quick_sort)
  - Merge Sort    (40_merge_sort)
  - Heap Sort     (41_heap_sort)

For each algorithm we measure:
  1. Execution time on the same random data (time complexity, empirical)
  2. Stability — whether equal elements retain their original relative order
  3. Peak memory usage during sorting (space complexity, empirical)

Results are displayed in a formatted table for three input sizes
(small, medium, large) so you can see how each algorithm scales.
"""

import importlib.util
import os
import random
import time
import tracemalloc
from itertools import groupby
from typing import Callable, Dict, List, Tuple

# ---------------------------------------------------------------------------
# Import sorting implementations from sibling modules
# ---------------------------------------------------------------------------
# Python module names cannot start with digits when using `from X import Y`,
# so we use importlib.util.spec_from_file_location to load them directly
# from their .py files on disk.
_DIR = os.path.dirname(os.path.abspath(__file__))

_SORT_MODULES: Dict[str, Tuple[str, str]] = {
    "Selection Sort": ("36_selection_sort.py", "selection_sort"),
    "Insertion Sort": ("37_insertion_sort.py", "insertion_sort"),
    "Bubble Sort":    ("38_bubble_sort.py",    "bubble_sort"),
    "Quick Sort":     ("39_quick_sort.py",     "quick_sort"),
    "Merge Sort":     ("40_merge_sort.py",     "merge_sort"),
    "Heap Sort":      ("41_heap_sort.py",      "heap_sort"),
}

ALGORITHMS: Dict[str, Callable[[List[int]], List[int]]] = {}
for _name, (_file, _func) in _SORT_MODULES.items():
    _spec = importlib.util.spec_from_file_location(_name, os.path.join(_DIR, _file))
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    ALGORITHMS[_name] = getattr(_mod, _func)


# ---------------------------------------------------------------------------
# Normalization helper
# ---------------------------------------------------------------------------
def normalize_result(original: List[int], sorted_result: List[int]) -> List[int]:
    """Return the sorted result, handling both in-place and copy-returning sorts.

    Some algorithms (selection, insertion, bubble, heap, quick) sort in-place
    and return the same list object. Others (merge sort) return a new list.
    This helper ensures we always get a sorted list without mutating the
    caller's original data.

    Args:
        original: The unsorted input list (kept unchanged).
        sorted_result: The result returned by a sorting function.

    Returns:
        A sorted list (either the same object if in-place, or a new list).
    """
    # If the sort returned a different object, it already made a copy or new list.
    # If it returned the same object, the original was sorted in-place — use a copy.
    if sorted_result is original:
        return sorted_result[:]
    return sorted_result


# ---------------------------------------------------------------------------
# Benchmark: execution time
# ---------------------------------------------------------------------------
def benchmark_time(
    sort_func: Callable[[List[int]], List[int]],
    data: List[int],
    repeats: int = 3,
) -> float:
    """Time how long a sorting function takes on a copy of *data*.

    Runs the sort *repeats* times and returns the best (minimum) time
    to reduce noise from system-level fluctuations.

    Args:
        sort_func: The sorting function to benchmark.
        data: The input list (will be copied so the original is untouched).
        repeats: Number of times to repeat the measurement.

    Returns:
        The minimum elapsed time in seconds across all repetitions.
    """
    best_time = float("inf")
    for _ in range(repeats):
        arr_copy = data[:]  # Fresh copy for each run
        start = time.perf_counter()
        sort_func(arr_copy)
        elapsed = time.perf_counter() - start
        if elapsed < best_time:
            best_time = elapsed
    return best_time


# ---------------------------------------------------------------------------
# Benchmark: peak memory usage
# ---------------------------------------------------------------------------
def benchmark_memory(
    sort_func: Callable[[List[int]], List[int]],
    data: List[int],
) -> int:
    """Measure the peak additional memory (bytes) used by a sort.

    Uses tracemalloc to track memory allocations during sorting.

    Args:
        sort_func: The sorting function to benchmark.
        data: The input list (will be copied so the original is untouched).

    Returns:
        Peak memory allocated during the sort, in bytes.
    """
    arr_copy = data[:]
    tracemalloc.start()
    sort_func(arr_copy)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


# ---------------------------------------------------------------------------
# Stability test
# ---------------------------------------------------------------------------
def test_stability(
    sort_func: Callable[[List[int]], List[int]],
) -> bool:
    """Check whether a sorting algorithm is stable.

    A stable sort preserves the relative order of elements that compare
    equal. We demonstrate this with key-value pairs where the key is
    the sort criterion and the value is the original index. After sorting
    by key, we verify that for any group of equal keys, the original
    indices remain in ascending order.

    Example:
        Input pairs (key, original_index):
            (3, 0), (1, 1), (3, 2), (2, 3), (1, 4)
        After sorting by key, stability requires:
            (1, 1) before (1, 4) and (3, 0) before (3, 2)

    Args:
        sort_func: The sorting function to test. It must accept a list
            of tuples and sort by the first element of each tuple.

    Returns:
        True if the sort is stable, False otherwise.
    """
    # Build a list of (key, original_index) pairs with duplicate keys.
    # We use a wrapper class so that comparisons only look at the key,
    # not the original index. This lets us detect whether the sort
    # preserves the relative order of equal keys (stability).
    class _Key:
        """Wrapper that compares only by sort key, not by original index.

        This lets us detect whether a sort is stable: equal keys must
        retain their original relative order after sorting.
        """
        __slots__ = ("key", "original_index")

        def __init__(self, key: int, original_index: int) -> None:
            self.key = key
            self.original_index = original_index

        def __lt__(self, other: "_Key") -> bool:
            return self.key < other.key

        def __le__(self, other: "_Key") -> bool:
            """Less-than-or-equal comparison by key only."""
            return self.key <= other.key

        def __ge__(self, other: "_Key") -> bool:
            """Greater-than-or-equal comparison by key only."""
            return self.key >= other.key

        def __eq__(self, other: object) -> bool:
            """Equality comparison by key only."""
            if not isinstance(other, _Key):
                return NotImplemented
            return self.key == other.key

        def __ne__(self, other: object) -> bool:
            """Inequality comparison by key only."""
            if not isinstance(other, _Key):
                return NotImplemented
            return self.key != other.key

        def __repr__(self) -> str:
            return f"({self.key}, idx={self.original_index})"

    # Sort by key only — the _Key wrapper makes comparison work
    # by key value, so unstable sorts will reorder equal keys.
    pairs: List[_Key] = [
        _Key(3, 0), _Key(1, 1), _Key(3, 2), _Key(2, 3), _Key(1, 4),
        _Key(5, 5), _Key(2, 6), _Key(4, 7), _Key(5, 8), _Key(1, 9),
    ]

    sorted_pairs = sort_func(pairs[:])  # type: ignore[arg-type]

    # For each group of equal keys, check that original indices are ascending.
    # A stable sort preserves insertion order for equal elements.
    for _key, group in groupby(sorted_pairs, key=lambda p: p.key):
        indices = [p.original_index for p in group]
        if indices != sorted(indices):
            return False
    return True


# ---------------------------------------------------------------------------
# Results display
# ---------------------------------------------------------------------------
def print_results_table(
    results: List[Dict[str, object]],
    input_size: int,
) -> None:
    """Print a formatted comparison table for a given input size.

    The table shows execution time, peak memory, and stability for each
    algorithm.

    Args:
        results: A list of dicts, one per algorithm, each containing
            'Algorithm', 'Time (s)', 'Peak Memory (KB)', and 'Stable'.
        input_size: The size of the input data used for these results.
    """
    header = f"\n{'=' * 72}"
    subheader = f"  Input size: {input_size:,} elements"
    print(f"\n{header}\n{subheader}\n{'=' * 72}")

    # Column widths
    col_algo = 18
    col_time = 16
    col_mem = 18
    col_stable = 10

    print(f"{'Algorithm':<{col_algo}} {'Time (s)':<{col_time}} "
          f"{'Peak Mem (KB)':<{col_mem}} {'Stable':<{col_stable}}")
    print(f"{'-' * col_algo} {'-' * col_time} "
          f"{'-' * col_mem} {'-' * col_stable}")

    for row in results:
        time_val = row["time"]
        mem_val = row["memory_kb"]
        stable_val = "Yes" if row["stable"] else "No"
        print(f"{row['algorithm']:<{col_algo}} {time_val:<{col_time}.6f} "
              f"{mem_val:<{col_mem}.1f} {stable_val:<{col_stable}}")

    print(f"{'=' * 72}")


# ---------------------------------------------------------------------------
# Full comparison runner
# ---------------------------------------------------------------------------
def run_comparison(sizes: List[int]) -> None:
    """Run the full sorting comparison across multiple input sizes.

    For each size:
      1. Generate a random list of integers.
      2. Time each algorithm.
      3. Measure peak memory for each algorithm.
      4. Test stability for each algorithm.
      5. Print a formatted results table.

    Args:
        sizes: A list of input sizes to test (e.g., [100, 1000, 5000]).
    """
    print("Sorting Algorithm Comparison & Benchmark")
    print("=" * 72)

    for size in sizes:
        # Generate the same random data for all algorithms so the
        # comparison is fair (same input, same conditions).
        random.seed(42)  # Reproducible results
        data = [random.randint(0, 100_000) for _ in range(size)]

        results: List[Dict[str, object]] = []

        for name, func in ALGORITHMS.items():
            # --- Time benchmark ---
            elapsed = benchmark_time(func, data)

            # --- Memory benchmark ---
            peak_bytes = benchmark_memory(func, data)
            peak_kb = peak_bytes / 1024  # Convert to KB

            # --- Stability test ---
            # Stability is tested once (it doesn't depend on data size)
            # but we run it for each size for completeness.
            stable = test_stability(func)

            results.append({
                "algorithm": name,
                "time": elapsed,
                "memory_kb": peak_kb,
                "stable": stable,
            })

        print_results_table(results, size)

    # --- Educational summary ---
    print("\n" + "=" * 72)
    print("Educational Summary")
    print("=" * 72)
    print("""
Time Complexity (observed):
  O(n²) algorithms — Selection, Insertion, Bubble:
    These show quadratic growth. Doubling the input size roughly
    quadruples the time. They are practical only for small inputs.

  O(n log n) algorithms — Quick, Merge, Heap:
    These scale much better. Doubling the input size roughly doubles
    the time (plus a small overhead). They handle large inputs well.

Stability:
  A stable sort preserves the relative order of equal elements.
  This matters when sorting records by a key — you want records with
  the same key to stay in their original order.
  Stable sorts in this comparison: Insertion, Bubble, Merge.
  Unstable sorts: Selection, Quick, Heap.

Space Complexity:
  In-place sorts (Selection, Insertion, Bubble, Quick, Heap) use O(1)
  or O(log n) extra memory (just a few variables or recursion stack).
  Merge Sort uses O(n) extra memory for the temporary arrays during
  merging, which is its main drawback compared to in-place algorithms.

Trade-offs:
  - For small or nearly-sorted data: Insertion Sort is fast and
    stable, with low overhead.
  - For general-purpose large data: Quick Sort is usually fastest
    in practice (good cache locality), but it is not stable and
    has O(n²) worst case.
  - When guaranteed O(n log n) is needed: Merge Sort or Heap Sort.
    Merge Sort is stable; Heap Sort uses less memory.
  - Selection Sort is simple but never a good choice for performance.
  - Bubble Sort is mainly educational — it is the slowest practical
    sort and should not be used in production.
""")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Define input sizes to test:
    #   small  — fast enough for O(n²) algorithms
    #   medium — shows O(n²) algorithms starting to slow down
    #   large  — clearly demonstrates the advantage of O(n log n) sorts
    input_sizes = [100, 1_000, 5_000]

    run_comparison(input_sizes)
