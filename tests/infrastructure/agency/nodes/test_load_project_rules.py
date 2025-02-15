import os
import unittest
import tempfile
import shutil
from infrastructure.agency.nodes.load_project_rules import LoadProjectRules


class TestLoadProjectRules(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        os.makedirs(".k", exist_ok=True)
        self.rules_content = "Rule1\nRule2"
        with open(os.path.join(".k", "rules.txt"), "w", encoding="utf-8") as f:
            f.write(self.rules_content)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_load_project_rules(self):
        node = LoadProjectRules()
        state = {}
        result = node(state)
        self.assertEqual(result["project_rules"], self.rules_content)
        self.assertEqual(result["progress"], "Project rules loaded.")


if __name__ == '__main__':
    unittest.main()
