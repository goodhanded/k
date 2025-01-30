from typing import Protocol

from domain.search import SearchResult

class SearchEngineProtocol(Protocol):
    def search(self, query) -> SearchResult:
        pass