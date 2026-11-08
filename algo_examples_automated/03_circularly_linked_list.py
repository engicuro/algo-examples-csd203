"""
03_circularly_linked_list.py - Circularly Linked List

A circularly linked list is a variation of a linked list where the
last node's `next` pointer wraps around to the first node (head),
forming a circle. There is no `None` terminator — traversal must
stop when it reaches the starting node again.

Properties:
  - No explicit "end" — any node can serve as a starting point
  - Useful for round-robin scheduling, cyclic buffers, and
    applications that need to cycle through elements repeatedly
  - Insertion at head/tail can be O(1) when a tail pointer is kept

Topics covered:
  - Node class definition
  - Insert at head and tail
  - Delete by value
  - Traversal (with cycle-awareness)
  - Circular detection (Floyd's tortoise-and-hare algorithm)
"""

from __future__ import annotations
from typing import Any, Optional


class Node:
    """A single node in a circularly linked list.

    Attributes:
        data: The value stored in this node.
        next: Reference to the next node; never None in a non-empty list.
    """

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.next: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.data!r})"


class CircularlyLinkedList:
    """Circularly linked list maintained via a tail pointer.

    The tail's `next` always points back to the head, forming the
    circle. When the list is empty, `tail` is None.

    This design lets us access both head (tail.next) and tail
    in O(1) time.
    """

    def __init__(self) -> None:
        self.tail: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        """Return True if the list has no elements."""
        return self.tail is None

    @property
    def head(self) -> Optional[Node]:
        """The head of the list (tail.next), or None if empty."""
        if self.is_empty():
            return None
        return self.tail.next

    # ------------------------------------------------------------------ #
    #  Insertion
    # ------------------------------------------------------------------ #

    def insert_at_head(self, data: Any) -> None:
        """Insert a new node at the front — O(1)."""
        new_node = Node(data)
        if self.is_empty():
            # First node: point to itself
            new_node.next = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.tail.next = new_node  # tail still points to new head
        self._size += 1

    def insert_at_tail(self, data: Any) -> None:
        """Append a new node at the end — O(1)."""
        new_node = Node(data)
        if self.is_empty():
            new_node.next = new_node
            self.tail = new_node
        else:
            new_node.next = self.head      # wrap around to head
            self.tail.next = new_node      # old tail points to new node
            self.tail = new_node           # new node becomes tail
        self._size += 1

    # ------------------------------------------------------------------ #
    #  Deletion
    # ------------------------------------------------------------------ #

    def delete_by_value(self, value: Any) -> bool:
        """Delete the first node containing `value`. Returns True if found. — O(n)."""
        if self.is_empty():
            return False

        # We need to find the node *before* the target to bypass it
        prev = self.tail
        current = self.head
        while True:
            if current.data == value:
                if current == self.head == self.tail:
                    # Single-node list — becomes empty
                    self.tail = None
                elif current == self.head:
                    # Removing head: advance tail's next pointer
                    self.tail.next = current.next
                elif current == self.tail:
                    # Removing tail: update tail to prev
                    prev.next = self.head
                    self.tail = prev
                else:
                    # Removing a middle node
                    prev.next = current.next
                self._size -= 1
                return True

            prev = current
            current = current.next
            if current == self.head:
                break  # full circle — value not found

        return False

    def delete_at_head(self) -> Optional[Any]:
        """Remove and return the head's data — O(1). Returns None if empty."""
        if self.is_empty():
            return None
        head = self.head
        if head == self.tail:
            # Single node
            self.tail = None
        else:
            self.tail.next = head.next
        self._size -= 1
        return head.data

    # ------------------------------------------------------------------ #
    #  Search
    # ------------------------------------------------------------------ #

    def search(self, value: Any) -> int:
        """Return the index of the first occurrence of `value`, or -1. — O(n)."""
        if self.is_empty():
            return -1
        current = self.head
        index = 0
        while True:
            if current.data == value:
                return index
            current = current.next
            index += 1
            if current == self.head:
                break
        return -1

    # ------------------------------------------------------------------ #
    #  Traversal
    # ------------------------------------------------------------------ #

    def display(self) -> str:
        """Return a string representation showing the circular link.

        Example: 10 -> 20 -> 30 -> (back to 10)
        """
        if self.is_empty():
            return "(empty)"
        parts: list[str] = []
        current = self.head
        while True:
            parts.append(str(current.data))
            current = current.next
            if current == self.head:
                break
        parts.append(f"(back to {parts[0]})")
        return " -> ".join(parts)

    def to_list(self) -> list[Any]:
        """Collect all elements into a standard Python list."""
        result: list[Any] = []
        if self.is_empty():
            return result
        current = self.head
        while True:
            result.append(current.data)
            current = current.next
            if current == self.head:
                break
        return result

    # ------------------------------------------------------------------ #
    #  Circular detection (Floyd's algorithm)
    # ------------------------------------------------------------------ #

    @staticmethod
    def has_cycle(head: Optional[Node]) -> bool:
        """Detect if a linked list has a cycle using Floyd's algorithm.

        Uses two pointers moving at different speeds. If they meet,
        a cycle exists. O(n) time, O(1) space.

        Args:
            head: The head node of a (potentially) singly linked list.

        Returns:
            True if a cycle is detected, False otherwise.
        """
        if head is None:
            return False

        slow: Optional[Node] = head
        fast: Optional[Node] = head

        while fast is not None and fast.next is not None:
            slow = slow.next          # move one step
            fast = fast.next.next     # move two steps
            if slow == fast:
                return True  # pointers met — cycle confirmed

        return False  # fast reached the end — no cycle


def main() -> None:
    """Run circularly linked list demonstrations."""
    print("=" * 60)
    print("Chapter 1 — Circularly Linked List")
    print("=" * 60)

    cll = CircularlyLinkedList()

    # 1. Insertion
    print("\n--- 1. Insertion ---")
    cll.insert_at_tail(10)
    cll.insert_at_tail(20)
    cll.insert_at_tail(30)
    print(f"After appending 10, 20, 30: {cll.display()}")
    print(f"  Length: {len(cll)}")

    cll.insert_at_head(5)
    print(f"After insert_at_head(5):     {cll.display()}")

    # 2. Traversal / to_list
    print("\n--- 2. Traversal ---")
    print(f"  to_list(): {cll.to_list()}")

    # 3. Search
    print("\n--- 3. Search ---")
    print(f"  search(20) -> index {cll.search(20)}")
    print(f"  search(99) -> index {cll.search(99)}")

    # 4. Deletion
    print("\n--- 4. Deletion ---")
    cll.delete_by_value(20)
    print(f"After delete(20):            {cll.display()}")

    cll.delete_at_head()
    print(f"After delete_at_head():      {cll.display()}")

    cll.delete_by_value(30)
    print(f"After delete(30):            {cll.display()}")

    print(f"  Length: {len(cll)}")

    # 5. Edge cases
    print("\n--- 5. Edge Cases ---")
    empty_cll = CircularlyLinkedList()
    print(f"  Empty list display: '{empty_cll.display()}'")
    print(f"  delete_at_head() on empty: {empty_cll.delete_at_head()}")
    print(f"  delete_by_value(1) on empty: {empty_cll.delete_by_value(1)}")

    # Single node
    single = CircularlyLinkedList()
    single.insert_at_head(42)
    print(f"  Single node: {single.display()}")
    single.delete_by_value(42)
    print(f"  After deleting the only node: '{single.display()}'")

    # 6. Circular detection
    print("\n--- 6. Circular Detection (Floyd's Algorithm) ---")

    # Build a normal (non-circular) linked list for testing
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    node_a.next = node_b
    node_b.next = node_c
    # node_c.next is None — no cycle
    print(f"  Linear list A->B->C->None has cycle: {CircularlyLinkedList.has_cycle(node_a)}")

    # Create a cycle: C -> B (not back to A)
    node_c.next = node_b
    print(f"  List A->B->C->B->... has cycle:    {CircularlyLinkedList.has_cycle(node_a)}")

    # Verify our own circular list is circular too
    # (tail.next points to head, so it has a cycle)
    print(f"  Our circular list has cycle:        {CircularlyLinkedList.has_cycle(cll.head)}")


if __name__ == "__main__":
    main()
