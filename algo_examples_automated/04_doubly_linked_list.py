"""
04_doubly_linked_list.py - Doubly Linked List

A doubly linked list extends the singly linked list by giving each
node two pointers: `prev` (to the previous node) and `next` (to the
next node). This enables bidirectional traversal — you can walk the
list forwards or backwards — at the cost of extra memory per node.

Properties:
  - O(1) insertion/deletion at head and tail (with head/tail pointers)
  - O(1) deletion of a known node (unlike singly linked lists)
  - O(n) search / access by index
  - Bidirectional traversal

Topics covered:
  - Node class with prev and next pointers
  - Insert at head and tail
  - Delete by value
  - Forward and backward traversal
  - Edge-case handling (empty list, single node)
"""

from __future__ import annotations
from typing import Any, Optional


class Node:
    """A node in a doubly linked list.

    Attributes:
        data: The value stored in this node.
        prev: Reference to the previous node, or None if this is the head.
        next: Reference to the next node, or None if this is the tail.
    """

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.data!r})"


class DoublyLinkedList:
    """Doubly linked list with head and tail pointers.

    Sentinel-like behaviour: head.prev is always None and tail.next
    is always None for a well-formed list.
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
        """Insert a new node at the front — O(1)."""
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def insert_at_tail(self, data: Any) -> None:
        """Append a new node at the end — O(1)."""
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
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

        # Decide whether to walk from head or tail for efficiency
        if index < self._size // 2:
            current = self.head
            for _ in range(index - 1):
                assert current is not None
                current = current.next
        else:
            current = self.tail
            for _ in range(self._size - index):
                assert current is not None
                current = current.prev

        new_node = Node(data)
        # Splice new_node between current and current.next
        new_node.next = current.next
        new_node.prev = current
        assert current.next is not None
        current.next.prev = new_node
        current.next = new_node
        self._size += 1

    # ------------------------------------------------------------------ #
    #  Deletion
    # ------------------------------------------------------------------ #

    def delete_by_value(self, value: Any) -> bool:
        """Delete the first node containing `value`. Returns True if found. — O(n)."""
        current = self.head
        while current is not None:
            if current.data == value:
                self._unlink(current)
                return True
            current = current.next
        return False

    def _unlink(self, node: Node) -> None:
        """Remove `node` from the list by updating its neighbours' pointers — O(1)."""
        if node.prev is not None:
            node.prev.next = node.next
        else:
            # node is the head
            self.head = node.next

        if node.next is not None:
            node.next.prev = node.prev
        else:
            # node is the tail
            self.tail = node.prev

        self._size -= 1

    def delete_at_head(self) -> Optional[Any]:
        """Remove and return the head's data — O(1). Returns None if empty."""
        if self.is_empty():
            return None
        data = self.head.data
        self._unlink(self.head)
        return data

    def delete_at_tail(self) -> Optional[Any]:
        """Remove and return the tail's data — O(1). Returns None if empty."""
        if self.is_empty():
            return None
        data = self.tail.data
        self._unlink(self.tail)
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
    #  Traversal
    # ------------------------------------------------------------------ #

    def display_forward(self) -> str:
        """Return a forward string representation: head -> ... -> tail -> None."""
        parts: list[str] = []
        current = self.head
        while current is not None:
            parts.append(str(current.data))
            current = current.next
        parts.append("None")
        return " <-> ".join(parts)

    def display_backward(self) -> str:
        """Return a backward string representation: tail -> ... -> head -> None."""
        parts: list[str] = []
        current = self.tail
        while current is not None:
            parts.append(str(current.data))
            current = current.prev
        parts.append("None")
        return " <-> ".join(parts)

    def to_list_forward(self) -> list[Any]:
        """Collect all elements into a standard Python list (head to tail)."""
        result: list[Any] = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def to_list_backward(self) -> list[Any]:
        """Collect all elements into a standard Python list (tail to head)."""
        result: list[Any] = []
        current = self.tail
        while current is not None:
            result.append(current.data)
            current = current.prev
        return result


def main() -> None:
    """Run doubly linked list demonstrations."""
    print("=" * 60)
    print("Chapter 1 — Doubly Linked List")
    print("=" * 60)

    dll = DoublyLinkedList()

    # 1. Insertion
    print("\n--- 1. Insertion ---")
    dll.insert_at_tail(10)
    dll.insert_at_tail(20)
    dll.insert_at_tail(30)
    print(f"After appending 10, 20, 30:")
    print(f"  Forward:  {dll.display_forward()}")
    print(f"  Backward: {dll.display_backward()}")

    dll.insert_at_head(5)
    print(f"After insert_at_head(5):")
    print(f"  Forward:  {dll.display_forward()}")
    print(f"  Backward: {dll.display_backward()}")

    dll.insert_at_index(2, 15)
    print(f"After insert_at_index(2, 15):")
    print(f"  Forward:  {dll.display_forward()}")
    print(f"  Backward: {dll.display_backward()}")

    print(f"  Length: {len(dll)}")

    # 2. Search
    print("\n--- 2. Search ---")
    print(f"  search(15) -> index {dll.search(15)}")
    print(f"  search(99) -> index {dll.search(99)}")
    print(f"  contains(20): {dll.contains(20)}")
    print(f"  contains(77): {dll.contains(77)}")

    # 3. Deletion
    print("\n--- 3. Deletion ---")
    dll.delete_by_value(15)
    print(f"After delete(15):")
    print(f"  Forward:  {dll.display_forward()}")
    print(f"  Backward: {dll.display_backward()}")

    dll.delete_at_head()
    print(f"After delete_at_head():")
    print(f"  Forward:  {dll.display_forward()}")
    print(f"  Backward: {dll.display_backward()}")

    dll.delete_at_tail()
    print(f"After delete_at_tail():")
    print(f"  Forward:  {dll.display_forward()}")
    print(f"  Backward: {dll.display_backward()}")

    dll.delete_by_value(20)
    print(f"After delete(20):")
    print(f"  Forward:  {dll.display_forward()}")
    print(f"  Backward: {dll.display_backward()}")

    print(f"  Length: {len(dll)}")

    # 4. Edge cases
    print("\n--- 4. Edge Cases ---")
    empty_dll = DoublyLinkedList()
    print(f"  Empty list forward:  '{empty_dll.display_forward()}'")
    print(f"  Empty list backward: '{empty_dll.display_backward()}'")
    print(f"  delete_at_head() on empty: {empty_dll.delete_at_head()}")
    print(f"  delete_at_tail() on empty: {empty_dll.delete_at_tail()}")
    print(f"  delete_by_value(1) on empty: {empty_dll.delete_by_value(1)}")

    # Single node
    single = DoublyLinkedList()
    single.insert_at_head(42)
    print(f"  Single node forward:  {single.display_forward()}")
    print(f"  Single node backward: {single.display_backward()}")
    single.delete_by_value(42)
    print(f"  After deleting the only node forward:  '{single.display_forward()}'")

    # 5. to_list conversions
    print("\n--- 5. to_list() Conversions ---")
    print(f"  Forward list:  {dll.to_list_forward()}")
    print(f"  Backward list: {dll.to_list_backward()}")


if __name__ == "__main__":
    main()
