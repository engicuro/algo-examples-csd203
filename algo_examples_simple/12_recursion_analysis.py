# 12_recursion_analysis.py
# Analyzing recursive algorithms: Fibonacci with call counting,
# and simple recurrence examples.
#
# Key ideas:
#   - Every recursive call adds a new frame to the call stack.
#   - Some recursions (like naive Fibonacci) do a LOT of repeated work.
#   - We can count calls to see how expensive a recursive algorithm is.


# ---- Fibonacci with call counting ----

def fibonacci(n):
    """Return the nth Fibonacci number using simple recursion.

    Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, ...
    fib(0) = 0, fib(1) = 1, fib(n) = fib(n-1) + fib(n-2).
    """
    # Base cases: fib(0) = 0, fib(1) = 1.
    if n <= 0:
        return 0
    if n == 1:
        return 1

    # Recursive case: fib(n) = fib(n-1) + fib(n-2).
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_counted(n):
    """Return [fib(n), call_count].

    We use a list [count] so the inner function can modify it
    (lists are mutable and can be changed inside nested functions).
    """
    call_count = [0]  # use a list so the inner function can update it

    def _fib(n):
        """Inner helper that counts every call."""
        call_count[0] = call_count[0] + 1

        # Base cases
        if n <= 0:
            return 0
        if n == 1:
            return 1

        # Recursive case
        return _fib(n - 1) + _fib(n - 2)

    result = _fib(n)
    return [result, call_count[0]]


# ---- Simple recurrence examples ----

def sum_to_n(n):
    """Return 1 + 2 + 3 + ... + n using recursion.

    Recurrence:  S(n) = n + S(n-1),  with S(0) = 0.
    """
    # Base case: sum of zero numbers is 0.
    if n <= 0:
        return 0

    # Recursive case: add n to the sum of 1..(n-1).
    return n + sum_to_n(n - 1)


def power(base, exponent):
    """Return base raised to the exponent using recursion.

    Recurrence:  power(b, e) = b * power(b, e-1),  with power(b, 0) = 1.
    """
    # Base case: anything raised to 0 is 1.
    if exponent <= 0:
        return 1

    # Recursive case: b^e = b * b^(e-1).
    return base * power(base, exponent - 1)


def count_down(n):
    """Print numbers from n down to 1, then 'Done!'.

    This is a simple example of linear recursion with no return value.
    """
    # Base case: we have counted down to 0.
    if n <= 0:
        print("Done!")
        return

    # Recursive case: print n, then count down from n-1.
    print(n)
    count_down(n - 1)


if __name__ == "__main__":
    print("=== Fibonacci (simple) ===")
    for i in range(10):
        print("  fib(%d) = %d" % (i, fibonacci(i)))

    print("\n=== Fibonacci with call counting ===")
    print("  (Shows how many recursive calls are made)")
    for i in range(10):
        result_and_count = fibonacci_counted(i)
        print("  fib(%d) = %d, calls = %d" % (i, result_and_count[0], result_and_count[1]))

    print("\n=== Sum from 1 to n ===")
    for n in [1, 5, 10]:
        print("  sum_to_n(%d) = %d" % (n, sum_to_n(n)))

    print("\n=== Power function ===")
    print("  2^10 =", power(2, 10))
    print("  3^4  =", power(3, 4))
    print("  5^0  =", power(5, 0))

    print("\n=== Count down ===")
    count_down(5)
