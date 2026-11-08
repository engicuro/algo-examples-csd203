# Chapter 1: Circularly Linked List (No-List Version)
# No Python lists used — only classes and simple logic.


class Node:
    """A single node in a circularly linked list."""

    def __init__(self, value):
        self.value = value
        self.next = None


class CircularlyLinkedList:
    """A circularly linked list where the tail points back to the head."""

    def __init__(self):
        self.head = None

    def is_empty(self):
        """Return True if the list has no elements."""
        return self.head is None

    def insert_at_head(self, value):
        """Insert a new node at the beginning of the list."""
        new_node = Node(value)

        if self.head is None:
            new_node.next = new_node
            self.head = new_node
        else:
            last = self.head
            while last.next != self.head:
                last = last.next

            new_node.next = self.head
            last.next = new_node
            self.head = new_node

    def insert_at_tail(self, value):
        """Insert a new node at the end of the list."""
        new_node = Node(value)

        if self.head is None:
            new_node.next = new_node
            self.head = new_node
        else:
            last = self.head
            while last.next != self.head:
                last = last.next

            last.next = new_node
            new_node.next = self.head

    def delete_by_value(self, value):
        """Delete the first node that contains the given value."""
        if self.head is None:
            print("List is empty. Nothing to delete.")
            return

        if self.head.value == value and self.head.next == self.head:
            self.head = None
            return

        if self.head.value == value:
            last = self.head
            while last.next != self.head:
                last = last.next

            last.next = self.head.next
            self.head = self.head.next
            return

        current = self.head
        while current.next != self.head:
            if current.next.value == value:
                current.next = current.next.next
                return
            current = current.next

        print(value, "not found in the list.")

    def traverse(self):
        """Print all values in the list by following the circle (no list used)."""
        if self.head is None:
            print("List is empty.")
            return

        # Build output string directly instead of collecting into a list
        output = ""
        current = self.head

        while True:
            output = output + str(current.value) + " -> "
            current = current.next
            if current == self.head:
                break

        output = output + "(back to head)"
        print(output)

    def is_circular(self):
        """Check whether the list is circular."""
        if self.head is None:
            print("List is empty (no circle).")
            return False

        current = self.head.next

        while current is not None and current != self.head:
            current = current.next

        if current == self.head:
            print("The list IS circular (tail points back to head).")
            return True
        else:
            print("The list is NOT circular (a node points to None).")
            return False


def main():
    print("=" * 50)
    print("Chapter 1: Circularly Linked List (No-List Version)")
    print("=" * 50)

    cll = CircularlyLinkedList()

    print("\n--- Insert at Tail ---")
    cll.insert_at_tail(10)
    cll.insert_at_tail(20)
    cll.insert_at_tail(30)
    print("After inserting 10, 20, 30 at tail:")
    cll.traverse()

    print("\n--- Insert at Head ---")
    cll.insert_at_head(5)
    cll.insert_at_head(1)
    print("After inserting 5 and 1 at head:")
    cll.traverse()

    print("\n--- Is Circular? ---")
    cll.is_circular()

    print("\n--- Delete ---")
    print("Before delete:")
    cll.traverse()

    cll.delete_by_value(20)
    print("After deleting 20:")
    cll.traverse()

    cll.delete_by_value(1)
    print("After deleting 1 (head):")
    cll.traverse()

    print("\n--- Delete All ---")
    cll.delete_by_value(5)
    cll.delete_by_value(30)
    cll.delete_by_value(10)
    print("After deleting all nodes:")
    cll.traverse()

    print("\n--- Is Circular on Empty List? ---")
    cll.is_circular()

    print("\nDone with Circularly Linked List!")


if __name__ == "__main__":
    main()
