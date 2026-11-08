"""
Stack Implementation Examples (Chapter 2)
=========================================

A stack is a Last-In-First-Out (LIFO) data structure.
This file demonstrates:
  1. Stack using a Python list
  2. Stack using collections.deque
  3. Classic examples: balanced parentheses check and expression evaluation
"""

from collections import deque


# ---------------------------------------------------------------------------
# Stack implemented with a Python list
# ---------------------------------------------------------------------------
class StackList:
    """Stack backed by a Python list."""

    def __init__(self) -> None:
        """Initialize an empty stack."""
        self._items: list = []

    def push(self, item) -> None:
        """Push an item onto the top of the stack.

        Args:
            item: The element to push.
        """
        self._items.append(item)

    def pop(self):
        """Remove and return the top item from the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("peek from an empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the stack has no elements."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of elements in the stack."""
        return len(self._items)

    def __repr__(self) -> str:
        return f"StackList({self._items})"


# ---------------------------------------------------------------------------
# Stack implemented with collections.deque
# ---------------------------------------------------------------------------
class StackDeque:
    """Stack backed by collections.deque (faster for push/pop at both ends)."""

    def __init__(self) -> None:
        """Initialize an empty stack."""
        self._items: deque = deque()

    def push(self, item) -> None:
        """Push an item onto the top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item from the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("peek from an empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the stack has no elements."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of elements in the stack."""
        return len(self._items)

    def __repr__(self) -> str:
        return f"StackDeque({list(self._items)})"


# ---------------------------------------------------------------------------
# Example 1: Balanced Parentheses Checker
# ---------------------------------------------------------------------------
def is_balanced(expression: str) -> bool:
    """Check whether all brackets in *expression* are correctly matched.

    Supports (), [], and {} pairs.

    Args:
        expression: A string containing brackets and other characters.

    Returns:
        True if every opening bracket has a matching closing bracket in
        the correct order; False otherwise.
    """
    stack = StackList()
    matching = {")": "(", "]": "[", "}": "{"}

    for char in expression:
        if char in "([{":
            # Opening bracket — push onto stack
            stack.push(char)
        elif char in ")]}":
            # Closing bracket — stack must have the corresponding opener
            if stack.is_empty():
                return False
            if stack.pop() != matching[char]:
                return False

    # If stack is empty, all brackets were matched
    return stack.is_empty()


# ---------------------------------------------------------------------------
# Example 2: Simple Expression Evaluator (postfix / Reverse Polish Notation)
# ---------------------------------------------------------------------------
def eval_postfix(tokens: list[str]) -> float:
    """Evaluate a postfix (Reverse Polish Notation) expression.

    Args:
        tokens: List of strings — numbers and operators (+ - * /).

    Returns:
        The numeric result of the expression.

    Raises:
        ValueError: If the expression is malformed or divides by zero.
    """
    stack = StackList()
    operators = {"+", "-", "*", "/"}

    for token in tokens:
        if token not in operators:
            # Operand — push its numeric value
            stack.push(float(token))
        else:
            # Operator — pop two operands, apply operator, push result
            if stack.size() < 2:
                raise ValueError(f"Too few operands for operator '{token}'")
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                result = a + b
            elif token == "-":
                result = a - b
            elif token == "*":
                result = a * b
            elif token == "/":
                if b == 0:
                    raise ValueError("Division by zero")
                result = a / b
            stack.push(result)

    if stack.size() != 1:
        raise ValueError("Invalid expression — too many operands")
    return stack.pop()


# ---------------------------------------------------------------------------
# __main__ block — run examples when executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Stack Examples — Chapter 2")
    print("=" * 60)

    # --- Basic operations with StackList ---
    print("\n--- StackList: basic operations ---")
    s = StackList()
    print(f"Is empty? {s.is_empty()}")
    for i in range(1, 6):
        s.push(i)
        print(f"Push {i} -> {s}")
    print(f"Peek top: {s.peek()}")
    print(f"Size: {s.size()}")
    while not s.is_empty():
        print(f"Pop -> {s.pop()}, remaining: {s}")

    # --- Basic operations with StackDeque ---
    print("\n--- StackDeque: basic operations ---")
    sd = StackDeque()
    for ch in "ABCDE":
        sd.push(ch)
        print(f"Push '{ch}' -> {sd}")
    print(f"Peek top: {sd.peek()}")
    print(f"Size: {sd.size()}")
    while not sd.is_empty():
        print(f"Pop -> {sd.pop()}, remaining: {sd}")

    # --- Example 1: Balanced Parentheses ---
    print("\n--- Example 1: Balanced Parentheses ---")
    test_cases = [
        "((()))",
        "([{}])",
        "((())",
        "([)]",
        "{[()()]}",
        "a + (b * c) - [d / {e + f}]",
    ]
    for expr in test_cases:
        result = "balanced" if is_balanced(expr) else "NOT balanced"
        print(f"  {expr!r:40s} -> {result}")

    # --- Example 2: Postfix Expression Evaluation ---
    print("\n--- Example 2: Postfix Expression Evaluation ---")
    examples = [
        (["3", "4", "+", "2", "*"],       # (3 + 4) * 2 = 14
         "(3 + 4) * 2"),
        (["5", "1", "2", "+", "4", "*", "+", "3", "-"],  # 5 + ((1+2)*4) - 3 = 14
         "5 + ((1+2)*4) - 3"),
        (["8", "2", "/", "3", "*"],        # (8 / 2) * 3 = 12
         "(8 / 2) * 3"),
    ]
    for tokens, infix in examples:
        result = eval_postfix(tokens)
        print(f"  {infix!r:35s} = {result}")
