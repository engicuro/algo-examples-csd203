"""
52_huffman_coding.py - Huffman Coding
==========================================

Huffman coding is a lossless compression algorithm that
assigns shorter codes to more frequent characters and
longer codes to less frequent characters.

How it works:
  1. Count the frequency of each character in the text.
  2. Build a binary tree (Huffman tree) by repeatedly
     combining the two least frequent nodes.
  3. Traverse the tree to assign binary codes:
       - Go left  → append '0'
       - Go right → append '1'
  4. Encode the text using the codes.
  5. Decode by walking the tree using the encoded bits.

Example:
  Text: "BCCABBDDAEC"
  Frequencies: A=2, B=3, C=2, D=2, E=1
  Huffman codes might be: A='10', B='0', C='110', D='111', E='100'
  Encoded: much shorter than the original 8-bit ASCII representation!

This implementation uses a simple class-based tree structure.
"""

import math
from _structures import LinkedList


class HuffmanNode:
    """A node in the Huffman tree.

    Leaf nodes hold a character and its frequency.
    Internal nodes hold the combined frequency of their children.
    """

    def __init__(self, char, freq):
        """Initialize a node.

        Args:
            char: The character (None for internal nodes).
            freq: The frequency count.
        """
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def is_leaf(self):
        """Return True if this node is a leaf (has a character)."""
        return self.left is None and self.right is None


def count_frequencies(text):
    """Count how many times each character appears in the text.

    Args:
        text: The input string.

    Returns:
        A dictionary mapping each character to its frequency.
    """
    frequencies = {}
    for i in range(len(text)):
        char = text[i]
        if char in frequencies:
            frequencies[char] = frequencies[char] + 1
        else:
            frequencies[char] = 1
    return frequencies


def build_huffman_tree(frequencies):
    """Build a Huffman tree from character frequencies.

    The algorithm:
      1. Create a leaf node for each character.
      2. Repeat until only one node remains:
         a. Find the two nodes with the smallest frequencies.
         b. Create a new internal node with these two as children.
         c. The new node's frequency is the sum of its children's.
         d. Put the new node back in the list.

    Args:
        frequencies: A dictionary mapping characters to frequencies.

    Returns:
        The root node of the Huffman tree.
    """
    # Create a leaf node for each character
    nodes = LinkedList()
    for char in frequencies:
        node = HuffmanNode(char, frequencies[char])
        nodes.append(node)

    # Repeatedly combine the two smallest nodes
    while len(nodes) > 1:
        # Sort nodes by frequency (ascending)
        # We use a simple bubble-sort-like approach to keep it basic
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if nodes.get(j).freq < nodes.get(i).freq:
                    temp = nodes.get(i)
                    nodes.set(i, nodes.get(j))
                    nodes.set(j, temp)

        # Take the two nodes with the smallest frequencies
        left = nodes.get(0)
        right = nodes.get(1)

        # Create a new internal node combining them
        combined = HuffmanNode(None, left.freq + right.freq)
        combined.left = left
        combined.right = right

        # Remove the two used nodes and add the combined node
        new_nodes = LinkedList()
        new_nodes.append(combined)
        for i in range(2, len(nodes)):
            new_nodes.append(nodes.get(i))
        nodes = new_nodes

    # The last remaining node is the root of the Huffman tree
    return nodes.get(0)


def build_codes(node, current_code, codes):
    """Traverse the Huffman tree and build the binary codes.

    Going left  appends '0' to the code.
    Going right appends '1' to the code.
    When we reach a leaf, we store the code for that character.

    Args:
        node: The current node in the tree.
        current_code: The binary string built so far.
        codes: A dictionary to store char -> code mappings.
    """
    if node is None:
        return

    # If this is a leaf node, store the code
    if node.is_leaf():
        # Handle the special case where there's only one unique character
        if current_code == "":
            current_code = "0"
        codes[node.char] = current_code
        return

    # Traverse left (append '0')
    build_codes(node.left, current_code + "0", codes)

    # Traverse right (append '1')
    build_codes(node.right, current_code + "1", codes)


def encode_text(text, codes):
    """Encode the text using the Huffman codes.

    Args:
        text: The original text string.
        codes: A dictionary mapping characters to binary codes.

    Returns:
        The encoded binary string.
    """
    encoded = ""
    for i in range(len(text)):
        char = text[i]
        encoded = encoded + codes[char]
    return encoded


def decode_text(encoded, root):
    """Decode a binary string using the Huffman tree.

    Start at the root. For each bit:
      - '0' → go left
      - '1' → go right
    When we reach a leaf, output the character and start over
    from the root.

    Args:
        encoded: The binary string to decode.
        root: The root of the Huffman tree.

    Returns:
        The decoded text string.
    """
    decoded = ""
    current = root

    for i in range(len(encoded)):
        bit = encoded[i]

        if bit == '0':
            current = current.left
        else:
            current = current.right

        # If we reached a leaf, output the character
        if current.is_leaf():
            decoded = decoded + current.char
            current = root  # Reset to root for the next character

    return decoded


def print_tree(node, prefix="", is_left=True):
    """Print the Huffman tree structure (for visualization).

    Args:
        node: The current node.
        prefix: The prefix string for indentation.
        is_left: Whether this node is a left child.
    """
    if node is None:
        return

    if node.is_leaf():
        print("  {}'-- '{}' (freq={})".format(
            prefix, node.char, node.freq))
    else:
        print("  {}'-- * (freq={})".format(prefix, node.freq))

    if node.left is not None or node.right is not None:
        if node.left:
            print_tree(node.left, prefix + ("|   " if is_left else "    "), True)
        if node.right:
            print_tree(node.right, prefix + ("|   " if is_left else "    "), False)


if __name__ == "__main__":
    print("=" * 50)
    print("  Huffman Coding — Educational Demo")
    print("=" * 50)

    # --- Example 1: Simple text ---
    print("\n--- Example 1: Simple text ---")
    text1 = "BCCABBDDAEC"
    print("Original text: \"{}\"".format(text1))
    print("Text length: {} characters".format(len(text1)))

    # Count frequencies
    freq1 = count_frequencies(text1)
    print("\nCharacter frequencies:")
    for char in sorted(freq1.keys()):
        print("  '{}': {}".format(char, freq1[char]))

    # Build the Huffman tree
    tree1 = build_huffman_tree(freq1)

    # Build the codes
    codes1 = {}
    build_codes(tree1, "", codes1)

    print("\nHuffman codes:")
    for char in sorted(codes1.keys()):
        print("  '{}': {}".format(char, codes1[char]))

    # Encode
    encoded1 = encode_text(text1, codes1)
    print("\nEncoded: {}".format(encoded1))
    print("Encoded length: {} bits".format(len(encoded1)))

    # Original size (8 bits per character)
    original_bits = len(text1) * 8
    print("Original size: {} bits ({} chars * 8 bits/char)".format(
        original_bits, len(text1)))
    print("Compressed size: {} bits".format(len(encoded1)))
    print("Compression ratio: {:.1f}%".format(
        (1 - len(encoded1) / original_bits) * 100))

    # Decode
    decoded1 = decode_text(encoded1, tree1)
    print("\nDecoded: \"{}\"".format(decoded1))
    print("Decoded matches original: {}".format(decoded1 == text1))

    # --- Example 2: Text with skewed frequencies ---
    print("\n" + "=" * 50)
    print("  Example 2: Text with skewed frequencies ---")
    text2 = "AAAAAAABBC"
    print("Original text: \"{}\"".format(text2))

    freq2 = count_frequencies(text2)
    print("\nCharacter frequencies:")
    for char in sorted(freq2.keys()):
        print("  '{}': {}".format(char, freq2[char]))

    tree2 = build_huffman_tree(freq2)
    codes2 = {}
    build_codes(tree2, "", codes2)

    print("\nHuffman codes:")
    for char in sorted(codes2.keys()):
        print("  '{}': {}".format(char, codes2[char]))

    encoded2 = encode_text(text2, codes2)
    print("\nEncoded: {}".format(encoded2))
    print("Encoded length: {} bits".format(len(encoded2)))
    print("Original size: {} bits".format(len(text2) * 8))
    print("Compression ratio: {:.1f}%".format(
        (1 - len(encoded2) / (len(text2) * 8)) * 100))

    decoded2 = decode_text(encoded2, tree2)
    print("Decoded: \"{}\"".format(decoded2))
    print("Decoded matches original: {}".format(decoded2 == text2))

    # --- Summary ---
    print("\n" + "=" * 50)
    print("  Summary")
    print("=" * 50)
    print("""
Huffman coding is optimal for prefix-free codes:
  - No code is a prefix of another code (unambiguous).
  - More frequent characters get shorter codes.
  - Achieves the minimum expected code length for
    a given set of character frequencies.

Applications:
  - File compression (ZIP, GZIP)
  - JPEG image compression
  - MP3 audio compression
""")
