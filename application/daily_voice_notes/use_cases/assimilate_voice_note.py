import os
from application.transcription import TranscriberProtocol
from application.util import DatetimeServiceProtocol
from application.daily_voice_notes import DocumentConsolidatorProtocol
from domain.filesystem import AudioFile, DocumentCollection

class AssimilateVoiceNoteUseCase:

    def __init__(self,
                 transcriber: TranscriberProtocol,
                 document_consolidator: DocumentConsolidatorProtocol,
                 transcripts_path: str,
                 datetime_service: DatetimeServiceProtocol):
        self.transcriber = transcriber
        self.transcripts_path = transcripts_path
        self.datetime_service = datetime_service
        self.todays_transcripts_path = os.path.join(self.transcripts_path, *self.datetime_service.ymd())
        self.document_consolidator = document_consolidator
        
    def execute(self, path: str):
        os.makedirs(self.transcripts_path, exist_ok=True)
        audio_file = AudioFile(path)
        transcription = self.transcriber.transcribe(audio_file)

        new_transcript_file_path = os.path.join(self.todays_transcripts_path, f"{audio_file.name_without_extension}.md")
        transcription.to_file(new_transcript_file_path)
        todays_transcripts = DocumentCollection.from_path(self.todays_transcripts_path)
        todays_transcripts.add(transcription)

        self.document_consolidator.consolidate(todays_transcripts)
        print(f"Assimilated {len(todays_transcripts)} notes into today's daily note")
