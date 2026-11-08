"""
Priority Queue Implementation Examples (Chapter 2)
===================================================

A priority queue is an abstract data type where each element has an
associated priority. Elements are dequeued in priority order (lowest
priority value first by default with heapq).

This file demonstrates:
  1. Priority queue using heapq (min-heap)
  2. Priority queue using heapq with tuples for tie-breaking
  3. Priority queue using heapq for max-heap behavior (negation trick)
  4. Practical examples: task scheduler and merge k sorted lists
"""

import heapq
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Basic Priority Queue using heapq
# ---------------------------------------------------------------------------
class PriorityQueue:
    """Min-priority queue backed by the heapq module.

    The smallest priority value is dequeued first.

    Usage:
        pq = PriorityQueue()
        pq.push("task_a", priority=3)
        pq.push("task_b", priority=1)
        pq.pop()  # returns ("task_b", 1)
    """

    def __init__(self) -> None:
        """Initialize an empty priority queue."""
        self._heap: list[tuple[int, Any]] = []
        self._counter = 0  # tie-breaker for equal priorities

    def push(self, item: Any, priority: int = 0) -> None:
        """Add an item with the given priority.

        Args:
            item:     The element to store.
            priority: Lower values = higher priority (dequeued first).
        """
        # The counter ensures stable ordering for items with equal priority
        # (heapq compares tuples element-by-element)
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def pop(self) -> tuple[Any, int]:
        """Remove and return the highest-priority item.

        Returns:
            A (item, priority) tuple.

        Raises:
            IndexError: If the priority queue is empty.
        """
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")
        priority, _, item = heapq.heappop(self._heap)
        return item, priority

    def peek(self) -> tuple[Any, int]:
        """Return the highest-priority item without removing it.

        Returns:
            A (item, priority) tuple.

        Raises:
            IndexError: If the priority queue is empty.
        """
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")
        priority, _, item = self._heap[0]
        return item, priority

    def is_empty(self) -> bool:
        """Return True if the priority queue has no elements."""
        return len(self._heap) == 0

    def size(self) -> int:
        """Return the number of elements in the priority queue."""
        return len(self._heap)

    def __repr__(self) -> str:
        items = [(item, pri) for pri, _, item in self._heap]
        return f"PriorityQueue({items})"


# ---------------------------------------------------------------------------
# Max-Priority Queue (using negation trick)
# ---------------------------------------------------------------------------
class MaxPriorityQueue:
    """Max-priority queue built on top of heapq by negating priorities.

    The largest priority value is dequeued first.
    """

    def __init__(self) -> None:
        """Initialize an empty max-priority queue."""
        self._heap: list[tuple[int, int, Any]] = []
        self._counter = 0

    def push(self, item: Any, priority: int = 0) -> None:
        """Add an item. Higher priority values = dequeued first."""
        # Negate the priority so that heapq (a min-heap) behaves as a max-heap
        heapq.heappush(self._heap, (-priority, self._counter, item))
        self._counter += 1

    def pop(self) -> tuple[Any, int]:
        """Remove and return the highest-priority item."""
        if self.is_empty():
            raise IndexError("pop from an empty max-priority queue")
        neg_priority, _, item = heapq.heappop(self._heap)
        return item, -neg_priority  # restore original priority

    def peek(self) -> tuple[Any, int]:
        """Return the highest-priority item without removing it."""
        if self.is_empty():
            raise IndexError("peek from an empty max-priority queue")
        neg_priority, _, item = self._heap[0]
        return item, -neg_priority

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)


# ---------------------------------------------------------------------------
# Example 1: Task Scheduler
# ---------------------------------------------------------------------------
def task_scheduler() -> None:
    """Demonstrate a priority-based task scheduler.

    Tasks with lower priority numbers are executed first.
    """
    pq = PriorityQueue()

    # Submit tasks with various priorities
    pq.push("Write report", priority=3)
    pq.push("Fix critical bug", priority=1)
    pq.push("Reply to emails", priority=4)
    pq.push("Code review", priority=2)
    pq.push("Update documentation", priority=5)

    print("  Tasks submitted (lower number = higher priority):")
    print(f"  Queue size: {pq.size()}\n")

    print("  Executing tasks in priority order:")
    order = 0
    while not pq.is_empty():
        task, priority = pq.pop()
        order += 1
        print(f"    {order}. [priority={priority}] {task}")


# ---------------------------------------------------------------------------
# Example 2: Merge K Sorted Lists using a Priority Queue
# ---------------------------------------------------------------------------
def merge_k_sorted_lists(lists: list[list[int]]) -> list[int]:
    """Merge *k* sorted lists into a single sorted list.

    Uses a min-priority queue to always pick the smallest available
    element across all lists.

    Args:
        lists: A list of sorted integer lists.

    Returns:
        A single sorted list containing all elements.

    Time complexity: O(N log k) where N = total elements, k = number of lists.
    """
    pq = PriorityQueue()
    result: list[int] = []

    # Push the first element of each non-empty list along with
    # (list_index, element_index) so we can fetch the next element
    for i, lst in enumerate(lists):
        if lst:
            # priority = value, item = (value, list_index, element_index)
            pq.push((lst[0], i, 0), priority=lst[0])

    while not pq.is_empty():
        (value, list_idx, elem_idx), _ = pq.pop()
        result.append(value)

        # If there is a next element in the same list, push it
        next_idx = elem_idx + 1
        if next_idx < len(lists[list_idx]):
            next_val = lists[list_idx][next_idx]
            pq.push((next_val, list_idx, next_idx), priority=next_val)

    return result


# ---------------------------------------------------------------------------
# Example 3: Max-Priority Queue demonstration
# ---------------------------------------------------------------------------
def demo_max_priority_queue() -> None:
    """Show that MaxPriorityQueue dequeues highest priority first."""
    mpq = MaxPriorityQueue()
    mpq.push("Low urgency task", priority=1)
    mpq.push("High urgency task", priority=10)
    mpq.push("Medium urgency task", priority=5)
    mpq.push("Urgent task", priority=8)

    print("  Max-Priority Queue (higher number = higher priority):")
    while not mpq.is_empty():
        task, priority = mpq.pop()
        print(f"    [priority={priority}] {task}")


# ---------------------------------------------------------------------------
# Example 4: Heapq module direct usage (quick reference)
# ---------------------------------------------------------------------------
def demo_heapq_direct() -> None:
    """Show common heapq module functions directly."""
    print("  --- Direct heapq usage ---")

    # heapify an existing list in-place
    data = [5, 3, 8, 1, 2, 7, 4, 6]
    print(f"  Original list: {data}")
    heapq.heapify(data)
    print(f"  After heapify (min-heap): {data}")

    # heappush and heappop
    heapq.heappush(data, 0)
    print(f"  After heappush(0): {data}")
    smallest = heapq.heappop(data)
    print(f"  heappop() -> {smallest}, heap now: {data}")

    # nsmallest and nlargest (convenience, don't modify the heap)
    print(f"  3 smallest: {heapq.nsmallest(3, data)}")
    print(f"  3 largest:  {heapq.nlargest(3, data)}")

    # heapreplace: pop smallest then push new item (one atomic operation)
    replaced = heapq.heapreplace(data, -1)
    print(f"  heapreplace(0, -1) -> replaced {replaced}, heap now: {data}")


# ---------------------------------------------------------------------------
# __main__ block — run examples when executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Priority Queue Examples — Chapter 2")
    print("=" * 60)

    # --- Basic operations ---
    print("\n--- PriorityQueue: basic operations ---")
    pq = PriorityQueue()
    print(f"Is empty? {pq.is_empty()}")
    pq.push("task_a", priority=5)
    pq.push("task_b", priority=1)
    pq.push("task_c", priority=3)
    print(f"Queue: {pq}")
    print(f"Peek: {pq.peek()}")
    print(f"Size: {pq.size()}")
    while not pq.is_empty():
        item, pri = pq.pop()
        print(f"  Pop -> {item!r} (priority={pri})")

    # --- Example 1: Task Scheduler ---
    print("\n--- Example 1: Task Scheduler ---")
    task_scheduler()

    # --- Example 2: Merge K Sorted Lists ---
    print("\n--- Example 2: Merge K Sorted Lists ---")
    sorted_lists = [
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
    ]
    print(f"  Input lists: {sorted_lists}")
    merged = merge_k_sorted_lists(sorted_lists)
    print(f"  Merged result: {merged}")

    # --- Example 3: Max Priority Queue ---
    print("\n--- Example 3: Max-Priority Queue ---")
    demo_max_priority_queue()

    # --- Example 4: Direct heapq usage ---
    print("\n--- Example 4: Direct heapq module usage ---")
    demo_heapq_direct()
