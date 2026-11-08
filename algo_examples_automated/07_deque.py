"""
Deque (Double-Ended Queue) Implementation Examples (Chapter 2)
==============================================================

A deque (pronounced "deck") allows insertion and removal at both ends —
front and rear — in O(1) time. This file demonstrates:
  1. Deque using collections.deque (the standard library implementation)
  2. Operations at both ends: append, appendleft, pop, popleft
  3. Examples: palindrome checker and sliding-window maximum
"""

from collections import deque


# ---------------------------------------------------------------------------
# Deque using collections.deque
# ---------------------------------------------------------------------------
class Deque:
    """Double-ended queue backed by collections.deque."""

    def __init__(self) -> None:
        """Initialize an empty deque."""
        self._items: deque = deque()

    def add_front(self, item) -> None:
        """Insert an item at the front (left side) of the deque."""
        self._items.appendleft(item)

    def add_rear(self, item) -> None:
        """Insert an item at the rear (right side) of the deque."""
        self._items.append(item)

    def remove_front(self):
        """Remove and return the front item.

        Raises:
            IndexError: If the deque is empty.
        """
        if self.is_empty():
            raise IndexError("remove_front from an empty deque")
        return self._items.popleft()

    def remove_rear(self):
        """Remove and return the rear item.

        Raises:
            IndexError: If the deque is empty.
        """
        if self.is_empty():
            raise IndexError("remove_rear from an empty deque")
        return self._items.pop()

    def peek_front(self):
        """Return the front item without removing it.

        Raises:
            IndexError: If the deque is empty.
        """
        if self.is_empty():
            raise IndexError("peek_front from an empty deque")
        return self._items[0]

    def peek_rear(self):
        """Return the rear item without removing it.

        Raises:
            IndexError: If the deque is empty.
        """
        if self.is_empty():
            raise IndexError("peek_rear from an empty deque")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the deque has no elements."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of elements in the deque."""
        return len(self._items)

    def __repr__(self) -> str:
        return f"Deque({list(self._items)})"


# ---------------------------------------------------------------------------
# Example 1: Palindrome Checker using a Deque
# ---------------------------------------------------------------------------
def is_palindrome(text: str) -> bool:
    """Check whether *text* is a palindrome using a deque.

    The algorithm:
      1. Strip non-alphanumeric characters and convert to lowercase.
      2. Push every character onto a deque.
      3. Repeatedly remove from both ends and compare.

    Args:
        text: The string to check.

    Returns:
        True if *text* reads the same forwards and backwards.
    """
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    d = Deque()

    for ch in cleaned:
        d.add_rear(ch)

    while d.size() > 1:
        front = d.remove_front()
        rear = d.remove_rear()
        if front != rear:
            return False

    return True


# ---------------------------------------------------------------------------
# Example 2: Sliding-Window Maximum
# ---------------------------------------------------------------------------
def sliding_window_maximum(nums: list[int], k: int) -> list[int]:
    """Return the maximum value in each sliding window of size *k*.

    Uses a deque to store indices of elements in decreasing order of value.
    The front of the deque always holds the index of the current window's
    maximum.

    Args:
        nums: List of integers.
        k:    Window size (1 <= k <= len(nums)).

    Returns:
        A list of maximums, one per window position.

    Time complexity: O(n) — each element is added and removed at most once.
    """
    if not nums or k <= 0:
        return []
    if k == 1:
        return nums[:]

    d = Deque()  # stores indices
    result: list[int] = []

    for i, val in enumerate(nums):
        # Remove indices that are outside the current window
        while not d.is_empty() and d.peek_front() < i - k + 1:
            d.remove_front()

        # Remove indices whose corresponding values are smaller than val
        # (they can never be the maximum for any future window)
        while not d.is_empty() and nums[d.peek_rear()] < val:
            d.remove_rear()

        d.add_rear(i)

        # The front of the deque is the max of the current window
        if i >= k - 1:
            result.append(nums[d.peek_front()])

    return result


# ---------------------------------------------------------------------------
# Example 3: Demonstrating all deque operations at both ends
# ---------------------------------------------------------------------------
def demo_operations() -> None:
    """Showcase every operation of the Deque class."""
    d = Deque()

    print("  Starting empty:", d)

    d.add_rear(1)
    d.add_rear(2)
    d.add_rear(3)
    print("  After add_rear(1,2,3):", d)

    d.add_front(0)
    d.add_front(-1)
    print("  After add_front(0, -1):", d)

    print(f"  peek_front() = {d.peek_front()}")
    print(f"  peek_rear()  = {d.peek_rear()}")
    print(f"  size()       = {d.size()}")

    print(f"  remove_front() = {d.remove_front()}  -> {d}")
    print(f"  remove_rear()  = {d.remove_rear()}   -> {d}")

    while not d.is_empty():
        print(f"  remove_front() = {d.remove_front()}  -> {d}")

    print(f"  Is empty? {d.is_empty()}")


# ---------------------------------------------------------------------------
# __main__ block — run examples when executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Deque Examples — Chapter 2")
    print("=" * 60)

    # --- All operations demo ---
    print("\n--- Deque: all operations ---")
    demo_operations()

    # --- Example 1: Palindrome Checker ---
    print("\n--- Example 1: Palindrome Checker ---")
    test_cases = [
        "racecar",
        "A man, a plan, a canal: Panama",
        "hello",
        "Was it a car or a cat I saw?",
        "No 'x' in Nixon",
        "Madam, I'm Adam",
    ]
    for text in test_cases:
        result = "palindrome" if is_palindrome(text) else "NOT a palindrome"
        print(f"  {text!r:45s} -> {result}")

    # --- Example 2: Sliding Window Maximum ---
    print("\n--- Example 2: Sliding Window Maximum ---")
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(f"  Array: {nums}")
    print(f"  Window size k = {k}")
    result = sliding_window_maximum(nums, k)
    print(f"  Sliding-window maximums: {result}")
    # Expected: [3, 3, 5, 5, 6, 7]

    # --- Edge cases ---
    print("\n--- Edge cases ---")
    print(f"  sliding_window_maximum([], 3) = {sliding_window_maximum([], 3)}")
    print(f"  sliding_window_maximum([5], 1) = {sliding_window_maximum([5], 1)}")
    print(f"  sliding_window_maximum([4, 2], 2) = {sliding_window_maximum([4, 2], 2)}")
