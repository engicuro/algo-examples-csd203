class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            new_node.next = self.head
        else:
            curr = self.head
            while curr.next != self.head:
                curr = curr.next
            curr.next = new_node
            new_node.next = self.head
        self.size += 1

    def display(self):
        if self.head is None:
            print("Empty")
            return
        curr = self.head
        out = ""
        while True:
            out += str(curr.value) + " -> "
            curr = curr.next
            if curr == self.head:
                break
        out += "(head: " + str(self.head.value) + ")"
        print(out)
