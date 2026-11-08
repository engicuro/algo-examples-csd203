"""
49_python_hash_table.py - Custom Hash Table Class
====================================================

This file shows how a hash table works internally by building
a simple custom class from scratch using only plain Python lists.

Python's built-in dict is a highly optimized hash table, but
understanding how one works helps you appreciate what happens
when you write ``my_dict[key] = value``.

Our custom class supports:
  - put(key, value): insert or update
  - get(key): retrieve a value
  - remove(key): delete a key-value pair
  - __str__: pretty-print the table

We use chaining (list of lists) to handle collisions and
track the load factor to trigger automatic rehashing.
"""

import math


class SimpleHashTable:
    """A simple hash table implemented with chaining and auto-rehashing.

    Attributes:
        size: The current number of buckets.
        count: The number of key-value pairs stored.
        buckets: A list of lists.  Each inner list holds (key, value) pairs.
        max_load_factor: When count / size exceeds this, the table is rehashed.
    """

    def __init__(self, initial_size=7, max_load=0.7):
        """Initialize an empty hash table.

        Args:
            initial_size: The starting number of buckets (should be prime).
            max_load: The load factor threshold that triggers rehashing.
        """
        self.size = initial_size
        self.count = 0
        self.max_load = max_load
        self.buckets = []
        for i in range(self.size):
            self.buckets.append([])

    def _hash(self, key):
        """Compute the bucket index for a key.

        Uses Python's built-in hash() function (works for strings and
        integers) and takes the remainder with the table size.

        Args:
            key: The key (can be an int or a string).

        Returns:
            The bucket index.
        """
        return hash(key) % self.size

    def _load_factor(self):
        """Compute the current load factor.

        Returns:
            The ratio of stored items to total buckets.
        """
        return self.count / self.size

    def _rehash(self):
        """Double the table size and re-insert all existing items.

        This is called automatically when the load factor exceeds
        the maximum threshold.
        """
        old_buckets = self.buckets
        old_size = self.size

        # Double the size and find a prime-like number
        self.size = self.size * 2
        self.buckets = []
        for i in range(self.size):
            self.buckets.append([])
        self.count = 0

        # Re-insert all items from the old table
        for i in range(old_size):
            for j in range(len(old_buckets[i])):
                key = old_buckets[i][j][0]
                value = old_buckets[i][j][1]
                self.put(key, value)

    def put(self, key, value):
        """Insert a key-value pair.  Updates the value if the key exists.

        Args:
            key: The key (int or string).
            value: The value to store.
        """
        # Check if rehashing is needed before inserting
        if self._load_factor() > self.max_load:
            self._rehash()

        index = self._hash(key)
        bucket = self.buckets[index]

        # Check if key already exists — update if so
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, value)
                return

        # Key is new — add it
        bucket.append((key, value))
        self.count += 1

    def get(self, key):
        """Retrieve the value for a key.

        Args:
            key: The key to look up.

        Returns:
            The value if found, or None.
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                return bucket[i][1]

        return None

    def remove(self, key):
        """Remove a key-value pair from the table.

        Args:
            key: The key to remove.

        Returns:
            True if the key was found and removed, False otherwise.
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                self.count -= 1
                return True

        return False

    def __str__(self):
        """Return a string representation of the hash table."""
        lines = []
        lines.append("HashTable(size={}, count={}, load={:.2f})".format(
            self.size, self.count, self._load_factor()))

        for i in range(self.size):
            if len(self.buckets[i]) > 0:
                lines.append("  Bucket {}: {}".format(i, self.buckets[i]))

        return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 50)
    print("  Custom Hash Table Class — Educational Demo")
    print("=" * 50)

    # Create a new hash table
    ht = SimpleHashTable(initial_size=5, max_load=0.7)

    # Insert some integer keys
    print("\n--- Inserting integer keys ---")
    ht.put(10, "ten")
    ht.put(20, "twenty")
    ht.put(30, "thirty")
    print(ht)

    # Insert string keys
    print("\n--- Inserting string keys ---")
    ht.put("name", "Alice")
    ht.put("age", "25")
    ht.put("city", "Paris")
    print(ht)

    # Retrieve values
    print("\n--- Retrieving values ---")
    print("  ht.get(10)  =", ht.get(10))
    print("  ht.get('name') =", ht.get("name"))
    print("  ht.get('missing') =", ht.get("missing"))

    # Update an existing key
    print("\n--- Updating key 'age' ---")
    ht.put("age", "26")
    print("  ht.get('age') =", ht.get("age"))

    # Delete a key
    print("\n--- Deleting key 20 ---")
    removed = ht.remove(20)
    print("  Key 20 removed:", removed)
    print("  ht.get(20) =", ht.get(20))
    print(ht)

    # Trigger rehashing by adding more items
    print("\n--- Adding items to trigger rehashing ---")
    print("  Current size: {}, count: {}, load factor: {:.2f}".format(
        ht.size, ht.count, ht._load_factor()))
    print("  Adding keys 1..10...")

    for i in range(1, 11):
        ht.put(i, "number_{}".format(i))
        print("  Added key={} -> size={}, count={}, load={:.2f}".format(
            i, ht.size, ht.count, ht._load_factor()))

    print("\nFinal table state:")
    print(ht)
