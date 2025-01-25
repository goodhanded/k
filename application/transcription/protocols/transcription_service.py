from typing import Protocol
from domain.notes import Note
from domain.notes import VoiceMemo

class TranscriptionServiceInterface(Protocol):
  def transcribe(self, voice_memo: VoiceMemo) -> Note:
    pass