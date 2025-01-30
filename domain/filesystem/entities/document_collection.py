import os
from typing import List
from domain.filesystem import File, Document

class DocumentCollection:
    """
    Represents a collection of documents in memory. Can be read from or written to a directory.

    Attributes:
    - content: str
    - metadata: dict
    """
    documents: List[Document]

    def __init__(self, documents: List[Document]):
        """
        Initializes a DocumentCollection with a list of documents.
        """
        self.documents = documents

    def to_document(self, delimiter: str = '\n\n') -> Document:
        """
        Converts the collection to a Document object.
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

    @staticmethod
    def from_path(path: str) -> 'DocumentCollection':
        """
        Reads all documents from a directory and returns a DocumentCollection.

        Args:
            - path: str: The path to the directory containing the documents.
        """

        documents = []
        for file_name in os.listdir(path):
        # Ignore dot files or hidden files
            if file_name.startswith('.'):
                continue

            file_path = os.path.join(path, file_name)
            document = Document.from_path(file_path)
            documents.append(document)
        
        return DocumentCollection(documents)

    def __iter__(self):
        return iter(self.documents)

    def __len__(self):
        return len(self.documents)