class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def quick_sort(head):
    if not head or not head.next:
        return head
    pivot = head
    less_head = None; less_tail = None
    greater_head = None; greater_tail = None
    curr = head.next
    pivot.next = None

    while curr:
        nxt = curr.next
        curr.next = None
        if curr.value < pivot.value:
            if not less_head:
                less_head = less_tail = curr
            else:
                less_tail.next = curr
                less_tail = curr
        else:
            if not greater_head:
                greater_head = greater_tail = curr
            else:
                greater_tail.next = curr
                greater_tail = curr
        curr = nxt

    sorted_less = quick_sort(less_head)
    sorted_greater = quick_sort(greater_head)

    if sorted_less:
        temp = sorted_less
        while temp.next:
            temp = temp.next
        temp.next = pivot
        pivot.next = sorted_greater
        return sorted_less
    else:
        pivot.next = sorted_greater
        return pivot

def print_list(head):
    curr = head
    out = ""
    while curr:
        out += str(curr.value) + " -> "
        curr = curr.next
    print(out + "None")

if __name__ == "__main__":
    n1 = Node(9); n2 = Node(3); n3 = Node(7); n4 = Node(1); n5 = Node(5)
    n1.next = n2; n2.next = n3; n3.next = n4; n4.next = n5
    print_list(quick_sort(n1))
