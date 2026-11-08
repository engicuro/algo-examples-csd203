# Chapter 1: Singly Linked List
# Each node stores a value and a pointer to the next node.
# No fancy Python features — just classes, loops, and simple logic.

from _structures import LinkedList


class Node:
    """A single node in a linked list.

    Each node holds a value and a reference (pointer) to the next node.
    The last node's next pointer is None (meaning "end of list").
    """

    def __init__(self, value):
        self.value = value  # the data stored in this node
        self.next = None    # pointer to the next node (None means no next node)


class SinglyLinkedList:
    """A singly linked list that tracks only the head (first node)."""

    def __init__(self):
        self.head = None  # the list starts empty (no head node)

    def insert_at_head(self, value):
        """Insert a new node at the beginning of the list."""
        new_node = Node(value)  # create the new node
        new_node.next = self.head  # point the new node to the old first node
        self.head = new_node  # update head to be the new node

    def insert_at_tail(self, value):
        """Insert a new node at the end of the list."""
        new_node = Node(value)

        # If the list is empty, the new node becomes the head
        if self.head is None:
            self.head = new_node
            return

        # Walk to the last node (the one whose next is None)
        current = self.head
        while current.next is not None:
            current = current.next

        # Attach the new node after the last node
        current.next = new_node

    def delete_by_value(self, value):
        """Delete the first node that contains the given value."""
        # If the list is empty, nothing to delete
        if self.head is None:
            print("List is empty. Nothing to delete.")
            return

        # Special case: the value is in the head node
        if self.head.value == value:
            self.head = self.head.next  # move head to the second node
            return

        # Walk through the list to find the node before the one to delete
        current = self.head
        while current.next is not None:
            if current.next.value == value:
                # Skip over the node to delete it
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
        """Print all values in the list from head to tail."""
        elements = LinkedList()
        current = self.head
        while current is not None:
            elements.append(str(current.value))
            current = current.next
        # Build the display string by iterating the LinkedList
        parts = []
        for val in elements:
            parts.append(val)
        print(" -> ".join(parts) + " -> None")

    def reverse(self):
        """Reverse the linked list in place."""
        previous = None   # the node that comes before current (starts as None)
        current = self.head  # the node we are currently looking at

        while current is not None:
            # Save the next node before we change current.next
            next_node = current.next

            # Reverse the pointer: point current back to previous
            current.next = previous

            # Move previous and current one step forward
            previous = current
            current = next_node

        # After the loop, previous is the new head
        self.head = previous


def main():
    print("=" * 50)
    print("Chapter 1: Singly Linked List")
    print("=" * 50)

    # Create a new empty linked list
    linked_list = SinglyLinkedList()

    # Insert elements at the tail
    print("\n--- Insert at Tail ---")
    linked_list.insert_at_tail(10)
    linked_list.insert_at_tail(20)
    linked_list.insert_at_tail(30)
    print("After inserting 10, 20, 30 at tail:")
    linked_list.display()

    # Insert elements at the head
    print("\n--- Insert at Head ---")
    linked_list.insert_at_head(5)
    linked_list.insert_at_head(1)
    print("After inserting 5 and 1 at head:")
    linked_list.display()

    # Search for values
    print("\n--- Search ---")
    print("Search for 20:", linked_list.search(20))
    print("Search for 99:", linked_list.search(99))

    # Delete by value
    print("\n--- Delete ---")
    print("Before delete:")
    linked_list.display()

    linked_list.delete_by_value(20)
    print("After deleting 20:")
    linked_list.display()

    linked_list.delete_by_value(1)
    print("After deleting 1 (head):")
    linked_list.display()

    # Reverse the list
    print("\n--- Reverse ---")
    linked_list.reverse()
    print("After reversing:")
    linked_list.display()

    print("\nDone with Singly Linked List!")


if __name__ == "__main__":
    main()
