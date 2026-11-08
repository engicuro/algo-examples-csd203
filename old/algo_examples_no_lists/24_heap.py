"""
24_heap.py - Min-Heap and Max-Heap (using custom data structures)

A heap is a complete binary tree stored in a flat array.
For a node at index i (0-based):
  - Parent index:   (i - 1) // 2
  - Left child:     2 * i + 1
  - Right child:    2 * i + 2

This file implements both a min-heap and a max-heap from scratch
using a LinkedList (instead of a Python list).  We do NOT use
the heapq module.

Topics covered:
  - Sift up  (bubble a value up to restore heap property after push)
  - Sift down (sink a value down to restore heap property after pop)
  - Push     (add a value to the heap)
  - Pop      (remove and return the top value)
  - Heap sort (sort a list using a heap)
"""

import math

from _structures import LinkedList, IntArray


# ===========================================================================
# Min-Heap
# ===========================================================================
class MinHeap:
    """A min-heap: the smallest value is always at the top (index 0).

    Stored as a LinkedList where the heap property is:
      parent <= children   (for every node)
    """

    def __init__(self):
        self.data = LinkedList()  # the underlying linked list

    # ------------------------------------------------------------------
    # Helper: parent / child index calculations
    # ------------------------------------------------------------------
    def _parent(self, index):
        """Return the index of the parent of the node at `index`."""
        return (index - 1) // 2

    def _left_child(self, index):
        """Return the index of the left child of the node at `index`."""
        return 2 * index + 1

    def _right_child(self, index):
        """Return the index of the right child of the node at `index`."""
        return 2 * index + 2

    # ------------------------------------------------------------------
    # Sift up: move a value up the tree until the heap property is restored
    # ------------------------------------------------------------------
    def _sift_up(self, index):
        """Move the value at `index` upward until the min-heap property holds.

        Compare the value with its parent.  If it is smaller, swap them.
        Repeat until the value is no longer smaller than its parent,
        or it reaches the root.
        """
        while index > 0:
            parent_index = self._parent(index)
            # If current value is smaller than its parent, swap them
            if self.data.get(index) < self.data.get(parent_index):
                # Swap
                temp = self.data.get(index)
                self.data.set(index, self.data.get(parent_index))
                self.data.set(parent_index, temp)
                # Move up to the parent's position
                index = parent_index
            else:
                # The heap property is satisfied — stop
                break

    # ------------------------------------------------------------------
    # Sift down: move a value down the tree until the heap property is restored
    # ------------------------------------------------------------------
    def _sift_down(self, index):
        """Move the value at `index` downward until the min-heap property holds.

        Compare the value with its children.  If it is larger than either
        child, swap it with the smaller child.  Repeat until the value is
        smaller than both children, or it reaches a leaf.
        """
        size = len(self.data)
        while True:
            smallest = index
            left = self._left_child(index)
            right = self._right_child(index)

            # Check if left child exists and is smaller than current
            if left < size and self.data.get(left) < self.data.get(smallest):
                smallest = left

            # Check if right child exists and is smaller than current smallest
            if right < size and self.data.get(right) < self.data.get(smallest):
                smallest = right

            # If the smallest is not the current node, swap and continue
            if smallest != index:
                temp = self.data.get(index)
                self.data.set(index, self.data.get(smallest))
                self.data.set(smallest, temp)
                index = smallest
            else:
                # The heap property is satisfied — stop
                break

    # ------------------------------------------------------------------
    # Push: add a value to the heap
    # ------------------------------------------------------------------
    def push(self, value):
        """Add a value to the heap.

        Steps:
          1. Append the value to the end of the list.
          2. Sift it up to restore the heap property.
        """
        self.data.append(value)
        self._sift_up(len(self.data) - 1)

    # ------------------------------------------------------------------
    # Pop: remove and return the smallest value (the root)
    # ------------------------------------------------------------------
    def pop(self):
        """Remove and return the smallest value from the heap.

        Steps:
          1. Save the root value (the minimum).
          2. Move the last element to the root position.
          3. Remove the last element from the list.
          4. Sift the new root down to restore the heap property.
          5. Return the saved minimum value.
        """
        if len(self.data) == 0:
            print("  Heap is empty — cannot pop.")
            return None

        # Save the minimum value (root)
        min_value = self.data.get(0)

        # Move the last element to the root
        last_value = self.data.remove_last()
        if len(self.data) > 0:
            self.data.set(0, last_value)
            # Sift the new root down
            self._sift_down(0)

        return min_value

    # ------------------------------------------------------------------
    # Peek: return the minimum value without removing it
    # ------------------------------------------------------------------
    def peek(self):
        """Return the smallest value without removing it."""
        if len(self.data) == 0:
            return None
        return self.data.get(0)

    # ------------------------------------------------------------------
    # Size
    # ------------------------------------------------------------------
    def size(self):
        """Return the number of elements in the heap."""
        return len(self.data)

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------
    def __str__(self):
        return str(self.data)


# ===========================================================================
# Max-Heap
# ===========================================================================
class MaxHeap:
    """A max-heap: the largest value is always at the top (index 0).

    Stored as a LinkedList where the heap property is:
      parent >= children   (for every node)
    """

    def __init__(self):
        self.data = LinkedList()  # the underlying linked list

    def _parent(self, index):
        return (index - 1) // 2

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    # ------------------------------------------------------------------
    # Sift up for max-heap: move a value up if it is LARGER than its parent
    # ------------------------------------------------------------------
    def _sift_up(self, index):
        """Move the value at `index` upward until the max-heap property holds."""
        while index > 0:
            parent_index = self._parent(index)
            # If current value is larger than its parent, swap them
            if self.data.get(index) > self.data.get(parent_index):
                temp = self.data.get(index)
                self.data.set(index, self.data.get(parent_index))
                self.data.set(parent_index, temp)
                index = parent_index
            else:
                break

    # ------------------------------------------------------------------
    # Sift down for max-heap: move a value down if it is SMALLER than a child
    # ------------------------------------------------------------------
    def _sift_down(self, index):
        """Move the value at `index` downward until the max-heap property holds."""
        size = len(self.data)
        while True:
            largest = index
            left = self._left_child(index)
            right = self._right_child(index)

            # Check if left child exists and is larger than current
            if left < size and self.data.get(left) > self.data.get(largest):
                largest = left

            # Check if right child exists and is larger than current largest
            if right < size and self.data.get(right) > self.data.get(largest):
                largest = right

            # If the largest is not the current node, swap and continue
            if largest != index:
                temp = self.data.get(index)
                self.data.set(index, self.data.get(largest))
                self.data.set(largest, temp)
                index = largest
            else:
                break

    # ------------------------------------------------------------------
    # Push: add a value to the max-heap
    # ------------------------------------------------------------------
    def push(self, value):
        """Add a value to the max-heap."""
        self.data.append(value)
        self._sift_up(len(self.data) - 1)

    # ------------------------------------------------------------------
    # Pop: remove and return the largest value (the root)
    # ------------------------------------------------------------------
    def pop(self):
        """Remove and return the largest value from the max-heap."""
        if len(self.data) == 0:
            print("  Heap is empty — cannot pop.")
            return None

        max_value = self.data.get(0)
        last_value = self.data.remove_last()
        if len(self.data) > 0:
            self.data.set(0, last_value)
            self._sift_down(0)

        return max_value

    # ------------------------------------------------------------------
    # Peek: return the largest value without removing it
    # ------------------------------------------------------------------
    def peek(self):
        """Return the largest value without removing it."""
        if len(self.data) == 0:
            return None
        return self.data.get(0)

    # ------------------------------------------------------------------
    # Size
    # ------------------------------------------------------------------
    def size(self):
        return len(self.data)

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------
    def __str__(self):
        return str(self.data)


# ===========================================================================
# Heap Sort
# ===========================================================================
def heap_sort_ascending(arr):
    """Sort a list in ascending order using a min-heap.

    Steps:
      1. Build a min-heap from all elements.
      2. Repeatedly pop the minimum and collect the results.

    Time complexity: O(n log n)
    Space complexity: O(n) for the new heap and result.
    """
    heap = MinHeap()
    # Push all elements into the heap
    for value in arr:
        heap.push(value)

    # Pop all elements — they come out in sorted order
    result = IntArray(len(arr))
    i = 0
    while heap.size() > 0:
        result.set(i, heap.pop())
        i += 1
    return result


def heap_sort_descending(arr):
    """Sort a list in descending order using a max-heap."""
    heap = MaxHeap()
    for value in arr:
        heap.push(value)

    result = IntArray(len(arr))
    i = 0
    while heap.size() > 0:
        result.set(i, heap.pop())
        i += 1
    return result


# ---------------------------------------------------------------------------
# Main block — simple example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Chapter 24 — Min-Heap and Max-Heap")
    print("=" * 60)

    # --- Min-Heap demo ---
    print("\n--- Min-Heap ---")
    min_heap = MinHeap()
    values = [15, 10, 20, 8, 25, 5, 12]
    print("Pushing values: " + str(values))
    for val in values:
        min_heap.push(val)
        print("  After pushing " + str(val) + ": " + str(min_heap))

    print("\nMin-heap contents: " + str(min_heap))
    print("Peek (minimum): " + str(min_heap.peek()))

    print("\nPopping all values (should come out in sorted order):")
    while min_heap.size() > 0:
        val = min_heap.pop()
        print("  Popped: " + str(val) + "  Remaining: " + str(min_heap))

    # --- Max-Heap demo ---
    print("\n--- Max-Heap ---")
    max_heap = MaxHeap()
    values2 = [15, 10, 20, 8, 25, 5, 12]
    print("Pushing values: " + str(values2))
    for val in values2:
        max_heap.push(val)
        print("  After pushing " + str(val) + ": " + str(max_heap))

    print("\nMax-heap contents: " + str(max_heap))
    print("Peek (maximum): " + str(max_heap.peek()))

    print("\nPopping all values (should come out in reverse sorted order):")
    while max_heap.size() > 0:
        val = max_heap.pop()
        print("  Popped: " + str(val) + "  Remaining: " + str(max_heap))

    # --- Heap Sort demo ---
    print("\n--- Heap Sort ---")
    unsorted = [64, 25, 12, 22, 11, 90, 3, 47]
    print("Original list: " + str(unsorted))

    sorted_asc = heap_sort_ascending(unsorted)
    print("Sorted ascending (min-heap):  " + str(sorted_asc))

    sorted_desc = heap_sort_descending(unsorted)
    print("Sorted descending (max-heap): " + str(sorted_desc))
