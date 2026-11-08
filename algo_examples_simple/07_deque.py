# Deque (Double-Ended Queue) Implementation Examples (Chapter 2)
# ===============================================================
#
# A deque allows insertion and removal at BOTH ends — front and rear.
# This is more flexible than a stack (one end) or a queue (FIFO).
#
# This file uses only plain Python lists — no fancy features,
# no external libraries.


# ---------------------------------------------------------------------------
# Deque built on a plain Python list
# ---------------------------------------------------------------------------

def deque_create():
    """Create and return an empty deque."""
    return []


def deque_add_front(dq, item):
    """Insert an item at the front (left side) of the deque.

    Args:
        dq:   The deque (a Python list).
        item: The element to insert at the front.
    """
    dq.insert(0, item)


def deque_add_rear(dq, item):
    """Insert an item at the rear (right side) of the deque.

    Args:
        dq:   The deque (a Python list).
        item: The element to insert at the rear.
    """
    dq.append(item)


def deque_remove_front(dq):
    """Remove and return the front item from the deque.

    Returns None if the deque is empty.

    Args:
        dq: The deque (a Python list).

    Returns:
        The front element, or None if the deque is empty.
    """
    if deque_is_empty(dq):
        print("  [warn] remove_front called on an empty deque")
        return None
    return dq.pop(0)


def deque_remove_rear(dq):
    """Remove and return the rear item from the deque.

    Returns None if the deque is empty.

    Args:
        dq: The deque (a Python list).

    Returns:
        The rear element, or None if the deque is empty.
    """
    if deque_is_empty(dq):
        print("  [warn] remove_rear called on an empty deque")
        return None
    return dq.pop()


def deque_peek_front(dq):
    """Return the front item without removing it.

    Returns None if the deque is empty.

    Args:
        dq: The deque (a Python list).

    Returns:
        The front element, or None if the deque is empty.
    """
    if deque_is_empty(dq):
        print("  [warn] peek_front called on an empty deque")
        return None
    return dq[0]


def deque_peek_rear(dq):
    """Return the rear item without removing it.

    Returns None if the deque is empty.

    Args:
        dq: The deque (a Python list).

    Returns:
        The rear element, or None if the deque is empty.
    """
    if deque_is_empty(dq):
        print("  [warn] peek_rear called on an empty deque")
        return None
    return dq[-1]


def deque_is_empty(dq):
    """Return True if the deque has no elements.

    Args:
        dq: The deque (a Python list).

    Returns:
        True if the deque is empty, False otherwise.
    """
    return len(dq) == 0


def deque_size(dq):
    """Return the number of elements in the deque.

    Args:
        dq: The deque (a Python list).

    Returns:
        The count of items in the deque.
    """
    return len(dq)


# ---------------------------------------------------------------------------
# Example 1: Palindrome Checker using a Deque
# ---------------------------------------------------------------------------

def is_palindrome(text):
    """Check whether *text* is a palindrome using a deque.

    A palindrome reads the same forwards and backwards.
    For example: "racecar" and "A man, a plan, a canal: Panama".

    How it works:
      1. Remove spaces and punctuation, convert everything to lowercase.
      2. Put every character into the deque.
      3. Repeatedly remove one character from the front AND one from
         the rear, and compare them.
      4. If any pair does not match, it is NOT a palindrome.
      5. If all pairs match, it IS a palindrome.

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
        deque_add_rear(dq, ch)

    # Step 3: compare characters from both ends
    while deque_size(dq) > 1:
        front_char = deque_remove_front(dq)
        rear_char = deque_remove_rear(dq)
        if front_char != rear_char:
            return False

    # If we get here, every pair matched
    return True


# ---------------------------------------------------------------------------
# Example 2: Demonstrate all deque operations
# ---------------------------------------------------------------------------

def demo_deque_operations():
    """Showcase every operation of the deque."""
    dq = deque_create()

    print("  Starting with an empty deque: %s" % dq)

    # Add items at the rear
    deque_add_rear(dq, 1)
    deque_add_rear(dq, 2)
    deque_add_rear(dq, 3)
    print("  After add_rear(1, 2, 3): %s" % dq)

    # Add items at the front
    deque_add_front(dq, 0)
    deque_add_front(dq, -1)
    print("  After add_front(0, -1):  %s" % dq)

    # Peek at both ends
    print("  peek_front() = %s" % deque_peek_front(dq))
    print("  peek_rear()  = %s" % deque_peek_rear(dq))
    print("  size()       = %d" % deque_size(dq))

    # Remove from both ends
    print("  remove_front() = %s  ->  %s" % (deque_remove_front(dq), dq))
    print("  remove_rear()  = %s  ->  %s" % (deque_remove_rear(dq), dq))

    # Remove everything from the front
    print("  Removing all remaining items from the front:")
    while not deque_is_empty(dq):
        item = deque_remove_front(dq)
        print("    remove_front() = %s  ->  %s" % (item, dq))

    print("  Is empty? %s" % deque_is_empty(dq))


# ---------------------------------------------------------------------------
# __main__ — run examples when this file is executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Deque Examples — Chapter 2 (Simplified)")
    print("=" * 60)

    # --- All operations demo ---
    print("\n--- Deque: All Operations ---")
    demo_deque_operations()

    # --- Example 1: Palindrome Checker ---
    print("\n--- Example 1: Palindrome Checker ---")
    test_cases = [
        "racecar",
        "A man, a plan, a canal: Panama",
        "hello",
        "Was it a car or a cat I saw?",
        "No x in Nixon",
        "Madam, I'm Adam",
    ]
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
        deque_add_rear(dq, ch)
        print("  Push '%s' onto stack -> %s" % (ch, dq))

    print("  Pop from stack (rear):")
    while not deque_is_empty(dq):
        item = deque_remove_rear(dq)
        print("    Popped '%s' -> %s" % (item, dq))

    # Use as a queue (enqueue at rear, dequeue from front)
    print("\n  --- Using deque as a queue (FIFO) ---")
    dq = deque_create()
    for ch in "ABCDE":
        deque_add_rear(dq, ch)
        print("  Enqueue '%s' -> %s" % (ch, dq))

    print("  Dequeue from front:")
    while not deque_is_empty(dq):
        item = deque_remove_front(dq)
        print("    Dequeued '%s' -> %s" % (item, dq))
