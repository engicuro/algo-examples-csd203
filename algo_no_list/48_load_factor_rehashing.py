"""
48_load_factor_rehashing.py - Load Factor and Rehashing
==========================================================

Load factor measures how full a hash table is:

    load_factor = number_of_items / table_size

When the load factor gets too high, collisions increase and
operations slow down.  The solution is to **rehash**: create
a larger table and move all existing items into it.

A common rule of thumb: rehash when load factor exceeds 0.7.
The new table size is usually doubled (or the next prime number).

This example shows:
  1. Inserting items and watching the load factor grow.
  2. Triggering a rehash when the threshold is exceeded.
  3. Comparing the table state before and after rehashing.
"""

import math


def simple_hash(key, table_size):
    """Compute bucket index using the division method."""
    return key % table_size


def create_table(size):
    """Create an empty hash table with ``size`` buckets."""
    table = ()
    for i in range(size):
        table = table + ((),)
    return table


def count_items(table):
    """Count the total number of items stored in the hash table.

    Args:
        table: The hash table (tuple of tuples).

    Returns:
        The total number of (key, value) pairs across all buckets.
    """
    total = 0
    for i in range(len(table)):
        total += len(table[i])
    return total


def load_factor(table):
    """Compute the current load factor of the hash table.

    Args:
        table: The hash table (tuple of tuples).

    Returns:
        The load factor as a float (items / buckets).
    """
    return count_items(table) / len(table)


def insert(table, key, value):
    """Insert a (key, value) pair into the hash table.

    If the key already exists, update its value.

    Args:
        table: The hash table (tuple of tuples).
        key: The integer key.
        value: The value to store.
    """
    bucket_index = simple_hash(key, len(table))
    bucket = table[bucket_index]

    for i in range(len(bucket)):
        if bucket[i][0] == key:
            bucket = bucket[:i] + ((key, value),) + bucket[i+1:]
            table = table[:bucket_index] + (bucket,) + table[bucket_index+1:]
            return

    bucket = bucket + ((key, value),)
    table = table[:bucket_index] + (bucket,) + table[bucket_index+1:]


def search(table, key):
    """Search for a key in the hash table.

    Args:
        table: The hash table (tuple of tuples).
        key: The integer key to look up.

    Returns:
        The value if found, or None.
    """
    bucket_index = simple_hash(key, len(table))
    bucket = table[bucket_index]

    for i in range(len(bucket)):
        if bucket[i][0] == key:
            return bucket[i][1]

    return None


def rehash(old_table, new_size):
    """Create a new, larger table and move all items into it.

    Rehashing reduces the load factor by spreading items across
    more buckets, which reduces collisions.

    Args:
        old_table: The current (overloaded) hash table.
        new_size: The size of the new table.

    Returns:
        A new hash table with all items re-inserted.
    """
    print("\n  --- REHASHING ---")
    print("  Old table size: {}".format(len(old_table)))
    print("  Old item count: {}".format(count_items(old_table)))
    print("  Old load factor: {:.2f}".format(load_factor(old_table)))
    print("  New table size: {}".format(new_size))

    # Create the new empty table
    new_table = create_table(new_size)

    # Re-insert every item from the old table into the new table
    for i in range(len(old_table)):
        for j in range(len(old_table[i])):
            key = old_table[i][j][0]
            value = old_table[i][j][1]
            insert(new_table, key, value)

    print("  New load factor: {:.2f}".format(load_factor(new_table)))
    print("  --- REHASHING DONE ---\n")

    return new_table


def print_table(table):
    """Print the hash table contents (only non-empty buckets)."""
    for i in range(len(table)):
        if len(table[i]) > 0:
            print("  Bucket {}: {}".format(i, table[i]))


if __name__ == "__main__":
    print("=" * 50)
    print("  Load Factor and Rehashing — Educational Demo")
    print("=" * 50)

    # Start with a small table so rehashing happens quickly
    table_size = 5
    table = create_table(table_size)
    rehash_threshold = 0.7  # Rehash when load factor exceeds this

    # Insert items one by one and watch the load factor
    items_to_insert = (10, 20, 30, 40, 50, 60, 70)

    print("\n--- Inserting items and watching load factor ---\n")

    for key in items_to_insert:
        value = "item_{}".format(key)
        insert(table, key, value)

        current_load = load_factor(table)
        print("Inserted key={} ->  load factor = {:.2f} ({}/{})".format(
            key, current_load, count_items(table), len(table)))

        # Check if we need to rehash
        if current_load > rehash_threshold:
            print("  *** Load factor exceeded {:.2f} — triggering rehash! ***".format(
                rehash_threshold))
            new_size = len(table) * 2  # Double the table size
            table = rehash(table, new_size)

    # Show final table state
    print("\n--- Final table state after all insertions ---")
    print_table(table)
    print("\nFinal load factor: {:.2f}".format(load_factor(table)))

    # --- Show search still works after rehashing ---
    print("\n--- Searching for keys after rehashing ---")
    for key in items_to_insert:
        result = search(table, key)
        print("  search({}) = {}".format(key, result))

    print("  search(99) = {}".format(search(table, 99)))

    # --- Summary ---
    print("\n" + "=" * 50)
    print("  Summary")
    print("=" * 50)
    print("""
Load factor tells you how full the hash table is.
  - Low load factor (< 0.5):  few collisions, fast operations, wastes memory
  - High load factor (> 0.7): many collisions, slow operations, saves memory

Rehashing keeps the load factor in a healthy range:
  1. Create a new table that is larger (usually 2x the size).
  2. Recompute the hash for every existing key with the new table size.
  3. Move all items into the new table.

This is expensive (O(n)) but happens rarely, so the average
cost per operation stays O(1).
""")
