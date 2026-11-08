"""
53_lzw.py - LZW (Lempel-Ziv-Welch) Compression Algorithm

LZW is a lossless data compression algorithm that builds a dictionary of
substrings encountered in the input. It replaces repeated occurrences with
shorter dictionary codes, achieving compression without prior knowledge
of the data statistics.

Topics covered:
  - Dictionary-based compression concept
  - LZW encoding (compression)
  - LZW decoding (decompression)
  - Clear explanation of how the dictionary grows and is used

Reference:
  - Welch, T.A. (1984). "A Technique for High-Performance Data Compression"
    IEEE Computer, 17(6), pp. 8–19.
"""

from typing import Dict, List


def lzw_encode(data: str) -> List[int]:
    """Compress a string using the LZW algorithm.

    Builds a dictionary mapping substrings to integer codes. Starts with
    all single-character entries, then extends the dictionary on-the-fly
    as new substrings are encountered.

    Algorithm:
      1. Initialize dictionary with all single characters (code 0..n-1).
      2. Set current string `w` to the first input character.
      3. For each subsequent character `c`:
           - If `w + c` is in the dictionary, extend `w` to `w + c`.
           - Otherwise:
               * Output the code for `w`.
               * Add `w + c` to the dictionary with the next available code.
               * Reset `w` to `c`.
      4. After the loop, output the code for the remaining `w`.

    Args:
        data: The input string to compress.

    Returns:
        A list of integer codes representing the compressed data.
    """
    # Build the initial dictionary from all unique single characters.
    # Each character maps to its own ordinal value (or a sequential code).
    # Using ord() values as initial codes keeps the dictionary aligned
    # with the character set.
    dict_size = 256  # Standard ASCII range
    dictionary: Dict[str, int] = {chr(i): i for i in range(dict_size)}

    result: List[int] = []
    w = ""  # Current accumulating substring

    for c in data:
        wc = w + c
        if wc in dictionary:
            # The combined string is already known — extend the match.
            w = wc
        else:
            # Output the code for the longest known prefix `w`.
            result.append(dictionary[w])
            # Add the new substring `wc` to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            # Start a new match with the current character.
            w = c

    # Output the code for the final accumulated substring.
    if w:
        result.append(dictionary[w])

    return result


def lzw_decode(compressed: List[int]) -> str:
    """Decompress a list of LZW codes back into the original string.

    Rebuilds the same dictionary that the encoder used, entry by entry,
    so that each code can be translated back into its original substring.

    Algorithm:
      1. Initialize dictionary with all single characters (code 0..n-1).
      2. Read the first code `prev` and output its string.
      3. For each subsequent code `code`:
           - If `code` is in the dictionary, set `entry = dictionary[code]`.
           - Else (the special case where code == dict_size):
               * `entry = dictionary[prev] + dictionary[prev][0]`
               * (This handles the case where the encoder just added a
                 new entry and the decoder hasn't added it yet.)
           - Output `entry`.
           - Add `dictionary[prev] + entry[0]` to the dictionary.
           - Set `prev = code`.

    Args:
        compressed: A list of integer codes produced by lzw_encode().

    Returns:
        The decompressed original string.

    Raises:
        ValueError: If the compressed list is empty.
    """
    if not compressed:
        return ""

    dict_size = 256  # Must match the encoder's initial dictionary size
    dictionary: Dict[int, str] = {i: chr(i) for i in range(dict_size)}

    # The first code always maps directly to a single character.
    prev = compressed[0]
    result = dictionary[prev]

    for code in compressed[1:]:
        if code in dictionary:
            # Standard case: code is already in the dictionary.
            entry = dictionary[code]
        elif code == dict_size:
            # Edge case: the encoder just added this entry and the
            # decoder hasn't caught up yet. The entry is prev_string
            # repeated with its own first character.
            entry = dictionary[prev] + dictionary[prev][0]
        else:
            raise ValueError(f"Invalid compressed code {code} at position "
                             f"{len(result)}.")

        result += entry

        # Add the new entry to the dictionary: prev_string + entry[0].
        # This mirrors the encoder's dictionary growth.
        dictionary[dict_size] = dictionary[prev] + entry[0]
        dict_size += 1

        prev = code

    return result


def demonstrate_encoding() -> None:
    """Show step-by-step LZW encoding of a sample string."""
    text = "TOBEORNOTTOBEORTOBEORNOT"
    print(f"Original text:  \"{text}\"")
    print(f"Length:         {len(text)} characters")

    encoded = lzw_encode(text)
    print(f"\nEncoded codes:  {encoded}")
    print(f"Code count:     {len(encoded)}")

    # Calculate compression ratio
    original_bits = len(text) * 8  # 8 bits per ASCII char
    # Each code uses dict_size bits; estimate with 12-bit codes (common)
    compressed_bits = len(encoded) * 12
    ratio = original_bits / compressed_bits if compressed_bits else 0
    print(f"Original bits:  {original_bits} (8 bits/char × {len(text)} chars)")
    print(f"Compressed bits (est. 12-bit codes): {compressed_bits}")
    print(f"Compression ratio: {ratio:.2f}x")


def demonstrate_decoding() -> None:
    """Show that decoding the encoded output recovers the original."""
    text = "TOBEORNOTTOBEORTOBEORNOT"
    encoded = lzw_encode(text)
    decoded = lzw_decode(encoded)

    print(f"\nEncoded:  {encoded}")
    print(f"Decoded:  \"{decoded}\"")
    print(f"Match:    {decoded == text}")


def demonstrate_dictionary_growth() -> None:
    """Show how the dictionary grows during encoding."""
    text = "ABABABA"
    print(f"\nInput: \"{text}\"")

    # Manually trace through encoding to show dictionary growth
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    result = []
    w = ""

    print(f"\nInitial dictionary size: {dict_size} (all ASCII chars)")
    print(f"{'Step':<6} {'Char':<6} {'w':<8} {'w+c':<10} {'In dict?':<10} {'Action'}")
    print("-" * 55)

    for i, c in enumerate(text):
        wc = w + c
        in_dict = wc in dictionary
        if in_dict:
            action = f"Extend w to '{wc}'"
            w = wc
        else:
            action = f"Output code {dictionary[w]}, add '{wc}'={dict_size}"
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
        print(f"{i+1:<6} {c:<6} {w!r:<8} {wc!r:<10} {str(in_dict):<10} {action}")

    if w:
        result.append(dictionary[w])

    print(f"\nFinal encoded: {result}")
    print(f"Final dictionary size: {dict_size}")


def main() -> None:
    """Run all LZW demonstrations."""
    print("=" * 60)
    print("Chapter 53 — LZW (Lempel-Ziv-Welch) Compression")
    print("=" * 60)

    print("\n--- 1. Encoding Example ---")
    demonstrate_encoding()

    print("\n--- 2. Decoding (Round-trip Verification) ---")
    demonstrate_decoding()

    print("\n--- 3. Dictionary Growth Trace ---")
    demonstrate_dictionary_growth()

    print("\n--- 4. Edge Cases ---")

    # Single character
    single = "A"
    enc = lzw_encode(single)
    dec = lzw_decode(enc)
    print(f"  Single char  \"{single}\" -> {enc} -> \"{dec}\" ✓")

    # Repeated character
    repeated = "AAAAAAA"
    enc = lzw_encode(repeated)
    dec = lzw_decode(enc)
    print(f"  Repeated     \"{repeated}\" -> {enc} -> \"{dec}\" ✓")

    # Empty string
    empty = ""
    enc = lzw_encode(empty)
    print(f"  Empty string -> {enc} (empty list)")
    if enc:
        dec = lzw_decode(enc)
        print(f"  Decoded: \"{dec}\"")
    else:
        print(f"  Decoding skipped (nothing to decode)")


if __name__ == "__main__":
    main()
