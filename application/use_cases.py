from domain.notes import Note, VoiceMemo, NoteCollection
from domain.protocols import TranscriptionServiceInterface, NoteAssimilatorInterface, NoteVaultInterface

class AssimilateTodaysNotesIntoVault:
  def __init__(self,
               assimilator: NoteAssimilatorInterface):
    self.assimilator = assimilator

  def execute(self, notes: NoteCollection, vault: NoteVaultInterface):
    return self.assimilator.assimilate(notes, vault)

class TranscribeVoiceMemoUseCase:
  def __init__(self, 
               transcription_service: TranscriptionServiceInterface):
    self.transcriptionService = transcription_service

  def execute(self, voice_memo: VoiceMemo) -> Note:
    return self.transcriptionService.transcribe(voice_memo)
