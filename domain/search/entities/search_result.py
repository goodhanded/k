from typing import List
from dataclasses import dataclass, field

from ...filesystem.entities.document_collection import DocumentCollection

@dataclass
class SearchResult:
    query: str
    docs: DocumentCollection
    success: bool = True
    message: str = ""
    errors: List[str] = field(default_factory=list)