# 11_recursion_file_system.py
# File system traversal using recursion.
# A directory can contain files and subdirectories, and each subdirectory
# can contain more files and subdirectories.  Recursion is a natural way
# to explore this nested structure.
#
# Key ideas:
#   - Base case: the path is a file, so just print it.
#   - Recursive case: the path is a directory, so list its contents and
#     recurse into each subdirectory.
#
# NOTE: This script only reads the directory tree.  It does not modify
# anything on your computer.

import os


def list_files(path, indent=0):
    """Print all files under path, one per line, with indentation.

    path:       a file or directory path (string).
    indent:     how many spaces to indent (shows depth in the tree).
    """
    # Check if the path exists before trying to read it.
    if not os.path.exists(path):
        print(" " * indent + "[not found: %s]" % path)
        return

    # Base case: it is a file, not a directory.
    if os.path.isfile(path):
        print(" " * indent + "[file] " + os.path.basename(path))
        return

    # Recursive case: it is a directory.
    print(" " * indent + "[dir]  " + os.path.basename(path) + "/")

    # Try to list the contents of the directory.
    try:
        entries = os.listdir(path)
    except PermissionError:
        print(" " * indent + "  (permission denied)")
        return

    # Sort entries so the output is predictable and easy to read.
    entries.sort()

    # Recurse into each entry.
    for entry in entries:
        full_path = os.path.join(path, entry)
        list_files(full_path, indent + 2)


def count_files_and_dirs(path):
    """Count how many files and directories exist under path.

    Returns a tuple: (file_count, dir_count).
    """
    # Base case: it is a file.
    if os.path.isfile(path):
        return (1, 0)

    # Base case: it is not a file or directory (e.g. broken link).
    if not os.path.isdir(path):
        return (0, 0)

    # Recursive case: it is a directory.
    file_count = 0
    dir_count = 0

    try:
        entries = os.listdir(path)
    except PermissionError:
        return (0, 0)

    for entry in entries:
        full_path = os.path.join(path, entry)
        counts = count_files_and_dirs(full_path)
        file_count = file_count + counts[0]
        dir_count = dir_count + counts[1]

    # Count this directory itself.
    dir_count = dir_count + 1
    return (file_count, dir_count)


if __name__ == "__main__":
    # Use the current directory as an example.
    current_dir = os.getcwd()
    print("=== File tree under: %s ===\n" % current_dir)
    list_files(current_dir)

    print("\n=== Counting files and directories ===")
    counts = count_files_and_dirs(current_dir)
    print("Total files:   %d" % counts[0])
    print("Total dirs:    %d" % counts[1])
