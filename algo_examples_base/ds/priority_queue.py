class Node:
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority
        self.next = None

class PriorityQueue:
    def __init__(self):
        self.head = None

    def insert(self, value, priority):
        new_node = Node(value, priority)
        if self.head is None or priority < self.head.priority:
            new_node.next = self.head
            self.head = new_node
        else:
            curr = self.head
            while curr.next is not None and curr.next.priority <= priority:
                curr = curr.next
            new_node.next = curr.next
            curr.next = new_node

    def pop_min(self):
        if self.head is None:
            return None
        val = self.head.value
        self.head = self.head.next
        return val
