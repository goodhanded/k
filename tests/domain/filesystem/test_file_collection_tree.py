import os
import tempfile
import unittest

from domain.filesystem.entities.file_collection import FileCollection
from domain.filesystem.entities.file import File


class TestFileCollectionTree(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        # Create a directory structure
        os.makedirs(os.path.join(self.test_dir.name, "dir1"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir.name, "dir2"), exist_ok=True)
        
        # Create files
        with open(os.path.join(self.test_dir.name, "file1.txt"), "w") as f:
            f.write("Content of file 1")
        with open(os.path.join(self.test_dir.name, "dir1", "file2.txt"), "w") as f:
            f.write("Content of file 2")
        with open(os.path.join(self.test_dir.name, "dir2", "file3.txt"), "w") as f:
            f.write("Content of file 3")
    
    def tearDown(self):
        self.test_dir.cleanup()
    
    def test_tree_output(self):
        fc = FileCollection.from_path(self.test_dir.name)
        tree_str = fc.tree()
        # Check that tree string contains expected file/directory names
        self.assertIn("file1.txt", tree_str)
        self.assertIn("dir1", tree_str)
        self.assertIn("file2.txt", tree_str)
        self.assertIn("dir2", tree_str)
        self.assertIn("file3.txt", tree_str)


if __name__ == '__main__':
    unittest.main()
