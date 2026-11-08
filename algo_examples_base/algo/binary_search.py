class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedSequence:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, val):
        new_node = Node(val)
        if self.head is None:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self.size += 1

    def get(self, index):
        curr = self.head
        for _ in range(index):
            if curr is None:
                return None
            curr = curr.next
        return curr.value if curr else None

def binary_search(seq, target):
    low = 0
    high = seq.size - 1
    while low <= high:
        mid = (low + high) // 2
        val = seq.get(mid)
        if val == target:
            return mid
        elif val < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

if __name__ == "__main__":
    seq = LinkedSequence()
    seq.append(10)
    seq.append(20)
    seq.append(30)
    seq.append(40)
    seq.append(50)
    print("Index of 30:", binary_search(seq, 30))
