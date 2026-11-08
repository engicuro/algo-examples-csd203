class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class BucketNode:
    def __init__(self, index):
        self.index = index
        self.head = None
        self.tail = None
        self.next_bucket = None

def radix_sort(head, max_digits=3):
    curr_head = head
    exp = 1
    for d in range(max_digits):
        buckets_head = None
        curr_b = None
        for i in range(10):
            b = BucketNode(i)
            if buckets_head is None:
                buckets_head = b
            else:
                curr_b.next_bucket = b
            curr_b = b

        curr = curr_head
        while curr:
            nxt = curr.next
            curr.next = None
            digit = (curr.value // exp) % 10
            b = buckets_head
            while b and b.index != digit:
                b = b.next_bucket
            if b.head is None:
                b.head = b.tail = curr
            else:
                b.tail.next = curr
                b.tail = curr
            curr = nxt

        curr_head = None
        curr_tail = None
        b = buckets_head
        while b:
            if b.head:
                if curr_head is None:
                    curr_head = b.head
                    curr_tail = b.tail
                else:
                    curr_tail.next = b.head
                    curr_tail = b.tail
            b = b.next_bucket
        exp *= 10
    return curr_head

if __name__ == "__main__":
    n1 = Node(170); n2 = Node(45); n3 = Node(75); n4 = Node(90); n5 = Node(802)
    n1.next = n2; n2.next = n3; n3.next = n4; n4.next = n5
    res = radix_sort(n1)
    curr = res
    out = ""
    while curr:
        out += str(curr.value) + " -> "
        curr = curr.next
    print("Radix Sorted:", out + "None")
