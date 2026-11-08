class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class HeapSort:
    def __init__(self):
        self.root = None
        self.size = 0

    def _get_node(self, idx):
        if idx == 1:
            return self.root
        parent = self._get_node(idx // 2)
        return parent.left if idx % 2 == 0 else parent.right

    def insert(self, key):
        node = TreeNode(key)
        self.size += 1
        if self.size == 1:
            self.root = node
            return
        parent = self._get_node(self.size // 2)
        node.parent = parent
        if self.size % 2 == 0:
            parent.left = node
        else:
            parent.right = node
        self._upheap(node)

    def _upheap(self, node):
        while node.parent and node.key > node.parent.key:
            node.key, node.parent.key = node.parent.key, node.key
            node = node.parent

    def _downheap(self, node):
        while node:
            largest = node
            if node.left and node.left.key > largest.key:
                largest = node.left
            if node.right and node.right.key > largest.key:
                largest = node.right
            if largest == node:
                break
            node.key, largest.key = largest.key, node.key
            node = largest

    def extract_max(self):
        if self.size == 0:
            return None
        max_val = self.root.key
        if self.size == 1:
            self.root = None
            self.size = 0
            return max_val
        last_node = self._get_node(self.size)
        self.root.key = last_node.key
        parent = last_node.parent
        if parent.left == last_node:
            parent.left = None
        else:
            parent.right = None
        self.size -= 1
        self._downheap(self.root)
        return max_val

if __name__ == "__main__":
    hs = HeapSort()
    hs.insert(12); hs.insert(11); hs.insert(13); hs.insert(5); hs.insert(6)
    out = ""
    while hs.size > 0:
        out += str(hs.extract_max()) + " "
    print("Heap Sorted (Desc):", out)
