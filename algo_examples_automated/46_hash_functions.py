"""
46_hash_functions.py - Hash Functions in Python

Hash functions map arbitrary-sized data to fixed-size values (hash codes).
They are fundamental to hash tables, dictionaries, sets, checksums, and
cryptographic applications.

Topics covered:
  - Division method: h(k) = k mod m
  - Multiplication method: h(k) = floor(m * (k * A mod 1))
  - Universal hashing: randomized family of hash functions
  - Good hash function properties: uniform distribution, determinism,
    avalanche effect, efficiency
"""

import math
import random
from typing import Callable, List, Tuple


# ---------------------------------------------------------------------------
# 1. Division Method
# ---------------------------------------------------------------------------

def division_hash(key: int, table_size: int) -> int:
    """Compute a hash index using the division method.

    Formula: h(k) = k mod m

    The table size m is ideally a prime number not close to a power of 2,
    which helps distribute keys more uniformly across slots.

    Args:
        key: The integer key to hash.
        table_size: The size of the hash table (number of slots).

    Returns:
        The hash index in the range [0, table_size - 1].

    Example:
        >>> division_hash(42, 11)
        9
    """
    return key % table_size


# ---------------------------------------------------------------------------
# 2. Multiplication Method
# ---------------------------------------------------------------------------

def multiplication_hash(key: int, table_size: int,
                       constant: float = 0.6180339887) -> int:
    """Compute a hash index using the multiplication method.

    Formula: h(k) = floor(m * ((k * A) mod 1))

    where A is a constant in the range (0, 1). Knuth recommends
    A ≈ (√5 - 1) / 2 ≈ 0.6180339887 (the golden ratio conjugate),
    which provides good distribution regardless of m.

    Args:
        key: The integer key to hash.
        table_size: The size of the hash table (number of slots).
        constant: The multiplicative constant A (default is the golden
                  ratio conjugate).

    Returns:
        The hash index in the range [0, table_size - 1].

    Example:
        >>> multiplication_hash(42, 11)
        10
    """
    # Multiply key by constant, extract fractional part, scale by table size
    product = key * constant
    fractional = product - math.floor(product)  # k * A mod 1
    return int(math.floor(table_size * fractional))


# ---------------------------------------------------------------------------
# 3. Universal Hashing
# ---------------------------------------------------------------------------

def make_universal_hash(table_size: int,
                        prime: int = 104729) -> Callable[[int], int]:
    """Return a universal hash function for integer keys.

    A universal hash family randomly selects parameters at construction
    time, guaranteeing that for any two distinct keys, the probability of
    collision is at most 1/m (where m is the table size).

    Construction (Carter & Wegman):
        h_{a,b}(k) = ((a * k + b) mod p) mod m

    where:
        p is a prime larger than the universe of keys,
        a ∈ {1, 2, ..., p - 1} is chosen randomly,
        b ∈ {0, 1, ..., p - 1} is chosen randomly.

    Args:
        table_size: The number of slots in the hash table.
        prime: A prime number larger than any possible key (default 104729).

    Returns:
        A callable hash function that maps an integer key to [0, table_size).

    Example:
        >>> random.seed(42)
        >>> h = make_universal_hash(10)
        >>> h(42)  # doctest: +SKIP
        4
    """
    a = random.randint(1, prime - 1)
    b = random.randint(0, prime - 1)

    def hash_func(key: int) -> int:
        """Universal hash for a single integer key."""
        return ((a * key + b) % prime) % table_size

    return hash_func


# ---------------------------------------------------------------------------
# 4. Demonstrating Good Hash Function Properties
# ---------------------------------------------------------------------------

def demonstrate_uniform_distribution(hash_func: Callable[[int], int],
                                     keys: List[int],
                                     table_size: int) -> List[int]:
    """Show how uniformly a hash function distributes keys across slots.

    A good hash function should spread keys approximately evenly,
    avoiding clustering in a small number of buckets.

    Args:
        hash_func: The hash function to evaluate.
        keys: The list of keys to hash.
        table_size: The number of buckets.

    Returns:
        A list of bucket sizes (index = bucket, value = count).
    """
    buckets: List[int] = [0] * table_size
    for key in keys:
        buckets[hash_func(key)] += 1
    return buckets


def print_bucket_distribution(buckets: List[int]) -> None:
    """Print a simple histogram of bucket occupancy.

    Args:
        buckets: List where buckets[i] is the count of keys in slot i.
    """
    max_count = max(buckets) if buckets else 1
    bar_width = 40  # width of the longest bar in characters

    for i, count in enumerate(buckets):
        # Scale bar length relative to the maximum bucket count
        bar_len = int((count / max_count) * bar_width) if max_count else 0
        bar = "█" * bar_len
        print(f"  Slot {i:>3}: {bar} ({count})")


def demonstrate_avalanche(hash_func: Callable[[int], int]) -> None:
    """Show the avalanche effect: small input changes cause large output changes.

    A good hash function should change the output significantly when the
    input is altered by even a single bit, making patterns in the input
    hard to predict from the hash values.

    Args:
        hash_func: The hash function to test (must accept int keys).
    """
    print("\n  Avalanche check (small input changes → large output changes):")
    base_key = 1000
    # Test flipping individual bits of the base key
    for bit in range(16):
        flipped = base_key ^ (1 << bit)  # toggle one bit
        original_hash = hash_func(base_key)
        flipped_hash = hash_func(flipped)
        # Count differing bits between the two hash values
        diff_bits = bin(original_hash ^ flipped_hash).count("1")
        print(f"    Key {base_key:>5} (bit {bit:>2} off) → "
              f"hash {original_hash} vs {flipped_hash}  "
              f"[{diff_bits} bits differ]")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Run all hash function demonstrations."""
    print("=" * 64)
    print("Chapter 46 — Hash Functions")
    print("=" * 64)

    table_size = 13  # prime number — recommended for division method
    keys = [10, 22, 31, 4, 15, 28, 17, 88, 59, 37, 62, 71, 45, 93, 11]

    # 1. Division Method
    print("\n--- 1. Division Method: h(k) = k mod m ---")
    print(f"  Table size (m): {table_size}")
    print(f"  Keys: {keys}")
    print("  Hash values:")
    for key in keys:
        idx = division_hash(key, table_size)
        print(f"    h({key:>2}) = {key} mod {table_size} = {idx}")

    # 2. Multiplication Method
    print("\n--- 2. Multiplication Method ---")
    print(f"  Table size (m): {table_size}")
    print(f"  Constant A: 0.6180339887 (golden ratio conjugate)")
    print("  Hash values:")
    for key in keys:
        idx = multiplication_hash(key, table_size)
        print(f"    h({key:>2}) = floor({table_size} * "
              f"({key} * A mod 1)) = {idx}")

    # 3. Universal Hashing
    print("\n--- 3. Universal Hashing ---")
    print(f"  Table size: {table_size}")
    print(f"  Prime p: 104729")
    print("  Parameters are chosen randomly at construction time.")
    # Create two independent universal hash functions to show variability
    h1 = make_universal_hash(table_size)
    h2 = make_universal_hash(table_size)
    print(f"\n  Hash function 1:")
    for key in keys[:5]:
        print(f"    h1({key:>2}) = {h1(key)}")
    print(f"\n  Hash function 2 (different random parameters):")
    for key in keys[:5]:
        print(f"    h2({key:>2}) = {h2(key)}")

    # 4. Good Hash Function Properties
    print("\n--- 4. Good Hash Function Properties ---")

    # 4a. Uniform distribution
    print("\n  4a. Uniform Distribution (division method):")
    buckets = demonstrate_uniform_distribution(
        lambda k: division_hash(k, table_size), keys, table_size
    )
    print_bucket_distribution(buckets)

    print("\n  4b. Uniform Distribution (multiplication method):")
    buckets = demonstrate_uniform_distribution(
        lambda k: multiplication_hash(k, table_size), keys, table_size
    )
    print_bucket_distribution(buckets)

    # 4c. Avalanche effect
    print("\n  4c. Avalanche Effect (multiplication method):")
    demonstrate_avalanche(lambda k: multiplication_hash(k, table_size))

    # 4d. Determinism check
    print("\n  4d. Determinism: same key always produces same hash")
    for key in [10, 59, 93]:
        results = [division_hash(key, table_size) for _ in range(5)]
        consistent = len(set(results)) == 1
        print(f"    division_hash({key}) × 5 runs → {results[0]} "
              f"{'✓ consistent' if consistent else '✗ INCONSISTENT'}")


if __name__ == "__main__":
    main()
