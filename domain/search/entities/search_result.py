from typing import List
from dataclasses import dataclass, field

from ...filesystem.entities.document import Document

@dataclass
class SearchResult:
    query: str
    results: List[Document]
    success: bool = True
    message: str = ""
    errors: List[str] = field(default_factory=list)