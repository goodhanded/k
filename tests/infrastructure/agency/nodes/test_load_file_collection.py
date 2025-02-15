import os
import unittest
import tempfile
import shutil
from infrastructure.agency.nodes.load_file_collection import LoadFileCollection
from domain.filesystem.entities.file_collection import FileCollection


class TestLoadFileCollection(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        with open(os.path.join(self.test_dir, "test1.txt"), "w", encoding="utf-8") as f:
            f.write("Hello")
        with open(os.path.join(self.test_dir, "test2.py"), "w", encoding="utf-8") as f:
            f.write("print('Hi')")
        with open(os.path.join(self.test_dir, "ignore.log"), "w", encoding="utf-8") as f:
            f.write("Log")
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_file_collection(self):
        node = LoadFileCollection()
        state = {
            "project_path": self.test_dir,
            "include_rules": "*.txt|*.py",
            "exclude_rules": "*.log"
        }
        result = node(state)
        self.assertIn("file_collection", result)
        fc = result["file_collection"]
        file_names = [os.path.basename(f.path) for f in fc.files]
        self.assertIn("test1.txt", file_names)
        self.assertIn("test2.py", file_names)
        self.assertNotIn("ignore.log", file_names)
        self.assertEqual(result["progress"], "File collection loaded.")


if __name__ == '__main__':
    unittest.main()
