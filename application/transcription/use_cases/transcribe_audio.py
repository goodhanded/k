from domain.filesystem import AudioFile, Document
from ..protocols.transcriber import TranscriberProtocol

class TranscribeAudioUseCase:
    def __init__(self, transcription_service: TranscriberProtocol):
        self.transcriptionService = transcription_service

    def execute(self, path: str) -> Document:
        audio_file = AudioFile(path)
        document = self.transcriptionService.transcribe(audio_file)
        print(document)
        return document