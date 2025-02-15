import os
import unittest
import tempfile
import shutil
from infrastructure.agency.nodes.implement_changeset import ImplementChangeset
from infrastructure.agency.nodes.generate_changeset import FileChange


class TestImplementChangeset(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Create a file to be removed
        self.remove_file = os.path.join(self.test_dir, "remove.txt")
        with open(self.remove_file, "w", encoding="utf-8") as f:
            f.write("To be removed")
        # Create a file for modification
        self.mod_file = os.path.join(self.test_dir, "mod.txt")
        with open(self.mod_file, "w", encoding="utf-8") as f:
            f.write("Old content")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_implement_changeset(self):
        changeset = type("DummyChangeset", (), {})()
        changeset.additions = [FileChange(path="added.txt", content="Added content")]
        changeset.modifications = [FileChange(path="mod.txt", content="Modified content")]
        changeset.removals = [FileChange(path="remove.txt", content=None)]
        node = ImplementChangeset()
        state = {
            "changeset": changeset,
            "project_path": self.test_dir
        }
        result = node(state)
        self.assertEqual(result["progress"], "Changeset implemented.")
        added_file = os.path.join(self.test_dir, "added.txt")
        self.assertTrue(os.path.exists(added_file))
        with open(added_file, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "Added content")
        with open(self.mod_file, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "Modified content")
        self.assertFalse(os.path.exists(self.remove_file))


if __name__ == '__main__':
    unittest.main()
