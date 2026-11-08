class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def get_middle(head):
    if not head:
        return head
    slow = head
    fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    return slow

def merge(left, right):
    if not left:
        return right
    if not right:
        return left
    if left.value <= right.value:
        result = left
        result.next = merge(left.next, right)
    else:
        result = right
        result.next = merge(left, right.next)
    return result

def merge_sort(head):
    if not head or not head.next:
        return head
    mid = get_middle(head)
    next_to_mid = mid.next
    mid.next = None

    left = merge_sort(head)
    right = merge_sort(next_to_mid)

    return merge(left, right)

def print_list(head):
    curr = head
    out = ""
    while curr:
        out += str(curr.value) + " -> "
        curr = curr.next
    print(out + "None")

if __name__ == "__main__":
    n1 = Node(15); n2 = Node(10); n3 = Node(5); n4 = Node(20); n5 = Node(3)
    n1.next = n2; n2.next = n3; n3.next = n4; n4.next = n5
    print_list(merge_sort(n1))
