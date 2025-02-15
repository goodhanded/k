import unittest
from unittest.mock import patch, MagicMock
from infrastructure.agency.nodes.git_status import GitStatus


class TestGitStatus(unittest.TestCase):
    @patch("infrastructure.agency.nodes.git_status.subprocess.run")
    def test_git_status(self, mock_run):
        dummy_result = MagicMock()
        dummy_result.stdout = "dummy git status"
        dummy_result.returncode = 0
        mock_run.return_value = dummy_result

        node = GitStatus()
        state = {}
        result = node(state)
        self.assertIn("git_status", result)
        self.assertEqual(result["git_status"], "dummy git status")
        self.assertEqual(result["progress"], "Ran git status.")


if __name__ == '__main__':
    unittest.main()
