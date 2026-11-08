class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class BucketNode:
    def __init__(self, index):
        self.index = index
        self.head = None
        self.next_bucket = None

def bucket_sort(head, num_buckets=10):
    buckets_head = None
    curr_b = None
    for i in range(num_buckets):
        b = BucketNode(i)
        if buckets_head is None:
            buckets_head = b
        else:
            curr_b.next_bucket = b
        curr_b = b

    curr = head
    while curr:
        nxt = curr.next
        b_idx = int(curr.value * num_buckets)
        b = buckets_head
        while b and b.index != b_idx:
            b = b.next_bucket
        if b:
            curr.next = b.head
            b.head = curr
        curr = nxt

    # Sort each bucket using insertion sort
    b = buckets_head
    new_head = None
    new_tail = None
    while b:
        # insertion sort bucket
        sorted_b = None
        item = b.head
        while item:
            item_next = item.next
            if sorted_b is None or sorted_b.value >= item.value:
                item.next = sorted_b
                sorted_b = item
            else:
                s = sorted_b
                while s.next and s.next.value < item.value:
                    s = s.next
                item.next = s.next
                s.next = item
            item = item_next
        
        # append sorted_b to result
        item = sorted_b
        while item:
            nxt_item = item.next
            item.next = None
            if new_head is None:
                new_head = new_tail = item
            else:
                new_tail.next = item
                new_tail = item
            item = nxt_item
        b = b.next_bucket
    return new_head

if __name__ == "__main__":
    n1 = Node(0.42); n2 = Node(0.32); n3 = Node(0.23); n4 = Node(0.52); n5 = Node(0.25)
    n1.next = n2; n2.next = n3; n3.next = n4; n4.next = n5
    res = bucket_sort(n1)
    curr = res
    out = ""
    while curr:
        out += str(curr.value) + " -> "
        curr = curr.next
    print("Bucket Sorted:", out + "None")
