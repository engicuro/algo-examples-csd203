"""
49_python_hash_table.py

Python Hash Table Implementation
=================================

Demonstrates hash tables in Python using:
  1. The built-in dict type (Python's native hash table)
  2. A custom HashTable class with open-addressing (linear probing)
  3. Python's built-in hash() function

Topics covered:
  - How hash() works on different types
  - Collision handling via linear probing
  - Load factor and dynamic resizing
  - Basic operations: insert, lookup, delete

Run:
    python 49_python_hash_table.py
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Part 1 — Using Python's built-in dict (the standard hash table)
# ---------------------------------------------------------------------------

def demo_builtin_dict() -> None:
    """Show how Python's dict uses hashing under the hood."""
    print("=" * 60)
    print("Part 1: Python's built-in dict")
    print("=" * 60)

    # Create a dictionary — Python allocates a hash table internally.
    phonebook: dict[str, str] = {}

    # Insert key-value pairs.  dict uses hash(key) to find the bucket.
    phonebook["Alice"] = "555-0101"
    phonebook["Bob"] = "555-0102"
    phonebook["Charlie"] = "555-0103"

    # Lookup — O(1) average case.
    print(f"Alice's number: {phonebook['Alice']}")

    # Check membership — also O(1) average.
    print(f"'Bob' in phonebook: {'Bob' in phonebook}")
    print(f"'Eve' in phonebook: {'Eve' in phonebook}")

    # Delete a key.
    del phonebook["Bob"]
    print(f"After deleting Bob: {phonebook}")

    # Demonstrate hash() on various types.
    print("\nHash values for different keys:")
    for key in ["Alice", 42, (1, 2, 3), frozenset({1, 2})]:
        print(f"  hash({key!r}) = {hash(key)}")

    print()


# ---------------------------------------------------------------------------
# Part 2 — Custom HashTable with open addressing (linear probing)
# ---------------------------------------------------------------------------

class HashTable:
    """A simple hash table using open addressing with linear probing.

    Attributes:
        capacity: Number of slots in the underlying array.
        size: Current number of stored key-value pairs.
        keys: List storing keys (or _EMPTY / _DELETED sentinels).
        values: List storing corresponding values.
    """

    _EMPTY = object()   # sentinel for a never-used slot
    _DELETED = object()  # sentinel for a deleted slot

    def __init__(self, initial_capacity: int = 8) -> None:
        """Initialize the hash table with a given capacity."""
        self.capacity = initial_capacity
        self.size = 0
        self.keys: list[object] = [self._EMPTY] * self.capacity
        self.values: list[object] = [None] * self.capacity

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _hash(self, key: object) -> int:
        """Compute the bucket index for *key* using Python's built-in hash().

        Python's hash() returns an int; we take modulo capacity to map
        it into the valid index range [0, capacity).
        """
        return hash(key) % self.capacity

    def _probe(self, key: object) -> int:
        """Find the index where *key* lives or should be inserted.

        Uses linear probing: if the desired slot is occupied by a
        different key, we move forward (wrapping around) until we
        find an empty slot, a deleted slot, or the key itself.
        """
        index = self._hash(key)
        start = index

        while True:
            # Slot is empty → key is not present; return insertion point.
            if self.keys[index] is self._EMPTY:
                return index
            # Slot was deleted → could be our insertion point, but keep
            # probing in case the key exists further along.
            if self.keys[index] is self._DELETED:
                # Save the first deleted slot we find; use it if key
                # is not found later.
                first_deleted = index
                # Continue probing to check if key exists further.
                index = (index + 1) % self.capacity
                while self.keys[index] is not self._EMPTY:
                    if self.keys[index] == key:
                        return index
                    index = (index + 1) % self.capacity
                return first_deleted
            # Slot holds the key we are looking for.
            if self.keys[index] == key:
                return index
            # Slot holds a different key → linear probe forward.
            index = (index + 1) % self.capacity
            # Full table cycle → table is full (should not happen if
            # load factor is kept below 1.0).
            if index == start:
                raise RuntimeError("HashTable is full")

    def _resize(self, new_capacity: int) -> None:
        """Resize the internal arrays and rehash all existing entries."""
        old_keys = self.keys
        old_values = self.values

        self.capacity = new_capacity
        self.keys = [self._EMPTY] * self.capacity
        self.values = [None] * self.capacity
        self.size = 0

        # Re-insert every live entry into the new arrays.
        for key, value in zip(old_keys, old_values):
            if key is not self._EMPTY and key is not self._DELETED:
                self.insert(key, value)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def insert(self, key: object, value: object) -> None:
        """Insert or update *key* with *value*.

        If the load factor exceeds 0.7 after insertion, the table is
        resized to double its current capacity.
        """
        index = self._probe(key)

        # Key already exists → update value in place.
        if self.keys[index] == key:
            self.values[index] = value
            return

        # New key → store in the found slot.
        self.keys[index] = key
        self.values[index] = value
        self.size += 1

        # Resize if load factor is too high.
        if self.size / self.capacity > 0.7:
            self._resize(self.capacity * 2)

    def get(self, key: object) -> object:
        """Return the value associated with *key*.

        Raises:
            KeyError: If *key* is not in the table.
        """
        index = self._probe(key)
        if self.keys[index] == key:
            return self.values[index]
        raise KeyError(key)

    def delete(self, key: object) -> None:
        """Remove *key* from the table.

        Raises:
            KeyError: If *key* is not in the table.
        """
        index = self._probe(key)
        if self.keys[index] != key:
            raise KeyError(key)

        # Mark the slot as deleted (lazy deletion) so probing chains
        # for other keys remain intact.
        self.keys[index] = self._DELETED
        self.values[index] = None
        self.size -= 1

    def __contains__(self, key: object) -> bool:
        """Support 'key in table' syntax."""
        try:
            idx = self._probe(key)
            return self.keys[idx] == key
        except (KeyError, RuntimeError):
            return False

    def __getitem__(self, key: object) -> object:
        """Support table[key] syntax — returns the value for *key*."""
        return self.get(key)

    def __setitem__(self, key: object, value: object) -> None:
        """Support table[key] = value syntax — inserts or updates *key*."""
        self.insert(key, value)

    def __len__(self) -> int:
        """Return the number of stored entries."""
        return self.size

    def __repr__(self) -> str:
        """Return a readable representation of the table's contents."""
        items = []
        for key, value in zip(self.keys, self.values):
            if key is not self._EMPTY and key is not self._DELETED:
                items.append(f"{key!r}: {value!r}")
        return "HashTable({" + ", ".join(items) + "})"


def demo_custom_hash_table() -> None:
    """Demonstrate the custom HashTable class."""
    print("=" * 60)
    print("Part 2: Custom HashTable with linear probing")
    print("=" * 60)

    ht = HashTable(initial_capacity=4)

    # Insert some entries.
    ht.insert("apple", 3)
    ht.insert("banana", 5)
    ht.insert("cherry", 7)
    print(f"After inserts: {ht}")
    print(f"  Size: {len(ht)}, Capacity: {ht.capacity}")

    # Lookup.
    print(f"\n  ht['apple'] = {ht['apple']}")
    print(f"  ht['banana'] = {ht['banana']}")

    # Update an existing key.
    ht.insert("apple", 10)
    print(f"\nAfter updating apple: ht['apple'] = {ht['apple']}")

    # Check membership.
    print(f"\n  'cherry' in ht: {'cherry' in ht}")
    print(f"  'date' in ht: {'date' in ht}")

    # Delete a key.
    ht.delete("banana")
    print(f"\nAfter deleting banana: {ht}")
    print(f"  Size: {len(ht)}, Capacity: {ht.capacity}")

    # Demonstrate that deleted slots don't break probing chains.
    ht.insert("banana", 20)  # re-insert into a deleted slot
    print(f"\nAfter re-inserting banana: {ht}")

    # Show that resizing happens automatically.
    print("\nAdding more entries to trigger a resize...")
    for i in range(20):
        ht.insert(f"key_{i}", i * 100)
    print(f"  Size: {len(ht)}, Capacity: {ht.capacity}")
    print(f"  Table: {ht}")

    print()


# ---------------------------------------------------------------------------
# Part 3 — Comparing hash values and understanding collisions
# ---------------------------------------------------------------------------

def demo_hash_collisions() -> None:
    """Show how different keys can produce the same hash bucket."""
    print("=" * 60)
    print("Part 3: Understanding hash collisions")
    print("=" * 60)

    # Two different strings that map to the same bucket for a small capacity.
    capacity = 4
    candidates = ["abc", "bca", "cab", "hello", "world", "python"]

    print(f"Bucket assignments (capacity = {capacity}):")
    buckets: dict[int, list[str]] = {}
    for s in candidates:
        bucket = hash(s) % capacity
        buckets.setdefault(bucket, []).append(s)

    for bucket, keys in sorted(buckets.items()):
        print(f"  Bucket {bucket}: {keys}")

    print(
        "\nNote: Different keys mapping to the same bucket is a collision. "
        "Our custom HashTable handles this via linear probing."
    )
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demo_builtin_dict()
    demo_custom_hash_table()
    demo_hash_collisions()
