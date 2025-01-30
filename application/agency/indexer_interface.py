from typing import Protocol
from application.intelligence import NoteVaultInterface
from domain.agency import IndexResult

class IndexerInterface(Protocol):
    def index(self, note_vault: NoteVaultInterface) -> IndexResult:
        pass