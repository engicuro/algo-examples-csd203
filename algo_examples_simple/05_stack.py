# Stack Implementation Examples (Chapter 2)
# ==========================================
#
# A stack is a Last-In-First-Out (LIFO) data structure.
# The last item you push on is the first one you pop off.
#
# This file uses only plain Python lists — no fancy features,
# no external libraries.


# ---------------------------------------------------------------------------
# Stack built on a plain Python list
# ---------------------------------------------------------------------------

def stack_create():
    """Create and return an empty stack."""
    return []


def stack_push(stk, item):
    """Add an item to the top of the stack.

    Args:
        stk:   The stack (a Python list).
        item:  The element to push on top.
    """
    stk.append(item)


def stack_pop(stk):
    """Remove and return the top item from the stack.

    Returns None if the stack is empty.

    Args:
        stk: The stack (a Python list).

    Returns:
        The top element, or None if the stack is empty.
    """
    if stack_is_empty(stk):
        print("  [warn] pop called on an empty stack")
        return None
    return stk.pop()


def stack_peek(stk):
    """Return the top item without removing it.

    Returns None if the stack is empty.

    Args:
        stk: The stack (a Python list).

    Returns:
        The top element, or None if the stack is empty.
    """
    if stack_is_empty(stk):
        print("  [warn] peek called on an empty stack")
        return None
    return stk[-1]


def stack_is_empty(stk):
    """Return True if the stack has no elements.

    Args:
        stk: The stack (a Python list).

    Returns:
        True if the stack is empty, False otherwise.
    """
    return len(stk) == 0


def stack_size(stk):
    """Return the number of elements in the stack.

    Args:
        stk: The stack (a Python list).

    Returns:
        The count of items in the stack.
    """
    return len(stk)


# ---------------------------------------------------------------------------
# Example 1: Balanced Parentheses Checker
# ---------------------------------------------------------------------------

def is_balanced(expression):
    """Check whether all brackets in *expression* are correctly matched.

    Supports round (), square [], and curly {} pairs.

    How it works:
      - Walk through every character in the string.
      - When you see an opening bracket, push it on the stack.
      - When you see a closing bracket, pop from the stack and check
        that it matches the correct opening bracket.
      - At the end, the stack must be empty (every opener had a match).

    Args:
        expression: A string that may contain brackets and other characters.

    Returns:
        True if all brackets are correctly matched, False otherwise.
    """
    stk = stack_create()

    # Map each closing bracket to its matching opening bracket
    matching = {")": "(", "]": "[", "}": "{"}

    for char in expression:
        if char in "([{":
            # Opening bracket — push it onto the stack
            stack_push(stk, char)
        elif char in ")]}":
            # Closing bracket — the stack must have the matching opener
            if stack_is_empty(stk):
                return False
            top = stack_pop(stk)
            if top != matching[char]:
                return False

    # If the stack is empty, every opening bracket found its match
    return stack_is_empty(stk)


# ---------------------------------------------------------------------------
# Example 2: Simple Postfix Expression Evaluator
# ---------------------------------------------------------------------------

def eval_postfix(tokens):
    """Evaluate a postfix (Reverse Polish Notation) expression.

    In postfix notation, the operator comes after its operands.
    For example:  "3 4 +"  means  3 + 4

    How it works:
      - Walk through each token (number or operator).
      - If it is a number, push it on the stack.
      - If it is an operator, pop two numbers, apply the operator,
        and push the result back.
      - At the end, the stack has exactly one value: the answer.

    Args:
        tokens: A list of strings — numbers and operators (+ - * /).

    Returns:
        The numeric result of the expression.
    """
    stk = stack_create()
    operators = {"+", "-", "*", "/"}

    for token in tokens:
        if token not in operators:
            # It is a number — convert to float and push
            stack_push(stk, float(token))
        else:
            # It is an operator — pop two operands
            b = stack_pop(stk)
            a = stack_pop(stk)

            # Apply the operator
            if token == "+":
                result = a + b
            elif token == "-":
                result = a - b
            elif token == "*":
                result = a * b
            elif token == "/":
                if b == 0:
                    print("  [error] Division by zero")
                    return None
                result = a / b

            # Push the result back onto the stack
            stack_push(stk, result)

    # The final answer is the only item left on the stack
    return stack_pop(stk)


# ---------------------------------------------------------------------------
# __main__ — run examples when this file is executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Stack Examples — Chapter 2 (Simplified)")
    print("=" * 60)

    # --- Basic stack operations ---
    print("\n--- Basic Stack Operations ---")
    s = stack_create()
    print("Created an empty stack.")
    print("Is empty? %s" % stack_is_empty(s))

    # Push some numbers
    for i in range(1, 6):
        stack_push(s, i)
        print("Push %d -> stack size is now %d" % (i, stack_size(s)))

    print("Top element (peek): %s" % stack_peek(s))
    print("Stack size: %d" % stack_size(s))

    # Pop everything off
    print("Popping all elements:")
    while not stack_is_empty(s):
        item = stack_pop(s)
        print("  Popped %s, remaining size: %d" % (item, stack_size(s)))

    # --- Example 1: Balanced Parentheses ---
    print("\n--- Example 1: Balanced Parentheses Checker ---")
    test_cases = [
        "((()))",
        "([{}])",
        "((())",
        "([)]",
        "{[()()]}",
        "a + (b * c) - [d / {e + f}]",
    ]
    for expr in test_cases:
        if is_balanced(expr):
            print("  %s  ->  balanced" % expr)
        else:
            print("  %s  ->  NOT balanced" % expr)

    # --- Example 2: Postfix Expression Evaluation ---
    print("\n--- Example 2: Postfix Expression Evaluation ---")
    examples = [
        (["3", "4", "+", "2", "*"], "(3 + 4) * 2  = 14"),
        (["5", "1", "2", "+", "4", "*", "+", "3", "-"], "5 + ((1+2)*4) - 3  = 14"),
        (["8", "2", "/", "3", "*"], "(8 / 2) * 3  = 12"),
    ]
    for tokens, description in examples:
        result = eval_postfix(tokens)
        print("  %-40s = %s" % (description, result))
