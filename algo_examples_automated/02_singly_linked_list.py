"""
02_singly_linked_list.py - Singly Linked List

A singly linked list is a linear data structure where each element
(node) stores a reference (pointer) to the next node in sequence.
Unlike arrays, linked list nodes are not stored contiguously in
memory — they are scattered and linked via pointers.

Properties:
  - O(1) insertion at head
  - O(n) search / access by index
  - O(1) insertion at tail (if tail pointer is maintained)
  - O(n) deletion by value

Topics covered:
  - Node class definition
  - Insert at head and tail
  - Delete by value
  - Search
  - Display / string representation
  - Reverse (in-place)
"""

from __future__ import annotations
from typing import Any, Optional


class Node:
    """A single node in a singly linked list.

    Attributes:
        data: The value stored in this node.
        next: Reference to the next node, or None if this is the tail.
    """

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.next: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.data!r})"


class SinglyLinkedList:
    """Singly linked list with head and tail pointers.

    Maintaining a tail pointer allows O(1) append at the end.
    """

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        """Return True if the list has no elements."""
        return self.head is None

    # ------------------------------------------------------------------ #
    #  Insertion
    # ------------------------------------------------------------------ #

    def insert_at_head(self, data: Any) -> None:
        """Insert a new node at the front of the list — O(1)."""
        new_node = Node(data)
        if self.is_empty():
            # First node: both head and tail point to it
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self._size += 1

    def insert_at_tail(self, data: Any) -> None:
        """Append a new node at the end of the list — O(1) with tail."""
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            assert self.tail is not None
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def insert_at_index(self, index: int, data: Any) -> None:
        """Insert at a specific 0-based index — O(n).

        Raises IndexError if index is out of bounds.
        """
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range for list of size {self._size}")
        if index == 0:
            self.insert_at_head(data)
            return
        if index == self._size:
            self.insert_at_tail(data)
            return

        # Traverse to the node just before the insertion point
        current = self.head
        for _ in range(index - 1):
            assert current is not None
            current = current.next

        new_node = Node(data)
        new_node.next = current.next
        current.next = new_node
        self._size += 1

    # ------------------------------------------------------------------ #
    #  Deletion
    # ------------------------------------------------------------------ #

    def delete_by_value(self, value: Any) -> bool:
        """Delete the first node containing `value`. Returns True if found. — O(n)."""
        if self.is_empty():
            return False

        # Special case: the head holds the value
        if self.head.data == value:
            self.head = self.head.next
            self._size -= 1
            if self.is_empty():
                self.tail = None
            return True

        # Walk the list looking for the node *before* the target
        current = self.head
        while current.next is not None:
            if current.next.data == value:
                # Bypass the target node
                current.next = current.next.next
                self._size -= 1
                # If we removed the tail, update tail
                if current.next is None:
                    self.tail = current
                return True
            current = current.next

        return False  # value not found

    def delete_at_head(self) -> Optional[Any]:
        """Remove and return the head's data — O(1). Returns None if empty."""
        if self.is_empty():
            return None
        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        if self.is_empty():
            self.tail = None
        return data

    # ------------------------------------------------------------------ #
    #  Search
    # ------------------------------------------------------------------ #

    def search(self, value: Any) -> int:
        """Return the index of the first occurrence of `value`, or -1. — O(n)."""
        current = self.head
        index = 0
        while current is not None:
            if current.data == value:
                return index
            current = current.next
            index += 1
        return -1

    def contains(self, value: Any) -> bool:
        """Return True if `value` exists in the list."""
        return self.search(value) != -1

    # ------------------------------------------------------------------ #
    #  Display
    # ------------------------------------------------------------------ #

    def display(self) -> str:
        """Return a string representation of the list.

        Example: 10 -> 20 -> 30 -> None
        """
        parts: list[str] = []
        current = self.head
        while current is not None:
            parts.append(str(current.data))
            current = current.next
        parts.append("None")
        return " -> ".join(parts)

    # ------------------------------------------------------------------ #
    #  Reverse (in-place)
    # ------------------------------------------------------------------ #

    def reverse(self) -> None:
        """Reverse the list in-place by flipping every next pointer — O(n).

        After reversal, update head and tail accordingly.
        """
        prev: Optional[Node] = None
        current = self.head
        self.tail = self.head  # old head becomes new tail
        while current is not None:
            next_node = current.next   # save next
            current.next = prev        # reverse the link
            prev = current
            current = next_node
        self.head = prev  # last non-None node becomes new head

    # ------------------------------------------------------------------ #
    #  To Python list (convenience)
    # ------------------------------------------------------------------ #

    def to_list(self) -> list[Any]:
        """Collect all elements into a standard Python list."""
        result: list[Any] = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result


def main() -> None:
    """Run singly linked list demonstrations."""
    print("=" * 60)
    print("Chapter 1 — Singly Linked List")
    print("=" * 60)

    sll = SinglyLinkedList()

    # 1. Insertion
    print("\n--- 1. Insertion ---")
    sll.insert_at_tail(10)
    sll.insert_at_tail(20)
    sll.insert_at_tail(30)
    print(f"After appending 10, 20, 30: {sll.display()}")

    sll.insert_at_head(5)
    print(f"After insert_at_head(5):     {sll.display()}")

    sll.insert_at_index(2, 15)
    print(f"After insert_at_index(2,15): {sll.display()}")

    print(f"  Length: {len(sll)}")

    # 2. Search
    print("\n--- 2. Search ---")
    print(f"  search(15) -> index {sll.search(15)}")
    print(f"  search(99) -> index {sll.search(99)}")
    print(f"  contains(20): {sll.contains(20)}")
    print(f"  contains(77): {sll.contains(77)}")

    # 3. Deletion
    print("\n--- 3. Deletion ---")
    sll.delete_by_value(15)
    print(f"After delete(15):            {sll.display()}")

    sll.delete_at_head()
    print(f"After delete_at_head():      {sll.display()}")

    sll.delete_by_value(30)
    print(f"After delete(30):            {sll.display()}")

    print(f"  Length: {len(sll)}")

    # 4. Reverse
    print("\n--- 4. Reverse ---")
    print(f"  Before reverse: {sll.display()}")
    sll.reverse()
    print(f"  After  reverse: {sll.display()}")

    # 5. Edge cases
    print("\n--- 5. Edge Cases ---")
    empty_list = SinglyLinkedList()
    print(f"  Empty list display: '{empty_list.display()}'")
    print(f"  delete_at_head() on empty: {empty_list.delete_at_head()}")
    print(f"  delete_by_value(1) on empty: {empty_list.delete_by_value(1)}")

    # 6. to_list conversion
    print("\n--- 6. to_list() ---")
    print(f"  sll.to_list(): {sll.to_list()}")


if __name__ == "__main__":
    main()
