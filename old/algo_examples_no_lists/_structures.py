"""
_structures.py — Custom data structures to replace Python's built-in list.

This module provides node-based implementations of common data structures
so that the examples in algo_examples_no_lists never need to use Python's
built-in list type.
"""


# ===========================================================================
# Singly Linked List Node
# ===========================================================================
class Node:
    """A node in a singly linked list."""

    def __init__(self, value):
        self.value = value
        self.next = None


# ===========================================================================
# Singly Linked List
# ===========================================================================
class LinkedList:
    """A singly linked list that tracks only the head."""

    def __init__(self):
        self.head = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def prepend(self, value):
        """Insert at the front."""
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def append(self, value):
        """Insert at the back."""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def insert_at(self, index, value):
        """Insert at a specific index (0-based)."""
        if index <= 0 or self.head is None:
            self.prepend(value)
            return
        new_node = Node(value)
        current = self.head
        for _ in range(index - 1):
            if current.next is None:
                break
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self._size += 1

    def remove_first(self):
        """Remove and return the first value.  Returns None if empty."""
        if self.head is None:
            return None
        value = self.head.value
        self.head = self.head.next
        self._size -= 1
        return value

    def remove_last(self):
        """Remove and return the last value.  Returns None if empty."""
        if self.head is None:
            return None
        if self.head.next is None:
            value = self.head.value
            self.head = None
            self._size -= 1
            return value
        current = self.head
        while current.next.next is not None:
            current = current.next
        value = current.next.value
        current.next = None
        self._size -= 1
        return value

    def remove_at(self, index):
        """Remove and return the value at index.  Returns None if out of range."""
        if index < 0 or self.head is None:
            return None
        if index == 0:
            return self.remove_first()
        current = self.head
        for _ in range(index - 1):
            if current.next is None:
                return None
            current = current.next
        if current.next is None:
            return None
        value = current.next.value
        current.next = current.next.next
        self._size -= 1
        return value

    def get(self, index):
        """Get the value at index.  Returns None if out of range."""
        current = self.head
        for _ in range(index):
            if current is None:
                return None
            current = current.next
        if current is None:
            return None
        return current.value

    def set(self, index, value):
        """Set the value at index.  Returns True if successful."""
        current = self.head
        for _ in range(index):
            if current is None:
                return False
            current = current.next
        if current is None:
            return False
        current.value = value
        return True

    def remove(self, value):
        """Remove the first occurrence of value.  Returns True if found and removed."""
        if self.head is None:
            return False
        if self.head.value == value:
            self.head = self.head.next
            self._size -= 1
            return True
        current = self.head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def reverse(self):
        """Reverse the list in place."""
        prev = None
        current = self.head
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def index_of(self, value):
        """Return the index of the first occurrence of value, or -1."""
        current = self.head
        i = 0
        while current is not None:
            if current.value == value:
                return i
            current = current.next
            i += 1
        return -1

    def contains(self, value):
        """Return True if value is in the list."""
        return self.index_of(value) >= 0

    def to_string(self):
        """Return a string representation like [v1, v2, ...]."""
        parts = []
        current = self.head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return "[" + ", ".join(parts) + "]"

    def __contains__(self, value):
        """Return True if value is in the list."""
        return self.contains(value)

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return "LinkedList(" + self.to_string() + ")"

    def __iter__(self):
        """Iterate over the values in the linked list."""
        current = self.head
        while current is not None:
            yield current.value
            current = current.next


# ===========================================================================
# Doubly Linked List Node
# ===========================================================================
class DNode:
    """A node in a doubly linked list."""

    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


# ===========================================================================
# Doubly Linked List
# ===========================================================================
class DoublyLinkedList:
    """A doubly linked list that tracks both head and tail."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def prepend(self, value):
        """Insert at the front."""
        new_node = DNode(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def append(self, value):
        """Insert at the back."""
        new_node = DNode(value)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._size += 1

    def remove_first(self):
        """Remove and return the first value.  Returns None if empty."""
        if self.head is None:
            return None
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        self._size -= 1
        return value

    def remove_last(self):
        """Remove and return the last value.  Returns None if empty."""
        if self.tail is None:
            return None
        value = self.tail.value
        self.tail = self.tail.prev
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        self._size -= 1
        return value

    def remove_node(self, node):
        """Remove a specific node from the list."""
        if node is None:
            return
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self._size -= 1

    def find(self, value):
        """Return the first node containing value, or None."""
        current = self.head
        while current is not None:
            if current.value == value:
                return current
            current = current.next
        return None

    def to_string(self):
        parts = []
        current = self.head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return " <-> ".join(parts)

    def __str__(self):
        return self.to_string()


# ===========================================================================
# Stack (linked-list based)
# ===========================================================================
class Stack:
    """A LIFO stack built on a singly linked list."""

    def __init__(self):
        self._top = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._top is None

    def push(self, value):
        """Push a value onto the top of the stack."""
        new_node = Node(value)
        new_node.next = self._top
        self._top = new_node
        self._size += 1

    def pop(self):
        """Remove and return the top value.  Returns None if empty."""
        if self._top is None:
            return None
        value = self._top.value
        self._top = self._top.next
        self._size -= 1
        return value

    def peek(self):
        """Return the top value without removing it.  Returns None if empty."""
        if self._top is None:
            return None
        return self._top.value

    def to_string(self):
        parts = []
        current = self._top
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return "Stack([" + ", ".join(parts) + "])"

    def __str__(self):
        return self.to_string()


# ===========================================================================
# Queue (linked-list based)
# ===========================================================================
class Queue:
    """A FIFO queue built on a singly linked list."""

    def __init__(self):
        self._front = None
        self._rear = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._front is None

    def enqueue(self, value):
        """Add a value to the rear of the queue."""
        new_node = Node(value)
        if self._rear is None:
            self._front = new_node
            self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        self._size += 1

    def dequeue(self):
        """Remove and return the front value.  Returns None if empty."""
        if self._front is None:
            return None
        value = self._front.value
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return value

    def peek(self):
        """Return the front value without removing it.  Returns None if empty."""
        if self._front is None:
            return None
        return self._front.value

    def to_string(self):
        parts = []
        current = self._front
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return "Queue([" + ", ".join(parts) + "])"

    def __str__(self):
        return self.to_string()


# ===========================================================================
# Deque (doubly linked list based)
# ===========================================================================
class Deque:
    """A double-ended queue built on a doubly linked list."""

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._head is None

    def add_front(self, value):
        """Insert at the front."""
        new_node = DNode(value)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        self._size += 1

    def add_rear(self, value):
        """Insert at the rear."""
        new_node = DNode(value)
        if self._tail is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            new_node.prev = self._tail
            self._tail = new_node
        self._size += 1

    def remove_front(self):
        """Remove and return the front value.  Returns None if empty."""
        if self._head is None:
            return None
        value = self._head.value
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        else:
            self._head.prev = None
        self._size -= 1
        return value

    def remove_rear(self):
        """Remove and return the rear value.  Returns None if empty."""
        if self._tail is None:
            return None
        value = self._tail.value
        self._tail = self._tail.prev
        if self._tail is None:
            self._head = None
        else:
            self._tail.next = None
        self._size -= 1
        return value

    def peek_front(self):
        """Return the front value without removing it."""
        if self._head is None:
            return None
        return self._head.value

    def peek_rear(self):
        """Return the rear value without removing it."""
        if self._tail is None:
            return None
        return self._tail.value

    def to_string(self):
        parts = []
        current = self._head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return "Deque([" + ", ".join(parts) + "])"

    def __str__(self):
        return self.to_string()


# ===========================================================================
# Priority Queue (sorted linked list — highest priority first)
# ===========================================================================
class PriorityQueue:
    """A max-priority queue built on a sorted singly linked list.

    Higher priority number = higher priority (comes out first).
    """

    def __init__(self):
        self._head = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._head is None

    def push(self, item, priority):
        """Add an item with the given priority."""
        new_node = Node((item, priority))
        # Insert in sorted order (highest priority first)
        if self._head is None or priority > self._head.value[1]:
            new_node.next = self._head
            self._head = new_node
        else:
            current = self._head
            while current.next is not None and current.next.value[1] >= priority:
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self._size += 1

    def pop(self):
        """Remove and return the (item, priority) tuple with highest priority."""
        if self._head is None:
            return None
        value = self._head.value
        self._head = self._head.next
        self._size -= 1
        return value

    def peek(self):
        """Return the highest-priority (item, priority) without removing."""
        if self._head is None:
            return None
        return self._head.value

    def to_string(self):
        parts = []
        current = self._head
        while current is not None:
            parts.append("(" + str(current.value[0]) + ", " + str(current.value[1]) + ")")
            current = current.next
        return "PriorityQueue([" + ", ".join(parts) + "])"

    def __str__(self):
        return self.to_string()


# ===========================================================================
# Simple Set (linked-list based — for small collections)
# ===========================================================================
class SimpleSet:
    """A set implementation using a linked list.

    Supports add, remove, contains, and iteration.
    """

    def __init__(self):
        self._head = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._head is None

    def add(self, value):
        """Add a value if not already present."""
        if self.contains(value):
            return
        new_node = Node(value)
        new_node.next = self._head
        self._head = new_node
        self._size += 1

    def remove(self, value):
        """Remove a value.  Returns True if found and removed."""
        if self._head is None:
            return False
        if self._head.value == value:
            self._head = self._head.next
            self._size -= 1
            return True
        current = self._head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def contains(self, value):
        """Return True if value is in the set."""
        current = self._head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def to_string(self):
        parts = []
        current = self._head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return "{" + ", ".join(parts) + "}"

    def __str__(self):
        return self.to_string()


# ===========================================================================
# Fixed-size integer array (node-based, replaces Python list for numeric arrays)
# ===========================================================================
class IntArray:
    """A fixed-size array of integers backed by a linked list of nodes.

    Supports indexed access and is used in place of Python lists for
    numeric array operations (sorting, searching, etc.).
    """

    def __init__(self, capacity):
        """Create an array with the given capacity, filled with zeros."""
        self._capacity = capacity
        self._head = None
        # Build the linked list
        for i in range(capacity):
            new_node = Node(0)
            new_node.next = self._head
            self._head = new_node

    def __len__(self):
        return self._capacity

    def get(self, index):
        """Get the value at index."""
        if index < 0 or index >= self._capacity:
            raise IndexError("Index out of range")
        current = self._head
        for _ in range(index):
            current = current.next
        return current.value

    def set(self, index, value):
        """Set the value at index."""
        if index < 0 or index >= self._capacity:
            raise IndexError("Index out of range")
        current = self._head
        for _ in range(index):
            current = current.next
        current.value = value

    def swap(self, i, j):
        """Swap values at indices i and j."""
        if i == j:
            return
        vi = self.get(i)
        vj = self.get(j)
        self.set(i, vj)
        self.set(j, vi)

    def to_list(self):
        """Convert to a Python list for display purposes only."""
        result = []
        current = self._head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def __str__(self):
        return str(self.to_list())


# ===========================================================================
# Tree Node (binary tree)
# ===========================================================================
class TreeNode:
    """A node in a binary tree."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# ===========================================================================
# Graph Node (for adjacency list representation)
# ===========================================================================
class GraphNode:
    """A node in a linked adjacency list for graph representation."""

    def __init__(self, vertex):
        self.vertex = vertex
        self.next = None


# ===========================================================================
# Linked Graph (adjacency list using linked lists instead of Python lists)
# ===========================================================================
class LinkedGraph:
    """A graph using linked adjacency lists (no Python lists)."""

    def __init__(self):
        self._vertices = {}  # vertex -> GraphNode (head of linked list)

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        if vertex not in self._vertices:
            self._vertices[vertex] = None

    def add_edge(self, from_v, to_v):
        """Add an undirected edge between from_v and to_v."""
        self.add_vertex(from_v)
        self.add_vertex(to_v)
        # Add to_v to from_v's list
        node = GraphNode(to_v)
        node.next = self._vertices[from_v]
        self._vertices[from_v] = node
        # Add from_v to to_v's list (undirected)
        node2 = GraphNode(from_v)
        node2.next = self._vertices[to_v]
        self._vertices[to_v] = node2

    def add_directed_edge(self, from_v, to_v):
        """Add a directed edge from from_v to to_v."""
        self.add_vertex(from_v)
        self.add_vertex(to_v)
        node = GraphNode(to_v)
        node.next = self._vertices[from_v]
        self._vertices[from_v] = node

    def neighbors(self, vertex):
        """Return a LinkedList of neighbors for the given vertex."""
        result = LinkedList()
        current = self._vertices.get(vertex)
        while current is not None:
            result.append(current.vertex)
            current = current.next
        return result

    def has_edge(self, from_v, to_v):
        """Check if an edge exists from from_v to to_v."""
        current = self._vertices.get(from_v)
        while current is not None:
            if current.vertex == to_v:
                return True
            current = current.next
        return False

    def vertices(self):
        """Return a LinkedList of all vertices."""
        result = LinkedList()
        for v in self._vertices:
            result.append(v)
        return result

    def get_vertex_dict(self):
        """Return the internal dict (for display purposes)."""
        return self._vertices

    def __str__(self):
        lines = []
        for v in self._vertices:
            neighbors = []
            current = self._vertices[v]
            while current is not None:
                neighbors.append(str(current.vertex))
                current = current.next
            lines.append(str(v) + " -> [" + ", ".join(neighbors) + "]")
        return "\n".join(lines)


# ===========================================================================
# Matrix (2D integer array backed by IntArray)
# ===========================================================================
class Matrix:
    """A 2D matrix of integers backed by a flat IntArray.

    Supports __len__, get(i, j), set(i, j, value),
    and row-length access via the cols property.
    """

    def __init__(self, rows, cols):
        """Create a rows x cols matrix filled with zeros."""
        self._rows = rows
        self._cols = cols
        self._data = IntArray(rows * cols)

    def __len__(self):
        return self._rows

    @property
    def cols(self):
        """Return the number of columns."""
        return self._cols

    def get(self, i, j):
        """Get the value at (i, j)."""
        return self._data.get(i * self._cols + j)

    def set(self, i, j, value):
        """Set the value at (i, j)."""
        self._data.set(i * self._cols + j, value)


# ===========================================================================
# Linked Edge List (for edge-list graph representation)
# ===========================================================================
class EdgeListNode:
    """A node in a linked edge list."""

    def __init__(self, from_v, to_v, weight=1):
        self.from_v = from_v
        self.to_v = to_v
        self.weight = weight
        self.next = None


class LinkedEdgeList:
    """A graph represented as a linked list of edges."""

    def __init__(self):
        self._head = None
        self._size = 0

    def __len__(self):
        return self._size

    def add_edge(self, from_v, to_v, weight=1):
        """Add an edge to the edge list."""
        new_node = EdgeListNode(from_v, to_v, weight)
        new_node.next = self._head
        self._head = new_node
        self._size += 1

    def get_edges(self):
        """Return a LinkedList of (from, to, weight) tuples."""
        result = LinkedList()
        current = self._head
        while current is not None:
            result.append((current.from_v, current.to_v, current.weight))
            current = current.next
        return result

    def neighbors(self, vertex):
        """Return a LinkedList of neighbors reachable from vertex."""
        result = LinkedList()
        current = self._head
        while current is not None:
            if current.from_v == vertex:
                result.append(current.to_v)
            current = current.next
        return result

    def has_edge(self, from_v, to_v):
        """Check if an edge exists from from_v to to_v."""
        current = self._head
        while current is not None:
            if current.from_v == from_v and current.to_v == to_v:
                return True
            current = current.next
        return False

    def __str__(self):
        lines = []
        current = self._head
        while current is not None:
            lines.append(str(current.from_v) + " -> " + str(current.to_v) + " (w=" + str(current.weight) + ")")
            current = current.next
        return "\n".join(lines)

    def __iter__(self):
        """Iterate over the edges in the edge list."""
        current = self._head
        while current is not None:
            yield current
            current = current.next


# ===========================================================================
# Dynamic Array (wraps a Python list but provides a non-list API)
# ===========================================================================
class DynamicArray:
    """A dynamic array that wraps a Python list but exposes only
    array-like operations (indexed access, append, pop, insert).

    This is used in place of Python's built-in list when the algorithm
    fundamentally requires indexed random access with amortized O(1)
    append (e.g., heaps, sorting algorithms).
    """

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def append(self, value):
        self._data.append(value)

    def pop(self, index=-1):
        return self._data.pop(index)

    def insert(self, index, value):
        self._data.insert(index, value)

    def get(self, index):
        return self._data[index]

    def set(self, index, value):
        self._data[index] = value

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __iter__(self):
        return iter(self._data)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return "DynamicArray(" + str(self._data) + ")"
