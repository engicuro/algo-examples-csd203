# Chapter 1: Circularly Linked List
# In a circular linked list, the last node points back to the first node
# instead of pointing to None. This creates a loop in the list.

from _structures import LinkedList


class Node:
    """A single node in a circularly linked list.

    Each node holds a value and a pointer to the next node.
    The last node's next pointer points back to the head (first node).
    """

    def __init__(self, value):
        self.value = value  # the data stored in this node
        self.next = None    # pointer to the next node


class CircularlyLinkedList:
    """A circularly linked list where the tail points back to the head."""

    def __init__(self):
        self.head = None  # the list starts empty

    def is_empty(self):
        """Return True if the list has no elements."""
        return self.head is None

    def insert_at_head(self, value):
        """Insert a new node at the beginning of the list."""
        new_node = Node(value)

        if self.head is None:
            # First node: point it to itself (circular)
            new_node.next = new_node
            self.head = new_node
        else:
            # Find the last node (the one that points back to head)
            last = self.head
            while last.next != self.head:
                last = last.next

            # New node points to the old head
            new_node.next = self.head
            # Last node now points to the new node
            last.next = new_node
            # Update head to be the new node
            self.head = new_node

    def insert_at_tail(self, value):
        """Insert a new node at the end of the list."""
        new_node = Node(value)

        if self.head is None:
            # First node: point it to itself (circular)
            new_node.next = new_node
            self.head = new_node
        else:
            # Find the last node
            last = self.head
            while last.next != self.head:
                last = last.next

            # Last node points to the new node
            last.next = new_node
            # New node points back to head (completing the circle)
            new_node.next = self.head

    def delete_by_value(self, value):
        """Delete the first node that contains the given value."""
        if self.head is None:
            print("List is empty. Nothing to delete.")
            return

        # Special case: only one node in the list
        if self.head.value == value and self.head.next == self.head:
            self.head = None
            return

        # Special case: the value is in the head node
        if self.head.value == value:
            # Find the last node
            last = self.head
            while last.next != self.head:
                last = last.next

            # Last node points to the second node (new head)
            last.next = self.head.next
            self.head = self.head.next
            return

        # Walk through the list to find the node before the one to delete
        current = self.head
        while current.next != self.head:
            if current.next.value == value:
                # Skip over the node to delete it
                current.next = current.next.next
                return
            current = current.next

        print(value, "not found in the list.")

    def traverse(self):
        """Print all values in the list by following the circle."""
        if self.head is None:
            print("List is empty.")
            return

        elements = LinkedList()
        current = self.head

        # Walk through the circle until we get back to the head
        while True:
            elements.append(str(current.value))
            current = current.next
            if current == self.head:
                break

        # Build the display string by iterating the LinkedList
        parts = []
        for val in elements:
            parts.append(val)
        print(" -> ".join(parts) + " -> (back to head)")

    def is_circular(self):
        """Check whether the list is circular (last node points back to head)."""
        if self.head is None:
            print("List is empty (no circle).")
            return False

        # Start at the head and follow next pointers
        current = self.head.next

        # Walk until we either reach None (not circular) or get back to head (circular)
        while current is not None and current != self.head:
            current = current.next

        # If we reached the head again, the list is circular
        if current == self.head:
            print("The list IS circular (tail points back to head).")
            return True
        else:
            print("The list is NOT circular (a node points to None).")
            return False


def main():
    print("=" * 50)
    print("Chapter 1: Circularly Linked List")
    print("=" * 50)

    cll = CircularlyLinkedList()

    # Insert at tail
    print("\n--- Insert at Tail ---")
    cll.insert_at_tail(10)
    cll.insert_at_tail(20)
    cll.insert_at_tail(30)
    print("After inserting 10, 20, 30 at tail:")
    cll.traverse()

    # Insert at head
    print("\n--- Insert at Head ---")
    cll.insert_at_head(5)
    cll.insert_at_head(1)
    print("After inserting 5 and 1 at head:")
    cll.traverse()

    # Check if circular
    print("\n--- Is Circular? ---")
    cll.is_circular()

    # Delete by value
    print("\n--- Delete ---")
    print("Before delete:")
    cll.traverse()

    cll.delete_by_value(20)
    print("After deleting 20:")
    cll.traverse()

    cll.delete_by_value(1)
    print("After deleting 1 (head):")
    cll.traverse()

    # Delete all remaining nodes one by one
    print("\n--- Delete All ---")
    cll.delete_by_value(5)
    cll.delete_by_value(30)
    cll.delete_by_value(10)
    print("After deleting all nodes:")
    cll.traverse()

    # Check circular on empty list
    print("\n--- Is Circular on Empty List? ---")
    cll.is_circular()

    print("\nDone with Circularly Linked List!")


if __name__ == "__main__":
    main()
