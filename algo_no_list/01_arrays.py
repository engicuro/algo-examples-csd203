# Chapter 1: Arrays (using tuples instead of lists)
# This file covers array basics using tuples and loops.
# No lists are used — only tuples for sequence data.


def create_array():
    """Create an array (Python tuple) and print its elements."""
    # An array is an ordered collection of items stored in a tuple
    numbers = (10, 20, 30, 40, 50)
    print("Created array:", numbers)
    return numbers


def access_by_index(arr):
    """Access elements by their index (position)."""
    print("\n--- Accessing by Index ---")
    # Index starts at 0 for the first element
    print("First element (index 0):", arr[0])
    print("Second element (index 1):", arr[1])
    print("Last element (index -1):", arr[-1])


def slice_array(arr):
    """Show how slicing works to get a portion of the array."""
    print("\n--- Slicing ---")
    # arr[start:end] gives elements from index start up to (but not including) end
    print("First three elements arr[0:3]:", arr[0:3])
    print("From index 2 to end arr[2:]:", arr[2:])
    print("Every second element arr[::2]:", arr[::2])


def append_element(arr):
    """Add an element to the end of the array."""
    print("\n--- Append ---")
    print("Array before append:", arr)
    arr = arr + (60,)  # add 60 to the end
    print("Array after append(60):", arr)
    return arr


def insert_element(arr):
    """Insert an element at a specific position."""
    print("\n--- Insert ---")
    print("Array before insert:", arr)
    arr = arr[:2] + (25,) + arr[2:]  # insert 25 at index 2
    print("Array after insert(2, 25):", arr)
    return arr


def delete_element(arr):
    """Delete an element by value or by index."""
    print("\n--- Delete ---")
    print("Array before delete:", arr)

    # Delete by value: removes the first occurrence
    new_arr = ()
    found = False
    for item in arr:
        if not found and item == 25:
            found = True
            continue
        new_arr = new_arr + (item,)
    arr = new_arr
    print("After remove(25):", arr)

    # Delete by index: pop removes and returns the element at that index
    removed = arr[0]  # remove the first element
    arr = arr[1:]
    print("After pop(0) (removed", removed, "):", arr)
    return arr


def search_linear(arr, target):
    """Search for a value using a simple loop (linear search)."""
    print("\n--- Linear Search ---")
    # Walk through every element one by one
    for i in range(len(arr)):
        if arr[i] == target:
            print("Found", target, "at index", i)
            return i
    print(target, "not found in array")
    return -1


def sort_array(arr):
    """Sort the array using a simple bubble sort (explained with loops)."""
    print("\n--- Sorting (Bubble Sort) ---")
    print("Array before sort:", arr)

    # Bubble sort: repeatedly swap adjacent elements if they are in the wrong order
    n = len(arr)
    for i in range(n):
        # Each pass pushes the largest unsorted element to the end
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                # Swap the two elements by rebuilding the tuple
                arr = arr[:j] + (arr[j + 1],) + (arr[j],) + arr[j + 2:]

    print("Array after sort:", arr)
    return arr


def print_array(arr, label="Array"):
    """Helper: print all elements of an array on one line."""
    print(label + ":", end=" ")
    for item in arr:
        print(item, end=" ")
    print()  # newline at the end


if __name__ == "__main__":
    print("=" * 50)
    print("Chapter 1: Array Basics")
    print("=" * 50)

    # 1. Create an array
    my_array = create_array()

    # 2. Access elements by index
    access_by_index(my_array)

    # 3. Slice the array
    slice_array(my_array)

    # 4. Append an element
    my_array = append_element(my_array)

    # 5. Insert an element at a specific position
    my_array = insert_element(my_array)

    # 6. Delete elements
    my_array = delete_element(my_array)

    # 7. Search for a value
    search_linear(my_array, 30)
    search_linear(my_array, 99)  # value not in array

    # 8. Sort the array
    my_array = sort_array(my_array)

    print("\nDone with Chapter 1!")
