class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top_node = None
        self.size = 0

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.top_node
        self.top_node = new_node
        self.size += 1

    def pop(self):
        if self.top_node is None:
            return None
        val = self.top_node.value
        self.top_node = self.top_node.next
        self.size -= 1
        return val

    def peek(self):
        if self.top_node is None:
            return None
        return self.top_node.value

    def is_empty(self):
        return self.top_node is None
