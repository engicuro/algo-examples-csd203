class EntryNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashBucket:
    def __init__(self, index):
        self.index = index
        self.head = None
        self.next_bucket = None

class HashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.buckets_head = None
        curr = None
        for i in range(capacity):
            b = HashBucket(i)
            if self.buckets_head is None:
                self.buckets_head = b
            else:
                curr.next_bucket = b
            curr = b

    def _hash(self, key):
        return hash(key) % self.capacity

    def _get_bucket(self, index):
        curr = self.buckets_head
        while curr is not None:
            if curr.index == index:
                return curr
            curr = curr.next_bucket
        return None

    def put(self, key, value):
        idx = self._hash(key)
        bucket = self._get_bucket(idx)
        curr = bucket.head
        while curr is not None:
            if curr.key == key:
                curr.value = value
                return
            curr = curr.next
        new_node = EntryNode(key, value)
        new_node.next = bucket.head
        bucket.head = new_node

    def get(self, key):
        idx = self._hash(key)
        bucket = self._get_bucket(idx)
        curr = bucket.head
        while curr is not None:
            if curr.key == key:
                return curr.value
            curr = curr.next
        return None
