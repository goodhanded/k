import os
import tempfile
import unittest

from domain.util.datetime import ymd
from application.daily_voice_notes.use_cases.assimilate_voice_note import AssimilateVoiceNoteUseCase
from domain.filesystem.entities.document import Document
from domain.filesystem.entities.document_collection import DocumentCollection

class DummyTranscriber:
    def transcribe(self, audio_file):
        return Document("dummy transcription")

class DummyConsolidator:
    def __init__(self):
        self.consolidated = False
        self.last_collection = None
    def consolidate(self, document_collection: DocumentCollection):
        self.consolidated = True
        self.last_collection = document_collection
        return document_collection

class TestAssimilateVoiceNoteUseCase(unittest.TestCase):
    def test_execute_creates_transcript_file_and_consolidates(self):
        dummy_transcriber = DummyTranscriber()
        dummy_consolidator = DummyConsolidator()
        with tempfile.TemporaryDirectory() as temp_dir:
            # Use temp_dir as the base for transcripts
            use_case = AssimilateVoiceNoteUseCase(dummy_transcriber, dummy_consolidator, transcripts_path=temp_dir)
            # Create a temporary dummy audio file with valid extension
            temp_audio_file = os.path.join(temp_dir, "test_audio.wav")
            with open(temp_audio_file, "wb") as f:
                f.write(b"dummy audio content")
            
            # Execute the use case
            use_case.execute(temp_audio_file)
            
            # Construct the expected transcripts folder using ymd()
            todays_transcripts_path = os.path.join(temp_dir, *ymd())
            expected_transcript_file = os.path.join(todays_transcripts_path, "test_audio.md")
            self.assertTrue(os.path.exists(expected_transcript_file), "Transcript file was not created")
            
            with open(expected_transcript_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertEqual(content, "dummy transcription")
            
            # Check that the consolidator was called
            self.assertTrue(dummy_consolidator.consolidated, "Document consolidator was not invoked")

if __name__ == "__main__":
    unittest.main()
