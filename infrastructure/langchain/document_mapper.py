from typing import List
from langchain_core.documents import Document as LangchainDocument
from domain.filesystem import Document, DocumentCollection

class LangchainDocumentMapper:
    @staticmethod
    def from_langchain(doc: LangchainDocument | List[LangchainDocument]) -> Document | DocumentCollection:

        if isinstance(doc, list):
            return DocumentCollection([Document(
                id=d.id,
                content=d.page_content,
                metadata=d.metadata
            ) for d in doc])

        return Document(
            id=doc.id,
            content=doc.page_content,
            metadata=doc.metadata
        )

    @staticmethod
    def to_langchain(doc: Document | List[Document] | DocumentCollection) -> LangchainDocument | List[LangchainDocument]:

        if isinstance(doc, DocumentCollection):
            return [LangchainDocument(
                id=d.id,
                page_content=d.content,
                metadata=d.metadata
            ) for d in doc.documents]

        if isinstance(doc, list):
            return [LangchainDocument(
                id=d.id,
                page_content=d.content,
                metadata=d.metadata
            ) for d in doc]

        return LangchainDocument(
            id=doc.id,
            page_content=doc.content,
            metadata=doc.metadata
        )