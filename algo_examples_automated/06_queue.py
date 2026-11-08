"""
Queue Implementation Examples (Chapter 2)
=========================================

A queue is a First-In-First-Out (FIFO) data structure.
This file demonstrates:
  1. Queue using a Python list
  2. Queue using collections.deque
  3. Examples: hot-potato elimination game and printer spooler simulation
"""

from collections import deque


# ---------------------------------------------------------------------------
# Queue implemented with a Python list
# ---------------------------------------------------------------------------
class QueueList:
    """Queue backed by a Python list.

    Note:
        Using a list for a queue is educational but inefficient for large
        data — pop(0) is O(n). Prefer QueueDeque for production use.
    """

    def __init__(self) -> None:
        """Initialize an empty queue."""
        self._items: list = []

    def enqueue(self, item) -> None:
        """Add an item to the rear of the queue.

        Args:
            item: The element to add.
        """
        self._items.append(item)

    def dequeue(self):
        """Remove and return the front item from the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self._items.pop(0)

    def peek(self):
        """Return the front item without removing it.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("peek from an empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        """Return True if the queue has no elements."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of elements in the queue."""
        return len(self._items)

    def __repr__(self) -> str:
        return f"QueueList({self._items})"


# ---------------------------------------------------------------------------
# Queue implemented with collections.deque
# ---------------------------------------------------------------------------
class QueueDeque:
    """Queue backed by collections.deque (O(1) enqueue and dequeue)."""

    def __init__(self) -> None:
        """Initialize an empty queue."""
        self._items: deque = deque()

    def enqueue(self, item) -> None:
        """Add an item to the rear of the queue."""
        self._items.append(item)

    def dequeue(self):
        """Remove and return the front item from the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self._items.popleft()

    def peek(self):
        """Return the front item without removing it.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("peek from an empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        """Return True if the queue has no elements."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of elements in the queue."""
        return len(self._items)

    def __repr__(self) -> str:
        return f"QueueDeque({list(self._items)})"


# ---------------------------------------------------------------------------
# Example 1: Hot-Potato Elimination Game
# ---------------------------------------------------------------------------
def hot_potato(names: list[str], num: int) -> str:
    """Simulate the hot-potato elimination game.

    Players stand in a circle. A "potato" is passed around *num* times,
    and the player holding it is eliminated. This repeats until one
    player remains.

    Args:
        names: List of player names.
        num:   Number of passes before elimination.

    Returns:
        The name of the last remaining player.
    """
    queue = QueueDeque()
    for name in names:
        queue.enqueue(name)

    print(f"  Starting with {len(names)} players: {names}")
    print(f"  Passing the potato {num} times per round\n")

    round_num = 0
    while queue.size() > 1:
        round_num += 1
        # Pass the potato num times (rotate the queue)
        for _ in range(num):
            queue.enqueue(queue.dequeue())
        # The player at the front is eliminated
        eliminated = queue.dequeue()
        print(f"  Round {round_num:2d}: {eliminated!r} is eliminated  "
              f"| Remaining: {list(queue._items)}")

    winner = queue.dequeue()
    return winner


# ---------------------------------------------------------------------------
# Example 2: Printer Spooler Simulation
# ---------------------------------------------------------------------------
def printer_spooler(jobs: list[tuple[str, int]]) -> None:
    """Simulate a printer spooler that processes jobs in FIFO order.

    Args:
        jobs: List of (document_name, pages) tuples.
    """
    queue = QueueDeque()

    # Submit all print jobs
    for name, pages in jobs:
        queue.enqueue((name, pages))
        print(f"  [SUBMIT] {name} ({pages} page{'s' if pages != 1 else ''})")

    print(f"\n  Queue size after submission: {queue.size()}\n")

    # Process jobs one by one
    order = 0
    while not queue.is_empty():
        name, pages = queue.dequeue()
        order += 1
        print(f"  [PRINT #{order}] {name} ({pages} page{'s' if pages != 1 else ''})")

    print(f"\n  All {order} job(s) completed.")


# ---------------------------------------------------------------------------
# __main__ block — run examples when executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Queue Examples — Chapter 2")
    print("=" * 60)

    # --- Basic operations with QueueList ---
    print("\n--- QueueList: basic operations ---")
    q = QueueList()
    print(f"Is empty? {q.is_empty()}")
    for i in range(1, 6):
        q.enqueue(i)
        print(f"Enqueue {i} -> {q}")
    print(f"Peek front: {q.peek()}")
    print(f"Size: {q.size()}")
    while not q.is_empty():
        print(f"Dequeue -> {q.dequeue()}, remaining: {q}")

    # --- Basic operations with QueueDeque ---
    print("\n--- QueueDeque: basic operations ---")
    qd = QueueDeque()
    for ch in "ABCDE":
        qd.enqueue(ch)
        print(f"Enqueue '{ch}' -> {qd}")
    print(f"Peek front: {qd.peek()}")
    print(f"Size: {qd.size()}")
    while not qd.is_empty():
        print(f"Dequeue -> {qd.dequeue()}, remaining: {qd}")

    # --- Example 1: Hot-Potato Game ---
    print("\n--- Example 1: Hot-Potato Elimination Game ---")
    winner = hot_potato(
        names=["Alice", "Bob", "Charlie", "David", "Eve"],
        num=3,
    )
    print(f"\n  Winner: {winner!r}")

    # --- Example 2: Printer Spooler ---
    print("\n--- Example 2: Printer Spooler Simulation ---")
    printer_spooler([
        ("report.pdf", 3),
        ("photo.png", 1),
        ("thesis.docx", 12),
        ("notes.txt", 1),
        ("slides.pptx", 8),
    ])
