def brute_force_match(text, pattern):
    n = len(text)
    m = len(pattern)
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i
    return -1

if __name__ == "__main__":
    t = "ABABDABACDABABCABAB"
    p = "ABABCABAB"
    print("Pattern found at index:", brute_force_match(t, p))
