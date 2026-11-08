"""
Hash Table Implementation with Chaining (Separate Chaining)

This module demonstrates the fundamentals of hash tables:
  - Hash function design (division method)
  - Collision handling via chaining (linked lists at each bucket)
  - Core operations: insert, search, delete
  - Dynamic resizing to maintain load factor

A hash table maps keys to values in O(1) average time. When two keys hash
to the same bucket (a collision), chaining stores them together in a list
at that bucket position.
"""


class HashTable:
    """A hash table using separate chaining for collision resolution.

    Attributes:
        capacity (int): Number of buckets in the table.
        size (int): Current number of key-value pairs stored.
        buckets (list[list[tuple]]): Array of buckets, each a list of (key, value) pairs.
        load_factor_threshold (float): Maximum load factor before resizing.
    """

    def __init__(self, capacity: int = 8, load_factor_threshold: float = 0.75):
        """Initialize the hash table.

        Args:
            capacity: Initial number of buckets. Defaults to 8.
            load_factor_threshold: Ratio of size to capacity that triggers
                a resize. Defaults to 0.75.
        """
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        self.load_factor_threshold = load_factor_threshold

    # ------------------------------------------------------------------ #
    #  Hash function                                                       #
    # ------------------------------------------------------------------ #

    def _hash(self, key) -> int:
        """Compute the bucket index for a given key.

        Uses Python's built-in hash() combined with the modulo operation
        (division method). This ensures the index falls within the valid
        range [0, self.capacity).

        Args:
            key: Any hashable object (str, int, tuple, etc.).

        Returns:
            The bucket index where the key should be stored.
        """
        return hash(key) % self.capacity

    # ------------------------------------------------------------------ #
    #  Load factor & resizing                                             #
    # ------------------------------------------------------------------ #

    @property
    def load_factor(self) -> float:
        """Current load factor: ratio of stored entries to bucket count."""
        return self.size / self.capacity

    def _resize(self, new_capacity: int):
        """Expand the table and rehash all existing entries.

        When the load factor exceeds the threshold, we double the capacity
        and redistribute every (key, value) pair into the new buckets.
        This keeps average-case O(1) performance for operations.

        Args:
            new_capacity: The new number of buckets.
        """
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0  # reset size; _insert_into will re-increment

        for chain in old_buckets:
            for key, value in chain:
                self._insert_into(key, value)

    def _insert_into(self, key, value):
        """Insert a key-value pair without triggering resize.

        Internal helper used during resizing to avoid recursive resizes.
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        # Update if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

    # ------------------------------------------------------------------ #
    #  Public operations                                                   #
    # ------------------------------------------------------------------ #

    def insert(self, key, value):
        """Insert or update a key-value pair.

        If the key already exists, its value is updated in place.
        Otherwise the pair is appended to the appropriate bucket chain.

        Args:
            key: The hashable key to insert.
            value: The value associated with the key.
        """
        # Check if resize is needed before inserting
        if (self.size + 1) / self.capacity > self.load_factor_threshold:
            self._resize(self.capacity * 2)

        index = self._hash(key)
        bucket = self.buckets[index]

        # Update existing key
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # New key — append to chain
        bucket.append((key, value))
        self.size += 1

    def search(self, key):
        """Look up a value by its key.

        Traverses the chain at the hashed bucket index until the key
        is found or the chain is exhausted.

        Args:
            key: The key to search for.

        Returns:
            The associated value if found.

        Raises:
            KeyError: If the key is not present in the table.
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v

        raise KeyError(f"Key '{key}' not found in hash table.")

    def delete(self, key):
        """Remove a key-value pair from the table.

        Searches the chain at the hashed bucket and removes the entry
        if found.

        Args:
            key: The key to delete.

        Raises:
            KeyError: If the key is not present in the table.
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return

        raise KeyError(f"Key '{key}' not found in hash table.")

    def contains(self, key) -> bool:
        """Check whether a key exists in the table.

        Args:
            key: The key to check.

        Returns:
            True if the key is present, False otherwise.
        """
        index = self._hash(key)
        return any(k == key for k, _ in self.buckets[index])

    def keys(self) -> list:
        """Return a list of all keys in the table."""
        return [k for chain in self.buckets for k, _ in chain]

    def values(self) -> list:
        """Return a list of all values in the table."""
        return [v for chain in self.buckets for _, v in chain]

    def items(self) -> list:
        """Return a list of all (key, value) tuples in the table."""
        return [(k, v) for chain in self.buckets for k, v in chain]

    def __len__(self) -> int:
        """Return the number of key-value pairs stored."""
        return self.size

    def __repr__(self) -> str:
        """Return a string representation of the hash table."""
        pairs = ", ".join(f"{k!r}: {v!r}" for chain in self.buckets for k, v in chain)
        return f"HashTable({{{pairs}}})"


# ====================================================================== #
#  Example usage                                                          #
# ====================================================================== #

if __name__ == "__main__":
    print("=" * 60)
    print("Hash Table — Chaining (Separate Chaining) Demo")
    print("=" * 60)

    # --- Create table ---
    ht = HashTable(capacity=4)
    print(f"\nCreated hash table with capacity={ht.capacity}")

    # --- Insert ---
    print("\n--- Inserting key-value pairs ---")
    pairs = [
        ("apple", 5),
        ("banana", 3),
        ("cherry", 7),
        ("date", 2),
        ("elderberry", 9),
        ("fig", 1),
    ]
    for key, val in pairs:
        ht.insert(key, val)
        print(f"  insert({key!r}, {val})  →  bucket index = {ht._hash(key)}, "
              f"load factor = {ht.load_factor:.2f}")

    print(f"\nTable size: {len(ht)} entries across {ht.capacity} buckets")

    # --- Search ---
    print("\n--- Searching for keys ---")
    for key in ["apple", "cherry", "grape"]:
        try:
            result = ht.search(key)
            print(f"  search({key!r}) → {result}")
        except KeyError as e:
            print(f"  search({key!r}) → {e}")

    # --- Update existing key ---
    print("\n--- Updating 'apple' from 5 to 10 ---")
    ht.insert("apple", 10)
    print(f"  search('apple') → {ht.search('apple')}")

    # --- Contains ---
    print("\n--- Checking key existence ---")
    for key in ["banana", "grape"]:
        print(f"  contains({key!r}) → {ht.contains(key)}")

    # --- Delete ---
    print("\n--- Deleting keys ---")
    for key in ["date", "grape"]:
        try:
            ht.delete(key)
            print(f"  delete({key!r}) → success")
        except KeyError as e:
            print(f"  delete({key!r}) → {e}")

    print(f"\nTable size after deletions: {len(ht)}")

    # --- List all entries ---
    print("\n--- All entries ---")
    for k, v in ht.items():
        print(f"  {k!r}: {v}")

    # --- Keys / Values ---
    print(f"\nKeys:   {ht.keys()}")
    print(f"Values: {ht.values()}")

    # --- Resize demonstration ---
    print("\n--- Triggering a resize ---")
    print(f"  Before resize: capacity={ht.capacity}, size={len(ht)}, "
          f"load_factor={ht.load_factor:.2f}")
    for i in range(20):
        ht.insert(f"key_{i}", i * 10)
    print(f"  After adding 20 more entries: capacity={ht.capacity}, size={len(ht)}, "
          f"load_factor={ht.load_factor:.2f}")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)
