from uuid import uuid4
from domain.filesystem import File

class Document:
    """
    Represents a document in memory. Can be saved to a file.

    Attributes:
    - content: str
    - id: str
    - metadata: dict
    """
    content: str
    id: str = uuid4()
    metadata: dict = None

    def __init__(self, content: str, id: str = uuid4(), metadata: dict = {}):
        """
        Initializes a Document with content and metadata.

        Args:
            - content: str: The content of the document.
            - metadata: dict: The metadata of the document.
        """
        self.content = content
        self.metadata = metadata

    def __str__(self):
        return self.content

    def content_with_path(self) -> str:
        """
        Returns the content of the document with the path.
        """
        if "path" not in self.metadata:
            return self.content
        
        extension = self.metadata["path"].split(".")[-1]
        return f"\n\n{self.metadata['path']}:\n```{extension}\n{self.content}\n```\n\n"

    def to_file(self, path: str) -> File:
        """
        Saves the document to a file.

        Args:
            - path: str: The path to save the file to.
        """
        return File.from_content(self.content, path)
    
    @staticmethod
    def from_path(path: str) -> 'Document':
        """
        Reads a document from a file.

        Args:
            - path: str: The path to read the file from.
        """
        with open(path, "r") as f:
            content = f.read()

        metadata = {"path": path}
        return Document(content=content, metadata=metadata)