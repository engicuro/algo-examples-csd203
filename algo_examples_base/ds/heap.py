class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class MinHeapTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def _get_node_at(self, index):
        if index == 1:
            return self.root
        parent = self._get_node_at(index // 2)
        if index % 2 == 0:
            return parent.left
        else:
            return parent.right

    def insert(self, key):
        new_node = Node(key)
        self.size += 1
        if self.root is None:
            self.root = new_node
            return

        parent = self._get_node_at(self.size // 2)
        new_node.parent = parent
        if self.size % 2 == 0:
            parent.left = new_node
        else:
            parent.right = new_node

        self._upheap(new_node)

    def _upheap(self, node):
        while node.parent is not None and node.key < node.parent.key:
            node.key, node.parent.key = node.parent.key, node.key
            node = node.parent

    def peek_min(self):
        return self.root.key if self.root else None
