"""
54_run_length_encoding.py - Run-Length Encoding
==========================================================

Run-length encoding (RLE) is a simple compression algorithm
that replaces consecutive repeated characters with a count
and the character.

Example:
  "AAABBBCCCDA" → "3A3B3C1D1A"
  "AAAA"        → "4A"
  "ABCD"        → "1A1B1C1D"  (no compression — can actually get bigger!)

RLE works best when the data has many repeated characters
(e.g., simple graphics, sparse data, or binary images).

This implementation handles:
  - Encoding: compress a string using RLE.
  - Decoding: decompress an RLE-encoded string back to the original.
  - Compression ratio calculation.
"""


def rle_encode(text):
    """Compress a string using run-length encoding.

    Consecutive repeated characters are replaced with
    a count followed by the character.

    Example: "AAABBBCC" → "3A3B2C"

    Args:
        text: The input string to compress.

    Returns:
        The run-length encoded string.
    """
    if len(text) == 0:
        return ""

    encoded = ""
    current_char = text[0]
    count = 1

    # Walk through the text starting from the second character
    for i in range(1, len(text)):
        if text[i] == current_char:
            # Same character as before — increment count
            count = count + 1
        else:
            # Different character — write the run and start a new one
            encoded = encoded + str(count) + current_char
            current_char = text[i]
            count = 1

    # Don't forget the last run
    encoded = encoded + str(count) + current_char

    return encoded


def rle_decode(encoded):
    """Decompress a run-length encoded string.

    Reads pairs of (count, character) and expands them.

    Example: "3A3B2C" → "AAABBBCC"

    Args:
        encoded: The run-length encoded string.

    Returns:
        The decoded original string.
    """
    if len(encoded) == 0:
        return ""

    decoded = ""
    count_str = ""

    for i in range(len(encoded)):
        char = encoded[i]

        if char.isdigit():
            # Accumulate digits to form the count
            count_str = count_str + char
        else:
            # Non-digit character — this is the character to repeat
            count = int(count_str)
            decoded = decoded + (char * count)
            count_str = ""  # Reset for the next run

    return decoded


def print_comparison(original, encoded):
    """Print a side-by-side comparison of original and encoded strings.

    Args:
        original: The original string.
        encoded: The run-length encoded string.
    """
    original_size = len(original)
    encoded_size = len(encoded)

    if original_size == 0:
        ratio = 0.0
    else:
        ratio = (1 - encoded_size / original_size) * 100

    print("  Original: \"{}\" ({} characters)".format(original, original_size))
    print("  Encoded:  \"{}\" ({} characters)".format(encoded, encoded_size))

    if ratio > 0:
        print("  Compression: {:.1f}% smaller".format(ratio))
    elif ratio < 0:
        print("  Expansion: {:.1f}% larger (RLE made it bigger!)".format(abs(ratio)))
    else:
        print("  Same size (no change)")


if __name__ == "__main__":
    print("=" * 50)
    print("  Run-Length Encoding — Educational Demo")
    print("=" * 50)

    # --- Example 1: Text with many repeats ---
    print("\n--- Example 1: Text with many repeats (good for RLE) ---")
    text1 = "AAABBBCCCDDDDDEEE"
    print_comparison(text1, rle_encode(text1))
    decoded1 = rle_decode(rle_encode(text1))
    print("  Decoded: \"{}\"".format(decoded1))
    print("  Decoding correct: {}".format(decoded1 == text1))

    # --- Example 2: Text with no repeats ---
    print("\n--- Example 2: Text with no repeats (RLE makes it bigger) ---")
    text2 = "ABCDEFG"
    print_comparison(text2, rle_encode(text2))
    decoded2 = rle_decode(rle_encode(text2))
    print("  Decoded: \"{}\"".format(decoded2))
    print("  Decoding correct: {}".format(decoded2 == text2))

    # --- Example 3: Mixed text ---
    print("\n--- Example 3: Mixed text (some repeats, some not) ---")
    text3 = "AAAABBBCCDAA"
    print_comparison(text3, rle_encode(text3))
    decoded3 = rle_decode(rle_encode(text3))
    print("  Decoded: \"{}\"".format(decoded3))
    print("  Decoding correct: {}".format(decoded3 == text3))

    # --- Example 4: Simple graphics-like data ---
    print("\n--- Example 4: Simple grid-like data ---")
    text4 = "WWWWWWWWWWBBBWWWWWWWWWWWWBBBWWWWWWWWWWWWWW"
    print_comparison(text4, rle_encode(text4))
    decoded4 = rle_decode(rle_encode(text4))
    print("  Decoded: \"{}\"".format(decoded4))
    print("  Decoding correct: {}".format(decoded4 == text4))

    # --- Example 5: Single character ---
    print("\n--- Example 5: Single character ---")
    text5 = "A"
    print_comparison(text5, rle_encode(text5))
    decoded5 = rle_decode(rle_encode(text5))
    print("  Decoded: \"{}\"".format(decoded5))
    print("  Decoding correct: {}".format(decoded5 == text5))

    # --- Example 6: Empty string ---
    print("\n--- Example 6: Empty string ---")
    text6 = ""
    encoded6 = rle_encode(text6)
    print("  Original: \"{}\" (0 characters)".format(text6))
    print("  Encoded:  \"{}\" ({} characters)".format(encoded6, len(encoded6)))
    decoded6 = rle_decode(encoded6)
    print("  Decoded: \"{}\"".format(decoded6))
    print("  Decoding correct: {}".format(decoded6 == text6))

    # --- Summary ---
    print("\n" + "=" * 50)
    print("  Summary")
    print("=" * 50)
    print("""
Run-length encoding:
  + Very simple to understand and implement.
  + Fast — O(n) time for both encoding and decoding.
  + Works well for data with long runs of repeated values.
    (e.g., simple images, sparse data, binary raster graphics)

  - Can make data BIGGER if there are few repeats.
  - Only compresses runs of the same character.
  - Not suitable for complex text or diverse data.

RLE is often used as part of more complex compression
pipelines (e.g., in PNG images, where filter + RLE is
applied before the main compression step).
""")
