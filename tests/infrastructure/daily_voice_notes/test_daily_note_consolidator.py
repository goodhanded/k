import unittest
from domain.filesystem.entities.document import Document
from infrastructure.daily_voice_notes.services.daily_note_consolidator import DailyNoteConsolidator
from application.intelligence import LLMClientProtocol
from application.notes import NoteVaultProtocol


class DummyLLM(LLMClientProtocol):
    def chat(self, model: str, prompt: str) -> str:
        # Return a YAML formatted string with code fences
        return "```yaml\n- Dummy consolidated note\n```"

    @property
    def model(self) -> str:
        return "dummy-model"


class DummyNoteVault(NoteVaultProtocol):
    def __init__(self) -> None:
        self.daily_note = Document("")
        self.overwritten_content = ""

    def get(self, path: str) -> Document:
        return Document("")

    def save(self, document: Document, path: str) -> None:
        pass

    def list(self, path: str):
        pass

    def get_daily_note(self) -> Document:
        return self.daily_note

    def get_all_notes(self):
        pass

    def overwrite_daily_note(self, content: str) -> None:
        self.overwritten_content = content


class TestDailyNoteConsolidator(unittest.TestCase):
    def test_consolidate(self) -> None:
        llm = DummyLLM()
        vault = DummyNoteVault()
        consolidator = DailyNoteConsolidator(llm, vault)
        from domain.filesystem.entities.document_collection import DocumentCollection
        doc = Document("Dummy transcript")
        collection = DocumentCollection([doc])
        consolidator.consolidate(collection)
        self.assertEqual(vault.overwritten_content, "- Dummy consolidated note")


if __name__ == '__main__':
    unittest.main()
