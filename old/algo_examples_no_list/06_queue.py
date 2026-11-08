# Queue Implementation Examples (Chapter 2) — No-List Version
# ==========================================
#
# A queue is a First-In-First-Out (FIFO) data structure.
# This version uses a linked list instead of Python lists.
# No external libraries.


# ---------------------------------------------------------------------------
# Node class for the linked-list-based queue
# ---------------------------------------------------------------------------
class _Node:
    """A single node in the linked list used by the queue."""

    def __init__(self, value):
        self.value = value
        self._next = None


# ---------------------------------------------------------------------------
# Queue built on a linked list (with head and tail pointers)
# ---------------------------------------------------------------------------

def queue_create():
    """Create and return an empty queue.

    The queue is represented as (head, tail) tuple of node references.
    (None, None) means empty.
    """
    return (None, None)


def queue_enqueue(q, item):
    """Add an item to the rear of the queue.

    Args:
        q:    The queue tuple (head, tail).
        item: The element to add.

    Returns:
        The new queue tuple.
    """
    new_node = _Node(item)
    head, tail = q

    if tail is None:
        # Queue is empty — new node is both head and tail
        return (new_node, new_node)
    else:
        # Attach new node after the current tail
        tail._next = new_node
        return (head, new_node)


def queue_dequeue(q):
    """Remove and return the front item from the queue.

    Returns (value, new_queue) where new_queue is the queue after removal.
    Returns (None, q) if the queue is empty.

    Args:
        q: The queue tuple (head, tail).

    Returns:
        A tuple (front_element, new_queue).
    """
    head, tail = q
    if queue_is_empty(q):
        print("  [warn] dequeue called on an empty queue")
        return None, q

    value = head.value
    new_head = head._next
    if new_head is None:
        # Queue is now empty
        return value, (None, None)
    return value, (new_head, tail)


def queue_peek(q):
    """Return the front item without removing it.

    Returns None if the queue is empty.

    Args:
        q: The queue tuple (head, tail).

    Returns:
        The front element, or None if the queue is empty.
    """
    head, tail = q
    if queue_is_empty(q):
        print("  [warn] peek called on an empty queue")
        return None
    return head.value


def queue_is_empty(q):
    """Return True if the queue has no elements.

    Args:
        q: The queue tuple (head, tail).

    Returns:
        True if the queue is empty, False otherwise.
    """
    head, tail = q
    return head is None


def queue_size(q):
    """Return the number of elements in the queue.

    Args:
        q: The queue tuple (head, tail).

    Returns:
        The count of items in the queue.
    """
    head, tail = q
    count = 0
    current = head
    while current is not None:
        count = count + 1
        current = current._next
    return count


# ---------------------------------------------------------------------------
# Helper: convert queue to a readable string (no list used)
# ---------------------------------------------------------------------------
def _queue_to_string(q):
    """Build a string representation of the queue without using a list."""
    head, tail = q
    if head is None:
        return "[]"
    parts = ""
    current = head
    first = True
    while current is not None:
        if not first:
            parts = parts + ", "
        parts = parts + str(current.value)
        first = False
        current = current._next
    return "[" + parts + "]"


# ---------------------------------------------------------------------------
# Example 1: Hot-Potato Elimination Game
# ---------------------------------------------------------------------------

def hot_potato(names, num):
    """Simulate the hot-potato elimination game.

    Uses a linked-list-based queue instead of a Python list.

    Args:
        names: A tuple of player names.
        num:   How many passes to make before each elimination.

    Returns:
        The name of the last remaining player (the winner).
    """
    q = queue_create()

    # Put every player into the queue
    for name in names:
        q = queue_enqueue(q, name)

    print("  Starting with %d players" % len(names))
    print("  Passing the potato %d times per round\n" % num)

    round_num = 0
    while queue_size(q) > 1:
        round_num = round_num + 1

        # Pass the potato 'num' times by rotating the queue
        for _ in range(num):
            front_player, q = queue_dequeue(q)
            q = queue_enqueue(q, front_player)

        # The player at the front is eliminated
        eliminated, q = queue_dequeue(q)
        print("  Round %2d: %s is eliminated  |  Remaining: %s"
              % (round_num, eliminated, _queue_to_string(q)))

    # The last player left is the winner
    winner, _ = queue_dequeue(q)
    return winner


# ---------------------------------------------------------------------------
# Example 2: Simple Print Job Queue
# ---------------------------------------------------------------------------

def print_queue_demo(jobs):
    """Simulate a printer that processes jobs in FIFO order.

    Args:
        jobs: A tuple of (document_name, pages) tuples.
    """
    q = queue_create()

    # Submit all print jobs
    print("  Submitting print jobs:")
    for name, pages in jobs:
        q = queue_enqueue(q, (name, pages))
        print("    [SUBMIT] %s (%d page%s)"
              % (name, pages, "s" if pages != 1 else ""))

    print("\n  Queue size after submission: %d\n" % queue_size(q))

    # Process each job in order
    order = 0
    while not queue_is_empty(q):
        name, pages, q = queue_dequeue(q)
        order = order + 1
        print("    [PRINT #%d] %s (%d page%s)"
              % (order, name, pages, "s" if pages != 1 else ""))

    print("\n  All %d job(s) completed." % order)


# ---------------------------------------------------------------------------
# __main__ — run examples when this file is executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Queue Examples — Chapter 2 (No-List Version)")
    print("=" * 60)

    # --- Basic queue operations ---
    print("\n--- Basic Queue Operations ---")
    q = queue_create()
    print("Created an empty queue.")
    print("Is empty? %s" % queue_is_empty(q))

    # Enqueue some numbers
    for i in range(1, 6):
        q = queue_enqueue(q, i)
        print("Enqueue %d -> queue size is now %d" % (i, queue_size(q)))

    print("Front element (peek): %s" % queue_peek(q))
    print("Queue size: %d" % queue_size(q))

    # Dequeue everything
    print("Dequeuing all elements:")
    while not queue_is_empty(q):
        item, q = queue_dequeue(q)
        print("  Dequeued %s, remaining size: %d" % (item, queue_size(q)))

    # --- Example 1: Hot-Potato Game ---
    print("\n--- Example 1: Hot-Potato Elimination Game ---")
    winner = hot_potato(
        names=("Alice", "Bob", "Charlie", "David", "Eve"),
        num=3,
    )
    print("\n  Winner: %s" % winner)

    # --- Example 2: Print Job Queue ---
    print("\n--- Example 2: Print Job Queue ---")
    print_queue_demo((
        ("report.pdf", 3),
        ("photo.png", 1),
        ("thesis.docx", 12),
        ("notes.txt", 1),
        ("slides.pptx", 8),
    ))
