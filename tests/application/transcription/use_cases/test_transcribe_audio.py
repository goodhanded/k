import os
import tempfile
import unittest

from application.transcription.use_cases.transcribe_audio import TranscribeAudioUseCase
from domain.filesystem.entities.document import Document


class DummyTranscriber:
    def transcribe(self, audio_file):
        # Return a dummy Document with fixed content
        return Document("dummy transcription")


class DummyAudioFile:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.name_without_extension = os.path.splitext(self.name)[0]


class TestTranscribeAudio(unittest.TestCase):
    def test_execute(self):
        dummy_transcriber = DummyTranscriber()
        use_case = TranscribeAudioUseCase(dummy_transcriber)
        
        # Create a temporary dummy audio file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(b"dummy audio content")
            tmp_path = tmp.name
        
        result = use_case.execute(tmp_path)
        self.assertIsInstance(result, Document)
        self.assertEqual(result.content, "dummy transcription")
        os.remove(tmp_path)


if __name__ == '__main__':
    unittest.main()
