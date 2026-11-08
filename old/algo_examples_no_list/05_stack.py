# Stack Implementation Examples (Chapter 2) — No-List Version
# ==========================================
#
# A stack is a Last-In-First-Out (LIFO) data structure.
# This version uses a linked list (Node class) instead of Python lists.
# No external libraries.


# ---------------------------------------------------------------------------
# Node class for the linked-list-based stack
# ---------------------------------------------------------------------------
class _Node:
    """A single node in the linked list used by the stack."""

    def __init__(self, value):
        self.value = value
        self._next = None  # pointer to the next node (below this one)


# ---------------------------------------------------------------------------
# Stack built on a linked list
# ---------------------------------------------------------------------------

def stack_create():
    """Create and return an empty stack.

    The stack is represented by its top node (None means empty).
    """
    return None


def stack_push(stk, item):
    """Add an item to the top of the stack.

    Args:
        stk:   The stack (top node reference, or None).
        item:  The element to push on top.

    Returns:
        The new top node of the stack.
    """
    new_node = _Node(item)
    new_node._next = stk
    return new_node


def stack_pop(stk):
    """Remove and return the top item from the stack.

    Returns (value, new_stack) where new_stack is the stack after removal.
    Returns (None, stk) if the stack is empty.

    Args:
        stk: The stack (top node reference, or None).

    Returns:
        A tuple (top_element, new_stack).
    """
    if stack_is_empty(stk):
        print("  [warn] pop called on an empty stack")
        return None, stk
    return stk.value, stk._next


def stack_peek(stk):
    """Return the top item without removing it.

    Returns None if the stack is empty.

    Args:
        stk: The stack (top node reference, or None).

    Returns:
        The top element, or None if the stack is empty.
    """
    if stack_is_empty(stk):
        print("  [warn] peek called on an empty stack")
        return None
    return stk.value


def stack_is_empty(stk):
    """Return True if the stack has no elements.

    Args:
        stk: The stack (top node reference, or None).

    Returns:
        True if the stack is empty, False otherwise.
    """
    return stk is None


def stack_size(stk):
    """Return the number of elements in the stack.

    Args:
        stk: The stack (top node reference, or None).

    Returns:
        The count of items in the stack.
    """
    count = 0
    current = stk
    while current is not None:
        count = count + 1
        current = current._next
    return count


# ---------------------------------------------------------------------------
# Example 1: Balanced Parentheses Checker
# ---------------------------------------------------------------------------

def is_balanced(expression):
    """Check whether all brackets in *expression* are correctly matched.

    Uses a linked-list-based stack instead of a Python list.

    Supports round (), square [], and curly {} pairs.

    Args:
        expression: A string that may contain brackets and other characters.

    Returns:
        True if all brackets are correctly matched, False otherwise.
    """
    stk = stack_create()

    matching = {")": "(", "]": "[", "}": "{"}

    for char in expression:
        if char in "([{":
            stk = stack_push(stk, char)
        elif char in ")]}":
            if stack_is_empty(stk):
                return False
            top, stk = stack_pop(stk)
            if top != matching[char]:
                return False

    return stack_is_empty(stk)


# ---------------------------------------------------------------------------
# Example 2: Simple Postfix Expression Evaluator
# ---------------------------------------------------------------------------

def eval_postfix(tokens):
    """Evaluate a postfix (Reverse Polish Notation) expression.

    Uses a linked-list-based stack instead of a Python list.

    Args:
        tokens: A tuple of strings — numbers and operators (+ - * /).

    Returns:
        The numeric result of the expression.
    """
    stk = stack_create()
    operators = {"+", "-", "*", "/"}

    for token in tokens:
        if token not in operators:
            stk = stack_push(stk, float(token))
        else:
            b, stk = stack_pop(stk)
            a, stk = stack_pop(stk)

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

            stk = stack_push(stk, result)

    result, _ = stack_pop(stk)
    return result


# ---------------------------------------------------------------------------
# __main__ — run examples when this file is executed directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Stack Examples — Chapter 2 (No-List Version)")
    print("=" * 60)

    # --- Basic stack operations ---
    print("\n--- Basic Stack Operations ---")
    s = stack_create()
    print("Created an empty stack.")
    print("Is empty? %s" % stack_is_empty(s))

    # Push some numbers
    for i in range(1, 6):
        s = stack_push(s, i)
        print("Push %d -> stack size is now %d" % (i, stack_size(s)))

    print("Top element (peek): %s" % stack_peek(s))
    print("Stack size: %d" % stack_size(s))

    # Pop everything off
    print("Popping all elements:")
    while not stack_is_empty(s):
        item, s = stack_pop(s)
        print("  Popped %s, remaining size: %d" % (item, stack_size(s)))

    # --- Example 1: Balanced Parentheses ---
    print("\n--- Example 1: Balanced Parentheses Checker ---")
    test_cases = (
        "((()))",
        "([{}])",
        "((())",
        "([)]",
        "{[()()]}",
        "a + (b * c) - [d / {e + f}]",
    )
    for expr in test_cases:
        if is_balanced(expr):
            print("  %s  ->  balanced" % expr)
        else:
            print("  %s  ->  NOT balanced" % expr)

    # --- Example 2: Postfix Expression Evaluation ---
    print("\n--- Example 2: Postfix Expression Evaluation ---")
    examples = (
        (("3", "4", "+", "2", "*"), "(3 + 4) * 2  = 14"),
        (("5", "1", "2", "+", "4", "*", "+", "3", "-"), "5 + ((1+2)*4) - 3  = 14"),
        (("8", "2", "/", "3", "*"), "(8 / 2) * 3  = 12"),
    )
    for tokens, description in examples:
        result = eval_postfix(tokens)
        print("  %-40s = %s" % (description, result))
