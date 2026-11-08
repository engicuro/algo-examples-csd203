class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            curr = self.head
            while curr.next is not None:
                curr = curr.next
            curr.next = new_node
        self.size += 1

    def prepend(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def delete(self, value):
        if self.head is None:
            return False
        if self.head.value == value:
            self.head = self.head.next
            self.size -= 1
            return True
        curr = self.head
        while curr.next is not None and curr.next.value != value:
            curr = curr.next
        if curr.next is not None:
            curr.next = curr.next.next
            self.size -= 1
            return True
        return False

    def display(self):
        curr = self.head
        out = ""
        while curr is not None:
            out += str(curr.value) + " -> "
            curr = curr.next
        out += "None"
        print(out)
