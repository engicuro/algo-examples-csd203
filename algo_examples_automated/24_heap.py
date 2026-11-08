"""
24_heap.py - Heap Data Structure (Min-Heap & Max-Heap) in Python

A heap is a complete binary tree that satisfies the heap property:
  - Min-Heap: every parent node is <= its children (root is the minimum).
  - Max-Heap: every parent node is >= its children (root is the maximum).

Heaps are commonly implemented as arrays (Python lists) where for a node
at index i:
  - Left child  index: 2*i + 1
  - Right child index: 2*i + 2
  - Parent index:     (i - 1) // 2

Topics covered:
  - MinHeap implementation (push, pop, peek, heapify_up, heapify_down)
  - MaxHeap implementation (same API, reversed comparisons)
  - heap_sort: sort a list by building a heap and extracting elements
  - PriorityQueue: a thin wrapper around MinHeap for priority-queue semantics

Complexity reference (for both MinHeap and MaxHeap):
  - push:  O(log n) — bubble up
  - pop:   O(log n) — bubble down
  - peek:  O(1)
  - size:  O(1)
  - is_empty: O(1)
  - heap_sort: O(n log n) time, O(n) space (uses a copy of the input)
"""

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# MinHeap
# ---------------------------------------------------------------------------
class MinHeap(Generic[T]):
    """A min-heap backed by a Python list.

    The smallest element is always at the root (index 0).
    """

    def __init__(self) -> None:
        """Initialize an empty heap."""
        self._data: List[T] = []

    # -- internal helpers ---------------------------------------------------

    def _left_child(self, index: int) -> int:
        """Return the index of the left child of *index*."""
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        """Return the index of the right child of *index*."""
        return 2 * index + 2

    def _parent(self, index: int) -> int:
        """Return the index of the parent of *index*."""
        return (index - 1) // 2

    def _swap(self, i: int, j: int) -> None:
        """Swap elements at positions *i* and *j*."""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    # -- heap maintenance ---------------------------------------------------

    def heapify_up(self, index: int) -> None:
        """Bubble the element at *index* up to restore the heap property.

        Time complexity: O(log n) — at most the height of the tree.
        """
        parent = self._parent(index)
        while index > 0 and self._data[index] < self._data[parent]:
            self._swap(index, parent)
            index = parent
            parent = self._parent(index)

    def heapify_down(self, index: int) -> None:
        """Bubble the element at *index* down to restore the heap property.

        Time complexity: O(log n) — at most the height of the tree.
        """
        size = len(self._data)
        while True:
            smallest = index
            left = self._left_child(index)
            right = self._right_child(index)

            if left < size and self._data[left] < self._data[smallest]:
                smallest = left
            if right < size and self._data[right] < self._data[smallest]:
                smallest = right

            if smallest == index:
                break

            self._swap(index, smallest)
            index = smallest

    # -- public API --------------------------------------------------------

    def push(self, value: T) -> None:
        """Insert *value* into the heap.

        Time complexity: O(log n).
        """
        self._data.append(value)
        self.heapify_up(len(self._data) - 1)

    def pop(self) -> T:
        """Remove and return the minimum element.

        Raises:
            IndexError: If the heap is empty.

        Time complexity: O(log n).
        """
        if self.is_empty():
            raise IndexError("pop from an empty heap")

        # Swap root with last element, remove last, then bubble down
        self._swap(0, len(self._data) - 1)
        min_val = self._data.pop()
        if self._data:
            self.heapify_down(0)
        return min_val

    def peek(self) -> T:
        """Return the minimum element without removing it.

        Raises:
            IndexError: If the heap is empty.

        Time complexity: O(1).
        """
        if self.is_empty():
            raise IndexError("peek from an empty heap")
        return self._data[0]

    def size(self) -> int:
        """Return the number of elements in the heap.

        Time complexity: O(1).
        """
        return len(self._data)

    def is_empty(self) -> bool:
        """Return True if the heap contains no elements.

        Time complexity: O(1).
        """
        return len(self._data) == 0

    def __repr__(self) -> str:
        return f"MinHeap({self._data})"


# ---------------------------------------------------------------------------
# MaxHeap
# ---------------------------------------------------------------------------
class MaxHeap(Generic[T]):
    """A max-heap backed by a Python list.

    The largest element is always at the root (index 0).
    """

    def __init__(self) -> None:
        """Initialize an empty heap."""
        self._data: List[T] = []

    # -- internal helpers ---------------------------------------------------

    def _left_child(self, index: int) -> int:
        """Return the index of the left child of *index*."""
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        """Return the index of the right child of *index*."""
        return 2 * index + 2

    def _parent(self, index: int) -> int:
        """Return the index of the parent of *index*."""
        return (index - 1) // 2

    def _swap(self, i: int, j: int) -> None:
        """Swap elements at positions *i* and *j*."""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    # -- heap maintenance ---------------------------------------------------

    def heapify_up(self, index: int) -> None:
        """Bubble the element at *index* up to restore the heap property.

        Time complexity: O(log n).
        """
        parent = self._parent(index)
        while index > 0 and self._data[index] > self._data[parent]:
            self._swap(index, parent)
            index = parent
            parent = self._parent(index)

    def heapify_down(self, index: int) -> None:
        """Bubble the element at *index* down to restore the heap property.

        Time complexity: O(log n).
        """
        size = len(self._data)
        while True:
            largest = index
            left = self._left_child(index)
            right = self._right_child(index)

            if left < size and self._data[left] > self._data[largest]:
                largest = left
            if right < size and self._data[right] > self._data[largest]:
                largest = right

            if largest == index:
                break

            self._swap(index, largest)
            index = largest

    # -- public API --------------------------------------------------------

    def push(self, value: T) -> None:
        """Insert *value* into the heap.

        Time complexity: O(log n).
        """
        self._data.append(value)
        self.heapify_up(len(self._data) - 1)

    def pop(self) -> T:
        """Remove and return the maximum element.

        Raises:
            IndexError: If the heap is empty.

        Time complexity: O(log n).
        """
        if self.is_empty():
            raise IndexError("pop from an empty heap")

        self._swap(0, len(self._data) - 1)
        max_val = self._data.pop()
        if self._data:
            self.heapify_down(0)
        return max_val

    def peek(self) -> T:
        """Return the maximum element without removing it.

        Raises:
            IndexError: If the heap is empty.

        Time complexity: O(1).
        """
        if self.is_empty():
            raise IndexError("peek from an empty heap")
        return self._data[0]

    def size(self) -> int:
        """Return the number of elements in the heap.

        Time complexity: O(1).
        """
        return len(self._data)

    def is_empty(self) -> bool:
        """Return True if the heap contains no elements.

        Time complexity: O(1).
        """
        return len(self._data) == 0

    def __repr__(self) -> str:
        return f"MaxHeap({self._data})"


# ---------------------------------------------------------------------------
# heap_sort
# ---------------------------------------------------------------------------
def heap_sort(arr: List[T]) -> List[T]:
    """Sort a list in ascending order using a min-heap.

    Args:
        arr: The list of elements to sort.

    Returns:
        A new list containing the elements in sorted order.

    Time complexity: O(n log n) — n insertions + n extractions, each O(log n).
    Space complexity: O(n) — a copy of the input is stored in the heap.
    """
    heap = MinHeap[T]()
    for item in arr:
        heap.push(item)                       # O(log n) per push

    result: List[T] = []
    while not heap.is_empty():
        result.append(heap.pop())             # O(log n) per pop

    return result


# ---------------------------------------------------------------------------
# PriorityQueue (wrapping MinHeap)
# ---------------------------------------------------------------------------
class PriorityQueue(Generic[T]):
    """A min-priority queue backed by a MinHeap.

    Lower priority values are dequeued first.

    Usage:
        pq = PriorityQueue()
        pq.push("task_a", priority=3)
        pq.push("task_b", priority=1)
        pq.pop()  # returns ("task_b", 1)
    """

    def __init__(self) -> None:
        """Initialize an empty priority queue."""
        self._heap: MinHeap[tuple[int, T]] = MinHeap()

    def push(self, item: T, priority: int = 0) -> None:
        """Add an item with the given priority.

        Lower priority values are dequeued first.

        Time complexity: O(log n).
        """
        # Store (priority, item) so the heap orders by priority first
        self._heap.push((priority, item))

    def pop(self) -> T:
        """Remove and return the highest-priority item (lowest priority value).

        Raises:
            IndexError: If the priority queue is empty.

        Time complexity: O(log n).
        """
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")
        priority, item = self._heap.pop()
        return item

    def peek(self) -> T:
        """Return the highest-priority item without removing it.

        Raises:
            IndexError: If the priority queue is empty.

        Time complexity: O(1).
        """
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")
        priority, item = self._heap.peek()
        return item

    def size(self) -> int:
        """Return the number of elements in the priority queue.

        Time complexity: O(1).
        """
        return self._heap.size()

    def is_empty(self) -> bool:
        """Return True if the priority queue has no elements.

        Time complexity: O(1).
        """
        return self._heap.is_empty()

    def __repr__(self) -> str:
        return f"PriorityQueue({self._heap})"


# ---------------------------------------------------------------------------
# __main__ — demonstrations
# ---------------------------------------------------------------------------
def main() -> None:
    """Run all heap demonstrations."""
    print("=" * 60)
    print("Chapter 24 — Heap (Min-Heap & Max-Heap)")
    print("=" * 60)

    # --- MinHeap ---
    print("\n--- MinHeap: basic operations ---")
    min_heap = MinHeap[int]()
    print(f"Is empty? {min_heap.is_empty()}")

    for val in [10, 4, 15, 1, 7, 3]:
        min_heap.push(val)
        print(f"  push({val:>2}) -> heap: {min_heap._data}")

    print(f"Peek (min): {min_heap.peek()}")
    print(f"Size: {min_heap.size()}")

    print("  Popping all elements in sorted order:")
    while not min_heap.is_empty():
        print(f"    pop() -> {min_heap.pop()}")

    print(f"Is empty? {min_heap.is_empty()}")

    # --- MaxHeap ---
    print("\n--- MaxHeap: basic operations ---")
    max_heap = MaxHeap[int]()
    print(f"Is empty? {max_heap.is_empty()}")

    for val in [10, 4, 15, 1, 7, 3]:
        max_heap.push(val)
        print(f"  push({val:>2}) -> heap: {max_heap._data}")

    print(f"Peek (max): {max_heap.peek()}")
    print(f"Size: {max_heap.size()}")

    print("  Popping all elements (descending order):")
    while not max_heap.is_empty():
        print(f"    pop() -> {max_heap.pop()}")

    print(f"Is empty? {max_heap.is_empty()}")

    # --- heap_sort ---
    print("\n--- heap_sort ---")
    unsorted = [5, 3, 8, 1, 2, 7, 4, 6]
    print(f"  Input:   {unsorted}")
    sorted_arr = heap_sort(unsorted)
    print(f"  Sorted:  {sorted_arr}")
    print(f"  Original unchanged: {unsorted}")

    # --- PriorityQueue ---
    print("\n--- PriorityQueue: task scheduler ---")
    pq = PriorityQueue[str]()
    pq.push("Write report", priority=3)
    pq.push("Fix critical bug", priority=1)
    pq.push("Reply to emails", priority=4)
    pq.push("Code review", priority=2)
    pq.push("Update documentation", priority=5)

    print(f"  Queue size: {pq.size()}")
    print(f"  Next task (peek): {pq.peek()}")

    print("  Processing tasks in priority order (lower number = higher priority):")
    order = 0
    while not pq.is_empty():
        task = pq.pop()
        order += 1
        print(f"    {order}. {task}")

    # --- Edge cases ---
    print("\n--- Edge cases ---")
    empty_heap = MinHeap[int]()
    print(f"  Empty heap is_empty? {empty_heap.is_empty()}")
    print(f"  Empty heap size? {empty_heap.size()}")
    try:
        empty_heap.pop()
    except IndexError as e:
        print(f"  pop() on empty heap raises IndexError: {e}")
    try:
        empty_heap.peek()
    except IndexError as e:
        print(f"  peek() on empty heap raises IndexError: {e}")


if __name__ == "__main__":
    main()
