from typing import Protocol
from domain.filesystem import DocumentCollection

class DocumentLoaderProtocol(Protocol):
    def load(self) -> DocumentCollection:
        pass