from domain.filesystem import Document, DocumentCollection

from typing import Protocol

class NoteVaultProtocol(Protocol):
  path: str
  def save(self, document: Document, path: str):
    pass
  def get(self, path: str) -> Document:
    pass
  def list(self, path: str) -> DocumentCollection:
    pass
  def get_daily_note(self) -> Document:
    pass
  def get_all_notes(self) -> DocumentCollection:
    pass
  def overwrite_daily_note(self, content: str):
    pass