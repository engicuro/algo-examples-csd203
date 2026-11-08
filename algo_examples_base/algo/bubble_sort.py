class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def bubble_sort(head):
    if not head:
        return None
    swapped = True
    while swapped:
        swapped = False
        curr = head
        while curr.next:
            if curr.value > curr.next.value:
                curr.value, curr.next.value = curr.next.value, curr.value
                swapped = True
            curr = curr.next
    return head

def print_list(head):
    curr = head
    out = ""
    while curr:
        out += str(curr.value) + " -> "
        curr = curr.next
    print(out + "None")

if __name__ == "__main__":
    n1 = Node(10); n2 = Node(2); n3 = Node(8); n4 = Node(6)
    n1.next = n2; n2.next = n3; n3.next = n4
    print_list(bubble_sort(n1))
