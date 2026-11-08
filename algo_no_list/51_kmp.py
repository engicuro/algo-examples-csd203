"""
51_kmp.py - KMP (Knuth-Morris-Pratt) Pattern Matching
========================================================

The KMP algorithm searches for a pattern in a text efficiently
by avoiding unnecessary comparisons.

Key idea:
  When a mismatch occurs, KMP uses information from the pattern
  itself to skip ahead.  It knows how much of the pattern we
  have already matched, so it doesn't go back in the text.

How it works in two phases:
  Phase 1 — Build the "failure function" (also called the
            "partial match table" or "prefix function").
            This tells us: if we mismatch at position j in the
            pattern, where should we resume matching?

  Phase 2 — Use the failure function to scan the text in one
            pass without backtracking.

Time complexity:  O(n + m)
  n = length of the text
  m = length of the pattern

This is much faster than brute force O(n * m) for long texts.
"""


def build_failure_function(pattern):
    """Build the KMP failure function (partial match table).

    The failure function tells us: if we mismatch at position j
    in the pattern, the next position to try matching is
    failure[j].  This avoids re-checking characters we already
    know match.

    How it works:
      - failure[0] is always 0 (no proper prefix for a single char).
      - For each position j > 0, we find the length of the longest
        proper prefix of pattern[0..j] that is also a suffix.

    Example:
      pattern = "ABABC"
      failure  = {0: 0, 1: 0, 2: 1, 3: 2, 4: 0}

      At position 3 ("ABAB"), the longest prefix that is also a
      suffix is "AB" (length 2), so failure[3] = 2.

    Args:
        pattern: The pattern string.

    Returns:
        A dict of integers (the failure function).
    """
    m = len(pattern)
    failure = {}

    # j tracks the length of the current matching prefix
    j = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[j]:
            # Characters match — extend the prefix length
            j += 1
            failure[i] = j
            i += 1
        else:
            if j > 0:
                # Mismatch — fall back to the previous best prefix
                # This is the key insight: we don't need to restart
                # from 0; we reuse what we already matched.
                j = failure[j - 1]
            else:
                # No prefix to fall back to
                failure[i] = 0
                i += 1

    return failure


def kmp_search(text, pattern):
    """Search for all occurrences of ``pattern`` in ``text`` using KMP.

    Args:
        text: The text string to search in.
        pattern: The pattern string to search for.

    Returns:
        A tuple of starting positions where the pattern was found.
    """
    n = len(text)
    m = len(pattern)
    positions = ()

    # Build the failure function first
    failure = build_failure_function(pattern)

    print("Pattern: \"{}\"".format(pattern))
    print("Failure function: {}".format(failure))
    print("-" * 50)

    # Scan through the text
    i = 0  # Position in text
    j = 0  # Position in pattern

    while i < n:
        print("  i={}, j={}: comparing text[{}]='{}' with pattern[{}]='{}'".format(
            i, j, i, text[i], j, pattern[j]))

        if text[i] == pattern[j]:
            # Characters match — advance both pointers
            i += 1
            j += 1

            if j == m:
                # Full pattern matched!
                start_pos = i - j
                print("  *** Full match found at position {}! ***".format(start_pos))
                positions = positions + (start_pos,)
                # Use failure function to continue searching
                j = failure[j - 1]
        else:
            # Mismatch
            if j > 0:
                # Use failure function to skip ahead in the pattern
                # We don't move i back — that's the key advantage of KMP!
                print("    Mismatch — fall back pattern pointer j: {} -> {}".format(
                    j, failure[j - 1]))
                j = failure[j - 1]
            else:
                # j is already 0, just move to the next character in text
                print("    Mismatch at j=0 — advance text pointer i")
                i += 1

    return positions


if __name__ == "__main__":
    print("=" * 50)
    print("  KMP Algorithm — Educational Demo")
    print("=" * 50)

    # --- Example 1: Pattern found ---
    print("\n--- Example 1: Pattern found ---")
    text1 = "ABABABCABABABC"
    pattern1 = "ABABC"
    print("Text: \"{}\"".format(text1))
    result1 = kmp_search(text1, pattern1)
    print("\nResult: pattern found at positions {}".format(result1))

    # --- Example 2: Pattern found multiple times ---
    print("\n" + "=" * 50)
    print("  Example 2: Pattern found multiple times ---")
    text2 = "AAAAAA"
    pattern2 = "AAA"
    print("Text: \"{}\"".format(text2))
    result2 = kmp_search(text2, pattern2)
    print("\nResult: pattern found at positions {}".format(result2))

    # --- Example 3: Pattern not found ---
    print("\n" + "=" * 50)
    print("  Example 3: Pattern not found ---")
    text3 = "HELLO WORLD"
    pattern3 = "XYZ"
    print("Text: \"{}\"".format(text3))
    result3 = kmp_search(text3, pattern3)
    print("\nResult: pattern found at positions {}".format(result3))

    # --- Example 4: Show failure function in detail ---
    print("\n" + "=" * 50)
    print("  Example 4: Failure function for 'ABABCABAB' ---")
    pattern4 = "ABABCABAB"
    failure4 = build_failure_function(pattern4)
    print("Pattern:      \"{}\"".format(pattern4))
    print("Failure func: {}".format(failure4))
    print("""
Explanation of failure function values:
  failure[0] = 0  (single char has no proper prefix)
  failure[1] = 0  "AB" — no prefix is also a suffix
  failure[2] = 1  "ABA" — "A" is both prefix and suffix
  failure[3] = 2  "ABAB" — "AB" is both prefix and suffix
  failure[4] = 0  "ABABC" — no prefix is also a suffix
  failure[5] = 1  "ABABCA" — "A" is both prefix and suffix
  failure[6] = 2  "ABABCAB" — "AB" is both prefix and suffix
  failure[7] = 3  "ABABCABA" — "ABA" is both prefix and suffix
  failure[8] = 4  "ABABCABAB" — "ABAB" is both prefix and suffix
""")

    # --- Summary ---
    print("=" * 50)
    print("  Summary")
    print("=" * 50)
    print("""
KMP avoids re-examining text characters:
  - Build failure function in O(m) time.
  - Search text in O(n) time (never back up in the text).
  - Total: O(n + m) vs brute force O(n * m).

The failure function is the key:
  It tells us how much of the pattern we can reuse
  after a mismatch, so we don't start over from scratch.
""")
