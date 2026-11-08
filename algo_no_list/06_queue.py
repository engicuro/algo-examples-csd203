# Queue Implementation Examples (Chapter 2)
# ==========================================
#
# A queue is a First-In-First-Out (FIFO) data structure.
# The first item you enqueue is the first one you dequeue.
#
# This file uses tuples instead of Python lists — no lists,
# no external libraries.


# ---------------------------------------------------------------------------
# Queue built on a Python tuple
# ---------------------------------------------------------------------------

def queue_create():
    """Create and return an empty queue."""
    return ()


def queue_enqueue(q, item):
    """Add an item to the rear (back) of the queue.

    Args:
        q:    The queue (a Python tuple).
        item: The element to add.

    Returns:
        The new queue with the item added.
    """
    return q + (item,)


def queue_dequeue(q):
    """Remove and return the front item from the queue.

    Returns (None, q) if the queue is empty.

    Args:
        q: The queue (a Python tuple).

    Returns:
        A tuple of (front_element, new_queue), or (None, q) if empty.
    """
    if queue_is_empty(q):
        print("  [warn] dequeue called on an empty queue")
        return None, q
    return q[0], q[1:]


def queue_peek(q):
    """Return the front item without removing it.

    Returns None if the queue is empty.

    Args:
        q: The queue (a Python tuple).

    Returns:
        The front element, or None if the queue is empty.
    """
    if queue_is_empty(q):
        print("  [warn] peek called on an empty queue")
        return None
    return q[0]


def queue_is_empty(q):
    """Return True if the queue has no elements.

    Args:
        q: The queue (a Python tuple).

    Returns:
        True if the queue is empty, False otherwise.
    """
    return len(q) == 0


def queue_size(q):
    """Return the number of elements in the queue.

    Args:
        q: The queue (a Python tuple).

    Returns:
        The count of items in the queue.
    """
    return len(q)


# ---------------------------------------------------------------------------
# Example 1: Hot-Potato Elimination Game
# ---------------------------------------------------------------------------

def hot_potato(names, num):
    """Simulate the hot-potato elimination game.

    Players stand in a circle. A "potato" is passed around *num* times,
    and the player holding it is eliminated. This repeats until one
    player remains — the winner.

    How it works:
      - Put all player names into the queue.
      - Each round, pass the potato by moving the front player to
        the back, *num* times.
      - The player now at the front is eliminated (dequeued and out).
      - Repeat until only one player is left.

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

    print("  Starting with %d players: %s" % (len(names), names))
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
              % (round_num, eliminated, q))

    # The last player left is the winner
    winner, q = queue_dequeue(q)
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
        job, q = queue_dequeue(q)
        name, pages = job
        order = order + 1
        print("    [PRINT #%d] %s (%d page%s)"
              % (order, name, pages, "s" if pages != 1 else ""))

    print("\n  All %d job(s) completed." % order)


# ---------------------------------------------------------------------------
# __main__ — run examples when this file is executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Queue Examples — Chapter 2 (Simplified)")
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
