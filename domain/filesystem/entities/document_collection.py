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