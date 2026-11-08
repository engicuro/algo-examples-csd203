"""
Brute Force Pattern Matching
=============================

Implements the brute force (naive) string pattern matching algorithm.

The algorithm checks every possible starting position in the text where the
pattern could fit, comparing character by character.

Time Complexity:  O(n * m)  where n = len(text), m = len(pattern)
Space Complexity: O(1)      (no extra space beyond the result list)

This is the simplest pattern matching approach and serves as a baseline
for understanding more efficient algorithms like KMP, Rabin-Karp, or Boyer-Moore.
"""


def brute_force_search(text: str, pattern: str) -> list[int]:
    """Find all occurrences of `pattern` in `text` using brute force.

    Args:
        text: The string to search within.
        pattern: The substring to search for.

    Returns:
        A list of starting indices where `pattern` is found in `text`.
        Returns an empty list if the pattern is empty, longer than the text,
        or not found.

    Examples:
        >>> brute_force_search("ababcabcabababd", "ababd")
        [10]
        >>> brute_force_search("aaaaa", "aa")
        [0, 1, 2, 3]
        >>> brute_force_search("hello world", "xyz")
        []
    """
    n = len(text)
    m = len(pattern)
    matches = []

    # Edge case: empty pattern or pattern longer than text
    if m == 0 or m > n:
        return matches

    # Iterate over every valid starting position in text.
    # The last valid start index is n - m (inclusive), because the pattern
    # of length m must fully fit within the remaining text.
    for i in range(n - m + 1):
        # Check if pattern matches text starting at position i
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1

        # If we matched all characters of the pattern, record the position
        if j == m:
            matches.append(i)

    return matches


def brute_force_search_first(text: str, pattern: str) -> int:
    """Find the first occurrence of `pattern` in `text` using brute force.

    Args:
        text: The string to search within.
        pattern: The substring to search for.

    Returns:
        The index of the first match, or -1 if not found.

    Examples:
        >>> brute_force_search_first("hello world", "world")
        6
        >>> brute_force_search_first("hello world", "xyz")
        -1
    """
    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return -1

    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i

    return -1


def _visualize_match(text: str, pattern: str, position: int) -> str:
    """Create a visual alignment showing where the pattern matches in the text.

    Args:
        text: The full text string.
        pattern: The pattern that was found.
        position: The starting index of the match.

    Returns:
        A formatted string showing the text, a caret line, and the pattern
        aligned at the match position.
    """
    # Build the caret line that points to the match start
    caret_line = " " * position + "^"
    # Build the pattern line aligned at the match position
    pattern_line = " " * position + pattern

    return f"  Text:    {text}\n  Caret:   {caret_line}\n  Pattern: {pattern_line}"


if __name__ == "__main__":
    # ── Example 1: Basic single match ──────────────────────────────────
    text1 = "hello world, welcome to the world"
    pattern1 = "world"
    print("=" * 60)
    print("Example 1: Basic single match")
    print(f"  Text:    '{text1}'")
    print(f"  Pattern: '{pattern1}'")
    positions1 = brute_force_search(text1, pattern1)
    print(f"  Matches found at indices: {positions1}")
    for pos in positions1:
        print(_visualize_match(text1, pattern1, pos))

    # ── Example 2: Multiple overlapping matches ─────────────────────────
    text2 = "aaaaaa"
    pattern2 = "aaa"
    print("\n" + "=" * 60)
    print("Example 2: Multiple overlapping matches")
    print(f"  Text:    '{text2}'")
    print(f"  Pattern: '{pattern2}'")
    positions2 = brute_force_search(text2, pattern2)
    print(f"  Matches found at indices: {positions2}")
    for pos in positions2:
        print(_visualize_match(text2, pattern2, pos))

    # ── Example 3: No match found ──────────────────────────────────────
    text3 = "abcdefg"
    pattern3 = "xyz"
    print("\n" + "=" * 60)
    print("Example 3: No match found")
    print(f"  Text:    '{text3}'")
    print(f"  Pattern: '{pattern3}'")
    positions3 = brute_force_search(text3, pattern3)
    print(f"  Matches found at indices: {positions3}")

    # ── Example 4: Edge cases ──────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Example 4: Edge cases")

    # Empty pattern
    print(f"  Empty pattern in 'test': {brute_force_search('test', '')}")

    # Pattern longer than text
    print(f"  Pattern longer than text: {brute_force_search('hi', 'hello')}")

    # Exact match (pattern == text)
    print(f"  Exact match: {brute_force_search('abc', 'abc')}")

    # First-occurrence variant
    print(f"  First occurrence of 'test' in 'test test test': "
          f"{brute_force_search_first('test test test', 'test')}")

    # ── Example 5: Complexity demonstration ─────────────────────────────
    print("\n" + "=" * 60)
    print("Example 5: Complexity demonstration")
    print("  The outer loop runs (n - m + 1) times.")
    print("  The inner loop runs up to m times per position.")
    print("  Worst case: O(n * m) — e.g., text='aaa...a', pattern='aa...ab'")
    print("  Best case:  O(n)   — e.g., first char of pattern never matches")

    # Demonstrate worst-case scenario
    import time

    n = 10000
    m = 500
    worst_case_text = "a" * n
    worst_case_pattern = "a" * (m - 1) + "b"  # almost matches everywhere

    start = time.perf_counter()
    result = brute_force_search(worst_case_text, worst_case_pattern)
    elapsed = time.perf_counter() - start

    print(f"\n  Worst-case test: n={n}, m={m}")
    print(f"  Matches found: {len(result)}")
    print(f"  Time elapsed:  {elapsed:.6f} seconds")
