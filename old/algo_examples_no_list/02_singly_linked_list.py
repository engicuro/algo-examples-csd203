# Chapter 1: Singly Linked List (No-List Version)
# Each node stores a value and a pointer to the next node.
# No Python lists used anywhere — only classes, loops, and simple logic.


class Node:
    """A single node in a linked list."""

    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    """A singly linked list that tracks only the head (first node)."""

    def __init__(self):
        self.head = None

    def insert_at_head(self, value):
        """Insert a new node at the beginning of the list."""
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node

    def insert_at_tail(self, value):
        """Insert a new node at the end of the list."""
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next

        current.next = new_node

    def delete_by_value(self, value):
        """Delete the first node that contains the given value."""
        if self.head is None:
            print("List is empty. Nothing to delete.")
            return

        if self.head.value == value:
            self.head = self.head.next
            return

        current = self.head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                return
            current = current.next

        print(value, "not found in the list.")

    def search(self, value):
        """Search for a value and return True if found, False otherwise."""
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def display(self):
        """Print all values in the list from head to tail (no list used)."""
        # Build the output string directly instead of collecting into a list
        output = ""
        current = self.head
        while current is not None:
            output = output + str(current.value) + " -> "
            current = current.next
        output = output + "None"
        print(output)

    def reverse(self):
        """Reverse the linked list in place."""
        previous = None
        current = self.head

        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self.head = previous


def main():
    print("=" * 50)
    print("Chapter 1: Singly Linked List (No-List Version)")
    print("=" * 50)

    linked_list = SinglyLinkedList()

    print("\n--- Insert at Tail ---")
    linked_list.insert_at_tail(10)
    linked_list.insert_at_tail(20)
    linked_list.insert_at_tail(30)
    print("After inserting 10, 20, 30 at tail:")
    linked_list.display()

    print("\n--- Insert at Head ---")
    linked_list.insert_at_head(5)
    linked_list.insert_at_head(1)
    print("After inserting 5 and 1 at head:")
    linked_list.display()

    print("\n--- Search ---")
    print("Search for 20:", linked_list.search(20))
    print("Search for 99:", linked_list.search(99))

    print("\n--- Delete ---")
    print("Before delete:")
    linked_list.display()

    linked_list.delete_by_value(20)
    print("After deleting 20:")
    linked_list.display()

    linked_list.delete_by_value(1)
    print("After deleting 1 (head):")
    linked_list.display()

    print("\n--- Reverse ---")
    linked_list.reverse()
    print("After reversing:")
    linked_list.display()

    print("\nDone with Singly Linked List!")


if __name__ == "__main__":
    main()
