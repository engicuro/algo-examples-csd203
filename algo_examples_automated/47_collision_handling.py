"""
Collision Handling Strategies in Hash Tables
=============================================

This module demonstrates four common strategies for resolving hash collisions:

1. **Chaining**         – Each bucket holds a linked list of entries.
2. **Linear Probing**   – On collision, probe the next slot sequentially.
3. **Quadratic Probing** – On collision, probe at quadratic offsets.
4. **Double Hashing**   – On collision, use a second hash function for the step size.

Each strategy is implemented as a self-contained class with the same public API
(insert, search, delete) so they can be compared directly.

Run this file directly to see example usage and output:
    python 47_collision_handling.py
"""

from typing import Any, Optional, Tuple, List


# ---------------------------------------------------------------------------
# 1. Chaining (Separate Chaining)
# ---------------------------------------------------------------------------
class HashTableChaining:
    """Hash table that resolves collisions by chaining (linked lists per bucket).

    Each slot in the underlying array holds a list of (key, value) pairs.
    When a collision occurs (two keys hash to the same index), the new entry
    is appended to that bucket's list.

    Time complexity (average / worst case):
        Insert:  O(1) / O(n)
        Search:  O(1) / O(n)
        Delete:  O(1) / O(n)

    Attributes:
        capacity: Number of buckets in the table.
        size:      Current number of key-value pairs stored.
        table:     List of lists, where each inner list is a chain of entries.
    """

    def __init__(self, capacity: int = 10) -> None:
        """Initialize the hash table with a fixed number of buckets."""
        self.capacity: int = capacity
        self.size: int = 0
        # Each bucket starts as an empty list (the chain)
        self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(capacity)]

    def _hash(self, key: Any) -> int:
        """Compute the bucket index for a given key."""
        return hash(key) % self.capacity

    def insert(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair.

        If the key already exists in the chain, its value is updated.
        Otherwise, a new entry is appended to the chain.
        """
        index = self._hash(key)
        chain = self.table[index]

        # Check if key already exists in this chain – update if so
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return

        # Key not found – append new entry
        chain.append((key, value))
        self.size += 1

    def search(self, key: Any) -> Optional[Any]:
        """Return the value associated with *key*, or None if not found."""
        index = self._hash(key)
        chain = self.table[index]

        for k, v in chain:
            if k == key:
                return v
        return None

    def delete(self, key: Any) -> bool:
        """Remove *key* from the table. Returns True if found and removed."""
        index = self._hash(key)
        chain = self.table[index]

        for i, (k, v) in enumerate(chain):
            if k == key:
                del chain[i]
                self.size -= 1
                return True
        return False

    def __repr__(self) -> str:
        """Show non-empty buckets only, for easy inspection."""
        items = []
        for i, chain in enumerate(self.table):
            if chain:
                items.append(f"  bucket[{i}]: {chain}")
        return "HashTableChaining(\n" + "\n".join(items) + "\n)"


# ---------------------------------------------------------------------------
# 2. Linear Probing (Open Addressing)
# ---------------------------------------------------------------------------
class HashTableLinearProbing:
    """Hash table that resolves collisions via linear probing.

    When a collision occurs at index *i*, the algorithm probes *i+1, i+2, …*
    (wrapping around) until an empty slot is found.

    Deleted slots are marked with a sentinel object so that probing chains
    are not broken during search.

    Time complexity (average / worst case):
        Insert:  O(1) / O(n)
        Search:  O(1) / O(n)
        Delete:  O(1) / O(n)
    """

    _DELETED = object()  # Sentinel marker for deleted slots

    def __init__(self, capacity: int = 10) -> None:
        """Initialize the table with *capacity* slots, all empty."""
        self.capacity: int = capacity
        self.size: int = 0
        # Each slot is None (empty), _DELETED (tombstone), or (key, value)
        self.keys: List[Optional[Any]] = [None] * capacity
        self.values: List[Optional[Any]] = [None] * capacity

    def _hash(self, key: Any) -> int:
        """Primary hash function."""
        return hash(key) % self.capacity

    def _probe(self, key: Any) -> int:
        """Find the index where *key* lives or should be inserted.

        Walks the probe sequence linearly until it hits an empty slot or
        finds the key. Returns the index.
        """
        index = self._hash(key)
        # Probe until we find an empty slot (None) or the key itself
        while self.keys[index] is not None and self.keys[index] is not self._DELETED:
            if self.keys[index] == key:
                return index          # key already present
            index = (index + 1) % self.capacity
        return index                  # empty slot – key not present

    def insert(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair using linear probing."""
        # Grow if load factor exceeds 0.7
        if self.size >= self.capacity * 0.7:
            self._resize(self.capacity * 2)

        index = self._probe(key)

        if self.keys[index] == key:
            # Key already exists – update value
            self.values[index] = value
        else:
            # New key – place in the empty (or deleted) slot
            self.keys[index] = key
            self.values[index] = value
            self.size += 1

    def search(self, key: Any) -> Optional[Any]:
        """Return the value for *key*, or None if not found."""
        index = self._hash(key)

        # Walk the probe sequence
        while self.keys[index] is not None:
            if self.keys[index] is not self._DELETED and self.keys[index] == key:
                return self.values[index]
            index = (index + 1) % self.capacity
        return None

    def delete(self, key: Any) -> bool:
        """Remove *key* by marking its slot as deleted (tombstone)."""
        index = self._hash(key)

        while self.keys[index] is not None:
            if self.keys[index] is not self._DELETED and self.keys[index] == key:
                self.keys[index] = self._DELETED
                self.values[index] = None
                self.size -= 1
                return True
            index = (index + 1) % self.capacity
        return False

    def _resize(self, new_capacity: int) -> None:
        """Rehash all entries into a larger table."""
        old_keys = self.keys
        old_values = self.values
        self.capacity = new_capacity
        self.keys = [None] * new_capacity
        self.values = [None] * new_capacity
        self.size = 0

        for k, v in zip(old_keys, old_values):
            if k is not None and k is not self._DELETED:
                self.insert(k, v)

    def __repr__(self) -> str:
        items = []
        for i in range(self.capacity):
            if self.keys[i] is not None and self.keys[i] is not self._DELETED:
                items.append(f"  slot[{i}]: ({self.keys[i]!r}, {self.values[i]!r})")
        return "HashTableLinearProbing(\n" + "\n".join(items) + "\n)"


# ---------------------------------------------------------------------------
# 3. Quadratic Probing (Open Addressing)
# ---------------------------------------------------------------------------
class HashTableQuadraticProbing:
    """Hash table that resolves collisions via quadratic probing.

    On a collision at index *i*, the probe sequence is:
        i, i+1², i+2², i+3², …  (mod capacity)

    This reduces primary clustering compared to linear probing, but can
    suffer from secondary clustering. The table size is kept prime to
    guarantee that all slots are visited when the load factor < 0.5.

    Time complexity (average / worst case):
        Insert:  O(1) / O(n)
        Search:  O(1) / O(n)
        Delete:  O(1) / O(n)
    """

    _DELETED = object()

    def __init__(self, capacity: int = 11) -> None:
        """Initialize with a prime capacity for better probe coverage."""
        self.capacity: int = capacity
        self.size: int = 0
        self.keys: List[Optional[Any]] = [None] * capacity
        self.values: List[Optional[Any]] = [None] * capacity

    def _hash(self, key: Any) -> int:
        """Primary hash function."""
        return hash(key) % self.capacity

    def _probe(self, key: Any) -> int:
        """Walk the quadratic probe sequence for *key*.

        Returns the index of the key if found, or the first available
        (empty or deleted) slot if not found.
        """
        index = self._hash(key)
        step = 0

        while self.keys[index] is not None:
            if self.keys[index] is not self._DELETED and self.keys[index] == key:
                return index
            step += 1
            # Quadratic offset: try i + step^2
            index = (self._hash(key) + step * step) % self.capacity
            # Safety: avoid infinite loop if table is full
            if step >= self.capacity:
                raise RuntimeError("Hash table is full; cannot probe further.")
        return index

    def insert(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair using quadratic probing."""
        if self.size >= self.capacity // 2:
            self._resize(self._next_prime(self.capacity * 2))

        index = self._probe(key)

        if self.keys[index] == key:
            self.values[index] = value
        else:
            self.keys[index] = key
            self.values[index] = value
            self.size += 1

    def search(self, key: Any) -> Optional[Any]:
        """Return the value for *key*, or None if not found."""
        index = self._hash(key)
        step = 0

        while self.keys[index] is not None:
            if self.keys[index] is not self._DELETED and self.keys[index] == key:
                return self.values[index]
            step += 1
            index = (self._hash(key) + step * step) % self.capacity
            if step >= self.capacity:
                break
        return None

    def delete(self, key: Any) -> bool:
        """Remove *key* by marking its slot as a tombstone."""
        index = self._hash(key)
        step = 0

        while self.keys[index] is not None:
            if self.keys[index] is not self._DELETED and self.keys[index] == key:
                self.keys[index] = self._DELETED
                self.values[index] = None
                self.size -= 1
                return True
            step += 1
            index = (self._hash(key) + step * step) % self.capacity
            if step >= self.capacity:
                break
        return False

    def _resize(self, new_capacity: int) -> None:
        """Rehash all entries into a larger prime-sized table."""
        old_keys = self.keys
        old_values = self.values
        self.capacity = new_capacity
        self.keys = [None] * new_capacity
        self.values = [None] * new_capacity
        self.size = 0

        for k, v in zip(old_keys, old_values):
            if k is not None and k is not self._DELETED:
                self.insert(k, v)

    @staticmethod
    def _next_prime(n: int) -> int:
        """Return the smallest prime >= *n*."""
        if n <= 2:
            return 2
        candidate = n if n % 2 != 0 else n + 1
        while True:
            if all(candidate % i != 0 for i in range(2, int(candidate ** 0.5) + 1)):
                return candidate
            candidate += 2

    def __repr__(self) -> str:
        items = []
        for i in range(self.capacity):
            if self.keys[i] is not None and self.keys[i] is not self._DELETED:
                items.append(f"  slot[{i}]: ({self.keys[i]!r}, {self.values[i]!r})")
        return "HashTableQuadraticProbing(\n" + "\n".join(items) + "\n)"


# ---------------------------------------------------------------------------
# 4. Double Hashing (Open Addressing)
# ---------------------------------------------------------------------------
class HashTableDoubleHashing:
    """Hash table that resolves collisions via double hashing.

    Uses two independent hash functions:
        h1(key) = hash(key) % capacity          – primary index
        h2(key) = prime - (hash(key) % prime)    – probe step (never 0)

    The probe sequence is:
        index = (h1(key) + i * h2(key)) % capacity,  for i = 0, 1, 2, …

    Double hashing minimizes both primary and secondary clustering because
    the step size depends on the key itself.

    Time complexity (average / worst case):
        Insert:  O(1) / O(n)
        Search:  O(1) / O(n)
        Delete:  O(1) / O(n)
    """

    _DELETED = object()

    def __init__(self, capacity: int = 11) -> None:
        """Initialize with a prime capacity."""
        self.capacity: int = capacity
        self.size: int = 0
        self.keys: List[Optional[Any]] = [None] * capacity
        self.values: List[Optional[Any]] = [None] * capacity
        # A smaller prime used inside h2 to ensure the step is never 0
        self._prime: int = self._prev_prime(capacity)

    def _hash1(self, key: Any) -> int:
        """Primary hash – determines the starting slot."""
        return hash(key) % self.capacity

    def _hash2(self, key: Any) -> int:
        """Secondary hash – determines the probe step size.

        Must never return 0, so we use a prime smaller than capacity and
        subtract the modulus result from it.
        """
        return self._prime - (hash(key) % self._prime)

    def _probe(self, key: Any) -> int:
        """Walk the double-hashing probe sequence for *key*."""
        h1 = self._hash1(key)
        h2 = self._hash2(key)
        index = h1
        step = 0

        while self.keys[index] is not None:
            if self.keys[index] is not self._DELETED and self.keys[index] == key:
                return index
            step += 1
            index = (h1 + step * h2) % self.capacity
            if step >= self.capacity:
                raise RuntimeError("Hash table is full; cannot probe further.")
        return index

    def insert(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair using double hashing."""
        if self.size >= self.capacity // 2:
            self._resize(self._next_prime(self.capacity * 2))

        index = self._probe(key)

        if self.keys[index] == key:
            self.values[index] = value
        else:
            self.keys[index] = key
            self.values[index] = value
            self.size += 1

    def search(self, key: Any) -> Optional[Any]:
        """Return the value for *key*, or None if not found."""
        h1 = self._hash1(key)
        h2 = self._hash2(key)
        index = h1
        step = 0

        while self.keys[index] is not None:
            if self.keys[index] is not self._DELETED and self.keys[index] == key:
                return self.values[index]
            step += 1
            index = (h1 + step * h2) % self.capacity
            if step >= self.capacity:
                break
        return None

    def delete(self, key: Any) -> bool:
        """Remove *key* by marking its slot as a tombstone."""
        h1 = self._hash1(key)
        h2 = self._hash2(key)
        index = h1
        step = 0

        while self.keys[index] is not None:
            if self.keys[index] is not self._DELETED and self.keys[index] == key:
                self.keys[index] = self._DELETED
                self.values[index] = None
                self.size -= 1
                return True
            step += 1
            index = (h1 + step * h2) % self.capacity
            if step >= self.capacity:
                break
        return False

    def _resize(self, new_capacity: int) -> None:
        """Rehash all entries into a larger prime-sized table."""
        old_keys = self.keys
        old_values = self.values
        self.capacity = new_capacity
        self._prime = self._prev_prime(new_capacity)
        self.keys = [None] * new_capacity
        self.values = [None] * new_capacity
        self.size = 0

        for k, v in zip(old_keys, old_values):
            if k is not None and k is not self._DELETED:
                self.insert(k, v)

    @staticmethod
    def _prev_prime(n: int) -> int:
        """Return the largest prime < *n* (used for h2 step size)."""
        if n <= 2:
            return 1
        candidate = n - 1 if n % 2 == 0 else n - 2
        while candidate > 1:
            if all(candidate % i != 0 for i in range(2, int(candidate ** 0.5) + 1)):
                return candidate
            candidate -= 2
        return 2

    @staticmethod
    def _next_prime(n: int) -> int:
        """Return the smallest prime >= *n*."""
        if n <= 2:
            return 2
        candidate = n if n % 2 != 0 else n + 1
        while True:
            if all(candidate % i != 0 for i in range(2, int(candidate ** 0.5) + 1)):
                return candidate
            candidate += 2

    def __repr__(self) -> str:
        items = []
        for i in range(self.capacity):
            if self.keys[i] is not None and self.keys[i] is not self._DELETED:
                items.append(f"  slot[{i}]: ({self.keys[i]!r}, {self.values[i]!r})")
        return "HashTableDoubleHashing(\n" + "\n".join(items) + "\n)"


# ---------------------------------------------------------------------------
# Example usage / demo
# ---------------------------------------------------------------------------
def demo_chaining() -> None:
    """Demonstrate chaining-based collision resolution."""
    print("=" * 60)
    print("Chaining (Separate Chaining)")
    print("=" * 60)

    ht = HashTableChaining(capacity=7)

    # Insert several keys that will collide
    ht.insert("apple", 1)
    ht.insert("banana", 2)
    ht.insert("cherry", 3)
    ht.insert("date", 4)
    ht.insert("elderberry", 5)

    print(f"Table after inserts:\n{ht}")
    print(f"Search 'cherry': {ht.search('cherry')}")
    print(f"Search 'fig' (absent): {ht.search('fig')}")

    ht.delete("banana")
    print(f"\nAfter deleting 'banana':")
    print(f"Search 'banana': {ht.search('banana')}")
    print(f"Table:\n{ht}")


def demo_linear_probing() -> None:
    """Demonstrate linear probing collision resolution."""
    print("\n" + "=" * 60)
    print("Linear Probing")
    print("=" * 60)

    ht = HashTableLinearProbing(capacity=7)

    ht.insert("apple", 10)
    ht.insert("banana", 20)
    ht.insert("cherry", 30)
    ht.insert("date", 40)

    print(f"Table after inserts:\n{ht}")
    print(f"Search 'cherry': {ht.search('cherry')}")
    print(f"Search 'elderberry' (absent): {ht.search('elderberry')}")

    ht.delete("banana")
    print(f"\nAfter deleting 'banana':")
    print(f"Search 'banana': {ht.search('banana')}")
    print(f"Table:\n{ht}")


def demo_quadratic_probing() -> None:
    """Demonstrate quadratic probing collision resolution."""
    print("\n" + "=" * 60)
    print("Quadratic Probing")
    print("=" * 60)

    ht = HashTableQuadraticProbing(capacity=7)

    ht.insert("apple", 100)
    ht.insert("banana", 200)
    ht.insert("cherry", 300)
    ht.insert("date", 400)

    print(f"Table after inserts:\n{ht}")
    print(f"Search 'date': {ht.search('date')}")
    print(f"Search 'fig' (absent): {ht.search('fig')}")

    ht.delete("banana")
    print(f"\nAfter deleting 'banana':")
    print(f"Search 'banana': {ht.search('banana')}")
    print(f"Table:\n{ht}")


def demo_double_hashing() -> None:
    """Demonstrate double hashing collision resolution."""
    print("\n" + "=" * 60)
    print("Double Hashing")
    print("=" * 60)

    ht = HashTableDoubleHashing(capacity=7)

    ht.insert("apple", 1000)
    ht.insert("banana", 2000)
    ht.insert("cherry", 3000)
    ht.insert("date", 4000)

    print(f"Table after inserts:\n{ht}")
    print(f"Search 'cherry': {ht.search('cherry')}")
    print(f"Search 'elderberry' (absent): {ht.search('elderberry')}")

    ht.delete("banana")
    print(f"\nAfter deleting 'banana':")
    print(f"Search 'banana': {ht.search('banana')}")
    print(f"Table:\n{ht}")


def compare_strategies() -> None:
    """Compare all four strategies side-by-side."""
    print("\n" + "=" * 60)
    print("Side-by-Side Comparison")
    print("=" * 60)

    keys = ["alpha", "beta", "gamma", "delta", "epsilon"]
    values = [1, 2, 3, 4, 5]

    chaining = HashTableChaining(capacity=7)
    linear = HashTableLinearProbing(capacity=7)
    quadratic = HashTableQuadraticProbing(capacity=7)
    double = HashTableDoubleHashing(capacity=7)

    for k, v in zip(keys, values):
        chaining.insert(k, v)
        linear.insert(k, v)
        quadratic.insert(k, v)
        double.insert(k, v)

    print(f"\nChaining:\n{chaining}")
    print(f"\nLinear Probing:\n{linear}")
    print(f"\nQuadratic Probing:\n{quadratic}")
    print(f"\nDouble Hashing:\n{double}")

    # Verify all strategies return the same values
    for k in keys:
        assert chaining.search(k) == linear.search(k) == quadratic.search(k) == double.search(k)
    print("\nAll strategies return consistent search results ✓")


if __name__ == "__main__":
    demo_chaining()
    demo_linear_probing()
    demo_quadratic_probing()
    demo_double_hashing()
    compare_strategies()
