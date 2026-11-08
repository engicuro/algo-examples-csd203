"""
11_recursion_file_system.py
===========================
Recursion Topic: File System Traversal

Recursion is a natural fit for traversing hierarchical data structures.
A file system is a tree: directories contain files and sub-directories,
which themselves contain more files and directories — the structure is
self-similar (recursive).

This example walks a directory tree recursively, listing every file found.

Key recursive ideas:
  - Base case: a path is a file → print/collect it and return.
  - Recursive case: a path is a directory → iterate over its children
    and recurse into each one.

Time complexity : O(n) where n is the total number of files + directories.
Space complexity: O(d) where d is the maximum depth of the tree (call stack).
"""

import os
from pathlib import Path
from typing import List


def list_files_recursive(directory: str, indent: int = 0) -> List[str]:
    """Recursively list all files under a directory tree.

    Args:
        directory: Path to the root directory to traverse.
        indent:    Current indentation level for pretty printing.

    Returns:
        A list of absolute file paths found in the tree.
    """
    files_found: List[str] = []
    prefix = "  " * indent  # visual indentation to show depth

    # --- Base case: path does not exist ---
    if not os.path.exists(directory):
        print(f"{prefix}[!] Path does not exist: {directory}")
        return files_found

    # --- Base case: path is a file ---
    # A file is a leaf node — no further recursion needed.
    if os.path.isfile(directory):
        print(f"{prefix}📄 {os.path.basename(directory)}")
        files_found.append(os.path.abspath(directory))
        return files_found

    # --- Recursive case: path is a directory ---
    # We recurse into each child (file or subdirectory).
    print(f"{prefix}📁 {os.path.basename(directory)}/")

    try:
        entries = sorted(os.listdir(directory))
    except PermissionError:
        print(f"{prefix}  [permission denied]")
        return files_found

    for entry in entries:
        full_path = os.path.join(directory, entry)
        # Recurse into each child — this is where the tree unfolds
        files_found.extend(list_files_recursive(full_path, indent + 1))

    return files_found


def count_files_and_dirs(directory: str) -> tuple[int, int]:
    """Recursively count files and directories in a tree.

    Returns:
        A tuple (file_count, dir_count).
    """
    # Base case: not a directory
    if os.path.isfile(directory):
        return 1, 0

    if not os.path.isdir(directory):
        return 0, 0

    file_count = 0
    dir_count = 0

    try:
        entries = os.listdir(directory)
    except PermissionError:
        return 0, 0

    for entry in entries:
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path):
            file_count += 1
        elif os.path.isdir(full_path):
            # Count this directory, then recurse into it
            dir_count += 1
            sub_files, sub_dirs = count_files_and_dirs(full_path)
            file_count += sub_files
            dir_count += sub_dirs

    return file_count, dir_count


def build_file_tree(directory: str, indent: int = 0) -> str:
    """Build a string representation of the directory tree.

    Returns:
        A formatted string showing the tree structure.
    """
    lines: List[str] = []
    prefix = "│  " * indent

    if os.path.isfile(directory):
        lines.append(f"{prefix}├── {os.path.basename(directory)}")
        return "\n".join(lines)

    if not os.path.isdir(directory):
        return ""

    name = os.path.basename(directory) or directory
    lines.append(f"{prefix}├── {name}/")

    try:
        entries = sorted(os.listdir(directory))
    except PermissionError:
        lines.append(f"{prefix}│  ├── [permission denied]")
        return "\n".join(lines)

    for i, entry in enumerate(entries):
        full_path = os.path.join(directory, entry)
        is_last = (i == len(entries) - 1)
        connector = "└──" if is_last else "├──"
        if os.path.isdir(full_path):
            # Recurse into subdirectory
            sub_tree = build_file_tree(full_path, indent + 1)
            lines.append(f"{prefix}│  {connector} {entry}/")
            # Add the subtree entries with extra indentation
            for sub_line in sub_tree.split("\n")[1:]:
                lines.append(f"{prefix}│  {sub_line}")
        else:
            lines.append(f"{prefix}│  {connector} {entry}")

    return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 55)
    print("Recursion Example: File System Traversal")
    print("=" * 55)

    # Use the current directory as an example
    start_dir = os.getcwd()
    print(f"\nTraversing: {start_dir}\n")

    print("--- File listing (recursive) ---")
    all_files = list_files_recursive(start_dir)
    print(f"\nTotal files found: {len(all_files)}")

    print("\n--- File and directory counts ---")
    f_count, d_count = count_files_and_dirs(start_dir)
    print(f"  Files: {f_count}")
    print(f"  Directories: {d_count}")

    print("\n--- Tree view ---")
    # Limit tree depth for readability
    tree = build_file_tree(start_dir)
    # Show only first 40 lines for brevity
    for line in tree.split("\n")[:40]:
        print(line)
    total_lines = len(tree.split("\n"))
    if total_lines > 40:
        print(f"  ... ({total_lines - 40} more lines)")

    print("\n--- Recursive structure explanation ---")
    print("""
  Directory tree is inherently recursive:

  /home/user/project/
  ├── src/           ← directory → recurse into it
  │   ├── main.py    ← file (base case)
  │   └── utils/     ← directory → recurse into it
  │       └── helper.py ← file (base case)
  └── README.md      ← file (base case)

  Each directory is a "recursive case" — we process its children.
  Each file is a "base case" — we stop recursing.
  """)
