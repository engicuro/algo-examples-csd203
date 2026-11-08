# Priority Queue Implementation Examples (Chapter 2)
# ===================================================
#
# A priority queue is a data structure where each element has a
# priority. Elements are removed in priority order — the highest
# priority item comes out first.
#
# In this file, "higher priority number" means "comes out first"
# (a max-priority queue).
#
# This file uses tuples instead of Python lists — no lists,
# no heapq, no external libraries.


# ---------------------------------------------------------------------------
# Priority Queue built on a Python tuple
# ---------------------------------------------------------------------------

def pq_create():
    """Create and return an empty priority queue.

    The priority queue is stored as a tuple of (item, priority) tuples.
    """
    return ()


def pq_push(pq, item, priority):
    """Add an item with the given priority.

    We insert the item in sorted order so that the highest-priority
    item is always at the front of the tuple.

    How insertion works:
      - Walk through the tuple to find the right position.
      - Insert the new item there so the tuple stays sorted by
        priority (highest first).

    Args:
        pq:       The priority queue (a Python tuple of tuples).
        item:     The element to store.
        priority: The priority — higher number = higher priority.

    Returns:
        The new priority queue with the item inserted.
    """
    new_entry = (item, priority)

    # Find the correct position to keep the tuple sorted
    # (highest priority first)
    new_pq = ()
    inserted = False
    for i in range(len(pq)):
        # If the new item has higher priority than the item at index i,
        # insert it before that item
        if not inserted and priority > pq[i][1]:
            new_pq = new_pq + (new_entry,)
            inserted = True
        new_pq = new_pq + (pq[i],)

    # If we did not insert anywhere, the new item has the lowest
    # priority — put it at the end
    if not inserted:
        new_pq = new_pq + (new_entry,)

    return new_pq


def pq_pop(pq):
    """Remove and return the highest-priority item.

    Since the tuple is sorted with the highest priority first,
    we simply remove and return the first element.

    Returns (None, pq) if the priority queue is empty.

    Args:
        pq: The priority queue (a Python tuple of tuples).

    Returns:
        A tuple of ((item, priority), new_queue), or (None, pq) if empty.
    """
    if pq_is_empty(pq):
        print("  [warn] pop called on an empty priority queue")
        return None, pq
    return pq[0], pq[1:]


def pq_peek(pq):
    """Return the highest-priority item without removing it.

    Returns None if the priority queue is empty.

    Args:
        pq: The priority queue (a Python tuple of tuples).

    Returns:
        The (item, priority) tuple of the highest-priority element,
        or None if the queue is empty.
    """
    if pq_is_empty(pq):
        print("  [warn] peek called on an empty priority queue")
        return None
    return pq[0]


def pq_is_empty(pq):
    """Return True if the priority queue has no elements.

    Args:
        pq: The priority queue (a Python tuple of tuples).

    Returns:
        True if the queue is empty, False otherwise.
    """
    return len(pq) == 0


def pq_size(pq):
    """Return the number of elements in the priority queue.

    Args:
        pq: The priority queue (a Python tuple of tuples).

    Returns:
        The count of items in the priority queue.
    """
    return len(pq)


# ---------------------------------------------------------------------------
# Alternative: Simple version that scans for the minimum on every pop
# ---------------------------------------------------------------------------

def pq_push_simple(pq, item, priority):
    """Add an item to the priority queue (simple version).

    Unlike the sorted version above, we just append to the end.
    On pop, we scan the whole tuple to find the highest-priority item.

    This is simpler to understand but slower for large queues.

    Args:
        pq:       The priority queue (a Python tuple of tuples).
        item:     The element to store.
        priority: The priority — higher number = higher priority.

    Returns:
        The new priority queue with the item appended.
    """
    return pq + ((item, priority),)


def pq_pop_simple(pq):
    """Remove and return the highest-priority item (simple scan version).

    How it works:
      - Walk through the entire tuple to find the entry with the
        highest priority.
      - Remove that entry and return it.

    Returns (None, pq) if the priority queue is empty.

    Args:
        pq: The priority queue (a Python tuple of tuples).

    Returns:
        A tuple of ((item, priority), new_queue), or (None, pq) if empty.
    """
    if pq_is_empty(pq):
        print("  [warn] pop called on an empty priority queue")
        return None, pq

    # Find the index of the entry with the highest priority
    best_index = 0
    best_priority = pq[0][1]

    for i in range(1, len(pq)):
        if pq[i][1] > best_priority:
            best_index = i
            best_priority = pq[i][1]

    # Rebuild the tuple without the best entry
    new_pq = pq[:best_index] + pq[best_index + 1:]
    return pq[best_index], new_pq


# ---------------------------------------------------------------------------
# Example 1: Task Scheduler
# ---------------------------------------------------------------------------

def task_scheduler():
    """Demonstrate a priority-based task scheduler.

    Tasks with higher priority numbers are executed first.
    """
    pq = pq_create()

    # Submit tasks with various priorities
    pq = pq_push(pq, "Write report", 3)
    pq = pq_push(pq, "Fix critical bug", 1)
    pq = pq_push(pq, "Reply to emails", 4)
    pq = pq_push(pq, "Code review", 2)
    pq = pq_push(pq, "Update documentation", 5)

    print("  Tasks submitted (higher number = higher priority):")
    print("  Queue size: %d\n" % pq_size(pq))

    print("  Executing tasks in priority order:")
    order = 0
    while not pq_is_empty(pq):
        task, pq = pq_pop(pq)
        priority = task[1]
        task = task[0]
        order = order + 1
        print("    %d. [priority=%d] %s" % (order, priority, task))


# ---------------------------------------------------------------------------
# Example 2: Emergency Room Triage Simulation
# ---------------------------------------------------------------------------

def er_triage_demo():
    """Simulate an emergency room where patients are seen by priority.

    Each patient has a name and a triage level:
      5 = most urgent (life-threatening)
      1 = least urgent (minor issue)
    """
    pq = pq_create()

    print("  Patients arriving at the emergency room:")
    pq = pq_push(pq, "Alice", 3)   # moderate
    pq = pq_push(pq, "Bob", 5)     # critical
    pq = pq_push(pq, "Charlie", 1) # minor
    pq = pq_push(pq, "Diana", 4)   # serious
    pq = pq_push(pq, "Eve", 2)     # mild

    print("  Patients in queue: %d\n" % pq_size(pq))

    print("  Treating patients in priority order:")
    order = 0
    while not pq_is_empty(pq):
        entry, pq = pq_pop(pq)
        patient = entry[0]
        priority = entry[1]
        order = order + 1
        urgency = ""
        if priority == 5:
            urgency = "CRITICAL"
        elif priority == 4:
            urgency = "serious"
        elif priority == 3:
            urgency = "moderate"
        elif priority == 2:
            urgency = "mild"
        else:
            urgency = "minor"
        print("    %d. Treat %s (priority=%d, %s)"
              % (order, patient, priority, urgency))


# ---------------------------------------------------------------------------
# Example 3: Compare sorted-insert vs scan-on-pop approaches
# ---------------------------------------------------------------------------

def compare_two_approaches():
    """Show that both priority queue approaches give the same results."""
    print("  --- Sorted-insert approach (push is slow, pop is fast) ---")
    pq1 = pq_create()
    pq1 = pq_push(pq1, "task_a", 5)
    pq1 = pq_push(pq1, "task_b", 1)
    pq1 = pq_push(pq1, "task_c", 3)
    pq1 = pq_push(pq1, "task_d", 2)
    pq1 = pq_push(pq1, "task_e", 4)

    print("  Queue after inserts: %s" % (pq1,))
    print("  Popping in priority order:")
    while not pq_is_empty(pq1):
        entry, pq1 = pq_pop(pq1)
        print("    [priority=%d] %s" % (entry[1], entry[0]))

    print("\n  --- Scan-on-pop approach (push is fast, pop is slow) ---")
    pq2 = pq_create()
    pq2 = pq_push_simple(pq2, "task_a", 5)
    pq2 = pq_push_simple(pq2, "task_b", 1)
    pq2 = pq_push_simple(pq2, "task_c", 3)
    pq2 = pq_push_simple(pq2, "task_d", 2)
    pq2 = pq_push_simple(pq2, "task_e", 4)

    print("  Queue after inserts: %s" % (pq2,))
    print("  Popping in priority order:")
    while not pq_is_empty(pq2):
        entry, pq2 = pq_pop_simple(pq2)
        print("    [priority=%d] %s" % (entry[1], entry[0]))


# ---------------------------------------------------------------------------
# __main__ — run examples when this file is executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Priority Queue Examples — Chapter 2 (Simplified)")
    print("=" * 60)

    # --- Basic priority queue operations ---
    print("\n--- Basic Priority Queue Operations ---")
    pq = pq_create()
    print("Created an empty priority queue.")
    print("Is empty? %s" % pq_is_empty(pq))

    # Push some items
    pq = pq_push(pq, "task_a", 5)
    pq = pq_push(pq, "task_b", 1)
    pq = pq_push(pq, "task_c", 3)
    print("After pushing 3 items: %s" % (pq,))
    print("Peek at highest priority: %s" % (str(pq_peek(pq)),))
    print("Queue size: %d" % pq_size(pq))

    # Pop everything
    print("Popping all items in priority order:")
    while not pq_is_empty(pq):
        entry, pq = pq_pop(pq)
        print("  Popped %s (priority=%d)" % (entry[0], entry[1]))

    # --- Example 1: Task Scheduler ---
    print("\n--- Example 1: Task Scheduler ---")
    task_scheduler()

    # --- Example 2: Emergency Room Triage ---
    print("\n--- Example 2: Emergency Room Triage ---")
    er_triage_demo()

    # --- Example 3: Compare both approaches ---
    print("\n--- Example 3: Compare Sorted-Insert vs Scan-on-Pop ---")
    compare_two_approaches()
