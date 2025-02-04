import os
from typing import List
from domain.filesystem import File, Document
from pathspec import PathSpec

class DocumentCollection:
    """
    Represents a collection of documents in memory. Can be read from or written to a directory.

    Attributes:
    - documents: List[Document]
    """
    documents: List[Document]

    def __init__(self, documents: List[Document]):
        """
        Initializes a DocumentCollection with a list of documents.
        """
        self.documents = documents

    def to_document(self, delimiter: str = '\n\n') -> Document:
        """
        Concatenates the collection into a single Document object.
        """
        content = delimiter.join([document.content for document in self.documents])
        return Document(content=content)

    def add(self, document: Document):
        """
        Adds a document to the collection.

        Args:
            - document: Document: The document to add.
        """
        self.documents.append(document)

    def remove(self, document: Document):
        """
        Removes a document from the collection.

        Args:
            - document: Document: The document to remove.
        """
        self.documents.remove(document)

    def to_list(self) -> List[Document]:
        """
        Returns the collection as a list of Document objects.
        """
        return self.documents
    
    def pop(self, index: int = 0) -> Document:
        """
        Removes and returns the document at the specified index.

        Args:
            - index: int: The index of the document to remove.
        """
        return self.documents.pop(index)
    
    def push(self, document: Document):
        """
        Appends a document to the collection.

        Args:
            - document: Document: The document to append.
        """
        self.add(document)

    @staticmethod
    def from_path(path: str, ignore_rule: str = None) -> 'DocumentCollection':
        spec = PathSpec.from_lines('gitwildmatch', ignore_rule.split('|')) if ignore_rule else None
        documents = []

        for root, dirs, files in os.walk(path):
            # Filter out directories that match ignore specs
            dirs[:] = [
                d for d in dirs
                if not spec or not spec.match_file(os.path.relpath(os.path.join(root, d), path))
            ]
            for file_name in files:
                rel_file = os.path.relpath(os.path.join(root, file_name), path)
                # Skip files that match the ignore specs
                if spec and spec.match_file(rel_file):
                    continue
                
                full_path = os.path.join(root, file_name)

                print(f"Reading document from {full_path}")

                document = Document.from_path(full_path)
                # Only add it if it is not None (i.e., read successfully)
                if document:
                    documents.append(document)

        return DocumentCollection(documents)

    @staticmethod
    def from_list(documents: List[Document]) -> 'DocumentCollection':
        """
        Returns a DocumentCollection from a list of Document objects.

        Args:
            - documents: List[Document]: The list of Document objects.
        """
        return DocumentCollection(documents)

    def __iter__(self):
        return iter(self.documents)

    def __len__(self):
        return len(self.documents)
    
    def __str__(self):
        return self.to_document().content