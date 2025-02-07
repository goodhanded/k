import os
import tempfile
import shutil
import unittest

from application.init.init_k import InitKUseCase


class TestInitKUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self) -> None:
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_execute_creates_k_directory(self):
        use_case = InitKUseCase()
        use_case.execute()
        k_dir = os.path.join(os.getcwd(), ".k")
        self.assertTrue(os.path.exists(k_dir), ".k directory was not created")
        
        # Check that excludes.txt exists and contains expected content
        excludes_path = os.path.join(k_dir, "excludes.txt")
        self.assertTrue(os.path.exists(excludes_path), "excludes.txt was not created")
        with open(excludes_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn(".git", content)

    def test_execute_when_k_exists(self):
        os.makedirs(".k", exist_ok=True)
        use_case = InitKUseCase()
        # Execute should detect existing .k and skip initialization
        use_case.execute()
        k_dir = os.path.join(os.getcwd(), ".k")
        self.assertTrue(os.path.exists(k_dir), "The existing .k directory should still exist")


if __name__ == '__main__':
    unittest.main()
