class DictNode:
    def __init__(self, string, code):
        self.string = string
        self.code = code
        self.next = None

class DynamicDict:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        for i in range(256):
            self.add(chr(i), i)

    def add(self, string, code):
        n = DictNode(string, code)
        if not self.head:
            self.head = self.tail = n
        else:
            self.tail.next = n
            self.tail = n
        self.size += 1

    def find_code(self, string):
        curr = self.head
        while curr:
            if curr.string == string:
                return curr.code
            curr = curr.next
        return -1

class CodeNode:
    def __init__(self, code):
        self.code = code
        self.next = None

def lzw_compress(text):
    dictionary = DynamicDict()
    code_counter = 256
    p = ""
    compressed_head = None
    compressed_tail = None

    for c in text:
        pc = p + c
        if dictionary.find_code(pc) != -1:
            p = pc
        else:
            code = dictionary.find_code(p)
            cn = CodeNode(code)
            if not compressed_head:
                compressed_head = compressed_tail = cn
            else:
                compressed_tail.next = cn
                compressed_tail = cn
            dictionary.add(pc, code_counter)
            code_counter += 1
            p = c

    if p != "":
        code = dictionary.find_code(p)
        cn = CodeNode(code)
        if not compressed_head:
            compressed_head = compressed_tail = cn
        else:
            compressed_tail.next = cn
            compressed_tail = cn

    return compressed_head

if __name__ == "__main__":
    text = "TOBEORNOTTOBEORTOBEORNOT"
    res = lzw_compress(text)
    curr = res
    out = ""
    while curr:
        out += str(curr.code) + " "
        curr = curr.next
    print("LZW Compressed Codes:", out)
