import unittest
from unittest.mock import MagicMock, patch
from infrastructure.langchain.document_loaders.obsidian import ObsidianDocumentLoader
from domain.filesystem.entities.document_collection import DocumentCollection


class DummyLangchainDoc:
    def __init__(self, id: str, page_content: str, metadata: dict) -> None:
        self.id = id
        self.page_content = page_content
        self.metadata = metadata


class TestObsidianDocumentLoader(unittest.TestCase):
    @patch('infrastructure.langchain.document_loaders.obsidian.ObsidianLoader', autospec=True)
    def test_load(self, mock_obsidian_loader: any) -> None:
        dummy_docs = [DummyLangchainDoc("1", "Note Content", {})]
        instance = MagicMock()
        instance.load.return_value = dummy_docs
        mock_obsidian_loader.return_value = instance

        from infrastructure.langchain.document_mapper import LangchainDocumentMapper
        vault_path = "dummy_vault"
        loader = ObsidianDocumentLoader(mapper=LangchainDocumentMapper(), vault_path=vault_path)
        collection = loader.load()
        self.assertIsInstance(collection, DocumentCollection)
        self.assertEqual(len(collection.documents), 1)


if __name__ == '__main__':
    unittest.main()
