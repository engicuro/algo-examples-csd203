class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def selection_sort(head):
    curr = head
    while curr:
        min_node = curr
        r = curr.next
        while r:
            if r.value < min_node.value:
                min_node = r
            r = r.next
        curr.value, min_node.value = min_node.value, curr.value
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
    n1 = Node(64); n2 = Node(25); n3 = Node(12); n4 = Node(22); n5 = Node(11)
    n1.next = n2; n2.next = n3; n3.next = n4; n4.next = n5
    print("Original:")
    print_list(n1)
    sorted_head = selection_sort(n1)
    print("Sorted:")
    print_list(sorted_head)
