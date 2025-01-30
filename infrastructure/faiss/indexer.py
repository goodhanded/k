from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from application.agency import IndexerProtocol
from domain.search import IndexResult

class FAISSIndexer(IndexerProtocol):
    def __init__(self,
                 docs_path: str,
                 chunk_size: int = 1000,
                 chunk_overlap: int = 100,
                 save_path: str = "faiss_index_folder"
    ):
        self.docs_path = docs_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.save_path = save_path

    def index(self) -> IndexResult:

        try:

            # Load documents
            loader = DirectoryLoader(self.docs_path, glob="**/*.md")
            raw_docs = loader.load()

            # Chunk documents
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
            docs = text_splitter.split_documents(raw_docs)

            # Define embeddings (OpenAI in this example)
            embeddings = OpenAIEmbeddings()

            # Build FAISS index
            faiss_index = FAISS.from_documents(docs, embeddings)
            faiss_index.save_local(self.save_path)
        except Exception as e:
            return IndexResult(success=False, message=str(e), errors=[str(e)])

        return IndexResult(success=True, message="Indexing complete")