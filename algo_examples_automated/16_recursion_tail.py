"""
16_recursion_tail.py
====================
Recursion Topic: Tail Recursion

Tail recursion is a special form of recursion where the recursive call is
the LAST operation in the function — there is no pending computation after
the call returns.

Key ideas:
  1. In a tail-recursive function, the result of the recursive call is
     returned directly without any further processing.
  2. In languages that support Tail Call Optimization (TCO), the compiler
     can reuse the current stack frame for the next call, making tail
     recursion as efficient as a loop (O(1) space).
  3. Python does NOT support TCO, but writing tail-recursive code is
     still valuable for understanding the pattern and for converting to
     iteration.

This file covers:
  1. Tail-recursive examples (factorial, sum, power)
  2. Converting tail recursion to iteration
  3. Comparing standard vs tail recursion
"""

from typing import List


# ---------------------------------------------------------------------------
# 1. Standard (non-tail) Recursion vs Tail Recursion
# ---------------------------------------------------------------------------

def factorial_standard(n: int) -> int:
    """Standard (non-tail) recursive factorial.

    The multiplication `n * factorial(n-1)` happens AFTER the recursive
    call returns — so the call stack must remember each `n` to perform
    the multiplication later.  This is NOT tail recursion.

    Call stack for factorial(4):
      factorial(4) → 4 * factorial(3)  ← pending: need 4 later
        factorial(3) → 3 * factorial(2)  ← pending: need 3 later
          factorial(2) → 2 * factorial(1)  ← pending: need 2 later
            factorial(1) → 1  ← base case
          ← 2 * 1 = 2
        ← 3 * 2 = 6
      ← 4 * 6 = 24
    """
    if n <= 1:
        return 1
    return n * factorial_standard(n - 1)  # NOT tail: multiplication after call


def factorial_tail(n: int, accumulator: int = 1) -> int:
    """Tail-recursive factorial.

    The accumulator carries the intermediate result forward.  The recursive
    call is the LAST operation — nothing is pending after it returns.

    Call stack for factorial_tail(4):
      factorial_tail(4, acc=1)
        → factorial_tail(3, acc=4)   ← just passes values, no pending work
          → factorial_tail(2, acc=12)
            → factorial_tail(1, acc=24)
              → return 1  [base case]
            ← return 24
          ← return 24
        ← return 24

    In a TCO-enabled language, the compiler would reuse the same stack
    frame for each call, making this O(1) in space.

    Args:
        n:           The number to compute factorial for.
        accumulator: Carries the running product (starts at 1).

    Returns:
        n!
    """
    # Base case: when n reaches 1, the accumulator holds the final result
    if n <= 1:
        return accumulator

    # Tail call: the recursive call is the LAST operation
    # Pass the updated accumulator (n * accumulator) and reduce n by 1
    return factorial_tail(n - 1, n * accumulator)


# ---------------------------------------------------------------------------
# 2. Tail-Recursive Sum of a List
# ---------------------------------------------------------------------------

def sum_standard(lst: List[int], index: int = 0) -> int:
    """Standard (non-tail) recursive sum — pending addition after call."""
    if index >= len(lst):
        return 0
    return lst[index] + sum_standard(lst, index + 1)  # NOT tail: addition after call


def sum_tail(lst: List[int], index: int = 0, accumulator: int = 0) -> int:
    """Tail-recursive sum — accumulator carries the running total.

    The recursive call is the last operation — no pending computation.
    """
    if index >= len(lst):
        return accumulator
    return sum_tail(lst, index + 1, accumulator + lst[index])  # TAIL call


# ---------------------------------------------------------------------------
# 3. Tail-Recursive Power Function
# ---------------------------------------------------------------------------

def power_standard(base: float, exp: int) -> float:
    """Standard (non-tail) recursive power."""
    if exp == 0:
        return 1
    return base * power_standard(base, exp - 1)  # NOT tail


def power_tail(base: float, exp: int, accumulator: float = 1.0) -> float:
    """Tail-recursive power function.

    The accumulator builds up the result as exp decreases to 0.
    """
    if exp == 0:
        return accumulator
    return power_tail(base, exp - 1, accumulator * base)  # TAIL call


# ---------------------------------------------------------------------------
# 4. Converting Tail Recursion to Iteration
# ---------------------------------------------------------------------------

def factorial_iterative(n: int) -> int:
    """Iterative factorial — the direct conversion of tail recursion.

    The tail-recursive parameters become loop variables:
      - n becomes the loop counter (decreasing)
      - accumulator becomes the running product
    """
    accumulator = 1
    while n > 1:
        accumulator *= n  # same as the accumulator update in tail recursion
        n -= 1             # same as n-1 in tail recursion
    return accumulator


def sum_iterative(lst: List[int]) -> int:
    """Iterative sum — direct conversion of tail-recursive sum."""
    accumulator = 0
    index = 0
    while index < len(lst):
        accumulator += lst[index]  # same accumulator update
        index += 1                  # same index advance
    return accumulator


def power_iterative(base: float, exp: int) -> float:
    """Iterative power — direct conversion of tail-recursive power."""
    accumulator = 1.0
    while exp > 0:
        accumulator *= base  # same accumulator update
        exp -= 1              # same exponent decrement
    return accumulator


# ---------------------------------------------------------------------------
# 5. A More Complex Example: Tail-Recursive GCD (Euclidean Algorithm)
# ---------------------------------------------------------------------------

def gcd_tail(a: int, b: int) -> int:
    """Compute GCD using tail recursion (Euclidean algorithm).

    GCD(a, b) = GCD(b, a mod b)  until b == 0

    This is naturally tail-recursive because each call replaces the
    current parameters — no pending computation after the call.

    Args:
        a: First non-negative integer.
        b: Second non-negative integer.

    Returns:
        The greatest common divisor of a and b.
    """
    # Base case: when b is 0, a is the GCD
    if b == 0:
        return a

    # Tail call: replace (a, b) with (b, a % b)
    return gcd_tail(b, a % b)


def gcd_iterative(a: int, b: int) -> int:
    """Iterative GCD — direct conversion of the tail-recursive version."""
    while b != 0:
        a, b = b, a % b  # same parameter update as tail recursion
    return a


# ---------------------------------------------------------------------------
# 6. Converting Non-Tail Recursion to Iteration (using an explicit stack)
# ---------------------------------------------------------------------------

def factorial_iterative_with_stack(n: int) -> int:
    """Convert standard (non-tail) recursion to iteration using an explicit stack.

    When a function is NOT tail-recursive, we can simulate the call stack
    manually using a stack data structure.  This is the general technique
    for converting any recursion to iteration.
    """
    stack = []
    result = 1

    # Simulate the recursive calls by pushing values onto the stack
    while n > 1:
        stack.append(n)  # this is what the call stack "remembers"
        n -= 1

    # Now unwind the stack, performing the pending multiplications
    while stack:
        result *= stack.pop()  # this is the "pending" multiplication

    return result


if __name__ == "__main__":
    print("=" * 55)
    print("Recursion Example: Tail Recursion")
    print("=" * 55)

    # --- 1. Factorial comparison ---
    print("\n--- 1. Factorial: Standard vs Tail Recursion ---")
    for i in range(8):
        std = factorial_standard(i)
        tail = factorial_tail(i)
        it = factorial_iterative(i)
        print(f"  {i}! = {std}  (standard={std}, tail={tail}, iterative={it}, all match: {std == tail == it})")

    # --- 2. Sum comparison ---
    print("\n--- 2. Sum: Standard vs Tail Recursion ---")
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"  List: {nums}")
    print(f"  sum_standard({nums}) = {sum_standard(nums)}")
    print(f"  sum_tail({nums})     = {sum_tail(nums)}")
    print(f"  sum_iterative({nums}) = {sum_iterative(nums)}")
    assert sum_standard(nums) == sum_tail(nums) == sum_iterative(nums)

    # --- 3. Power comparison ---
    print("\n--- 3. Power: Standard vs Tail Recursion ---")
    for base, exp in [(2, 10), (3, 5), (1.5, 4)]:
        std = power_standard(base, exp)
        tail = power_tail(base, exp)
        it = power_iterative(base, exp)
        print(f"  {base}^{exp} = {std}  (all match: {std == tail == it})")

    # --- 4. GCD ---
    print("\n--- 4. GCD (naturally tail-recursive) ---")
    pairs = [(48, 18), (56, 98), (101, 103), (270, 192)]
    for a, b in pairs:
        tail_result = gcd_tail(a, b)
        iter_result = gcd_iterative(a, b)
        print(f"  gcd({a}, {b}) = {tail_result}  (tail={tail_result}, iterative={iter_result}, match: {tail_result == iter_result})")

    # --- 5. Conversion table ---
    print("\n--- 5. Tail Recursion → Iteration Conversion Guide ---")
    print("""
  +---------------------+----------------------------+---------------------------+
  | Tail-Recursive Form | Loop Variable              | Accumulator Variable      |
  +---------------------+----------------------------+---------------------------+
  | factorial_tail(n, acc)  | while n > 1: n -= 1    | acc *= n                  |
  | sum_tail(lst, i, acc)   | while i < len(lst): i+=1 | acc += lst[i]             |
  | power_tail(b, e, acc)   | while e > 0: e -= 1    | acc *= b                  |
  | gcd_tail(a, b)          | while b != 0:            | a, b = b, a % b           |
  +---------------------+----------------------------+---------------------------+

  General pattern for converting tail recursion to iteration:

  1. Identify the parameters that change with each call (loop variables).
  2. Identify the accumulator parameter (carries the result forward).
  3. Replace the function call with a loop that updates these variables.
  4. Return the accumulator when the base case condition is met.
    """)

    # --- 6. Non-tail to iteration with explicit stack ---
    print("--- 6. Non-Tail Recursion → Iteration with Explicit Stack ---")
    print(f"  factorial_iterative_with_stack(6) = {factorial_iterative_with_stack(6)}")
    print(f"  Expected: 720  ✓")
    assert factorial_iterative_with_stack(6) == 720

    # --- 7. Python and TCO ---
    print("\n--- 7. Python and Tail Call Optimization ---")
    print("""
  Python does NOT implement tail call optimization (TCO).

  Reasons (per Guido van Rossum):
    - TCO makes debugging harder (stack traces lose frames)
    - Python's philosophy favors explicit loops over implicit optimization
    - Iterative solutions are considered more "Pythonic"

  Consequences:
    - Tail-recursive functions in Python still use O(n) stack space
    - Deep recursion (default limit: 1000) will raise RecursionError
    - For production code, prefer iteration in Python

  However, understanding tail recursion is valuable because:
    - It reveals the structure of iterative algorithms
    - It's essential in functional programming languages (Haskell, Scala, Erlang)
    - It helps in converting recursive algorithms to iteration in any language
    - Some Python implementations (PyPy) may optimize tail calls in the future
    """)
