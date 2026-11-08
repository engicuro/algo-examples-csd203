# Chapter 1: Doubly Linked List
# Each node stores a value, a pointer to the next node, AND a pointer
# to the previous node. This allows traversal in both directions.

from _structures import LinkedList


class Node:
    """A single node in a doubly linked list.

    Each node holds a value, a pointer to the next node, and a pointer
    to the previous node. The first node's prev is None and the last
    node's next is None.
    """

    def __init__(self, value):
        self.value = value  # the data stored in this node
        self.next = None    # pointer to the next node (None if last)
        self.prev = None    # pointer to the previous node (None if first)


class DoublyLinkedList:
    """A doubly linked list that tracks both head and tail."""

    def __init__(self):
        self.head = None  # first node in the list
        self.tail = None  # last node in the list

    def insert_at_head(self, value):
        """Insert a new node at the beginning of the list."""
        new_node = Node(value)

        if self.head is None:
            # List is empty: new node is both head and tail
            self.head = new_node
            self.tail = new_node
        else:
            # Link the new node to the old head
            new_node.next = self.head
            self.head.prev = new_node
            # Update head to be the new node
            self.head = new_node

    def insert_at_tail(self, value):
        """Insert a new node at the end of the list."""
        new_node = Node(value)

        if self.tail is None:
            # List is empty: new node is both head and tail
            self.head = new_node
            self.tail = new_node
        else:
            # Link the old tail to the new node
            self.tail.next = new_node
            new_node.prev = self.tail
            # Update tail to be the new node
            self.tail = new_node

    def delete_by_value(self, value):
        """Delete the first node that contains the given value."""
        if self.head is None:
            print("List is empty. Nothing to delete.")
            return

        # Start at the head and walk forward
        current = self.head
        while current is not None:
            if current.value == value:
                # Case 1: deleting the only node in the list
                if current == self.head and current == self.tail:
                    self.head = None
                    self.tail = None

                # Case 2: deleting the head node
                elif current == self.head:
                    self.head = self.head.next
                    self.head.prev = None

                # Case 3: deleting the tail node
                elif current == self.tail:
                    self.tail = self.tail.prev
                    self.tail.next = None

                # Case 4: deleting a node in the middle
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev

                return

            current = current.next

        print(value, "not found in the list.")

    def traverse_forward(self):
        """Print all values from head to tail."""
        elements = LinkedList()
        current = self.head
        while current is not None:
            elements.append(str(current.value))
            current = current.next
        # Build the display string by iterating the LinkedList
        parts = []
        for val in elements:
            parts.append(val)
        print("Forward:  " + " <-> ".join(parts) + " -> None")

    def traverse_backward(self):
        """Print all values from tail to head."""
        elements = LinkedList()
        current = self.tail
        while current is not None:
            elements.append(str(current.value))
            current = current.prev
        # Build the display string by iterating the LinkedList
        parts = []
        for val in elements:
            parts.append(val)
        print("Backward: None <- " + " <-> ".join(parts))


def main():
    print("=" * 50)
    print("Chapter 1: Doubly Linked List")
    print("=" * 50)

    dll = DoublyLinkedList()

    # Insert at tail
    print("\n--- Insert at Tail ---")
    dll.insert_at_tail(10)
    dll.insert_at_tail(20)
    dll.insert_at_tail(30)
    print("After inserting 10, 20, 30 at tail:")
    dll.traverse_forward()
    dll.traverse_backward()

    # Insert at head
    print("\n--- Insert at Head ---")
    dll.insert_at_head(5)
    dll.insert_at_head(1)
    print("After inserting 5 and 1 at head:")
    dll.traverse_forward()
    dll.traverse_backward()

    # Delete from the middle
    print("\n--- Delete (Middle) ---")
    print("Before delete:")
    dll.traverse_forward()

    dll.delete_by_value(20)
    print("After deleting 20 (middle):")
    dll.traverse_forward()
    dll.traverse_backward()

    # Delete the head
    print("\n--- Delete (Head) ---")
    dll.delete_by_value(1)
    print("After deleting 1 (head):")
    dll.traverse_forward()
    dll.traverse_backward()

    # Delete the tail
    print("\n--- Delete (Tail) ---")
    dll.delete_by_value(30)
    print("After deleting 30 (tail):")
    dll.traverse_forward()
    dll.traverse_backward()

    # Delete the last remaining node
    print("\n--- Delete (Last Node) ---")
    dll.delete_by_value(5)
    print("After deleting 5 (last node):")
    dll.traverse_forward()
    dll.traverse_backward()

    # Try to delete from an empty list
    print("\n--- Delete from Empty List ---")
    dll.delete_by_value(99)

    print("\nDone with Doubly Linked List!")


if __name__ == "__main__":
    main()
