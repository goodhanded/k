import os
import tempfile
import unittest

from domain.util.datetime import date_string, ym
from infrastructure.obsidian.vault import ObsidianVault
from domain.filesystem.entities.document import Document

class TestObsidianVault(unittest.TestCase):
    def test_get_daily_note_creates_empty_note_if_not_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = ObsidianVault(temp_dir)
            # Call get_daily_note which should create the file if missing
            note = vault.get_daily_note()
            year, month = ym()
            daily_note_file = f"{date_string()}.md"
            expected_path = os.path.join(temp_dir, "Calendar", year, month, daily_note_file)
            self.assertTrue(os.path.exists(expected_path), "Daily note file was not created")
            self.assertEqual(note.content, "", "Daily note content should be empty by default")

    def test_overwrite_daily_note_updates_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = ObsidianVault(temp_dir)
            new_content = "New daily note content"
            vault.overwrite_daily_note(new_content)
            year, month = ym()
            daily_note_file = f"{date_string()}.md"
            expected_path = os.path.join(temp_dir, "Calendar", year, month, daily_note_file)
            self.assertTrue(os.path.exists(expected_path), "Daily note file was not created after overwrite")
            with open(expected_path, "r", encoding="utf-8") as f:
                file_content = f.read()
            self.assertEqual(file_content, new_content, "Content of daily note did not update correctly")

if __name__ == "__main__":
    unittest.main()
