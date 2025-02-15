import os
import unittest
import tempfile
import shutil
from infrastructure.agency.nodes.load_directory_tree import LoadDirectoryTree
from domain.filesystem.entities.file_collection import FileCollection


class TestLoadDirectoryTree(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "dir1"), exist_ok=True)
        with open(os.path.join(self.test_dir, "file1.txt"), "w", encoding="utf-8") as f:
            f.write("File 1")
        with open(os.path.join(self.test_dir, "dir1", "file2.txt"), "w", encoding="utf-8") as f:
            f.write("File 2")
        self.file_collection = FileCollection.from_path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_directory_tree(self):
        node = LoadDirectoryTree()
        state = {"file_collection": self.file_collection}
        result = node(state)
        self.assertIn("directory_tree", result)
        self.assertEqual(result["progress"], "Directory tree loaded.")
        tree_str = result["directory_tree"]
        self.assertIn("dir1", tree_str)
        self.assertIn("file1.txt", tree_str)


if __name__ == '__main__':
    unittest.main()
