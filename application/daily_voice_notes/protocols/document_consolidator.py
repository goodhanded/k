from typing import Protocol, List

from domain.filesystem import Document, DocumentCollection

class DocumentConsolidatorProtocol(Protocol):
    """
    Protocol for consolidating multiple documents into a single document
    """
    def consolidate(self, existing_document: Document, additional_documents: DocumentCollection) -> Document:
        """
        Consolidate multiple documents into a single document

        Args:
            - existing_document: Document: The existing document to consolidate into
            - additional_documents: DocumentCollection: The additional documents to consolidate

        Returns:
            The consolidated document
        """
        pass