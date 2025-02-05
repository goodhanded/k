import unittest

from infrastructure.obsidian import ObsidianPromptGenerator
from application.notes import NoteVaultProtocol
from domain.filesystem import Document


class DummyNoteVault(NoteVaultProtocol):
    def get(self, path: str) -> Document:
        # Return a dummy Document with a template containing placeholders
        return Document("Hello {name}, your item is {item}.")
    
    def save(self, document, path: str):
        pass

    def list(self, path: str):
        pass

    def get_daily_note(self) -> Document:
        return Document("")

    def get_all_notes(self):
        pass

    def overwrite_daily_note(self, content: str):
        pass


class TestPromptGenerator(unittest.TestCase):
    def test_generate(self):
        vault = DummyNoteVault()
        prompt_generator = ObsidianPromptGenerator(vault, prompt_template_path="dummy")
        output = prompt_generator.generate("prompt_name", name="Alice", item="apple")
        self.assertIn("Hello Alice, your item is apple.", output)


if __name__ == '__main__':
    unittest.main()
