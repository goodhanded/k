from typing import Protocol

from domain.filesystem import AudioFile, Document

class TranscriberProtocol(Protocol):
  def transcribe(self, audio_file: AudioFile) -> Document:
    pass