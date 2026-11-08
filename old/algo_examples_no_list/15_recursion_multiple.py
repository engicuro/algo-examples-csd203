# 15_recursion_multiple.py
# Multiple recursion examples: Pascal's triangle and combination calculation.
# "Multiple recursion" means a function calls itself more than twice,
# or calls multiple different recursive functions.
#
# Key ideas:
#   - Pascal's triangle: each number is the sum of the two numbers above it.
#   - Combinations (n choose k): C(n,k) = C(n-1,k-1) + C(n-1,k).
#   - Both have multiple recursive calls per function invocation.


# ---- Pascal's Triangle ----

def pascal_row(row_index):
    """Return one row of Pascal's triangle as a tuple.

    Row 0: (1,)
    Row 1: (1, 1)
    Row 2: (1, 2, 1)
    Row 3: (1, 3, 3, 1)
    Row 4: (1, 4, 6, 4, 1)

    Each element is a combination: row[n][k] = C(n, k).
    """
    # Base case: the first row is always (1,).
    if row_index == 0:
        return (1,)

    # Base case: the second row is always (1, 1).
    if row_index == 1:
        return (1, 1)

    # Recursive case: build this row from the previous row.
    prev_row = pascal_row(row_index - 1)
    print("  Building row %d from row %d: %s" % (row_index, row_index - 1, prev_row))

    # Start every row with 1.
    current_row = (1,)

    # Each middle element is the sum of the two elements above it.
    i = 1
    while i < row_index:
        left = prev_row[i - 1]
        right = prev_row[i] if i < len(prev_row) else 0
        current_row = current_row + (left + right,)
        i = i + 1

    # End every row with 1.
    current_row = current_row + (1,)
    return current_row


def print_pascal_triangle(num_rows):
    """Print Pascal's triangle with num_rows rows."""
    print("Pascal's Triangle (%d rows):" % num_rows)
    row_num = 0
    while row_num < num_rows:
        row = pascal_row(row_num)
        # Convert each number to a string and join with spaces.
        row_str = ""
        for num in row:
            row_str = row_str + str(num) + " "
        print("  " + row_str.strip())
        row_num = row_num + 1


# ---- Combination (n choose k) ----

def combination(n, k):
    """Return C(n, k) = the number of ways to choose k items from n.

    Formula:
      C(n, k) = C(n-1, k-1) + C(n-1, k)
      C(n, 0) = 1
      C(n, n) = 1
      C(n, k) = 0  if k > n

    This is the same recurrence as Pascal's triangle!
    """
    # Base cases
    if k > n:
        return 0
    if k == 0:
        return 1
    if k == n:
        return 1

    # Recursive case: C(n, k) = C(n-1, k-1) + C(n-1, k)
    # This makes TWO recursive calls, so it is multiple recursion.
    print("  C(%d, %d) = C(%d, %d) + C(%d, %d)" % (n, k, n - 1, k - 1, n - 1, k))
    result = combination(n - 1, k - 1) + combination(n - 1, k)
    print("  C(%d, %d) -> %d" % (n, k, result))
    return result


if __name__ == "__main__":
    print("=== Pascal's Triangle ===")
    print_pascal_triangle(6)

    print("\n=== Combination (n choose k) ===")
    print("C(5, 2) =", combination(5, 2))
    print()
    print("C(4, 2) =", combination(4, 2))
    print()
    print("C(6, 3) =", combination(6, 3))
