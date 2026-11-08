#!/usr/bin/env python3
"""
Huffman Coding Algorithm
========================

Huffman coding is a lossless data compression algorithm that uses a variable-length
prefix code based on the frequencies of characters. More frequent characters get
shorter codes, and less frequent characters get longer codes, resulting in optimal
compression for a given set of symbol frequencies.

This module demonstrates:
  1. Frequency counting from input text
  2. Building a Huffman tree using a min-heap (priority queue)
  3. Generating prefix codes by traversing the tree
  4. Encoding text into a compressed bit string
  5. Decoding a bit string back to the original text
  6. A simple compression ratio example

Time complexity:
  - Frequency counting:    O(n)  where n = length of input text
  - Tree building:         O(k log k) where k = number of unique characters
  - Encoding:              O(n) per character lookup (after tree is built)
  - Decoding:              O(n) traversing the tree bit by bit

Space complexity: O(k) for the tree and code table, where k = unique characters.

Reference:
  David A. Huffman, "A Method for the Construction of Minimum-Redundancy Codes",
  Proceedings of the IRE, 1952.
"""

import heapq
from collections import Counter


# ---------------------------------------------------------------------------
# Node class for the Huffman tree
# ---------------------------------------------------------------------------

class HuffmanNode:
    """A node in the Huffman coding tree.

    Leaf nodes store a character and its frequency.
    Internal nodes store the combined frequency of their children.
    """

    def __init__(self, char: str | None, freq: int):
        self.char = char      # Character (None for internal nodes)
        self.freq = freq      # Frequency (or combined frequency)
        self.left = None      # Left child  (bit 0)
        self.right = None     # Right child (bit 1)

    def __lt__(self, other: "HuffmanNode") -> bool:
        """Comparison for heapq — compare by frequency."""
        return self.freq < other.freq

    def __repr__(self) -> str:
        if self.char is not None:
            return f"HuffmanNode('{self.char}', freq={self.freq})"
        return f"HuffmanNode(internal, freq={self.freq})"


# ---------------------------------------------------------------------------
# Step 1: Frequency counting
# ---------------------------------------------------------------------------

def count_frequencies(text: str) -> dict[str, int]:
    """Count the frequency of each character in the input text.

    Args:
        text: The input string to analyze.

    Returns:
        A dictionary mapping each character to its occurrence count.

    Example:
        >>> count_frequencies("aabbc")
        {'a': 2, 'b': 2, 'c': 1}
    """
    return dict(Counter(text))


# ---------------------------------------------------------------------------
# Step 2: Build the Huffman tree
# ---------------------------------------------------------------------------

def build_huffman_tree(frequencies: dict[str, int]) -> HuffmanNode | None:
    """Build a Huffman coding tree from character frequencies.

    Algorithm:
      1. Create a leaf node for each character and push it onto a min-heap.
      2. While more than one node remains in the heap:
         a. Pop the two nodes with the smallest frequencies.
         b. Create a new internal node with these two as children.
            The new node's frequency is the sum of its children's frequencies.
         c. Push the new node back onto the heap.
      3. The last remaining node is the root of the Huffman tree.

    Args:
        frequencies: A dictionary mapping characters to their frequencies.

    Returns:
        The root node of the Huffman tree, or None if the frequency dict is empty.

    Example:
        >>> freqs = {'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45}
        >>> root = build_huffman_tree(freqs)
        >>> root.freq
        100
    """
    if not frequencies:
        return None

    # Edge case: only one unique character — create a tree with root and one leaf
    if len(frequencies) == 1:
        char = next(iter(frequencies))
        root = HuffmanNode(None, frequencies[char])
        root.left = HuffmanNode(char, frequencies[char])
        return root

    # Initialize the min-heap with leaf nodes
    heap: list[HuffmanNode] = []
    for char, freq in frequencies.items():
        heapq.heappush(heap, HuffmanNode(char, freq))

    # Repeatedly merge the two lowest-frequency nodes
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        # Create internal node with combined frequency
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    # The single remaining node is the root
    return heap[0]


# ---------------------------------------------------------------------------
# Step 3: Generate Huffman codes by traversing the tree
# ---------------------------------------------------------------------------

def generate_codes(node: HuffmanNode | None, prefix: str = "", code_map: dict[str, str] | None = None) -> dict[str, str]:
    """Recursively traverse the Huffman tree to generate prefix codes.

    Traversing left appends '0' to the prefix; traversing right appends '1'.
    When a leaf node is reached, the accumulated prefix becomes the code
    for that character.

    Args:
        node: The current node in the traversal.
        prefix: The bit string accumulated so far.
        code_map: Dictionary to populate with character-to-code mappings.

    Returns:
        A dictionary mapping each character to its binary Huffman code.

    Example:
        >>> freqs = {'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45}
        >>> root = build_huffman_tree(freqs)
        >>> codes = generate_codes(root)
        >>> codes['f']  # Most frequent character gets the shortest code
        '0'
    """
    if code_map is None:
        code_map = {}

    if node is None:
        return code_map

    # Leaf node: store the code for this character
    if node.char is not None:
        # If the tree has only one node (single char), assign code "0"
        code_map[node.char] = prefix if prefix else "0"
        return code_map

    # Traverse left (append '0') and right (append '1')
    generate_codes(node.left, prefix + "0", code_map)
    generate_codes(node.right, prefix + "1", code_map)

    return code_map


# ---------------------------------------------------------------------------
# Step 4: Encode text using the generated codes
# ---------------------------------------------------------------------------

def encode(text: str, code_map: dict[str, str]) -> str:
    """Encode a string into a binary bit string using Huffman codes.

    Each character in the input is replaced by its corresponding Huffman code.

    Args:
        text: The plaintext string to encode.
        code_map: A dictionary mapping characters to their Huffman codes.

    Returns:
        A string of '0' and '1' bits representing the encoded data.

    Raises:
        ValueError: If a character in the text is not present in the code map.

    Example:
        >>> codes = {'a': '0', 'b': '10', 'c': '11'}
        >>> encode("abc", codes)
        '01011'
    """
    encoded_bits = []
    for char in text:
        if char not in code_map:
            raise ValueError(f"Character '{char}' not found in Huffman code map. "
                             f"Ensure the code map was built from the same alphabet.")
        encoded_bits.append(code_map[char])
    return "".join(encoded_bits)


# ---------------------------------------------------------------------------
# Step 5: Decode a bit string using the Huffman tree
# ---------------------------------------------------------------------------

def decode(encoded_bits: str, root: HuffmanNode) -> str:
    """Decode a binary bit string back to the original text using the Huffman tree.

    Starting from the root, each '0' bit moves to the left child and each '1'
    bit moves to the right child. When a leaf is reached, the character is
    appended to the output and traversal resets to the root.

    Args:
        encoded_bits: A string of '0' and '1' bits to decode.
        root: The root node of the Huffman tree used for encoding.

    Returns:
        The decoded plaintext string.

    Raises:
        ValueError: If the bit string leads to an invalid traversal (e.g.,
                    hitting a None child or not ending on a leaf).

    Example:
        >>> freqs = {'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45}
        >>> root = build_huffman_tree(freqs)
        >>> encode("abc", root)  # doctest: +SKIP
        '...'
    """
    if root is None:
        return ""

    decoded_chars = []
    current = root

    # Edge case: tree with only one character (left leaf only)
    if root.char is not None:
        # This shouldn't happen in a properly built tree, but handle gracefully
        return root.char * len(encoded_bits)

    for bit in encoded_bits:
        # Navigate the tree based on the current bit
        if bit == "0":
            current = current.left
        elif bit == "1":
            current = current.right
        else:
            raise ValueError(f"Invalid bit '{bit}' in encoded data. "
                             f"Encoded string must contain only '0' and '1'.")

        if current is None:
            raise ValueError("Encoded bit string is invalid — reached a null node "
                             "during traversal. The data may be corrupted.")

        # If we've reached a leaf, record the character and reset to root
        if current.char is not None:
            decoded_chars.append(current.char)
            current = root

    # After processing all bits, we must be back at the root (i.e., we ended on a leaf)
    if current != root:
        raise ValueError("Encoded bit string ended mid-code — incomplete final character.")

    return "".join(decoded_chars)


# ---------------------------------------------------------------------------
# Step 6: Calculate compression statistics
# ---------------------------------------------------------------------------

def compression_stats(original_text: str, encoded_bits: str, code_map: dict[str, str]) -> dict:
    """Calculate compression statistics for the encoded data.

    Args:
        original_text: The original plaintext string.
        encoded_bits: The encoded binary string.
        code_map: The Huffman code mapping used.

    Returns:
        A dictionary with compression statistics including:
          - original_size_bits: Size of original text in bits (8 bits per char)
          - encoded_size_bits:  Size of encoded data in bits
          - compression_ratio:  Ratio of encoded size to original size
          - space_saved_pct:    Percentage of space saved
          - code_table:         The Huffman code mapping
    """
    original_bits = len(original_text) * 8  # 8 bits per ASCII character
    encoded_bit_count = len(encoded_bits)
    ratio = encoded_bit_count / original_bits if original_bits > 0 else 0
    saved = (1 - ratio) * 100 if original_bits > 0 else 0

    return {
        "original_size_bits": original_bits,
        "encoded_size_bits": encoded_bit_count,
        "compression_ratio": round(ratio, 4),
        "space_saved_pct": round(saved, 2),
        "code_table": code_map,
    }


# ---------------------------------------------------------------------------
# Main example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Sample text for demonstration
    sample_text = "huffman coding is a greedy algorithm used for lossless data compression"

    print("=" * 60)
    print("HUFFMAN CODING DEMONSTRATION")
    print("=" * 60)

    # Step 1: Count character frequencies
    print("\n--- Step 1: Frequency Counting ---")
    frequencies = count_frequencies(sample_text)
    print(f"Input text: \"{sample_text}\"")
    print(f"Text length: {len(sample_text)} characters")
    print(f"Unique characters: {len(frequencies)}")
    print("Frequencies:")
    for char, freq in sorted(frequencies.items(), key=lambda x: (-x[1], x[0])):
        display_char = repr(char) if char != " " else "' '"
        print(f"  {display_char}: {freq}")

    # Step 2: Build the Huffman tree
    print("\n--- Step 2: Building Huffman Tree ---")
    huffman_tree = build_huffman_tree(frequencies)
    print(f"Tree root frequency: {huffman_tree.freq}")

    # Step 3: Generate Huffman codes
    print("\n--- Step 3: Generating Huffman Codes ---")
    huffman_codes = generate_codes(huffman_tree)
    print("Character codes (sorted by code length, then alphabetically):")
    for char, code in sorted(huffman_codes.items(), key=lambda x: (len(x[1]), x[0])):
        display_char = repr(char) if char != " " else "' '"
        print(f"  {display_char}: {code}")

    # Step 4: Encode the text
    print("\n--- Step 4: Encoding ---")
    encoded = encode(sample_text, huffman_codes)
    print(f"Encoded bit string ({len(encoded)} bits):")
    # Show the encoded string in chunks for readability
    chunk_size = 8
    chunks = [encoded[i:i + chunk_size] for i in range(0, len(encoded), chunk_size)]
    print("  " + " ".join(chunks))

    # Step 5: Decode the bit string
    print("\n--- Step 5: Decoding ---")
    decoded = decode(encoded, huffman_tree)
    print(f"Decoded text: \"{decoded}\"")
    print(f"Decoding successful: {decoded == sample_text}")

    # Step 6: Compression statistics
    print("\n--- Step 6: Compression Statistics ---")
    stats = compression_stats(sample_text, encoded, huffman_codes)
    print(f"Original size:     {stats['original_size_bits']} bits ({len(sample_text)} chars × 8 bits)")
    print(f"Encoded size:      {stats['encoded_size_bits']} bits")
    print(f"Compression ratio: {stats['compression_ratio']:.4f} ({stats['compression_ratio'] * 100:.2f}% of original)")
    print(f"Space saved:       {stats['space_saved_pct']:.2f}%")

    # Additional example with a simpler string
    print("\n" + "=" * 60)
    print("ADDITIONAL EXAMPLE: 'abracadabra'")
    print("=" * 60)

    simple_text = "abracadabra"
    simple_freqs = count_frequencies(simple_text)
    simple_tree = build_huffman_tree(simple_freqs)
    simple_codes = generate_codes(simple_tree)
    simple_encoded = encode(simple_text, simple_codes)
    simple_decoded = decode(simple_encoded, simple_tree)

    print(f"\nFrequencies: {dict(sorted(simple_freqs.items()))}")
    print(f"Codes: {simple_codes}")
    print(f"Encoded: {simple_encoded} ({len(simple_encoded)} bits)")
    print(f"Decoded: \"{simple_decoded}\"")
    print(f"Match: {simple_decoded == simple_text}")

    simple_stats = compression_stats(simple_text, simple_encoded, simple_codes)
    print(f"Compression ratio: {simple_stats['compression_ratio']:.4f}")
    print(f"Space saved: {simple_stats['space_saved_pct']:.2f}%")
