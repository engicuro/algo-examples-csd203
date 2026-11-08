class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class DynamicIntSequence:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, val):
        n = Node(val)
        if not self.head:
            self.head = self.tail = n
        else:
            self.tail.next = n
            self.tail = n
        self.size += 1

    def set(self, index, val):
        curr = self.head
        for _ in range(index):
            curr = curr.next
        curr.val = val

    def get(self, index):
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr.val

def compute_lps(pattern):
    m = len(pattern)
    lps = DynamicIntSequence()
    for _ in range(m):
        lps.append(0)
    
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps.set(i, length)
            i += 1
        else:
            if length != 0:
                length = lps.get(length - 1)
            else:
                lps.set(i, 0)
                i += 1
    return lps

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps.get(j - 1)
            else:
                i += 1
    return -1

if __name__ == "__main__":
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    print("KMP Pattern match index:", kmp_search(text, pattern))
