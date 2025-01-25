from domain.notes import Note
from domain.notes.entities.note_collection import NoteCollection


from typing import Protocol


class NoteVaultInterface(Protocol):
  path: str
  def save(self, note: Note):
    pass
  def get(self, path: str) -> Note:
    pass
  def list(self, path: str) -> NoteCollection:
    pass