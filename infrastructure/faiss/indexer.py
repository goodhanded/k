from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from infrastructure.langchain.document_mapper import LangchainDocumentMapper
from application.agency import IndexerProtocol
from application.search import DocumentLoaderProtocol
from domain.search import IndexResult

class FAISSIndexer(IndexerProtocol):
    def __init__(self,
                 document_loader: DocumentLoaderProtocol,
                 mapper: LangchainDocumentMapper,
                 docs_path: str,
                 chunk_size: int = 1000,
                 chunk_overlap: int = 100,
                 save_path: str = "faiss_index_folder"
    ):
        self.document_loader = document_loader
        self.mapper = mapper
        self.docs_path = docs_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.save_path = save_path

    def index(self) -> IndexResult:

        # Load documents
        document_collection = self.document_loader.load()
        docs = self.mapper.to_langchain(document_collection)

        # Chunk documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        docs = text_splitter.split_documents(docs)

        # Define embeddings (OpenAI in this example)
        embeddings = OpenAIEmbeddings()

        # Build FAISS index
        faiss_index = FAISS.from_documents(docs, embeddings)
        faiss_index.save_local(self.save_path)

        return IndexResult(success=True, message="Indexing complete")