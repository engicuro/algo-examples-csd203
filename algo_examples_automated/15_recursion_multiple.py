"""
15_recursion_multiple.py
=======================
Recursion Topic: Multiple Recursion

Multiple recursion occurs when a function makes THREE or more recursive
calls per invocation.  The call tree branches into many paths, making
the analysis more complex but the pattern still the same:

  1. Define base case(s) — simplest inputs with direct answers.
  2. Define recursive case(s) — break the problem into multiple
     smaller sub-problems and combine their results.

Examples covered:
  1. Pascal's Triangle — each entry is the sum of the two entries
     above it, naturally expressed with multiple recursion.
  2. Combination (n choose k) — uses the identity C(n,k) = C(n-1,k-1) + C(n-1,k)

Both examples have overlapping subproblems, making them candidates
for memoization.
"""

from typing import List


# ---------------------------------------------------------------------------
# 1. Pascal's Triangle
# ---------------------------------------------------------------------------

def pascal_value(row: int, col: int) -> int:
    """Return the value at position (row, col) in Pascal's Triangle.

    Pascal's Triangle properties:
      - Row 0 is [1]
      - Row n has n+1 elements
      - Each element is the sum of the two elements directly above it
      - The edges are always 1

    Recurrence relation:
      C(row, col) = 1                           if col == 0 or col == row  (base cases)
      C(row, col) = C(row-1, col-1) + C(row-1, col)  (multiple recursion!)

    Args:
        row: The row index (0-based).
        col: The column index (0-based).

    Returns:
        The value at that position in Pascal's Triangle.

    Raises:
        ValueError: If col > row or either is negative.
    """
    # Validate input
    if row < 0 or col < 0:
        raise ValueError(f"Row and column must be non-negative: row={row}, col={col}")
    if col > row:
        raise ValueError(f"Column cannot exceed row: col={col} > row={row}")

    # --- Base cases ---
    # The left and right edges of Pascal's Triangle are always 1.
    # These two base cases stop the recursion.
    if col == 0 or col == row:
        return 1

    # --- Multiple recursion ---
    # Each value is the sum of the two values "above" it in the triangle.
    # This makes TWO recursive calls — multiple recursion!
    # C(row, col) = C(row-1, col-1) + C(row-1, col)
    return pascal_value(row - 1, col - 1) + pascal_value(row - 1, col)


def pascals_triangle(n: int) -> List[List[int]]:
    """Generate the first n rows of Pascal's Triangle using recursion.

    Args:
        n: Number of rows to generate.

    Returns:
        A list of lists, where each inner list is a row of Pascal's Triangle.
    """
    triangle: List[List[int]] = []

    for row in range(n):
        current_row: List[int] = []
        for col in range(row + 1):
            current_row.append(pascal_value(row, col))
        triangle.append(current_row)

    return triangle


def print_pascals_triangle(n: int) -> None:
    """Print Pascal's Triangle with nice formatting."""
    triangle = pascals_triangle(n)
    max_width = len(str(triangle[-1][len(triangle[-1]) // 2])) if triangle else 1
    max_width = max(max_width, 1)

    for row in triangle:
        # Center-align each row
        row_str = " ".join(f"{val:^{max_width}}" for val in row)
        padding = " " * ((n - len(row)) * (max_width + 1) // 2)
        print(f"{padding}{row_str}")


# ---------------------------------------------------------------------------
# 2. Combination (n choose k)
# ---------------------------------------------------------------------------

def combination(n: int, k: int) -> int:
    """Compute C(n, k) — the number of ways to choose k items from n.

    Using the recursive identity:
      C(n, k) = C(n-1, k-1) + C(n-1, k)   (Pascal's identity)

    Base cases:
      C(n, 0) = 1  — choosing 0 items always gives 1 way (the empty set)
      C(n, n) = 1  — choosing all n items gives 1 way
      C(n, k) = 0  if k > n  — impossible to choose more than available

    This is structurally identical to Pascal's Triangle and uses
    multiple recursion (two calls per non-base invocation).

    Args:
        n: Total number of items.
        k: Number of items to choose.

    Returns:
        The binomial coefficient C(n, k).
    """
    # Base cases
    if k < 0 or n < 0:
        return 0
    if k == 0 or k == n:
        return 1
    if k > n:
        return 0

    # Multiple recursion: two calls
    # C(n, k) = C(n-1, k-1) + C(n-1, k)
    return combination(n - 1, k - 1) + combination(n - 1, k)


def combination_memo(n: int, k: int, memo: dict = None) -> int:
    """Memoized version of combination to avoid redundant computation."""
    if memo is None:
        memo = {}

    key = (n, k)
    if key in memo:
        return memo[key]

    if k < 0 or n < 0:
        return 0
    if k == 0 or k == n:
        return 1
    if k > n:
        return 0

    memo[key] = combination_memo(n - 1, k - 1, memo) + combination_memo(n - 1, k, memo)
    return memo[key]


# ---------------------------------------------------------------------------
# 3. Tribonacci (three-way recursion)
# ---------------------------------------------------------------------------

def tribonacci(n: int) -> int:
    """Compute the n-th Tribonacci number using THREE-way recursion.

    Tribonacci extends Fibonacci by summing the previous THREE terms:
      T(0) = 0
      T(1) = 0
      T(2) = 1
      T(n) = T(n-1) + T(n-2) + T(n-3)  for n >= 3

    This is an example of multiple recursion with THREE calls per step.

    Args:
        n: The index in the Tribonacci sequence.

    Returns:
        The n-th Tribonacci number.
    """
    # Base cases
    if n == 0 or n == 1:
        return 0
    if n == 2:
        return 1

    # Multiple recursion: THREE recursive calls!
    return tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n - 3)


if __name__ == "__main__":
    print("=" * 55)
    print("Recursion Example: Multiple Recursion")
    print("=" * 55)

    # --- 1. Pascal's Triangle ---
    print("\n--- 1. Pascal's Triangle (first 7 rows) ---")
    print_pascals_triangle(7)

    print("\n  Individual values (showing multiple recursion):")
    print("  C(4,2) = C(3,1) + C(3,2)")
    print("         = [C(2,0)+C(2,1)] + [C(2,1)+C(2,2)]")
    print("         = [1 + 2] + [2 + 1]")
    print("         = 3 + 3 = 6")
    print(f"  pascal_value(4, 2) = {pascal_value(4, 2)}")
    print(f"  combination(4, 2)  = {combination(4, 2)}")

    # --- 2. Combinations ---
    print("\n--- 2. Combinations C(n, k) ---")
    print(f"  {'n':>2}  {'k':>2}  {'C(n,k)':>6}  {'Description'}")
    print("  " + "-" * 40)
    examples = [(5, 2), (6, 3), (8, 4), (10, 5), (4, 4), (7, 0)]
    for n, k in examples:
        result = combination(n, k)
        print(f"  {n:>2}  {k:>2}  {result:>6}  C({n},{k}) = {result}")

    # --- 3. Tribonacci ---
    print("\n--- 3. Tribonacci (3-way recursion) ---")
    print("  T(n) = T(n-1) + T(n-2) + T(n-3)")
    print("  Base cases: T(0)=0, T(1)=0, T(2)=1")
    print()
    for i in range(12):
        print(f"  T({i:>2}) = {tribonacci(i)}")

    # --- 4. Call tree visualization ---
    print("\n--- Call Tree for C(4,2) ---")
    print("""
              C(4,2)
             /       \\
         C(3,1)     C(3,2)
         /    \\     /    \\
     C(2,0) C(2,1) C(2,1) C(2,2)
      =1    / \\     / \\    =1
           C(1,0) C(1,1) C(1,0) C(1,1)
            =1    =1     =1    =1

    C(4,2) = 1 + 2 + 2 + 1 = 6
    Note: C(2,1) is computed TWICE — redundant work!
    """)

    # --- 5. Memoization comparison ---
    print("--- Memoization Comparison ---")
    print(f"  {'n':>3}  {'k':>3}  {'Naive calls':>12}  {'Memo calls':>10}")
    print("  " + "-" * 35)

    for n, k in [(10, 5), (15, 7), (20, 10)]:
        # Count naive calls
        count = [0]

        def count_comb(n, k):
            count[0] += 1
            if k < 0 or n < 0:
                return 0
            if k == 0 or k == n:
                return 1
            if k > n:
                return 0
            return count_comb(n - 1, k - 1) + count_comb(n - 1, k)

        count_comb(n, k)
        naive_count = count[0]

        # Count memoized calls
        memo_count = [0]

        def count_comb_memo(n, k, memo=None):
            if memo is None:
                memo = {}
            memo_count[0] += 1
            key = (n, k)
            if key in memo:
                return memo[key]
            if k < 0 or n < 0:
                return 0
            if k == 0 or k == n:
                return 1
            if k > n:
                return 0
            memo[key] = count_comb_memo(n - 1, k - 1, memo) + count_comb_memo(n - 1, k, memo)
            return memo[key]

        count_comb_memo(n, k)
        memo_count_val = memo_count[0]

        print(f"  {n:>3}  {k:>3}  {naive_count:>12}  {memo_count_val:>10}")
