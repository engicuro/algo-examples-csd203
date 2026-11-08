"""
Knuth-Morris-Pratt (KMP) String Matching Algorithm
===================================================

The KMP algorithm improves upon naive pattern matching by avoiding redundant
comparisons. It preprocesses the pattern to build a "failure function"
(also called the partial match table or prefix function), which tells the
algorithm how far to shift the pattern when a mismatch occurs, without
backtracking in the text.

Time complexity:  O(n + m)  where n = len(text), m = len(pattern)
Space complexity: O(m)      for the failure function table

Reference: Knuth, Morris, Pratt (1977)
"""


def compute_failure_function(pattern: str) -> list[int]:
    """
    Compute the KMP failure function (partial match table) for a pattern.

    The failure function f[i] stores the length of the longest proper
    prefix of pattern[0..i] that is also a suffix of pattern[0..i].

    A "proper" prefix excludes the entire string itself. This table is
    used during matching to determine how far to shift the pattern when
    a mismatch occurs, so that previously matched characters are not
    re-examined.

    Args:
        pattern: The pattern string to preprocess.

    Returns:
        A list of integers where f[i] is the length of the longest proper
        prefix of pattern[0..i] that is also a suffix.

    Example:
        >>> compute_failure_function("ABABC")
        [0, 0, 1, 2, 0]

        # Index 0: "A"       -> no proper prefix/suffix -> 0
        # Index 1: "AB"      -> no common prefix/suffix -> 0
        # Index 2: "ABA"     -> "A" is both prefix and suffix -> 1
        # Index 3: "ABAB"    -> "AB" is both prefix and suffix -> 2
        # Index 4: "ABABC"   -> no common prefix/suffix -> 0
    """
    m = len(pattern)
    failure = [0] * m  # Initialize all entries to 0
    j = 0  # Length of the previous longest prefix-suffix

    # Build the table iteratively from index 1 onwards
    for i in range(1, m):
        # Mismatch: fall back to the previous best prefix length
        while j > 0 and pattern[i] != pattern[j]:
            j = failure[j - 1]

        # If characters match, extend the current prefix-suffix length
        if pattern[i] == pattern[j]:
            j += 1

        failure[i] = j

    return failure


def kmp_search(text: str, pattern: str, verbose: bool = False) -> list[int]:
    """
    Search for all occurrences of a pattern in a text using the KMP algorithm.

    The algorithm uses the failure function to skip unnecessary comparisons.
    When a mismatch occurs at text[i] vs pattern[j], instead of restarting
    from text[i - j + 1], the failure function tells us the next valid
    position in the pattern to compare against, allowing the text pointer
    to advance without backtracking.

    Args:
        text:    The text string to search within.
        pattern: The pattern string to search for.
        verbose: If True, print a step-by-step trace of the matching process.

    Returns:
        A list of starting indices where pattern is found in text.

    Example:
        >>> kmp_search("ABABDABACDABABCABAB", "ABABCABAB")
        [10]
        >>> kmp_search("AAAAAA", "AAA")
        [0, 1, 2, 3]
    """
    n = len(text)
    m = len(pattern)

    # Edge case: empty pattern matches at every position
    if m == 0:
        return list(range(n + 1))

    # Edge case: pattern longer than text can never match
    if m > n:
        return []

    failure = compute_failure_function(pattern)
    matches = []
    j = 0  # Current position in the pattern

    if verbose:
        print(f"Text:    {text!r}")
        print(f"Pattern: {pattern!r}")
        print(f"Failure: {failure}")
        print(f"{'Step':<6} {'i':>4} {'j':>4} {'Comparison':^20} {'Action':<30} {'Match?'}")
        print("-" * 75)

    i = 0  # Current position in the text
    step = 0

    while i < n:
        step += 1
        comparison = f"text[{i}]={text[i]!r} vs pattern[{j}]={pattern[j]!r}"

        if text[i] == pattern[j]:
            # Characters match — advance both pointers
            if verbose:
                print(f"{step:<6} {i:>4} {j:>4} {comparison:^20} {'Advance both i and j':<30} {'✓'}")
            i += 1
            j += 1

            # Full pattern match found
            if j == m:
                start_index = i - m
                matches.append(start_index)
                if verbose:
                    print(f"{'':<6} {'':>4} {'':>4} {'':^20} {'*** MATCH at index ' + str(start_index):<30} {'★'}")
                # Use failure function to continue searching for overlapping matches
                j = failure[j - 1]
        else:
            # Mismatch — use failure function to determine next alignment
            if j > 0:
                fallback = failure[j - 1]
                if verbose:
                    print(f"{step:<6} {i:>4} {j:>4} {comparison:^20} {'Mismatch → fallback j to ' + str(fallback):<30} {'✗'}")
                j = fallback
                # Do NOT advance i — we retry the same text position with a
                # shorter pattern prefix, which is the key insight of KMP.
            else:
                # j == 0 and still no match — simply advance the text pointer
                if verbose:
                    print(f"{step:<6} {i:>4} {j:>4} {comparison:^20} {'Mismatch, j=0 → advance i':<30} {'✗'}")
                i += 1

    if verbose and not matches:
        print(f"\nNo occurrences of {pattern!r} found in {text!r}.")
    elif verbose:
        print(f"\nTotal matches found at indices: {matches}")

    return matches


def kmp_search_first(text: str, pattern: str) -> int:
    """
    Find the first occurrence of a pattern in text using KMP.

    Returns the starting index of the first match, or -1 if not found.
    This is a convenience wrapper that stops after the first match.

    Args:
        text:    The text string to search within.
        pattern: The pattern string to search for.

    Returns:
        The starting index of the first match, or -1 if not found.
    """
    n = len(text)
    m = len(pattern)

    if m == 0:
        return 0
    if m > n:
        return -1

    failure = compute_failure_function(pattern)
    j = 0

    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = failure[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == m:
            return i - m + 1

    return -1


if __name__ == "__main__":
    # ── Example 1: Basic single match ──────────────────────────────────
    print("=" * 60)
    print("Example 1: Basic single match")
    print("=" * 60)
    text1 = "ABABDABACDABABCABAB"
    pattern1 = "ABABCABAB"
    print(f"Text:    {text1!r}")
    print(f"Pattern: {pattern1!r}")
    result1 = kmp_search(text1, pattern1, verbose=True)
    print(f"Result:  Pattern found at indices: {result1}\n")

    # ── Example 2: Multiple overlapping matches ─────────────────────────
    print("=" * 60)
    print("Example 2: Multiple overlapping matches")
    print("=" * 60)
    text2 = "AAAAAA"
    pattern2 = "AAA"
    print(f"Text:    {text2!r}")
    print(f"Pattern: {pattern2!r}")
    result2 = kmp_search(text2, pattern2, verbose=True)
    print(f"Result:  Pattern found at indices: {result2}\n")

    # ── Example 3: No match ─────────────────────────────────────────────
    print("=" * 60)
    print("Example 3: No match")
    print("=" * 60)
    text3 = "HELLO WORLD"
    pattern3 = "XYZ"
    print(f"Text:    {text3!r}")
    print(f"Pattern: {pattern3!r}")
    result3 = kmp_search(text3, pattern3, verbose=True)
    print(f"Result:  Pattern found at indices: {result3}\n")

    # ── Example 4: Failure function visualization ──────────────────────
    print("=" * 60)
    print("Example 4: Failure function computation")
    print("=" * 60)
    patterns = ["ABABCABAB", "AABAACAABAA", "ABCDEF", "AAAA", "ABABACA"]
    for p in patterns:
        fail = compute_failure_function(p)
        print(f"  Pattern: {p!r}")
        print(f"  Failure: {fail}")
        # Show the reasoning for each position
        for idx, val in enumerate(fail):
            prefix = p[:idx + 1]
            if val > 0:
                print(f"    f[{idx}] ({prefix!r}): longest proper prefix-suffix = {prefix[:val]!r} (length {val})")
            else:
                print(f"    f[{idx}] ({prefix!r}): no proper prefix-suffix → 0")
        print()

    # ── Example 5: First-occurrence convenience function ────────────────
    print("=" * 60)
    print("Example 5: First occurrence (kmp_search_first)")
    print("=" * 60)
    text5 = "The quick brown fox jumps over the lazy dog"
    pattern5 = "the"
    # Case-sensitive search
    idx5 = kmp_search_first(text5, pattern5)
    print(f"Text:    {text5!r}")
    print(f"Pattern: {pattern5!r}")
    print(f"First occurrence at index: {idx5}")

    # ── Example 6: Real-world use case — finding repeated substrings ───
    print("=" * 60)
    print("Example 6: Finding all occurrences of a word in a sentence")
    print("=" * 60)
    text6 = "the cat sat on the mat with the hat"
    pattern6 = "the"
    result6 = kmp_search(text6, pattern6)
    print(f"Text:    {text6!r}")
    print(f"Pattern: {pattern6!r}")
    print(f"Occurrences at indices: {result6}")
    for idx in result6:
        print(f"  → Found at index {idx}: ...{text6[max(0, idx-3):idx+len(pattern6)+3]}...")
