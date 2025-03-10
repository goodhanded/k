from typing import List, Optional
import os
from pathspec import PathSpec
from .file import File
from .document import Document
from .document_collection import DocumentCollection


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

    def to_markdown(self, base_path: str) -> str:
        """
        Returns a markdown representation of the collection.
        """
        markdown = ""
        for file in self.files:
            rel_path = os.path.relpath(file.path, base_path)
            markdown += f"## {file.name}\n"
            markdown += f"Path: `{rel_path}`\n\n"
            markdown += "```" + file.extension.lstrip('.') + "\n"
            try:
                with open(file.path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception as e:
                content = f"Could not read file: {e}"
            markdown += content
            markdown += "\n```\n\n"
        return markdown

    def to_document_collection(self) -> DocumentCollection:
        """
        Converts the FileCollection into a DocumentCollection.
        """
        documents = []
        for file in self.files:
            with open(file.path, "r", encoding="utf-8") as f:
                content = f.read()
                document = Document(content, metadata={"path": file.path})
                documents.append(document)
        return DocumentCollection(documents)

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
    def from_path(path: str, include_rule: str = None, exclude_rule: str = None) -> 'FileCollection':
        exclude_spec = PathSpec.from_lines('gitwildmatch', exclude_rule.split('|')) if exclude_rule else None
        include_spec = PathSpec.from_lines('gitwildmatch', include_rule.split('|')) if include_rule else None
        collected_files = []  # Renamed accumulator

        # Use a different variable name for the files returned by os.walk()
        for root, dirs, filenames in os.walk(path):
            # Filter out directories that match ignore specs
            dirs[:] = [
                d for d in dirs
                if not exclude_spec or not exclude_spec.match_file(os.path.relpath(os.path.join(root, d), path))
            ]
            for file_name in filenames:  # Now file_name is correctly a string
                rel_file = os.path.relpath(os.path.join(root, file_name), path)
                # Skip files that match the exclude specs
                if exclude_spec and exclude_spec.match_file(rel_file):
                    continue

                # Skip files that do not match any of the include specs if include_rule is set
                if include_spec and not include_spec.match_file(rel_file):
                    continue

                full_path = os.path.join(root, file_name)

                # print(f"Reading file from {full_path}")

                file = File(full_path)
                # Only add it if it is not None (i.e., read successfully)
                if file:
                    collected_files.append(file)

        return FileCollection(collected_files)

    def tree(self, base_path: Optional[str] = None) -> str:
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

        if base_path is None:
            base_path = os.getcwd()

        tree_dict = {}

        # Insert each file into the tree structure.
        for f in self.files:
            # Compute the relative path from the base.
            rel_path = os.path.relpath(f.path, base_path)
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
