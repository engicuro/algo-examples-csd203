# Deque (Double-Ended Queue) Implementation Examples (Chapter 2) — No-List Version
# ===============================================================
#
# A deque allows insertion and removal at BOTH ends — front and rear.
# This version uses a doubly-linked list instead of Python lists.
# No external libraries.


# ---------------------------------------------------------------------------
# Node class for the doubly-linked-list-based deque
# ---------------------------------------------------------------------------
class _Node:
    """A single node in the doubly linked list used by the deque."""

    def __init__(self, value):
        self.value = value
        self._next = None
        self._prev = None


# ---------------------------------------------------------------------------
# Deque built on a doubly linked list (with head and tail pointers)
# ---------------------------------------------------------------------------

def deque_create():
    """Create and return an empty deque.

    The deque is represented as (head, tail) tuple of node references.
    (None, None) means empty.
    """
    return (None, None)


def deque_add_front(dq, item):
    """Insert an item at the front (left side) of the deque.

    Args:
        dq:   The deque tuple (head, tail).
        item: The element to insert at the front.

    Returns:
        The new deque tuple.
    """
    new_node = _Node(item)
    head, tail = dq

    if head is None:
        return (new_node, new_node)
    else:
        new_node._next = head
        head._prev = new_node
        return (new_node, tail)


def deque_add_rear(dq, item):
    """Insert an item at the rear (right side) of the deque.

    Args:
        dq:   The deque tuple (head, tail).
        item: The element to insert at the rear.

    Returns:
        The new deque tuple.
    """
    new_node = _Node(item)
    head, tail = dq

    if tail is None:
        return (new_node, new_node)
    else:
        tail._next = new_node
        new_node._prev = tail
        return (head, new_node)


def deque_remove_front(dq):
    """Remove and return the front item from the deque.

    Returns (value, new_deque) where new_deque is the deque after removal.
    Returns (None, dq) if the deque is empty.

    Args:
        dq: The deque tuple (head, tail).

    Returns:
        A tuple (front_element, new_deque).
    """
    head, tail = dq
    if deque_is_empty(dq):
        print("  [warn] remove_front called on an empty deque")
        return None, dq

    value = head.value
    new_head = head._next
    if new_head is None:
        return value, (None, None)
    new_head._prev = None
    return value, (new_head, tail)


def deque_remove_rear(dq):
    """Remove and return the rear item from the deque.

    Returns (value, new_deque) where new_deque is the deque after removal.
    Returns (None, dq) if the deque is empty.

    Args:
        dq: The deque tuple (head, tail).

    Returns:
        A tuple (rear_element, new_deque).
    """
    head, tail = dq
    if deque_is_empty(dq):
        print("  [warn] remove_rear called on an empty deque")
        return None, dq

    value = tail.value
    new_tail = tail._prev
    if new_tail is None:
        return value, (None, None)
    new_tail._next = None
    return value, (head, new_tail)


def deque_peek_front(dq):
    """Return the front item without removing it.

    Returns None if the deque is empty.

    Args:
        dq: The deque tuple (head, tail).

    Returns:
        The front element, or None if the deque is empty.
    """
    head, tail = dq
    if deque_is_empty(dq):
        print("  [warn] peek_front called on an empty deque")
        return None
    return head.value


def deque_peek_rear(dq):
    """Return the rear item without removing it.

    Returns None if the deque is empty.

    Args:
        dq: The deque tuple (head, tail).

    Returns:
        The rear element, or None if the deque is empty.
    """
    head, tail = dq
    if deque_is_empty(dq):
        print("  [warn] peek_rear called on an empty deque")
        return None
    return tail.value


def deque_is_empty(dq):
    """Return True if the deque has no elements.

    Args:
        dq: The deque tuple (head, tail).

    Returns:
        True if the deque is empty, False otherwise.
    """
    head, tail = dq
    return head is None


def deque_size(dq):
    """Return the number of elements in the deque.

    Args:
        dq: The deque tuple (head, tail).

    Returns:
        The count of items in the deque.
    """
    head, tail = dq
    count = 0
    current = head
    while current is not None:
        count = count + 1
        current = current._next
    return count


# ---------------------------------------------------------------------------
# Helper: convert deque to a readable string (no list used)
# ---------------------------------------------------------------------------
def _deque_to_string(dq):
    """Build a string representation of the deque without using a list."""
    head, tail = dq
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
# Example 1: Palindrome Checker using a Deque
# ---------------------------------------------------------------------------

def is_palindrome(text):
    """Check whether *text* is a palindrome using a deque.

    Uses a doubly-linked-list-based deque instead of a Python list.

    A palindrome reads the same forwards and backwards.

    Args:
        text: The string to check.

    Returns:
        True if *text* is a palindrome, False otherwise.
    """
    # Step 1: keep only letters and digits, all lowercase
    cleaned = ""
    for ch in text:
        if ch.isalnum():
            cleaned = cleaned + ch.lower()

    dq = deque_create()

    # Step 2: put every character into the deque
    for ch in cleaned:
        dq = deque_add_rear(dq, ch)

    # Step 3: compare characters from both ends
    while deque_size(dq) > 1:
        front_char, dq = deque_remove_front(dq)
        rear_char, dq = deque_remove_rear(dq)
        if front_char != rear_char:
            return False

    return True


# ---------------------------------------------------------------------------
# Example 2: Demonstrate all deque operations
# ---------------------------------------------------------------------------

def demo_deque_operations():
    """Showcase every operation of the deque."""
    dq = deque_create()

    print("  Starting with an empty deque: %s" % _deque_to_string(dq))

    # Add items at the rear
    dq = deque_add_rear(dq, 1)
    dq = deque_add_rear(dq, 2)
    dq = deque_add_rear(dq, 3)
    print("  After add_rear(1, 2, 3): %s" % _deque_to_string(dq))

    # Add items at the front
    dq = deque_add_front(dq, 0)
    dq = deque_add_front(dq, -1)
    print("  After add_front(0, -1):  %s" % _deque_to_string(dq))

    # Peek at both ends
    print("  peek_front() = %s" % deque_peek_front(dq))
    print("  peek_rear()  = %s" % deque_peek_rear(dq))
    print("  size()       = %d" % deque_size(dq))

    # Remove from both ends
    val, dq = deque_remove_front(dq)
    print("  remove_front() = %s  ->  %s" % (val, _deque_to_string(dq)))
    val, dq = deque_remove_rear(dq)
    print("  remove_rear()  = %s  ->  %s" % (val, _deque_to_string(dq)))

    # Remove everything from the front
    print("  Removing all remaining items from the front:")
    while not deque_is_empty(dq):
        val, dq = deque_remove_front(dq)
        print("    remove_front() = %s  ->  %s" % (val, _deque_to_string(dq)))

    print("  Is empty? %s" % deque_is_empty(dq))


# ---------------------------------------------------------------------------
# __main__ — run examples when this file is executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Deque Examples — Chapter 2 (No-List Version)")
    print("=" * 60)

    # --- All operations demo ---
    print("\n--- Deque: All Operations ---")
    demo_deque_operations()

    # --- Example 1: Palindrome Checker ---
    print("\n--- Example 1: Palindrome Checker ---")
    test_cases = (
        "racecar",
        "A man, a plan, a canal: Panama",
        "hello",
        "Was it a car or a cat I saw?",
        "No x in Nixon",
        "Madam, I'm Adam",
    )
    for text in test_cases:
        if is_palindrome(text):
            print("  %-45s -> palindrome" % text)
        else:
            print("  %-45s -> NOT a palindrome" % text)

    # --- Example 2: Using deque as both stack and queue ---
    print("\n--- Example 2: Deque Used as Stack and Queue ---")

    # Use as a stack (push/pop from the rear)
    print("  --- Using deque as a stack (LIFO) ---")
    dq = deque_create()
    for ch in "ABCDE":
        dq = deque_add_rear(dq, ch)
        print("  Push '%s' onto stack -> %s" % (ch, _deque_to_string(dq)))

    print("  Pop from stack (rear):")
    while not deque_is_empty(dq):
        val, dq = deque_remove_rear(dq)
        print("    Popped '%s' -> %s" % (val, _deque_to_string(dq)))

    # Use as a queue (enqueue at rear, dequeue from front)
    print("\n  --- Using deque as a queue (FIFO) ---")
    dq = deque_create()
    for ch in "ABCDE":
        dq = deque_add_rear(dq, ch)
        print("  Enqueue '%s' -> %s" % (ch, _deque_to_string(dq)))

    print("  Dequeue from front:")
    while not deque_is_empty(dq):
        val, dq = deque_remove_front(dq)
        print("    Dequeued '%s' -> %s" % (val, _deque_to_string(dq)))
