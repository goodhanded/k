from langchain_community.document_loaders.obsidian import ObsidianLoader

from application.search import DocumentLoaderProtocol
from domain.filesystem import DocumentCollection

from ..document_mapper import LangchainDocumentMapper

class ObsidianDocumentLoader(DocumentLoaderProtocol):
    def __init__(self, mapper: LangchainDocumentMapper, vault_path: str):
        self.mapper = mapper
        self.loader = ObsidianLoader(vault_path)

    def load(self) -> DocumentCollection:
        langchain_docs = self.loader.load()
        document_collection = self.mapper.from_langchain(langchain_docs)
        return document_collection
