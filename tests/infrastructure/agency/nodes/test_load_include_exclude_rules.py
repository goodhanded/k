import os
import unittest
import tempfile
import shutil
from infrastructure.agency.nodes.load_include_exclude_rules import LoadIncludeExcludeRules


class TestLoadIncludeExcludeRules(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        os.makedirs(".k", exist_ok=True)
        with open(os.path.join(".k", "includes.txt"), "w", encoding="utf-8") as f:
            f.write("*.py\n*.md")
        with open(os.path.join(".k", "excludes.txt"), "w", encoding="utf-8") as f:
            f.write(".git\nvenv")

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_load_rules(self):
        node = LoadIncludeExcludeRules()
        state = {}
        result = node(state)
        self.assertIn("include_rules", result)
        self.assertIn("exclude_rules", result)
        self.assertEqual(result["progress"], "Include and exclude rules loaded.")
        self.assertIn("*.py", result["include_rules"])
        self.assertIn("venv", result["exclude_rules"])


if __name__ == '__main__':
    unittest.main()
