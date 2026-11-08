# Priority Queue Implementation Examples (Chapter 2) — No-List Version
# ===================================================
#
# A priority queue is a data structure where each element has a
# priority. Elements are removed in priority order.
# This version uses a linked list instead of Python lists.
# No heapq, no fancy features, no external libraries.


# ---------------------------------------------------------------------------
# Node class for the linked-list-based priority queue
# ---------------------------------------------------------------------------
class _Node:
    """A single node in the linked list used by the priority queue."""

    def __init__(self, item, priority):
        self.item = item
        self.priority = priority
        self._next = None


# ---------------------------------------------------------------------------
# Priority Queue built on a sorted linked list
# ---------------------------------------------------------------------------

def pq_create():
    """Create and return an empty priority queue.

    The priority queue is represented by its head node (None means empty).
    """
    return None


def pq_push(pq, item, priority):
    """Add an item with the given priority.

    We insert the node in sorted order so that the highest-priority
    item is always at the front of the list.

    Args:
        pq:       The priority queue (head node reference, or None).
        item:     The element to store.
        priority: The priority — higher number = higher priority.

    Returns:
        The new head node of the priority queue.
    """
    new_node = _Node(item, priority)

    # If the queue is empty or the new node has the highest priority
    if pq is None or priority > pq.priority:
        new_node._next = pq
        return new_node

    # Walk through the list to find the correct position
    current = pq
    while current._next is not None and current._next.priority >= priority:
        current = current._next

    # Insert the new node after current
    new_node._next = current._next
    current._next = new_node

    return pq


def pq_pop(pq):
    """Remove and return the highest-priority item.

    Since the list is sorted with the highest priority first,
    we simply remove the head node.

    Returns (item, priority, new_pq) where new_pq is the queue after removal.
    Returns (None, None, pq) if the priority queue is empty.

    Args:
        pq: The priority queue (head node reference, or None).

    Returns:
        A tuple (item, priority, new_pq).
    """
    if pq_is_empty(pq):
        print("  [warn] pop called on an empty priority queue")
        return None, None, pq

    return pq.item, pq.priority, pq._next


def pq_peek(pq):
    """Return the highest-priority item without removing it.

    Returns None if the priority queue is empty.

    Args:
        pq: The priority queue (head node reference, or None).

    Returns:
        The (item, priority) tuple of the highest-priority element,
        or None if the queue is empty.
    """
    if pq_is_empty(pq):
        print("  [warn] peek called on an empty priority queue")
        return None
    return (pq.item, pq.priority)


def pq_is_empty(pq):
    """Return True if the priority queue has no elements.

    Args:
        pq: The priority queue (head node reference, or None).

    Returns:
        True if the queue is empty, False otherwise.
    """
    return pq is None


def pq_size(pq):
    """Return the number of elements in the priority queue.

    Args:
        pq: The priority queue (head node reference, or None).

    Returns:
        The count of items in the priority queue.
    """
    count = 0
    current = pq
    while current is not None:
        count = count + 1
        current = current._next
    return count


# ---------------------------------------------------------------------------
# Alternative: Simple version that scans for the minimum on every pop
# ---------------------------------------------------------------------------

def pq_push_simple(pq, item, priority):
    """Add an item to the priority queue (simple version).

    Unlike the sorted version above, we just append to the end.
    On pop, we scan the whole list to find the highest-priority item.

    Args:
        pq:       The priority queue (head node reference, or None).
        item:     The element to store.
        priority: The priority — higher number = higher priority.

    Returns:
        The new head node of the priority queue.
    """
    new_node = _Node(item, priority)

    if pq is None:
        return new_node

    # Append to the end
    current = pq
    while current._next is not None:
        current = current._next
    current._next = new_node

    return pq


def pq_pop_simple(pq):
    """Remove and return the highest-priority item (simple scan version).

    How it works:
      - Walk through the entire list to find the entry with the
        highest priority.
      - Remove that entry and return it.

    Returns (item, priority, new_pq) where new_pq is the queue after removal.
    Returns (None, None, pq) if the priority queue is empty.

    Args:
        pq: The priority queue (head node reference, or None).

    Returns:
        A tuple (item, priority, new_pq).
    """
    if pq_is_empty(pq):
        print("  [warn] pop called on an empty priority queue")
        return None, None, pq

    # Find the node with the highest priority
    # We track the previous node so we can remove it
    best_node = pq
    best_prev = None
    current = pq
    prev = None

    while current is not None:
        if current.priority > best_node.priority:
            best_node = current
            best_prev = prev
        prev = current
        current = current._next

    # Remove best_node from the list
    if best_prev is None:
        # Best node is the head
        new_pq = pq._next
    else:
        best_prev._next = best_node._next
        new_pq = pq

    return best_node.item, best_node.priority, new_pq


# ---------------------------------------------------------------------------
# Helper: convert priority queue to a readable string (no list used)
# ---------------------------------------------------------------------------
def _pq_to_string(pq):
    """Build a string representation of the priority queue without using a list."""
    if pq is None:
        return "[]"
    parts = ""
    current = pq
    first = True
    while current is not None:
        if not first:
            parts = parts + ", "
        parts = parts + "(" + str(current.item) + ", " + str(current.priority) + ")"
        first = False
        current = current._next
    return "[" + parts + "]"


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
        task, priority, pq = pq_pop(pq)
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
    pq = pq_push(pq, "Alice", 3)
    pq = pq_push(pq, "Bob", 5)
    pq = pq_push(pq, "Charlie", 1)
    pq = pq_push(pq, "Diana", 4)
    pq = pq_push(pq, "Eve", 2)

    print("  Patients in queue: %d\n" % pq_size(pq))

    print("  Treating patients in priority order:")
    order = 0
    while not pq_is_empty(pq):
        patient, priority, pq = pq_pop(pq)
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

    print("  Queue after inserts: %s" % _pq_to_string(pq1))
    print("  Popping in priority order:")
    while not pq_is_empty(pq1):
        item, priority, pq1 = pq_pop(pq1)
        print("    [priority=%d] %s" % (priority, item))

    print("\n  --- Scan-on-pop approach (push is fast, pop is slow) ---")
    pq2 = pq_create()
    pq2 = pq_push_simple(pq2, "task_a", 5)
    pq2 = pq_push_simple(pq2, "task_b", 1)
    pq2 = pq_push_simple(pq2, "task_c", 3)
    pq2 = pq_push_simple(pq2, "task_d", 2)
    pq2 = pq_push_simple(pq2, "task_e", 4)

    print("  Queue after inserts: %s" % _pq_to_string(pq2))
    print("  Popping in priority order:")
    while not pq_is_empty(pq2):
        item, priority, pq2 = pq_pop_simple(pq2)
        print("    [priority=%d] %s" % (priority, item))


# ---------------------------------------------------------------------------
# __main__ — run examples when this file is executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Priority Queue Examples — Chapter 2 (No-List Version)")
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
    print("After pushing 3 items: %s" % _pq_to_string(pq))
    print("Peek at highest priority: %s" % str(pq_peek(pq)))
    print("Queue size: %d" % pq_size(pq))

    # Pop everything
    print("Popping all items in priority order:")
    while not pq_is_empty(pq):
        item, priority, pq = pq_pop(pq)
        print("  Popped %s (priority=%d)" % (item, priority))

    # --- Example 1: Task Scheduler ---
    print("\n--- Example 1: Task Scheduler ---")
    task_scheduler()

    # --- Example 2: Emergency Room Triage ---
    print("\n--- Example 2: Emergency Room Triage ---")
    er_triage_demo()

    # --- Example 3: Compare both approaches ---
    print("\n--- Example 3: Compare Sorted-Insert vs Scan-on-Pop ---")
    compare_two_approaches()
