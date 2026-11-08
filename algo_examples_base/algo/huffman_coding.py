class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        self.next = None

def insert_sorted(head, node):
    if head is None or node.freq < head.freq:
        node.next = head
        return node
    curr = head
    while curr.next and curr.next.freq <= node.freq:
        curr = curr.next
    node.next = curr.next
    curr.next = node
    return head

def build_huffman_tree(text):
    # Count frequencies using linked entries
    class FreqNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.next = None

    freq_head = None
    for char in text:
        curr = freq_head
        found = False
        while curr:
            if curr.char == char:
                curr.freq += 1
                found = True
                break
            curr = curr.next
        if not found:
            fn = FreqNode(char, 1)
            fn.next = freq_head
            freq_head = fn

    nodes_head = None
    curr = freq_head
    while curr:
        hn = HuffmanNode(curr.char, curr.freq)
        nodes_head = insert_sorted(nodes_head, hn)
        curr = curr.next

    while nodes_head and nodes_head.next:
        left = nodes_head
        right = nodes_head.next
        nodes_head = right.next

        parent = HuffmanNode(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        nodes_head = insert_sorted(nodes_head, parent)

    return nodes_head

def print_codes(root, code=""):
    if not root:
        return
    if root.char is not None:
        print(root.char + ": " + code)
    print_codes(root.left, code + "0")
    print_codes(root.right, code + "1")

if __name__ == "__main__":
    text = "BCAADDDCCACACAC"
    root = build_huffman_tree(text)
    print("Huffman Codes:")
    print_codes(root)
