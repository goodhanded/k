from typing import List
import os
from pathspec import PathSpec
from .file import File
from .document import Document

class FileCollection:
    """
    Represents a collection of files.
    """

    files: List[File]

    def __init__(self, files: List[File]):
        """
        Initializes a FileCollection with a list of files.
        """
        self.files = files

    def to_document(self, delimiter: str = '\n\n') -> Document:
        """
        Concatenates the collection into a single Document object.
        """
        content = delimiter.join([file.content for file in self.files])
        return Document(content=content)

    def add(self, file: File):
        """
        Adds a file to the collection.

        Args:
            - file: File: The file to add.
        """
        self.files.append(file)

    def remove(self, file: File):
        """
        Removes a file from the collection.

        Args:
            - file: File: The file to remove.
        """
        self.files.remove(file)

    def to_list(self) -> List[File]:
        """
        Returns the collection as a list of File objects.
        """
        return self.files
    
    def pop(self, index: int = 0) -> File:
        """
        Removes and returns the file at the specified index.

        Args:
            - index: int: The index of the file to remove.
        """
        return self.files.pop(index)
    
    def push(self, file: File):
        """
        Appends a file to the collection.

        Args:
            - file: File: The file to append.
        """
        self.add(file)

    @staticmethod
    def from_path(path: str, ignore_rule: str = None) -> 'FileCollection':
        spec = PathSpec.from_lines('gitwildmatch', ignore_rule.split('|')) if ignore_rule else None
        files = []

        for root, dirs, files in os.walk(path):
            # Filter out directories that match ignore specs
            dirs[:] = [
                d for d in dirs
                if not spec or not spec.match_file(os.path.relpath(os.path.join(root, d), path))
            ]
            for file in files:
                rel_file = os.path.relpath(os.path.join(root, file.name), path)

                # Skip files that match the ignore specs
                if spec and spec.match_file(rel_file):
                    continue
                
                full_path = os.path.join(root, file_name)

                print(f"Reading file from {full_path}")

                file = File(full_path)
                # Only add it if it is not None (i.e., read successfully)
                if file:
                    files.append(file)

        return FileCollection(files)

    def tree(self) -> str:
        """
        Returns a string directory/file tree representation of the collection.
        Implemented like the Unix tree command, using pipe and dash characters.

        Example output:
        .
        ├─ file1.txt
        ├─ file2.txt
        ├─ dir1
        │  ├─ file3.txt
        │  └─ file4.txt
        └─ dir2
           └─ file5.txt
        """

        # Build a tree dictionary from file paths.
        # Assume each File object has a 'path' attribute containing the full path.
        file_paths = [f.path for f in self.files]
        if not file_paths:
            return "."

        # Determine the common base directory.
        base = os.path.commonpath(file_paths)

        tree_dict = {}

        # Insert each file into the tree structure.
        for f in self.files:
            # Compute the relative path from the base.
            rel_path = os.path.relpath(f.path, base)
            parts = rel_path.split(os.sep)
            cur = tree_dict
            for part in parts[:-1]:
                cur = cur.setdefault(part, {})
            # Files are leaves, so set to None.
            cur[parts[-1]] = None

        def render_tree(d: dict, prefix="") -> list:
            lines = []
            items = sorted(d.items())
            count = len(items)
            for idx, (name, subtree) in enumerate(items):
                connector = "└─" if idx == count - 1 else "├─"
                lines.append(prefix + connector + " " + name)
                if isinstance(subtree, dict) and subtree:
                    extension = "   " if idx == count - 1 else "│  "
                    lines.extend(render_tree(subtree, prefix + extension))
            return lines

        tree_lines = ["."] + render_tree(tree_dict)
        return "\n".join(tree_lines)