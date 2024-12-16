from typing import Protocol
from domain.notes import VoiceMemo, Note, NoteCollection

class TranscriptionServiceInterface(Protocol):
  def transcribe(self, voice_memo: VoiceMemo) -> Note:
    pass

class LLMClientInterface(Protocol):
  def get_chat_completion(self, prompt: str) -> str:
    pass

class NoteVaultInterface(Protocol):
  path: str
  def save(self, note: Note):
    pass
  def get(self, path: str) -> Note:
    pass
  def list(self, path: str) -> NoteCollection:
    pass

class NoteAssimilatorInterface(Protocol):
  def assimilate(self, todays_notes: NoteCollection):
    pass