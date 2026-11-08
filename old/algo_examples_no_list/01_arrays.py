# Chapter 1: Array Basics (No-List Version)
# This version uses a dict-based array instead of Python lists.
# A dict with integer keys simulates an array with O(1) access.


def create_array():
    """Create and return an empty array (dict-based).

    We use a dictionary with integer keys to simulate an array.
    This avoids using Python's built-in list type.
    """
    return {}


def array_length(arr):
    """Return the number of elements in the dict-based array."""
    return len(arr)


def access_by_index(arr):
    """Access elements by index in a dict-based array."""
    print("\n--- Access by Index ---")
    # In a dict-based array, we store elements with integer keys
    arr[0] = 10
    arr[1] = 20
    arr[2] = 30
    arr[3] = 40
    arr[4] = 50

    print("Array contents:")
    for i in range(array_length(arr)):
        print("  arr[%d] = %d" % (i, arr[i]))

    # Access a specific index
    print("arr[2] =", arr[2])
    print("arr[0] =", arr[0])


def slice_array(arr):
    """Slice a dict-based array (returns a new dict-based array)."""
    print("\n--- Slicing ---")
    # Build a new dict with keys 1..3 (equivalent to arr[1:4])
    sliced = {}
    for i in range(1, 4):
        sliced[i - 1] = arr[i]

    print("Original array:", end=" ")
    for i in range(array_length(arr)):
        print(arr[i], end=" ")
    print()

    print("Sliced [1:4]:", end=" ")
    for i in range(array_length(sliced)):
        print(sliced[i], end=" ")
    print()


def append_element(arr):
    """Append an element to the end of the dict-based array."""
    print("\n--- Append Element ---")
    print("Array before append:", end=" ")
    for i in range(array_length(arr)):
        print(arr[i], end=" ")
    print()

    # Append: add a new key at the end
    arr[array_length(arr)] = 60

    print("Array after append(60):", end=" ")
    for i in range(array_length(arr)):
        print(arr[i], end=" ")
    print()


def insert_element(arr):
    """Insert an element at a specific position (shift elements right)."""
    print("\n--- Insert Element ---")
    print("Array before insert:", end=" ")
    for i in range(array_length(arr)):
        print(arr[i], end=" ")
    print()

    # Insert 99 at index 2: shift elements at index 2 and beyond right
    n = array_length(arr)
    # Shift right from the end
    arr[n] = arr[n - 1]
    for i in range(n - 1, 2, -1):
        arr[i] = arr[i - 1]
    arr[2] = 99

    print("Array after insert(99 at index 2):", end=" ")
    for i in range(array_length(arr)):
        print(arr[i], end=" ")
    print()


def delete_element(arr):
    """Delete an element by shifting elements left."""
    print("\n--- Delete Element ---")
    print("Array before delete:", end=" ")
    for i in range(array_length(arr)):
        print(arr[i], end=" ")
    print()

    # Delete element at index 2: shift elements left
    n = array_length(arr)
    for i in range(2, n - 1):
        arr[i] = arr[i + 1]
    # Remove the last duplicate key
    del arr[n - 1]

    print("Array after delete index 2:", end=" ")
    for i in range(array_length(arr)):
        print(arr[i], end=" ")
    print()

    # Delete by index: remove the first element
    n = array_length(arr)
    for i in range(0, n - 1):
        arr[i] = arr[i + 1]
    del arr[n - 1]
    print("After deleting first element:", end=" ")
    for i in range(array_length(arr)):
        print(arr[i], end=" ")
    print()


def search_linear(arr, target):
    """Search for a value using a simple loop (linear search)."""
    print("\n--- Linear Search ---")
    n = array_length(arr)
    for i in range(n):
        if arr[i] == target:
            print("Found", target, "at index", i)
            return i
    print(target, "not found in array")
    return -1


def sort_array(arr):
    """Sort the array using a simple bubble sort."""
    print("\n--- Sorting (Bubble Sort) ---")
    print("Array before sort:", end=" ")
    for i in range(array_length(arr)):
        print(arr[i], end=" ")
    print()

    # Bubble sort: repeatedly swap adjacent elements if they are in the wrong order
    n = array_length(arr)
    for i in range(n):
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                # Swap the two elements
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp

    print("Array after sort:", end=" ")
    for i in range(array_length(arr)):
        print(arr[i], end=" ")
    print()


def print_array(arr, label="Array"):
    """Helper: print all elements of a dict-based array on one line."""
    print(label + ":", end=" ")
    for i in range(array_length(arr)):
        print(arr[i], end=" ")
    print()  # newline at the end


if __name__ == "__main__":
    print("=" * 50)
    print("Chapter 1: Array Basics (No-List Version)")
    print("=" * 50)

    # 1. Create an array
    my_array = create_array()

    # 2. Access elements by index
    access_by_index(my_array)

    # 3. Slice the array
    slice_array(my_array)

    # 4. Append an element
    append_element(my_array)

    # 5. Insert an element at a specific position
    insert_element(my_array)

    # 6. Delete elements
    delete_element(my_array)

    # 7. Search for a value
    search_linear(my_array, 30)
    search_linear(my_array, 99)  # value not in array

    # 8. Sort the array
    sort_array(my_array)

    print("\nDone with Chapter 1!")
