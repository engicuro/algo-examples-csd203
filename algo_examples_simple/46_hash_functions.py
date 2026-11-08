"""
46_hash_functions.py - Hash Functions
==========================================

A hash function maps keys to bucket indices in a hash table.
Good hash functions spread keys evenly across buckets to
minimize collisions.

This example demonstrates two common hash functions:
  1. Division method:  h(key) = key % table_size
  2. Multiplication method: h(key) = floor(table_size * ((key * A) % 1))
     where A is a constant (0 < A < 1), often chosen as (sqrt(5) - 1) / 2

We compare how each function distributes keys across buckets.
"""

import math


def division_method(key, table_size):
    """Division method hash function.

    Computes the remainder when dividing the key by the table size.

    Formula:  h(key) = key % table_size

    This is the simplest hash function.  It works well when
    the table size is a prime number (not close to a power of 2),
    because prime sizes help spread keys more evenly.

    Args:
        key: An integer key.
        table_size: The number of buckets.

    Returns:
        The bucket index.
    """
    return key % table_size


def multiplication_method(key, table_size):
    """Multiplication method hash function.

    Multiplies the key by a constant A (between 0 and 1),
    takes the fractional part, then scales it to a bucket index.

    Formula:  h(key) = floor(table_size * ((key * A) % 1))

    Knuth recommends A = (sqrt(5) - 1) / 2 ≈ 0.6180339887
    (the golden ratio conjugate).  This value tends to produce
    well-distributed hashes regardless of the table size.

    Args:
        key: An integer key.
        table_size: The number of buckets.

    Returns:
        The bucket index.
    """
    A = (math.sqrt(5) - 1) / 2  # ≈ 0.6180339887
    product = key * A
    fractional = product - math.floor(product)  # Keep only the fractional part
    return int(math.floor(table_size * fractional))


def show_distribution(keys, table_size, hash_func, name):
    """Show how a set of keys is distributed across buckets.

    Args:
        keys: A list of integer keys to hash.
        table_size: The number of buckets.
        hash_func: The hash function to use (takes key, table_size).
        name: A descriptive name for the hash function.
    """
    print("\n--- {} ---".format(name))
    print("Table size: {}".format(table_size))
    print("Keys: {}".format(keys))

    # Count how many keys land in each bucket
    buckets = []
    for i in range(table_size):
        buckets.append([])

    for key in keys:
        index = hash_func(key, table_size)
        buckets[index].append(key)

    # Print the distribution
    for i in range(table_size):
        if len(buckets[i]) > 0:
            print("  Bucket {}: {}".format(i, buckets[i]))
        else:
            print("  Bucket {}: (empty)".format(i))

    # Count collisions (keys that share a bucket with at least one other key)
    total_collisions = 0
    for i in range(table_size):
        if len(buckets[i]) > 1:
            total_collisions += len(buckets[i]) - 1
    print("Total collisions: {}".format(total_collisions))


if __name__ == "__main__":
    print("=" * 50)
    print("  Hash Functions — Educational Demo")
    print("=" * 50)

    # A set of keys to hash
    keys = [10, 22, 31, 4, 15, 28, 17, 88, 59]
    table_size = 11  # A prime number works well with the division method

    # Show how the division method distributes keys
    show_distribution(keys, table_size, division_method, "Division Method (key % table_size)")

    # Show how the multiplication method distributes keys
    show_distribution(keys, table_size, multiplication_method, "Multiplication Method (Knuth's A)")

    # --- Demonstrate why table size matters for division method ---
    print("\n" + "=" * 50)
    print("  Why Table Size Matters (Division Method)")
    print("=" * 50)

    # With a table size that shares factors with keys, collisions increase
    keys2 = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    print("\nKeys that are all multiples of 10: {}".format(keys2))

    # Table size 10 (shares factor 10 with all keys) — all keys go to bucket 0!
    print("\n  Division method with table_size = 10 (bad — shares factor with keys):")
    show_distribution(keys2, 10, division_method, "")

    # Table size 11 (prime) — keys spread out better
    print("\n  Division method with table_size = 11 (prime — better spread):")
    show_distribution(keys2, 11, division_method, "")

    # --- Show the multiplication method is less sensitive to table size ---
    print("\n" + "=" * 50)
    print("  Multiplication Method Is Less Sensitive to Table Size")
    print("=" * 50)

    print("\n  Multiplication method with table_size = 10:")
    show_distribution(keys2, 10, multiplication_method, "")

    print("\n  Multiplication method with table_size = 11:")
    show_distribution(keys2, 11, multiplication_method, "")
