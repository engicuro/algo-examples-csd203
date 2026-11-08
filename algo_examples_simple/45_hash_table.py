"""
45_hash_table.py - Hash Table Basics
==========================================

A hash table stores key-value pairs using a hash function to
map keys to positions (called "buckets") in an array.

This example uses:
  - A simple hash function: hash(key) = key % table_size
  - Chaining: each bucket holds a list of (key, value) pairs
    so multiple items can share the same bucket.

Operations:
  - insert(key, value): add or update a key-value pair
  - search(key): find the value for a key
  - delete(key): remove a key-value pair

Time complexity (average):  O(1) for insert, search, delete
Time complexity (worst):    O(n) when all keys hash to the same bucket
Space complexity:           O(n + table_size)
"""


def simple_hash(key, table_size):
    """Compute a bucket index for a key using the division method.

    Args:
        key: An integer key.
        table_size: The number of buckets in the table.

    Returns:
        The bucket index (an integer from 0 to table_size - 1).
    """
    return key % table_size


def create_table(size):
    """Create an empty hash table with ``size`` buckets.

    Each bucket starts as an empty list.  We use a list of lists
    so that each bucket can hold multiple (key, value) pairs
    when collisions happen.

    Args:
        size: The number of buckets.

    Returns:
        A list of ``size`` empty lists.
    """
    table = []
    for i in range(size):
        table.append([])
    return table


def insert(table, key, value):
    """Insert a (key, value) pair into the hash table.

    If the key already exists, its value is updated.
    Otherwise, the pair is appended to the correct bucket.

    Args:
        table: The hash table (list of lists).
        key: The integer key.
        value: The value to store.
    """
    bucket_index = simple_hash(key, len(table))
    bucket = table[bucket_index]

    # Check if the key already exists in this bucket
    for i in range(len(bucket)):
        if bucket[i][0] == key:
            # Key found — update the existing value
            bucket[i] = (key, value)
            return

    # Key not found — add a new pair to the bucket
    bucket.append((key, value))


def search(table, key):
    """Search for a key in the hash table and return its value.

    Args:
        table: The hash table (list of lists).
        key: The integer key to look up.

    Returns:
        The value associated with the key, or None if not found.
    """
    bucket_index = simple_hash(key, len(table))
    bucket = table[bucket_index]

    for i in range(len(bucket)):
        if bucket[i][0] == key:
            return bucket[i][1]

    return None


def delete(table, key):
    """Delete a key-value pair from the hash table.

    Args:
        table: The hash table (list of lists).
        key: The integer key to remove.

    Returns:
        True if the key was found and removed, False otherwise.
    """
    bucket_index = simple_hash(key, len(table))
    bucket = table[bucket_index]

    for i in range(len(bucket)):
        if bucket[i][0] == key:
            # Remove the pair at index i
            bucket.pop(i)
            return True

    return False


def print_table(table):
    """Print the contents of the hash table bucket by bucket.

    Only buckets that are non-empty are printed.
    """
    print("Hash Table Contents:")
    for i in range(len(table)):
        if len(table[i]) > 0:
            print("  Bucket {}: {}".format(i, table[i]))


if __name__ == "__main__":
    print("=" * 50)
    print("  Hash Table Basics — Educational Demo")
    print("=" * 50)

    # Create a hash table with 7 buckets
    table_size = 7
    table = create_table(table_size)

    # Insert some key-value pairs
    print("\n--- Inserting key-value pairs ---")
    insert(table, 10, "apple")
    insert(table, 20, "banana")
    insert(table, 30, "cherry")
    insert(table, 15, "date")
    insert(table, 25, "elderberry")
    insert(table, 35, "fig")

    # Keys 10, 20, 30, 15, 25, 35 all hash to different buckets
    # because 10%7=3, 20%7=6, 30%7=2, 15%7=1, 25%7=4, 35%7=0
    print_table(table)

    # Search for keys
    print("\n--- Searching for keys ---")
    print("  search(10) =", search(table, 10))
    print("  search(20) =", search(table, 20))
    print("  search(99) =", search(table, 99))  # Not in table

    # Update an existing key
    print("\n--- Updating key 10 to 'avocado' ---")
    insert(table, 10, "avocado")
    print("  search(10) =", search(table, 10))
    print_table(table)

    # Delete a key
    print("\n--- Deleting key 20 ---")
    deleted = delete(table, 20)
    print("  Key 20 deleted:", deleted)
    print("  search(20) =", search(table, 20))
    print_table(table)

    # Try to delete a key that doesn't exist
    print("\n--- Deleting key 99 (not in table) ---")
    deleted = delete(table, 99)
    print("  Key 99 deleted:", deleted)
