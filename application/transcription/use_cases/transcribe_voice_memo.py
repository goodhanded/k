from application.transcription import TranscriptionServiceInterface
from domain.notes import Note
from domain.notes.entities.voice_memo import VoiceMemo

class TranscribeVoiceMemoUseCase:
  def __init__(self,
               transcription_service: TranscriptionServiceInterface):
    self.transcriptionService = transcription_service

  def execute(self, voice_memo: VoiceMemo) -> Note:
    return self.transcriptionService.transcribe(voice_memo)