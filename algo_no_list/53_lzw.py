"""
53_lzw.py - LZW Compression
================================

LZW (Lempel-Ziv-Welch) is a dictionary-based compression
algorithm.  It works by building a dictionary of substrings
as it reads the input, then replacing repeated substrings
with short codes.

How it works (encoding):
  1. Start with a dictionary of all single characters.
  2. Read characters one at a time, building up a current string.
  3. If the current string + next character is in the dictionary,
     extend the current string.
  4. If it's NOT in the dictionary:
     a. Output the code for the current string.
     b. Add the current string + next character to the dictionary.
     c. Start a new current string with just the next character.
  5. Repeat until all input is processed.

How it works (decoding):
  1. Start with the same initial dictionary.
  2. Read codes one at a time.
  3. Look up each code in the dictionary to get a string.
  4. Add new entries to the dictionary as you go.

LZW is used in:
  - GIF image format
  - UNIX compress command
  - TIFF image format

This implementation uses simple dictionaries and tuples.
"""


def lzw_encode(text):
    """Compress a string using LZW encoding.

    Uses ASCII codes 0-255 as the initial dictionary
    for all single characters, then builds new entries
    for longer substrings.

    Args:
        text: The input string to compress.

    Returns:
        A tuple of integer codes representing the compressed data.
    """
    # Step 1: Initialize the dictionary with all single ASCII characters
    dictionary = {}
    for i in range(256):
        dictionary[chr(i)] = i
    next_code = 256

    # Step 2: Encode the text
    result = ()
    current = ""  # Current string being built

    for i in range(len(text)):
        char = text[i]
        combined = current + char

        if combined in dictionary:
            # The combined string is in the dictionary — extend current
            current = combined
        else:
            # The combined string is NOT in the dictionary
            # Output the code for the current string
            result = result + (dictionary[current],)

            # Add the combined string to the dictionary
            dictionary[combined] = next_code
            next_code = next_code + 1
            print("  Added to dictionary: '{}' -> code {}".format(combined, dictionary[combined]))

            # Start a new current string with just this character
            current = char

    # Don't forget the last current string
    if current != "":
        result = result + (dictionary[current],)

    return result


def lzw_decode(codes):
    """Decompress a tuple of LZW codes back to the original string.

    Rebuilds the same initial ASCII dictionary and adds
    entries as it decodes.

    Args:
        codes: A tuple of integer codes (from lzw_encode).

    Returns:
        The decoded original string.
    """
    if len(codes) == 0:
        return ""

    # Step 1: Rebuild the initial ASCII dictionary
    dictionary = {}
    for i in range(256):
        dictionary[i] = chr(i)
    next_code = 256

    result = ""
    prev_string = ""

    for i in range(len(codes)):
        code = codes[i]

        # Look up the string for this code
        if code in dictionary:
            current_string = dictionary[code]
        elif code == next_code:
            # Special case: code not yet in dictionary.
            # This happens when a pattern is immediately repeated.
            # The string is prev_string + its first character.
            current_string = prev_string + prev_string[0]
        else:
            print("  ERROR: Invalid code {} encountered!".format(code))
            return ""

        # Add the decoded string to the result
        result = result + current_string

        # Add a new entry to the dictionary (if not the first code)
        if i > 0:
            new_entry = prev_string + current_string[0]
            dictionary[next_code] = new_entry
            next_code = next_code + 1
            print("  Added to dictionary: code {} -> '{}'".format(next_code - 1, new_entry))

        prev_string = current_string

    return result


def print_codes(codes, label):
    """Print a tuple of codes in a readable format.

    Args:
        codes: A tuple of integer codes.
        label: A label to print before the codes.
    """
    print("{}: {}".format(label, codes))
    print("  ({} codes, each stored as an integer)".format(len(codes)))


if __name__ == "__main__":
    print("=" * 50)
    print("  LZW Compression — Educational Demo")
    print("=" * 50)

    # --- Example 1: Simple repeated text ---
    print("\n--- Example 1: Simple repeated text ---")
    text1 = "ABABABA"
    print("Original text: \"{}\"".format(text1))
    print("Original size: {} characters".format(len(text1)))

    print("\n--- Encoding ---")
    encoded1 = lzw_encode(text1)
    print_codes(encoded1, "Encoded")

    print("\n--- Decoding ---")
    decoded1 = lzw_decode(encoded1)
    print("Decoded text: \"{}\"".format(decoded1))
    print("Decoding correct: {}".format(decoded1 == text1))

    # --- Example 2: Text with longer repeated patterns ---
    print("\n" + "=" * 50)
    print("  Example 2: Text with longer repeated patterns ---")
    text2 = "TOBEORNOTTOBEORTOBEORNOT"
    print("Original text: \"{}\"".format(text2))
    print("Original size: {} characters".format(len(text2)))

    print("\n--- Encoding ---")
    encoded2 = lzw_encode(text2)
    print_codes(encoded2, "Encoded")

    print("\n--- Decoding ---")
    decoded2 = lzw_decode(encoded2)
    print("Decoded text: \"{}\"".format(decoded2))
    print("Decoding correct: {}".format(decoded2 == text2))

    # --- Example 3: Single repeated character ---
    print("\n" + "=" * 50)
    print("  Example 3: Single repeated character ---")
    text3 = "AAAAAAA"
    print("Original text: \"{}\"".format(text3))
    print("Original size: {} characters".format(len(text3)))

    print("\n--- Encoding ---")
    encoded3 = lzw_encode(text3)
    print_codes(encoded3, "Encoded")

    print("\n--- Decoding ---")
    decoded3 = lzw_decode(encoded3)
    print("Decoded text: \"{}\"".format(decoded3))
    print("Decoding correct: {}".format(decoded3 == text3))

    # --- Summary ---
    print("\n" + "=" * 50)
    print("  Summary")
    print("=" * 50)
    print("""
LZW compression:
  - Builds a dictionary of substrings on the fly.
  - No need to transmit the dictionary (receiver builds it the same way).
  - Works well when the input has repeated patterns.
  - Used in GIF, TIFF, and UNIX compress.

Key insight:
  Instead of storing individual characters, LZW stores
  entire substrings as single codes.  The more the input
  repeats, the more compression we get.
""")
