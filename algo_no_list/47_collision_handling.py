"""
47_collision_handling.py - Collision Handling
==============================================

A collision happens when two different keys hash to the same
bucket index.  This example shows three strategies for
handling collisions:

  1. Chaining:      Each bucket holds a tuple of all items
                    that hash to it.  Simple and flexible.
  2. Linear Probing: If a bucket is occupied, check the next
                      bucket (index + 1, + 2, + 3, ...).
  3. Quadratic Probing: If a bucket is occupied, check buckets
                         at offsets 1, 4, 9, 16, ... (i^2).

Each strategy has trade-offs in speed, memory, and clustering.
"""

import math


# ---------------------------------------------------------------------------
# 1. Chaining (tuple of tuples)
# ---------------------------------------------------------------------------

def chaining_insert(table, key, value):
    """Insert a (key, value) pair using chaining.

    Each bucket is a tuple of (key, value) tuples.
    If the key already exists, update its value.

    Args:
        table: The hash table (tuple of tuples).
        key: The integer key.
        value: The value to store.
    """
    index = key % len(table)
    bucket = table[index]

    # Check if key already exists in this bucket
    for i in range(len(bucket)):
        if bucket[i][0] == key:
            bucket = bucket[:i] + ((key, value),) + bucket[i+1:]
            table = table[:index] + (bucket,) + table[index+1:]
            return

    # Key not found — add new pair
    bucket = bucket + ((key, value),)
    table = table[:index] + (bucket,) + table[index+1:]


def chaining_search(table, key):
    """Search for a key using chaining.

    Args:
        table: The hash table (tuple of tuples).
        key: The integer key to look up.

    Returns:
        The value if found, or None.
    """
    index = key % len(table)
    bucket = table[index]

    for i in range(len(bucket)):
        if bucket[i][0] == key:
            return bucket[i][1]

    return None


def chaining_delete(table, key):
    """Delete a key using chaining.

    Args:
        table: The hash table (tuple of tuples).
        key: The integer key to remove.

    Returns:
        True if the key was found and removed, False otherwise.
    """
    index = key % len(table)
    bucket = table[index]

    for i in range(len(bucket)):
        if bucket[i][0] == key:
            bucket = bucket[:i] + bucket[i+1:]
            table = table[:index] + (bucket,) + table[index+1:]
            return True

    return False


# ---------------------------------------------------------------------------
# 2. Linear Probing (using a dict for mutable index-based storage)
# ---------------------------------------------------------------------------

def linear_probe_insert(table, key, value, table_size):
    """Insert a (key, value) pair using linear probing.

    If the target bucket is occupied, try the next bucket
    (wrapping around to the beginning if needed).

    Args:
        table: The hash table (a dict mapping index to None, (key, value), or "DELETED").
        key: The integer key.
        value: The value to store.
        table_size: The number of buckets in the table.
    """
    index = key % table_size

    # Keep probing until we find an empty slot or the same key
    while table.get(index) is not None:
        if table.get(index)[0] == key:
            # Key already exists — update value
            table[index] = (key, value)
            return
        index = (index + 1) % table_size  # Move to next slot (wrap around)

    # Found an empty slot — insert here
    table[index] = (key, value)


def linear_probe_search(table, key, table_size):
    """Search for a key using linear probing.

    Args:
        table: The hash table (dict of None or (key, value) tuples).
        key: The integer key to look up.
        table_size: The number of buckets in the table.

    Returns:
        The value if found, or None.
    """
    index = key % table_size

    # Probe until we find the key or an empty slot
    while table.get(index) is not None:
        if table.get(index)[0] == key:
            return table.get(index)[1]
        index = (index + 1) % table_size

    return None


def linear_probe_delete(table, key, table_size):
    """Delete a key using linear probing.

    Uses a special "DELETED" marker so that probing chains
    are not broken.

    Args:
        table: The hash table (dict of None, (key, value), or "DELETED").
        key: The integer key to remove.
        table_size: The number of buckets in the table.

    Returns:
        True if the key was found and removed, False otherwise.
    """
    index = key % table_size

    while table.get(index) is not None:
        if table.get(index) != "DELETED" and table.get(index)[0] == key:
            table[index] = "DELETED"  # Mark as deleted (tombstone)
            return True
        index = (index + 1) % table_size

    return False


# ---------------------------------------------------------------------------
# 3. Quadratic Probing (using a dict for mutable index-based storage)
# ---------------------------------------------------------------------------

def quadratic_probe_insert(table, key, value, table_size):
    """Insert a (key, value) pair using quadratic probing.

    If the target bucket is occupied, try buckets at offsets
    1^2, 2^2, 3^2, ... (wrapping around).

    Note: quadratic probing may not find an empty slot even
    if the table isn't full (secondary clustering).  A safety
    limit prevents infinite loops.

    Args:
        table: The hash table (a dict mapping index to None or (key, value)).
        key: The integer key.
        value: The value to store.
        table_size: The number of buckets in the table.
    """
    index = key % table_size
    i = 0
    max_probes = table_size  # Safety limit to avoid infinite loops

    while table.get(index) is not None and i < max_probes:
        if table.get(index)[0] == key:
            # Key already exists — update value
            table[index] = (key, value)
            return
        i += 1
        index = (key % table_size + i * i) % table_size

    if i >= max_probes:
        print("  WARNING: quadratic probe table full for key {}".format(key))
        return

    # Found an empty slot — insert here
    table[index] = (key, value)


def quadratic_probe_search(table, key, table_size):
    """Search for a key using quadratic probing.

    Args:
        table: The hash table (dict of None or (key, value) tuples).
        key: The integer key to look up.
        table_size: The number of buckets in the table.

    Returns:
        The value if found, or None.
    """
    index = key % table_size
    i = 0
    max_probes = table_size  # Safety limit

    while table.get(index) is not None and i < max_probes:
        if table.get(index)[0] == key:
            return table.get(index)[1]
        i += 1
        index = (key % table_size + i * i) % table_size

    return None


def quadratic_probe_delete(table, key, table_size):
    """Delete a key using quadratic probing with tombstone markers.

    Args:
        table: The hash table (dict of None, (key, value), or "DELETED").
        key: The integer key to remove.
        table_size: The number of buckets in the table.

    Returns:
        True if the key was found and removed, False otherwise.
    """
    index = key % table_size
    i = 0
    max_probes = table_size  # Safety limit

    while table.get(index) is not None and i < max_probes:
        if table.get(index) != "DELETED" and table.get(index)[0] == key:
            table[index] = "DELETED"
            return True
        i += 1
        index = (key % table_size + i * i) % table_size

    return False


def print_table_state(table, name, table_size):
    """Print the current state of a hash table.

    Args:
        table: The hash table to print (tuple or dict).
        name: A label for this table.
        table_size: The number of buckets in the table.
    """
    print("\n  {}:".format(name))
    for i in range(table_size):
        if isinstance(table, dict):
            print("    Bucket {}: {}".format(i, table.get(i)))
        else:
            print("    Bucket {}: {}".format(i, table[i]))


if __name__ == "__main__":
    print("=" * 50)
    print("  Collision Handling — Educational Demo")
    print("=" * 50)

    # Keys that will collide (all hash to bucket 0 with table_size=5)
    keys = (5, 10, 15, 20)
    table_size = 5

    # --- 1. Chaining ---
    print("\n--- 1. Chaining ---")
    chaining = ()
    for i in range(table_size):
        chaining = chaining + ((),)

    for key in keys:
        chaining_insert(chaining, key, "value_{}".format(key))

    print_table_state(chaining, "Chaining Table", table_size)
    print("  search(10) =", chaining_search(chaining, 10))
    print("  search(99) =", chaining_search(chaining, 99))

    chaining_delete(chaining, 10)
    print("  After deleting key 10:")
    print_table_state(chaining, "Chaining Table", table_size)

    # --- 2. Linear Probing ---
    print("\n--- 2. Linear Probing ---")
    linear = {}

    for key in keys:
        linear_probe_insert(linear, key, "value_{}".format(key), table_size)

    print_table_state(linear, "Linear Probing Table", table_size)
    print("  search(10) =", linear_probe_search(linear, 10, table_size))
    print("  search(99) =", linear_probe_search(linear, 99, table_size))

    linear_probe_delete(linear, 10, table_size)
    print("  After deleting key 10 (tombstone 'DELETED'):")
    print_table_state(linear, "Linear Probing Table", table_size)

    # --- 3. Quadratic Probing ---
    print("\n--- 3. Quadratic Probing ---")
    quadratic = {}

    for key in keys:
        quadratic_probe_insert(quadratic, key, "value_{}".format(key), table_size)

    print_table_state(quadratic, "Quadratic Probing Table", table_size)
    print("  search(10) =", quadratic_probe_search(quadratic, 10, table_size))
    print("  search(99) =", quadratic_probe_search(quadratic, 99, table_size))

    quadratic_probe_delete(quadratic, 10, table_size)
    print("  After deleting key 10 (tombstone 'DELETED'):")
    print_table_state(quadratic, "Quadratic Probing Table", table_size)

    # --- Comparison ---
    print("\n" + "=" * 50)
    print("  Comparison of Strategies")
    print("=" * 50)
    print("""
Chaining:
  + Simple to implement
  + Never fills up (as long as there's memory for new tuples)
  - Uses extra memory for tuple pointers
  - Cache-unfriendly (items scattered in memory)

Linear Probing:
  + Cache-friendly (data stored in a contiguous array)
  + No extra pointers needed
  - Clustering: consecutive filled buckets form "clusters"
    that slow down future insertions and searches

Quadratic Probing:
  + Reduces primary clustering compared to linear probing
  - Can fail to find an empty slot even if the table isn't full
    (secondary clustering)
  - Table size should be prime for best results
""")
