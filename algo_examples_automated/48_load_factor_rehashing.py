"""
Load Factor and Rehashing in Hash Tables
=========================================

This module demonstrates:
  - Load factor calculation and its role in hash table performance
  - Rehashing strategy (expanding the table and re-inserting all entries)
  - Efficiency analysis comparing operations before and after rehashing

Key Concepts:
  - Load Factor (λ) = number_of_entries / table_capacity
  - A high load factor increases collision probability and degrades O(1) lookups
  - Rehashing doubles the table size and re-inserts all existing entries to
    restore a low load factor, keeping average-case operations at O(1)

Author: algo-examples
"""

from __future__ import annotations

import time
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Hash Table Implementation
# ---------------------------------------------------------------------------

class HashTable:
    """A hash table with separate chaining and automatic rehashing.

    Attributes:
        capacity (int): Current number of buckets in the table.
        size (int): Number of key-value pairs stored.
        buckets (list[list[tuple]]): Array of buckets, each a list of (key, value)
            pairs that hashed to the same index.
        max_load_factor (float): Threshold at which rehashing is triggered.
        rehashing_enabled (bool): Whether automatic rehashing is active.
        rehash_count (int): Number of times rehashing has occurred.
    """

    def __init__(
        self,
        initial_capacity: int = 8,
        max_load_factor: float = 0.75,
        rehashing_enabled: bool = True,
    ) -> None:
        """Initialize the hash table.

        Args:
            initial_capacity: Starting number of buckets. Must be >= 1.
            max_load_factor: Load factor threshold that triggers rehashing.
                Typical values are 0.7–0.75 for separate chaining.
            rehashing_enabled: If False, the table grows but never rehashes
                (useful for studying degradation).
        """
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be >= 1")
        if not (0.0 < max_load_factor <= 1.0):
            raise ValueError("max_load_factor must be in (0, 1]")

        self.capacity: int = initial_capacity
        self.size: int = 0
        self.buckets: list[list[tuple[Any, Any]]] = [[] for _ in range(self.capacity)]
        self.max_load_factor: float = max_load_factor
        self.rehashing_enabled: bool = rehashing_enabled
        self.rehash_count: int = 0

    # ------------------------------------------------------------------
    # Core helpers
    # ------------------------------------------------------------------

    def _hash(self, key: Any) -> int:
        """Compute the bucket index for a given key.

        Uses Python's built-in hash() and maps it into the range
        [0, self.capacity).

        Args:
            key: Any hashable object.

        Returns:
            Bucket index.
        """
        return hash(key) % self.capacity

    @property
    def load_factor(self) -> float:
        """Current load factor λ = size / capacity.

        A load factor close to 1.0 means buckets are densely populated,
        increasing the chance of collisions and degrading lookup time from
        O(1) toward O(n) in the worst case.

        Returns:
            The current load factor as a float.
        """
        return self.size / self.capacity

    # ------------------------------------------------------------------
    # Rehashing
    # ------------------------------------------------------------------

    def _rehash(self) -> None:
        """Double the table capacity and re-insert all existing entries.

        Rehashing restores a low load factor so that subsequent insertions,
        deletions, and lookups remain amortized O(1).

        Steps:
          1. Allocate a new bucket array with double the current capacity.
          2. Iterate over every bucket in the old array.
          3. For each (key, value) pair, recompute its index using the new
             capacity and append it to the corresponding new bucket.
          4. Replace the old bucket array with the new one.

        Time complexity: O(n) where n is the number of entries — every entry
        is visited exactly once and re-hashed.

        Note:
            Rehashing is expensive but happens infrequently. Amortized over
            many insertions, the cost per insertion remains O(1).
        """
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0  # reset size; _insert will increment it

        for bucket in old_buckets:
            for key, value in bucket:
                self._insert_no_rehash(key, value)

        self.rehash_count += 1

    def _insert_no_rehash(self, key: Any, value: Any) -> None:
        """Insert a key-value pair without triggering a rehash check.

        Used internally during rehashing to avoid recursive rehash calls.
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        # Update existing key if present
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Otherwise, append as a new entry
        bucket.append((key, value))
        self.size += 1

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def insert(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair.

        If the load factor exceeds max_load_factor after insertion and
        rehashing is enabled, the table is rehashed automatically.

        Args:
            key: The lookup key (must be hashable).
            value: The associated value.
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        # Check for existing key to update in-place
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # New key — append to bucket
        bucket.append((key, value))
        self.size += 1

        # Trigger rehash if load factor exceeds threshold
        if self.rehashing_enabled and self.load_factor > self.max_load_factor:
            self._rehash()

    def get(self, key: Any) -> Optional[Any]:
        """Retrieve the value associated with *key*.

        Args:
            key: The lookup key.

        Returns:
            The associated value, or None if the key is not found.
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key: Any) -> bool:
        """Remove *key* and its associated value from the table.

        Args:
            key: The key to remove.

        Returns:
            True if the key was found and removed, False otherwise.
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False

    def __len__(self) -> int:
        """Return the number of key-value pairs stored."""
        return self.size

    def __contains__(self, key: Any) -> bool:
        """Support `key in table` syntax."""
        return self.get(key) is not None

    def stats(self) -> dict[str, Any]:
        """Return a snapshot of the table's internal state.

        Returns:
            dict with keys: capacity, size, load_factor, rehash_count,
            and bucket_chain_lengths (a list of per-bucket entry counts).
        """
        chain_lengths = [len(bucket) for bucket in self.buckets]
        return {
            "capacity": self.capacity,
            "size": self.size,
            "load_factor": round(self.load_factor, 4),
            "rehash_count": self.rehash_count,
            "max_chain_length": max(chain_lengths) if chain_lengths else 0,
            "empty_buckets": chain_lengths.count(0),
            "chain_lengths": chain_lengths,
        }


# ---------------------------------------------------------------------------
# Efficiency Analysis Helpers
# ---------------------------------------------------------------------------

def measure_insert_time(table: HashTable, items: list[tuple[Any, Any]]) -> float:
    """Time how long it takes to insert a batch of items.

    Args:
        table: The hash table to insert into.
        items: List of (key, value) pairs to insert.

    Returns:
        Elapsed time in seconds.
    """
    start = time.perf_counter()
    for key, value in items:
        table.insert(key, value)
    return time.perf_counter() - start


def measure_lookup_time(table: HashTable, keys: list[Any]) -> float:
    """Time how long it takes to look up a batch of keys.

    Args:
        table: The hash table to search.
        keys: List of keys to look up.

    Returns:
        Elapsed time in seconds.
    """
    start = time.perf_counter()
    for key in keys:
        _ = table.get(key)
    return time.perf_counter() - start


def print_stats(label: str, table: HashTable) -> None:
    """Pretty-print the hash table's statistics.

    Args:
        label: A descriptive header printed before the stats.
        table: The hash table to inspect.
    """
    stats = table.stats()
    print(f"\n{'=' * 55}")
    print(f"  {label}")
    print(f"{'=' * 55}")
    print(f"  Capacity        : {stats['capacity']}")
    print(f"  Size (entries)  : {stats['size']}")
    print(f"  Load Factor λ   : {stats['load_factor']}")
    print(f"  Rehash Count    : {stats['rehash_count']}")
    print(f"  Max Chain Len   : {stats['max_chain_length']}")
    print(f"  Empty Buckets   : {stats['empty_buckets']} / {stats['capacity']}")
    print(f"{'=' * 55}")


# ---------------------------------------------------------------------------
# Demonstration / Educational Examples
# ---------------------------------------------------------------------------

def demo_load_factor_basics() -> None:
    """Show how load factor changes as entries are added to a fixed-size table.

    This demo disables automatic rehashing so we can observe load factor
    growing past the threshold and see the effect on chain lengths.
    """
    print("\n" + "#" * 55)
    print("#  Demo 1: Load Factor Basics (rehashing disabled)")
    print("#" * 55)

    # Create a small table that never rehashes so we can watch λ grow
    table = HashTable(initial_capacity=4, max_load_factor=0.75, rehashing_enabled=False)

    print(f"\nInitial state: capacity={table.capacity}, size={table.size}, "
          f"λ={table.load_factor:.2f}")

    # Insert entries one by one and print stats after each
    for i in range(1, 9):
        table.insert(f"key_{i}", f"value_{i}")
        stats = table.stats()
        print(f"  After inserting key_{i}: size={table.size}, "
              f"λ={table.load_factor:.2f}, "
              f"max_chain={stats['max_chain_length']}")

    print("\nObservation:")
    print("  - λ grew from 0.00 to 2.00 (8 entries in 4 buckets)")
    print("  - Max chain length increased, meaning lookups degrade toward O(n)")
    print("  - With rehashing enabled, the table would have doubled before λ hit 0.75")


def demo_rehashing_in_action() -> None:
    """Show how rehashing keeps the load factor bounded.

    Rehashing is enabled (default). We insert many items and watch the
    capacity double each time λ exceeds the threshold.
    """
    print("\n" + "#" * 55)
    print("#  Demo 2: Rehashing in Action")
    print("#" * 55)

    table = HashTable(initial_capacity=4, max_load_factor=0.75)

    # Insert 20 items — enough to trigger several rehashes
    items = [(f"k{i}", i) for i in range(20)]
    measure_insert_time(table, items)

    print_stats("After inserting 20 items with rehashing enabled", table)

    print("\nObservation:")
    print("  - Capacity grew: 4 → 8 → 16 → 32")
    print("  - Rehash count is > 0, confirming rehashing occurred")
    print("  - Load factor stayed below 0.75 after each rehash")
    print("  - Max chain length remains small, preserving O(1) lookups")


def demo_efficiency_comparison() -> None:
    """Compare insertion and lookup times with and without rehashing.

    We insert the same number of items into two tables:
      - Table A: rehashing enabled (load factor stays low)
      - Table B: rehashing disabled (load factor grows unbounded)

    Then we time lookups to show the performance difference.
    """
    print("\n" + "#" * 55)
    print("#  Demo 3: Efficiency Comparison")
    print("#" * 55)

    n = 5000
    keys = [f"key_{i}" for i in range(n)]
    items = [(k, i) for i, k in enumerate(keys)]

    # --- Table A: rehashing enabled ---
    table_a = HashTable(initial_capacity=8, max_load_factor=0.75)
    insert_time_a = measure_insert_time(table_a, items)
    lookup_time_a = measure_lookup_time(table_a, keys)

    # --- Table B: rehashing disabled ---
    table_b = HashTable(initial_capacity=8, max_load_factor=0.75, rehashing_enabled=False)
    insert_time_b = measure_insert_time(table_b, items)
    lookup_time_b = measure_lookup_time(table_b, keys)

    # --- Print comparison ---
    print(f"\n  {'Metric':<25} {'Rehashing ON':>14} {'Rehashing OFF':>14}")
    print(f"  {'-'*25} {'-'*14} {'-'*14}")
    print(f"  {'Insert time (s)':<25} {insert_time_a:>14.6f} {insert_time_b:>14.6f}")
    print(f"  {'Lookup time (s)':<25} {lookup_time_a:>14.6f} {lookup_time_b:>14.6f}")
    print(f"  {'Final capacity':<25} {table_a.capacity:>14} {table_b.capacity:>14}")
    print(f"  {'Final load factor λ':<25} {table_a.load_factor:>14.4f} {table_b.load_factor:>14.4f}")
    print(f"  {'Rehash count':<25} {table_a.rehash_count:>14} {'N/A':>14}")

    print("\nObservation:")
    print("  - Rehashing ON: inserts are slightly slower overall due to rehash")
    print("    events, but lookups are fast because λ stays low.")
    print("  - Rehashing OFF: inserts are faster per-op (no rehash overhead),")
    print("    but lookups slow down significantly as chains grow long.")
    print("  - The amortized cost of rehashing is worth it for sustained")
    print("    O(1) average-case performance.")


def demo_rehash_strategy_discussion() -> None:
    """Discuss common rehashing strategies and trade-offs.

    Covers:
      - Doubling (used in this implementation)
      - Incremental growth (e.g., +50%)
      - When to rehash (on insert vs. on delete)
      - Shrinking the table when load factor drops too low
    """
    print("\n" + "#" * 55)
    print("#  Demo 4: Rehashing Strategy Discussion")
    print("#" * 55)

    discussion = """
  Common Rehashing Strategies:

  1. Doubling the capacity (used in this module)
     - Simple and widely adopted (Python dict, Java HashMap).
     - Amortized O(1) per insertion.
     - May temporarily waste memory if the table is much larger than needed.

  2. Growth by a fixed percentage (e.g., +50%)
     - More memory-efficient; avoids large jumps.
     - Rehashes more frequently, so amortized cost per insert is slightly higher.

  3. Growth by a constant amount (e.g., +16 buckets)
     - Rarely used because it leads to O(n) amortized cost — the table
       must rehash O(n) times as it grows to n entries.

  4. Shrinking on deletion
     - Some implementations also shrink (e.g., halve capacity) when
       λ drops below a lower threshold (e.g., 0.25).
     - Prevents wasted memory after many deletions.
     - Must be careful to avoid "thrashing" (repeated grow/shrink cycles).

  When to trigger rehashing:
     - On insertion when λ > upper_threshold (e.g., 0.75).
     - On deletion when λ < lower_threshold (e.g., 0.25).
     - Some implementations defer rehashing to a background thread to
       avoid latency spikes (used in Redis, for example).

  Key trade-off:
     - Lower max_load_factor → fewer collisions, faster lookups, but more
       memory usage and more frequent rehashing.
     - Higher max_load_factor → less memory, fewer rehashes, but slower
       operations due to longer chains.
    """
    print(discussion)


# ---------------------------------------------------------------------------
# __main__ block
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """Run all educational demonstrations when the script is executed directly.

    Each demo highlights a different aspect of load factor and rehashing:
      1. How load factor grows without rehashing
      2. How rehashing keeps load factor bounded
      3. Quantitative efficiency comparison
      4. Discussion of rehashing strategies and trade-offs
    """
    print("=" * 55)
    print("  Load Factor & Rehashing — Educational Demo")
    print("=" * 55)

    demo_load_factor_basics()
    demo_rehashing_in_action()
    demo_efficiency_comparison()
    demo_rehash_strategy_discussion()

    print("\n" + "=" * 55)
    print("  All demos complete.")
    print("=" * 55)
