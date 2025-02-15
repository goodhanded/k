import os
import unittest
from infrastructure.agency.nodes.get_project_path import GetProjectPath


class TestGetProjectPath(unittest.TestCase):
    def test_get_project_path(self):
        node = GetProjectPath()
        state = {}
        result = node(state)
        self.assertIn("project_path", result)
        self.assertEqual(result["project_path"], os.getcwd())
        self.assertEqual(result["progress"], "Project path loaded.")


if __name__ == '__main__':
    unittest.main()
