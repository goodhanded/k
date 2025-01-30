from typing import Protocol
from application.notes import NoteVaultProtocol
from domain.search import IndexResult

class IndexerProtocol(Protocol):
    def index(self, note_vault: NoteVaultProtocol) -> IndexResult:
        pass