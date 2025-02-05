import unittest
from infrastructure.langchain.document_mapper import LangchainDocumentMapper
from domain.filesystem.entities.document import Document
from domain.filesystem.entities.document_collection import DocumentCollection


class DummyLangchainDocument:
    def __init__(self, id: str, page_content: str, metadata: dict) -> None:
        self.id = id
        self.page_content = page_content
        self.metadata = metadata


class TestLangchainDocumentMapper(unittest.TestCase):
    def test_from_langchain_single(self) -> None:
        dummy_doc = DummyLangchainDocument("1", "Content A", {"key": "value"})
        doc = LangchainDocumentMapper.from_langchain(dummy_doc)
        self.assertIsInstance(doc, Document)
        self.assertEqual(doc.content, "Content A")

    def test_from_langchain_list(self) -> None:
        docs = [DummyLangchainDocument("1", "Content A", {}), DummyLangchainDocument("2", "Content B", {})]
        collection = LangchainDocumentMapper.from_langchain(docs)
        self.assertIsInstance(collection, DocumentCollection)
        self.assertEqual(len(collection.documents), 2)

    def test_to_langchain_single(self) -> None:
        doc = Document("Content Test", metadata={"key": "value"})
        lc_doc = LangchainDocumentMapper.to_langchain(doc)
        self.assertTrue(hasattr(lc_doc, 'page_content'))
        self.assertEqual(lc_doc.page_content, "Content Test")

    def test_to_langchain_list(self) -> None:
        docs = [Document("A"), Document("B")]
        lc_docs = LangchainDocumentMapper.to_langchain(docs)
        self.assertIsInstance(lc_docs, list)
        self.assertEqual(len(lc_docs), 2)


if __name__ == '__main__':
    unittest.main()
