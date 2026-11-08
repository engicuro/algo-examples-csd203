"""
50_pattern_brute_force.py - Brute Force Pattern Matching
==========================================================

Brute force pattern matching checks every possible starting
position in the text to see if the pattern matches there.

How it works:
  1. Start at position 0 in the text.
  2. Compare the pattern with the text character by character.
  3. If all characters match, we found the pattern.
  4. If any character doesn't match, move one position to the right
     and try again.
  5. Repeat until we reach the end of the text.

Time complexity:  O(n * m)
  n = length of the text
  m = length of the pattern

This is simple but slow for long texts or patterns.
"""


def brute_force_search(text, pattern):
    """Search for all occurrences of ``pattern`` in ``text``.

    Prints every comparison so you can see exactly what
    the algorithm is doing step by step.

    Args:
        text: The text string to search in.
        pattern: The pattern string to search for.

    Returns:
        A list of starting positions where the pattern was found.
    """
    positions = []
    text_length = len(text)
    pattern_length = len(pattern)

    print("Text:    \"{}\" (length {})".format(text, text_length))
    print("Pattern: \"{}\" (length {})".format(pattern, pattern_length))
    print("-" * 50)

    # Try every possible starting position in the text
    # We only need to check up to position (text_length - pattern_length)
    # because there wouldn't be enough characters left to match.
    for i in range(text_length - pattern_length + 1):
        print("\n  Trying starting position i = {}...".format(i))
        match = True

        # Compare pattern character by character with text starting at i
        for j in range(pattern_length):
            text_char = text[i + j]
            pattern_char = pattern[j]
            print("    Compare text[{}]='{}' with pattern[{}]='{}' -> {}".format(
                i + j, text_char, j, pattern_char,
                "MATCH" if text_char == pattern_char else "DIFFER"))

            if text_char != pattern_char:
                match = False
                break  # No match at this position, try the next one

        if match:
            print("  *** Found pattern at position {}! ***".format(i))
            positions.append(i)
        else:
            print("  No match at position {}.".format(i))

    return positions


if __name__ == "__main__":
    print("=" * 50)
    print("  Brute Force Pattern Matching — Educational Demo")
    print("=" * 50)

    # --- Example 1: Pattern found once ---
    print("\n--- Example 1: Pattern found once ---")
    text1 = "ABABABCABABABC"
    pattern1 = "ABABC"
    result1 = brute_force_search(text1, pattern1)
    print("\nResult: pattern found at positions {}".format(result1))

    # --- Example 2: Pattern found multiple times ---
    print("\n" + "=" * 50)
    print("  Example 2: Pattern found multiple times ---")
    text2 = "AAAAAA"
    pattern2 = "AAA"
    result2 = brute_force_search(text2, pattern2)
    print("\nResult: pattern found at positions {}".format(result2))

    # --- Example 3: Pattern not found ---
    print("\n" + "=" * 50)
    print("  Example 3: Pattern not found ---")
    text3 = "HELLO WORLD"
    pattern3 = "XYZ"
    result3 = brute_force_search(text3, pattern3)
    print("\nResult: pattern found at positions {}".format(result3))

    # --- Example 4: Realistic example ---
    print("\n" + "=" * 50)
    print("  Example 4: Searching for a word in a sentence ---")
    text4 = "the cat sat on the mat the cat"
    pattern4 = "cat"
    result4 = brute_force_search(text4, pattern4)
    print("\nResult: pattern found at positions {}".format(result4))

    # --- Summary ---
    print("\n" + "=" * 50)
    print("  Summary")
    print("=" * 50)
    print("""
Brute force is easy to understand and implement:
  - Try every starting position.
  - At each position, compare character by character.
  - Stop comparing as soon as a mismatch is found.

But it can be slow:
  - Worst case: O(n * m) comparisons.
  - Example: text="AAAA...A" (n chars), pattern="AAA...AB" (m chars).
    At each position we compare m-1 characters before failing.

Better algorithms like KMP avoid re-examining characters
we have already compared, achieving O(n + m) time.
""")
