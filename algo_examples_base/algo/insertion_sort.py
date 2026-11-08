class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def insertion_sort(head):
    sorted_head = None
    curr = head
    while curr:
        nxt = curr.next
        if sorted_head is None or sorted_head.value >= curr.value:
            curr.next = sorted_head
            sorted_head = curr
        else:
            s_curr = sorted_head
            while s_curr.next and s_curr.next.value < curr.value:
                s_curr = s_curr.next
            curr.next = s_curr.next
            s_curr.next = curr
        curr = nxt
    return sorted_head

def print_list(head):
    curr = head
    out = ""
    while curr:
        out += str(curr.value) + " -> "
        curr = curr.next
    print(out + "None")

if __name__ == "__main__":
    n1 = Node(5); n2 = Node(2); n3 = Node(4); n4 = Node(1); n5 = Node(3)
    n1.next = n2; n2.next = n3; n3.next = n4; n4.next = n5
    print_list(insertion_sort(n1))
