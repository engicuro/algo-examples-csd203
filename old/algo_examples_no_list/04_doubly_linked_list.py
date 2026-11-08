# Chapter 1: Doubly Linked List (No-List Version)
# No Python lists used — only classes and simple logic.


class Node:
    """A single node in a doubly linked list."""

    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """A doubly linked list that tracks both head and tail."""

    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_head(self, value):
        """Insert a new node at the beginning of the list."""
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def insert_at_tail(self, value):
        """Insert a new node at the end of the list."""
        new_node = Node(value)

        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def delete_by_value(self, value):
        """Delete the first node that contains the given value."""
        if self.head is None:
            print("List is empty. Nothing to delete.")
            return

        current = self.head
        while current is not None:
            if current.value == value:
                # Case 1: deleting the only node
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

                # Case 4: deleting a middle node
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev

                return

            current = current.next

        print(value, "not found in the list.")

    def traverse_forward(self):
        """Print all values from head to tail (no list used)."""
        # Build output string directly
        output = "Forward:  "
        current = self.head
        first = True
        while current is not None:
            if not first:
                output = output + " <-> "
            output = output + str(current.value)
            first = False
            current = current.next
        output = output + " -> None"
        print(output)

    def traverse_backward(self):
        """Print all values from tail to head (no list used)."""
        # Build output string directly
        output = "Backward: None <- "
        current = self.tail
        first = True
        while current is not None:
            if not first:
                output = output + " <-> "
            output = output + str(current.value)
            first = False
            current = current.prev
        print(output)


def main():
    print("=" * 50)
    print("Chapter 1: Doubly Linked List (No-List Version)")
    print("=" * 50)

    dll = DoublyLinkedList()

    print("\n--- Insert at Tail ---")
    dll.insert_at_tail(10)
    dll.insert_at_tail(20)
    dll.insert_at_tail(30)
    print("After inserting 10, 20, 30 at tail:")
    dll.traverse_forward()
    dll.traverse_backward()

    print("\n--- Insert at Head ---")
    dll.insert_at_head(5)
    dll.insert_at_head(1)
    print("After inserting 5 and 1 at head:")
    dll.traverse_forward()
    dll.traverse_backward()

    print("\n--- Delete (Middle) ---")
    print("Before delete:")
    dll.traverse_forward()

    dll.delete_by_value(20)
    print("After deleting 20 (middle):")
    dll.traverse_forward()
    dll.traverse_backward()

    print("\n--- Delete (Head) ---")
    dll.delete_by_value(1)
    print("After deleting 1 (head):")
    dll.traverse_forward()
    dll.traverse_backward()

    print("\n--- Delete (Tail) ---")
    dll.delete_by_value(30)
    print("After deleting 30 (tail):")
    dll.traverse_forward()
    dll.traverse_backward()

    print("\n--- Delete (Last Node) ---")
    dll.delete_by_value(5)
    print("After deleting 5 (last node):")
    dll.traverse_forward()
    dll.traverse_backward()

    print("\n--- Delete from Empty List ---")
    dll.delete_by_value(99)

    print("\nDone with Doubly Linked List!")


if __name__ == "__main__":
    main()
