from typing import List
from langchain_core.documents import Document as LangchainDocument
from domain.filesystem import Document

class LangchainDocumentMapper:
    @staticmethod
    def from_langchain(doc: LangchainDocument | List[LangchainDocument]) -> Document | List[Document]:

        if isinstance(doc, list):
            return [Document(
                content=d.page_content,
                id=d.id,
                metadata=d.metadata
            ) for d in doc]

        return Document(
            content=doc.page_content,
            id=doc.id,
            metadata=doc.metadata
        )
    
    @staticmethod
    def to_langchain(doc: Document | List[Document]) -> LangchainDocument | List[LangchainDocument]:

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