import os
import unittest
import tempfile
import shutil
from infrastructure.agency.nodes.load_source_code import LoadSourceCode
from domain.filesystem.entities.file_collection import FileCollection


class TestLoadSourceCode(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        with open(os.path.join(self.test_dir, "test.txt"), "w", encoding="utf-8") as f:
            f.write("Source code here.")
        self.file_collection = FileCollection.from_path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_source_code(self):
        node = LoadSourceCode()
        state = {
            "file_collection": self.file_collection
        }
        result = node(state)
        self.assertIn("source_code", result)
        self.assertEqual(result["progress"], "Source code loaded.")
        self.assertIn("Source code here.", result["source_code"])


if __name__ == '__main__':
    unittest.main()
